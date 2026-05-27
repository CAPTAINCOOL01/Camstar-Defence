import glob
import os

STYLE_BLOCK = '''
<style>
/* ============================================================
   Camstar Defence – Sports Theme Override
   Matches camstarsports.com visual identity
   ============================================================ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
  --bg: #0a0a0a;
  --surface: #111111;
  --surface2: #181818;
  --surface3: #1f1f1f;
  --primary: #e02020;
  --primary-dark: #b91c1c;
  --red-glow: rgba(224,32,32,0.2);
  --text: #f0f0f0;
  --text-dim: rgba(255,255,255,0.58);
  --text-muted: rgba(255,255,255,0.35);
  --border: rgba(255,255,255,0.08);
  --border-light: rgba(255,255,255,0.14);
}

html {
  scroll-behavior: smooth !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px !important; height: 5px !important; }
::-webkit-scrollbar-track { background: var(--bg) !important; }
::-webkit-scrollbar-thumb { background: var(--primary) !important; border-radius: 3px !important; }
::selection { background: rgba(224,32,32,0.35) !important; }

/* Base */
body, html {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Inter', system-ui, sans-serif !important;
}

/* Kill white/light backgrounds everywhere */
*,
div, section, article, aside, main, footer, header,
.elementor-section, .elementor-container, .elementor-widget-wrap,
.elementor-widget-container, .e-container, .e-flex,
[class*="elementor-"], [class*="wp-block-"],
.site-main, .site-content, .site-wrapper, .page-wrapper,
.container, .container-fluid, .row,
.woocommerce, .woocommerce-page {
  background-color: transparent !important;
}

/* Re-apply dark bg to root elements */
body { background-color: var(--bg) !important; }
.site, #page, #content, .site-content, main, .main-content,
.elementor-section-wrap, .entry-content {
  background-color: var(--bg) !important;
}

/* Navbar / Header */
header, .site-header, #masthead, nav, .navbar,
.main-navigation, .header-main, .site-header-inner,
[class*="header"], [class*="nav-wrap"], [class*="menu-bar"],
.elementor-section.elementor-top-section:first-of-type {
  background: rgba(10,10,10,0.92) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border-bottom: 1px solid rgba(255,255,255,0.07) !important;
  position: sticky !important;
  top: 0 !important;
  z-index: 9999 !important;
}

/* Text colors */
p, span, li, td, th, label, input, textarea, select,
.elementor-widget-text-editor, .elementor-text-editor,
[class*="description"], [class*="content-text"] {
  color: var(--text-dim) !important;
}

h1, h2, h3, h4, h5, h6,
.elementor-heading-title, [class*="title"], [class*="heading"] {
  color: var(--text) !important;
}

/* Links */
a { color: var(--text-dim) !important; text-decoration: none !important; transition: color 0.2s !important; }
a:hover { color: var(--primary) !important; }

/* Buttons */
button, .button, .btn, input[type="submit"], input[type="button"],
a.button, a.btn, .wp-block-button__link,
.elementor-button, [class*="elementor-button"],
.woocommerce a.button, .woocommerce button.button,
.woocommerce input.button, .woocommerce #respond input#submit,
.add_to_cart_button, .single_add_to_cart_button {
  background: var(--primary) !important;
  background-color: var(--primary) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 6px !important;
  font-weight: 700 !important;
  font-family: 'Inter', system-ui, sans-serif !important;
  box-shadow: 0 0 20px rgba(224,32,32,0.3) !important;
  transition: background 0.2s, transform 0.2s, box-shadow 0.2s !important;
  cursor: pointer !important;
}
button:hover, .button:hover, .btn:hover, input[type="submit"]:hover,
a.button:hover, a.btn:hover, .wp-block-button__link:hover,
.elementor-button:hover, .woocommerce a.button:hover,
.woocommerce button.button:hover, .add_to_cart_button:hover,
.single_add_to_cart_button:hover {
  background: var(--primary-dark) !important;
  background-color: var(--primary-dark) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 0 28px rgba(224,32,32,0.45) !important;
}

/* Cards & surfaces */
.card, .product, li.product, .woocommerce-loop-product,
.elementor-widget, [class*="card"], [class*="-item"],
[class*="-box"], [class*="-panel"], [class*="-block"],
.wc-block-product-template, .woocommerce ul.products li.product,
article, .post, .entry {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
}

/* Section alternating backgrounds */
section:nth-child(even), .elementor-section:nth-child(even) {
  background: var(--surface2) !important;
}
section:nth-child(odd), .elementor-section:nth-child(odd) {
  background: var(--bg) !important;
}

/* Inputs & forms */
input, textarea, select {
  background: var(--surface3) !important;
  color: var(--text) !important;
  border: 1px solid var(--border-light) !important;
  border-radius: 6px !important;
}
input::placeholder, textarea::placeholder {
  color: var(--text-muted) !important;
}
input:focus, textarea:focus, select:focus {
  outline: none !important;
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 2px rgba(224,32,32,0.2) !important;
}

/* WooCommerce price */
.price, .woocommerce-Price-amount, ins .amount {
  color: var(--primary) !important;
}
del .amount { color: var(--text-muted) !important; }

/* Footer */
footer, .site-footer, #colophon, [class*="footer"] {
  background: var(--surface) !important;
  border-top: 1px solid var(--border) !important;
  color: var(--text-dim) !important;
}

/* Tables */
table { border-collapse: collapse !important; }
th { background: var(--surface3) !important; color: var(--text) !important; }
td { color: var(--text-dim) !important; border-color: var(--border) !important; }
tr:nth-child(even) { background: var(--surface2) !important; }

/* Breadcrumbs */
.woocommerce-breadcrumb, .breadcrumbs, [class*="breadcrumb"] {
  color: var(--text-muted) !important;
}

/* Badges / labels */
.onsale, .badge, [class*="badge"], [class*="label-"] {
  background: var(--primary) !important;
  color: #fff !important;
}

/* Dividers / hr */
hr { border-color: var(--border) !important; }

/* Image overlays – keep images visible */
img { opacity: 1 !important; }

/* Force remove any inline white backgrounds */
[style*="background: #fff"], [style*="background:#fff"],
[style*="background: white"], [style*="background:white"],
[style*="background-color: #fff"], [style*="background-color:#fff"],
[style*="background-color: white"], [style*="background-color:white"] {
  background: var(--surface) !important;
  background-color: var(--surface) !important;
}
[style*="color: #000"], [style*="color:#000"],
[style*="color: black"], [style*="color:black"],
[style*="color: #111"], [style*="color:#111"],
[style*="color: #222"], [style*="color:#222"],
[style*="color: #333"], [style*="color:#333"],
[style*="color: #444"], [style*="color:#444"] {
  color: var(--text) !important;
}
</style>
<!-- /Camstar Sports Theme -->
'''

cloned_root = r"C:\Users\ramay\Desktop\Camstar-Defence\cloned"

html_files = glob.glob(os.path.join(cloned_root, "**", "*.html"), recursive=True)
html_files += glob.glob(os.path.join(cloned_root, "*.html"))
# Deduplicate
html_files = list(set(html_files))

updated = []
skipped = []

for path in sorted(html_files):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Skip if already injected
    if "Camstar Sports Theme" in content:
        skipped.append(path)
        continue

    # Inject before </head>
    if "</head>" in content:
        content = content.replace("</head>", STYLE_BLOCK + "\n</head>", 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        updated.append(path)
    else:
        skipped.append(path)
        print(f"NO </head> found: {path}")

print(f"\nUpdated {len(updated)} files:")
for p in updated:
    print(" +", p)
print(f"\nSkipped {len(skipped)} files:")
for p in skipped:
    print(" -", p)
