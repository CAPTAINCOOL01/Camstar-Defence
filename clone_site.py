#!/usr/bin/env python3
"""
Static site cloner for https://camstardefence.com
Downloads pages up to 2 levels deep and all assets.
"""

import os
import re
import time
import hashlib
import mimetypes
from urllib.parse import urljoin, urlparse, unquote
from pathlib import Path, PurePosixPath

BASE_URL = "https://camstardefence.com"
OUTPUT_DIR = Path(r"C:\Users\ramay\Desktop\Camstar-Defence\cloned")
MAX_DEPTH = 2

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

import requests

session = requests.Session()
session.headers.update(HEADERS)

downloaded_assets = {}   # url -> local relative path (string, forward slashes)
visited_pages = set()
pages_saved = []
assets_saved = []
assets_failed = []


def is_same_domain(url):
    parsed = urlparse(url)
    base_parsed = urlparse(BASE_URL)
    return parsed.netloc == "" or parsed.netloc == base_parsed.netloc


def safe_rel_path(url_path, query=""):
    """
    Convert a URL path + optional query string into a safe relative path
    that is always BELOW OUTPUT_DIR (no leading drive letters or UNC paths).
    Returns a forward-slash string like 'wp-content/foo/bar.css'
    """
    # Strip leading slash(es) and normalise
    p = PurePosixPath(url_path.lstrip("/") or "index.html")

    # If path ends with '/' treat as directory index
    if url_path.endswith("/") and url_path != "/":
        p = p / "index.html"
    elif not p.suffix:
        p = p / "index.html"

    # Encode query string into filename to avoid collisions
    if query:
        qhash = hashlib.md5(query.encode()).hexdigest()[:8]
        p = p.parent / f"{p.stem}_{qhash}{p.suffix}"

    # Safety: collapse any '..' components
    parts = []
    for part in p.parts:
        if part in (".", ".."):
            continue
        parts.append(part)
    return "/".join(parts) if parts else "index.html"


def url_to_local_path(url):
    """Return an absolute Path inside OUTPUT_DIR for the given URL."""
    parsed = urlparse(url)
    rel = safe_rel_path(parsed.path, parsed.query)
    return OUTPUT_DIR / rel


def download_asset(url, referrer_url=None):
    """Download a single asset and return its local relative path string."""
    if url in downloaded_assets:
        return downloaded_assets[url]

    if url.startswith("data:") or url.startswith("mailto:") or url.startswith("#"):
        downloaded_assets[url] = url
        return url

    full_url = urljoin(referrer_url or BASE_URL, url)
    parsed = urlparse(full_url)

    if parsed.scheme not in ("http", "https"):
        downloaded_assets[url] = url
        return url

    local_path = url_to_local_path(full_url)

    if local_path.exists():
        try:
            rel = local_path.relative_to(OUTPUT_DIR)
            rel_str = str(rel).replace("\\", "/")
            downloaded_assets[url] = rel_str
            return rel_str
        except ValueError:
            pass

    try:
        resp = session.get(full_url, timeout=20, stream=True)
        if resp.status_code == 404:
            print(f"  [404] {full_url}")
            assets_failed.append(full_url)
            downloaded_assets[url] = url
            return url
        resp.raise_for_status()

        # Determine correct extension from content-type if missing
        content_type = resp.headers.get("Content-Type", "").split(";")[0].strip()
        if local_path.suffix == "" and content_type:
            ext = mimetypes.guess_extension(content_type) or ""
            if ext == ".jpe":
                ext = ".jpg"
            local_path = Path(str(local_path) + ext)

        os.makedirs(local_path.parent, exist_ok=True)
        with open(local_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=65536):
                f.write(chunk)

        rel = local_path.relative_to(OUTPUT_DIR)
        rel_str = str(rel).replace("\\", "/")
        downloaded_assets[url] = rel_str
        assets_saved.append(full_url)
        print(f"  [asset] {full_url} -> {rel_str}")
        return rel_str
    except Exception as e:
        print(f"  [error] {full_url}: {e}")
        assets_failed.append(full_url)
        downloaded_assets[url] = url
        return url


CSS_URL_RE = re.compile(r'url\(\s*["\']?([^)"\']+?)["\']?\s*\)', re.IGNORECASE)
CSS_IMPORT_RE = re.compile(r'@import\s+["\']([^"\']+)["\']', re.IGNORECASE)


