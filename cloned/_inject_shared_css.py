"""
Inject the master stylesheet (first <style> block of index.html) into pages
that carry a /*__SHARED_CSS__*/ placeholder. Run after any index.html CSS change:
    python _inject_shared_css.py products.html about.html contact.html
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
MARKER = "/*__SHARED_CSS__*/"

css = re.search(
    r"<style>(.*?)</style>",
    (BASE / "index.html").read_text(encoding="utf-8"),
    re.DOTALL,
).group(1)

for name in sys.argv[1:]:
    p = BASE / name
    html = p.read_text(encoding="utf-8")
    if MARKER not in html:
        # already injected: refresh by replacing everything between the
        # sentinel comments if present, else skip
        if "/*__SHARED_START__*/" in html:
            html = re.sub(
                r"/\*__SHARED_START__\*/.*?/\*__SHARED_END__\*/",
                "/*__SHARED_START__*/" + css + "/*__SHARED_END__*/",
                html,
                flags=re.DOTALL,
            )
            p.write_text(html, encoding="utf-8")
            print(f"refreshed  {name}")
        else:
            print(f"skipped    {name} (no marker)")
        continue
    html = html.replace(MARKER, "/*__SHARED_START__*/" + css + "/*__SHARED_END__*/")
    p.write_text(html, encoding="utf-8")
    print(f"injected   {name}")
