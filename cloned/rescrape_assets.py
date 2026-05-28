"""
rescrape_assets.py
------------------
Fetches https://camstardefence.com and a set of product pages, then
parses every page for image references (img/src, srcset, source,
inline background-image, link rel=preload as=image, og:image).

Only images hosted on camstardefence.com that are NOT already present
under cloned/wp-content/uploads/ are downloaded, preserving relative
directory structure.

Defensive: skips Google Fonts / external CDNs, handles 404s, supports
both http and https, uses a real browser User-Agent.
"""

import os
import re
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from html.parser import HTMLParser

BASE = "https://camstardefence.com"
ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOADS_ROOT = os.path.join(ROOT, "wp-content", "uploads")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

PAGES = [
    "/",
    "/about-us/",
    "/contact-us/",
    "/shop/",
    "/star-m45-ace-lite/",
    "/star-tt30/",
    "/star-m32/",
    "/star-m30/",
    "/super-30/",
    "/star-x32/",
    "/star-bolt-30/",
    "/star-max-32/",
    "/star-king-1911/",
    "/baaz-30/",
    "/star-fx-100/",
    "/star-30-original/",
    "/star-ss-1911/",
]

# Keywords used to bias what we report as "interesting" (banner/lifestyle)
HERO_KEYWORDS = ("hero", "banner", "slider", "lifestyle", "workshop",
                 "range", "background", "bg-", "landspace", "landscape",
                 "aesthetic")


class ImgParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = set()

    def _collect(self, value):
        if not value:
            return
        # srcset entries are comma-separated "url 1024w, url 1290w"
        for part in value.split(","):
            url = part.strip().split(" ")[0]
            if url:
                self.urls.add(url)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "img":
            if a.get("src"):
                self.urls.add(a["src"])
            if a.get("data-src"):
                self.urls.add(a["data-src"])
            if a.get("data-lazy-src"):
                self.urls.add(a["data-lazy-src"])
            self._collect(a.get("srcset"))
            self._collect(a.get("data-srcset"))
        elif tag == "source":
            self._collect(a.get("srcset"))
            self._collect(a.get("data-srcset"))
        elif tag == "link":
            if a.get("rel", "").lower() == "preload" and a.get("as") == "image":
                if a.get("href"):
                    self.urls.add(a["href"])
        elif tag == "meta":
            if a.get("property") in ("og:image", "og:image:secure_url",
                                     "twitter:image"):
                if a.get("content"):
                    self.urls.add(a["content"])
        # inline style background-image
        style = a.get("style")
        if style:
            for m in re.findall(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', style):
                self.urls.add(m)


def fetch(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(), r.status
    except urllib.error.HTTPError as e:
        return None, e.code
    except Exception as e:
        return None, str(e)


def normalize(url, page_url):
    if not url:
        return None
    url = url.strip()
    if url.startswith("data:"):
        return None
    if url.startswith("//"):
        url = "https:" + url
    if url.startswith("/"):
        url = urllib.parse.urljoin(BASE, url)
    if not url.startswith(("http://", "https://")):
        url = urllib.parse.urljoin(page_url, url)
    return url


def is_camstar(url):
    try:
        host = urllib.parse.urlparse(url).netloc.lower()
        return host.endswith("camstardefence.com")
    except Exception:
        return False


def is_external_cdn(url):
    bad = ("fonts.googleapis.com", "fonts.gstatic.com",
           "googletagmanager.com", "google-analytics.com",
           "facebook.com", "facebook.net", "cdn.jsdelivr.net",
           "gravatar.com", "youtube.com", "ytimg.com")
    host = urllib.parse.urlparse(url).netloc.lower()
    return any(b in host for b in bad)


def is_image(url):
    path = urllib.parse.urlparse(url).path.lower()
    return path.endswith((".jpg", ".jpeg", ".png", ".webp", ".gif",
                          ".svg", ".avif", ".ico"))


def local_path_for(url):
    """Map camstardefence.com/wp-content/uploads/... -> cloned/wp-content/uploads/..."""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lstrip("/")  # e.g. wp-content/uploads/2025/08/foo.jpg
    # strip query string already handled
    return os.path.join(ROOT, path.replace("/", os.sep))


def download(url, dest):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=25) as r:
            data = r.read()
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(data)
        return True, len(data)
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)


def main():
    discovered = set()
    print(f"[*] Crawling {len(PAGES)} pages on {BASE}\n")

    for path in PAGES:
        url = BASE.rstrip("/") + path
        body, status = fetch(url)
        if not body:
            print(f"  [skip] {path}  -> {status}")
            continue
        try:
            html = body.decode("utf-8", errors="ignore")
        except Exception:
            continue
        p = ImgParser()
        try:
            p.feed(html)
        except Exception:
            pass
        # Also raw regex for any url() in <style> blocks
        for m in re.findall(r'url\(\s*["\']?([^"\')]+\.(?:jpg|jpeg|png|webp|gif|svg|avif))["\']?\s*\)',
                            html, flags=re.IGNORECASE):
            p.urls.add(m)
        page_imgs = 0
        for u in p.urls:
            full = normalize(u, url)
            if not full:
                continue
            if is_external_cdn(full):
                continue
            if not is_image(full):
                continue
            if not is_camstar(full):
                continue
            discovered.add(full)
            page_imgs += 1
        print(f"  [ok]   {path}  -> {page_imgs} image refs")
        time.sleep(0.3)

    print(f"\n[*] {len(discovered)} unique camstardefence.com image URLs discovered.")

    # Filter to those missing locally
    missing = []
    hero_like = []
    for u in sorted(discovered):
        dest = local_path_for(u)
        if not os.path.exists(dest):
            missing.append((u, dest))
            low = u.lower()
            if any(k in low for k in HERO_KEYWORDS):
                hero_like.append(u)

    print(f"[*] {len(missing)} missing locally. {len(hero_like)} look hero/lifestyle.\n")

    if hero_like:
        print("    Hero/lifestyle candidates:")
        for u in hero_like:
            print(f"      - {u}")
        print()

    downloaded = 0
    failed = 0
    for u, dest in missing:
        ok, info = download(u, dest)
        rel = os.path.relpath(dest, ROOT)
        if ok:
            downloaded += 1
            print(f"  [+] {rel}  ({info} bytes)")
        else:
            failed += 1
            print(f"  [!] {rel}  -> {info}")
        time.sleep(0.15)

    print(f"\n[done] downloaded={downloaded}  failed={failed}  already_present={len(discovered)-len(missing)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