def rel_from_css(asset_local_rel, css_full_url):
    """Return a path from the CSS file's directory to the asset."""
    try:
        css_local = url_to_local_path(css_full_url)
        asset_abs = OUTPUT_DIR / asset_local_rel
        return os.path.relpath(asset_abs, css_local.parent).replace("\\", "/")
    except Exception:
        return asset_local_rel


def process_css_text(css_text, css_url):
    """Download assets referenced in CSS and rewrite URLs (relative to CSS file)."""
    def replace_url(m):
        asset_url = m.group(1).strip()
        if asset_url.startswith("data:"):
            return m.group(0)
        local = download_asset(asset_url, css_url)
        if local.startswith(("http", "//", "data:")):
            return f"url('{local}')"
        return f"url('{rel_from_css(local, css_url)}')"

    def replace_import(m):
        asset_url = m.group(1).strip()
        local = download_asset(asset_url, css_url)
        if local.startswith(("http", "//", "data:")):
            return f'@import "{local}"'
        return f'@import "{rel_from_css(local, css_url)}"'

    css_text = CSS_URL_RE.sub(replace_url, css_text)
    css_text = CSS_IMPORT_RE.sub(replace_import, css_text)
    return css_text


def download_css_asset(url, referrer_url=None):
    """Download CSS, process nested asset references, save processed version."""
    if url in downloaded_assets:
        return downloaded_assets[url]
    if url.startswith("data:") or url.startswith("mailto:") or url.startswith("#"):
        downloaded_assets[url] = url
        return url

    full_url = urljoin(referrer_url or BASE_URL, url)
    parsed = urlparse(full_url)

    if parsed.scheme not in ("http", "https"):
        downloaded_assets[url] = url
        return url

    local_path = url_to_local_path(full_url)
    if local_path.suffix == "":
        local_path = Path(str(local_path) + ".css")

    if local_path.exists():
        try:
            rel = local_path.relative_to(OUTPUT_DIR)
            rel_str = str(rel).replace("\\", "/")
            downloaded_assets[url] = rel_str
            return rel_str
        except ValueError:
            pass

    try:
        resp = session.get(full_url, timeout=20)
        if resp.status_code == 404:
            print(f"  [404] {full_url}")
            assets_failed.append(full_url)
            downloaded_assets[url] = url
            return url
        resp.raise_for_status()

        css_text = resp.text
        # Mark as downloaded first to prevent recursion loops
        downloaded_assets[url] = "_processing_"
        css_text = process_css_text(css_text, full_url)

        os.makedirs(local_path.parent, exist_ok=True)
        local_path.write_text(css_text, encoding="utf-8")

        rel = local_path.relative_to(OUTPUT_DIR)
        rel_str = str(rel).replace("\\", "/")
        downloaded_assets[url] = rel_str
        assets_saved.append(full_url)
        print(f"  [css]   {full_url} -> {rel_str}")
        return rel_str
    except Exception as e:
        print(f"  [error] {full_url}: {e}")
        assets_failed.append(full_url)
        downloaded_assets[url] = url
        return url


def compute_page_local_path(page_url):
    """Return the local HTML file path for a page URL."""
    parsed = urlparse(page_url)
    path = parsed.path or "/"
    rel = safe_rel_path(path)
    local = OUTPUT_DIR / rel
    # Ensure .html extension for pages
    if local.suffix not in (".html", ".htm"):
        if local.suffix == "":
            local = local.with_suffix(".html")
        # else keep as-is (e.g. .php served as html)
    return local


def page_relative(asset_local_rel, page_local_path):
    """Compute relative path from page HTML file to asset."""
    try:
        asset_abs = OUTPUT_DIR / asset_local_rel
        rel = os.path.relpath(asset_abs, page_local_path.parent).replace("\\", "/")
        return rel
    except Exception:
        return asset_local_rel


