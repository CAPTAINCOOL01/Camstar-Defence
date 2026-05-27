import re

with open(r'C:\Users\ramay\Desktop\Camstar-Defence\cloned\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacements = 0

# ── 1. HERO silhouette ──────────────────────────────────────────────────────
old_sil = re.search(r'<div class="silhouette">.*?</div>', html, re.DOTALL)
if old_sil:
    new_sil = '''<div class="silhouette">
        <img src="wp-content/uploads/2025/08/M45-Ace-Lite-101-Right-WEBP-1.webp" alt="Star M45 ACE Lite" style="width:90%;object-fit:contain;filter:drop-shadow(0 30px 60px rgba(209,30,58,0.35));" />
      </div>'''
    html = html[:old_sil.start()] + new_sil + html[old_sil.end():]
    replacements += 1
    print("1. Hero silhouette replaced")
else:
    print("MISS 1. Hero silhouette NOT found")

# ── 2. NAVBAR brand-mark ────────────────────────────────────────────────────
old_bm = re.search(r'<div class="brand-mark"><span>C</span></div>', html)
if old_bm:
    new_bm = '<img src="wp-content/uploads/2025/08/Logo-03-1-2.png" alt="Camstar Defence" style="height:42px;width:auto;filter:brightness(0) invert(1);" />'
    html = html[:old_bm.start()] + new_bm + html[old_bm.end():]
    replacements += 1
    print("2. Navbar brand-mark replaced")
else:
    print("MISS 2. Navbar brand-mark NOT found")

# ── 3. PRODUCT CARDS ────────────────────────────────────────────────────────
product_images = [
    ('SKU: M45-ACE',   'wp-content/uploads/2025/08/M45-Ace-Lite-101-Right-WEBP-1.webp', 'Star M45 ACE Lite'),
    ('SKU: TT-30',     'wp-content/uploads/2026/05/Star-TT30-Special-Right.png',        'Star TT30 Special'),
    ('SKU: M32',       'wp-content/uploads/2025/08/Star-M32-Right.webp',                'Star M32'),
    ('SKU: M30',       'wp-content/uploads/2025/08/Star-M30-Classic-Right-Black.webp',  'Star M30'),
    ('SKU: S30',       'wp-content/uploads/2025/08/Super-30-Right-scaled.webp',         'Star Super 30'),
    ('SKU: X32',       'wp-content/uploads/2025/08/Star-X32-Right-1.webp',              'Star X32'),
    ('SKU: B30',       'wp-content/uploads/2025/08/Star-Bolt-30-Right-1.webp',          'Star Bolt 30'),
    ('SKU: MX32',      'wp-content/uploads/2025/08/Star-Max-32-Right-1.webp',           'Star Max 32'),
    ('SKU: K1911',     'wp-content/uploads/2026/05/Star-King-1911-Right.png',           'Star King 1911'),
    ('SKU: BAAZ-30',   'wp-content/uploads/2026/05/BAAZ-30-scaled.png',                 'BAAZ 30'),
    ('SKU: FX-100',    'wp-content/uploads/2026/05/FX-100-Right.png',                   'Star FX-100'),
    ('SKU: 30-OG',     'wp-content/uploads/2026/05/Star-30-Original-Right-1.png',       'Star 30 Original'),
    ('SKU: SS-1911',   'wp-content/uploads/2026/05/Star-SS-1911-Right.png',             'Star SS 1911'),
]

for sku, src, alt in product_images:
    pattern = r'(<div class="product-sku">' + re.escape(sku) + r'</div>)(.*?)(<div class="product-name">.*?</div>)'
    def make_replacer(s, a):
        def replacer(m):
            pad = f'\n        <div class="pad"><img src="{s}" alt="{a}" class="product-photo" /></div>'
            return m.group(1) + m.group(2) + m.group(3) + pad
        return replacer
    new_html, n = re.subn(pattern, make_replacer(src, alt), html, flags=re.DOTALL)
    if n:
        html = new_html
        replacements += n
        print(f"3. Product pad added: {sku}")
    else:
        print(f"MISS 3. NOT found: {sku}")

# ── 4. About visual ─────────────────────────────────────────────────────────
m = re.search(r'(<div class="about-visual">.*?<div class="badge">.*?</div>)', html, re.DOTALL)
if m:
    img_tag = '\n        <img src="wp-content/uploads/2025/08/Star-M32-Landspace_1_11zon.jpg" alt="Camstar manufacturing" style="width:100%;height:100%;object-fit:cover;opacity:0.45;position:absolute;inset:0;" />'
    insert_pos = m.end(1)
    html = html[:insert_pos] + img_tag + html[insert_pos:]
    replacements += 1
    print("4. About visual image added")
else:
    print("MISS 4. About visual NOT found")

# ── 5. CSS ───────────────────────────────────────────────────────────────────
product_css = '''/* Product images */
.product-photo {
  width: 85%;
  height: 85%;
  object-fit: contain;
  object-position: center;
  transition: transform 0.5s ease, opacity 0.4s ease;
  filter: drop-shadow(0 20px 40px rgba(0,0,0,0.8));
}
.product:hover .product-photo {
  transform: scale(1.06);
}
.product.feature .product-photo {
  width: 75%;
  height: 75%;
}

'''
reveal_anchor = '/* ============================================================\n   REVEAL ANIMATION'
if reveal_anchor in html:
    html = html.replace(reveal_anchor, product_css + reveal_anchor, 1)
    replacements += 1
    print("5. Product CSS added before REVEAL ANIMATION")
else:
    html = html.replace('</style>', product_css + '</style>', 1)
    replacements += 1
    print("5. Product CSS added before </style> (fallback)")

with open(r'C:\Users\ramay\Desktop\Camstar-Defence\cloned\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal replacements/insertions: {replacements}")