def process_page(url, depth=0):
    """Fetch, process and save a page. Recursively crawl links up to MAX_DEPTH."""
    if url in visited_pages:
        return
    visited_pages.add(url)

    print(f"\n[page d={depth}] {url}")

    try:
        resp = session.get(url, timeout=30)
        if resp.status_code != 200:
            print(f"  [skip] status {resp.status_code}")
            return
    except Exception as e:
        print(f"  [error fetching page] {e}")
        return

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp.text, "html.parser")
    page_local = compute_page_local_path(url)

    # --- Download CSS ---
    for tag in soup.find_all("link", rel=lambda r: r and "stylesheet" in r):
        href = tag.get("href", "")
        if href:
            local = download_css_asset(href, url)
            if not local.startswith(("http", "//", "data:", "_processing_")):
                tag["href"] = page_relative(local, page_local)

    # --- Download JS ---
    for tag in soup.find_all("script", src=True):
        src = tag["src"]
        local = download_asset(src, url)
        if not local.startswith(("http", "//", "data:")):
            tag["src"] = page_relative(local, page_local)

    # --- Download images ---
    for tag in soup.find_all("img"):
        for attr in ("src", "data-src", "data-lazy-src"):
            val = tag.get(attr, "")
            if val and not val.startswith("data:"):
                local = download_asset(val, url)
                if not local.startswith(("http", "//", "data:")):
                    tag[attr] = page_relative(local, page_local)
        srcset = tag.get("srcset", "")
        if srcset:
            new_parts = []
            for part in srcset.split(","):
                part = part.strip()
                pieces = part.split()
                if pieces:
                    src_url = pieces[0]
                    descriptor = " ".join(pieces[1:])
                    local = download_asset(src_url, url)
                    loc = page_relative(local, page_local) if not local.startswith(("http", "//", "data:")) else local
                    new_parts.append(f"{loc} {descriptor}".strip())
            tag["srcset"] = ", ".join(new_parts)

    # --- Download source tags (video/audio) ---
    for tag in soup.find_all("source"):
        src = tag.get("src", "")
        if src:
            local = download_asset(src, url)
            if not local.startswith(("http", "//", "data:")):
                tag["src"] = page_relative(local, page_local)

    # --- Process inline styles ---
    for tag in soup.find_all(style=True):
        style = tag["style"]
        def repl(m, _url=url, _page_local=page_local):
            asset_url = m.group(1).strip()
            if asset_url.startswith("data:"):
                return m.group(0)
            local = download_asset(asset_url, _url)
            if local.startswith(("http", "//", "data:")):
                return f"url('{local}')"
            return f"url('{page_relative(local, _page_local)}')"
        tag["style"] = CSS_URL_RE.sub(repl, style)

    # --- Collect internal links for crawling ---
    internal_links = []
    if depth < MAX_DEPTH:
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            full = urljoin(url, href)
            parsed_full = urlparse(full)
            full_clean = parsed_full._replace(fragment="").geturl()
            if is_same_domain(full_clean) and full_clean not in visited_pages:
                ext = Path(parsed_full.path).suffix.lower()
                if ext in ("", ".html", ".htm", ".php", ".asp", ".aspx"):
                    internal_links.append(full_clean)

    # Rewrite anchor hrefs to local HTML files
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        full = urljoin(url, href)
        parsed_full = urlparse(full)
        parsed_base = urlparse(BASE_URL)
        if parsed_full.netloc in ("", parsed_base.netloc):
            local_href = compute_page_local_path(full)
            try:
                rel = os.path.relpath(local_href, page_local.parent).replace("\\", "/")
                frag = "#" + parsed_full.fragment if parsed_full.fragment else ""
                tag["href"] = rel + frag
            except Exception:
                pass

    # Save HTML
    os.makedirs(page_local.parent, exist_ok=True)
    page_local.write_text(str(soup), encoding="utf-8")
    pages_saved.append(url)
    print(f"  [saved] {page_local}")

    # Crawl internal links
    for link in internal_links:
        if link not in visited_pages:
            time.sleep(0.3)
            process_page(link, depth + 1)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Cloning {BASE_URL} into {OUTPUT_DIR}")
    print("=" * 60)
    process_page(BASE_URL, depth=0)

    print("\n" + "=" * 60)
    print(f"Pages saved   : {len(pages_saved)}")
    for p in pages_saved:
        print(f"  {p}")
    print(f"\nAssets saved  : {len(assets_saved)}")
    print(f"Assets failed : {len(assets_failed)}")
    if assets_failed:
        print("Failed assets (first 20):")
        for a in assets_failed[:20]:
            print(f"  {a}")
    print(f"\nOpen in browser: {OUTPUT_DIR / 'index.html'}")


if __name__ == "__main__":
    main()
