"""
Build premium product detail pages for all 13 Camstar Defence products.
Reuses the design system from cloned/index.html (CSS, nav, footer, scripts).
Writes UTF-8 to avoid garbled characters.
"""
from pathlib import Path
import re
import shutil
import random

BASE = Path(__file__).resolve().parent
LANDING = BASE / "index.html"

# -------------------------------------------------------------
# 1) Extract the shared CSS from the landing page
# -------------------------------------------------------------
landing_html = LANDING.read_text(encoding="utf-8")
css_match = re.search(r"<style>(.*?)</style>", landing_html, re.DOTALL)
SHARED_CSS = css_match.group(1) if css_match else ""

# -------------------------------------------------------------
# 2) Product data
# -------------------------------------------------------------
PRODUCTS = [
    {
        "slug": "star-m45-ace-lite",
        "name": "Star M45 ACE Lite",
        "sku": "M45-ACE",
        "caliber": ".45 ACP",
        "capacity": "10+1",
        "weight": "900 g",
        "action": "Single Action, Semi-Auto",
        "safety": "Triple Safety",
        "frame": "Forged Steel, Match-Grade",
        "finish": "Premium Black",
        "barrel": "5.0 in / 127 mm",
        "img_right": "wp-content/uploads/2025/08/M45-Ace-Lite-101-Right-WEBP-1.webp",
        "img_left": "wp-content/uploads/2025/08/M45-Ace-Lite-101-Left.webp",
        "tagline": "The flagship. Steel-on-steel lockup, competition-grade trigger break.",
        "tags": ["Flagship", ".45 ACP", "Competition", "Alloy Frame"],
    },
    {
        "slug": "star-tt30",
        "name": "Star TT 30 Special",
        "sku": "TT-30",
        "caliber": ".30 Bore",
        "capacity": "8+1",
        "weight": "830 g",
        "action": "Semi-Automatic",
        "safety": "Triple Safety",
        "frame": "Forged Steel",
        "finish": "Black Oxide",
        "barrel": "4.5 in / 114 mm",
        "img_right": "wp-content/uploads/2026/05/Star-TT30-Special-Right.png",
        "img_left": "wp-content/uploads/2026/05/Star-TT30-Special-Lift.png",
        "tagline": "A modern tribute to the legendary Tokarev. Refined for the licensed marksman.",
        "tags": [".30 Bore", "Classic", "All-Steel"],
    },
    {
        "slug": "star-m32",
        "name": "Star M32",
        "sku": "M32",
        "caliber": ".32 Bore",
        "capacity": "7+1",
        "weight": "740 g",
        "action": "Semi-Automatic",
        "safety": "Triple Safety",
        "frame": "Forged Steel",
        "finish": "Black Oxide",
        "barrel": "4.0 in / 102 mm",
        "img_right": "wp-content/uploads/2025/08/Star-M32-Right.webp",
        "img_left": "wp-content/uploads/2025/08/Star-M32-Left.webp",
        "tagline": "Compact precision. Ergonomic grip. Built for everyday carry.",
        "tags": [".32 Bore", "Compact", "EDC"],
    },
    {
        "slug": "star-m30",
        "name": "Star M30 Classic",
        "sku": "M30",
        "caliber": ".30 Bore",
        "capacity": "8+1",
        "weight": "820 g",
        "action": "Semi-Automatic",
        "safety": "Triple Safety",
        "frame": "Forged Steel",
        "finish": "Black Oxide",
        "barrel": "4.5 in / 114 mm",
        "img_right": "wp-content/uploads/2025/08/Star-M30-Classic-Right-Black.webp",
        "img_left": "wp-content/uploads/2025/08/Star-M30-Classic-Left-Black.webp",
        "tagline": "The original. Black finish. Triple-safety system.",
        "tags": [".30 Bore", "Classic", "Heritage"],
    },
    {
        "slug": "star-super-30",
        "name": "Star Super 30",
        "sku": "S30",
        "caliber": ".30 Bore",
        "capacity": "8+1",
        "weight": "850 g",
        "action": "Semi-Automatic",
        "safety": "Triple Safety",
        "frame": "Forged Steel, Enhanced",
        "finish": "Black Oxide",
        "barrel": "4.7 in / 119 mm",
        "img_right": "wp-content/uploads/2025/08/Super-30-Right-scaled.webp",
        "img_left": "wp-content/uploads/2025/08/Super-30-Right-scaled.webp",
        "tagline": "Enhanced barrel, refined recoil. The Super edition.",
        "tags": [".30 Bore", "Enhanced", "Super"],
    },
    {
        "slug": "star-x32",
        "name": "Star X32",
        "sku": "X32",
        "caliber": ".32 Bore",
        "capacity": "7+1",
        "weight": "730 g",
        "action": "Semi-Automatic",
        "safety": "Triple Safety",
        "frame": "Forged Steel",
        "finish": "Black Oxide",
        "barrel": "4.0 in / 102 mm",
        "img_right": "wp-content/uploads/2025/08/Star-X32-Right-1.webp",
        "img_left": "wp-content/uploads/2025/08/Star-X32-Left-1.webp",
        "tagline": "Compact frame. Tactical edge. Built for fast draw.",
        "tags": [".32 Bore", "Tactical", "Fast Draw"],
    },
    {
        "slug": "star-bolt-30",
        "name": "Star Bolt 30",
        "sku": "B30",
        "caliber": ".30 Bore",
        "capacity": "8+1",
        "weight": "840 g",
        "action": "Semi-Automatic",
        "safety": "Triple Safety",
        "frame": "Forged Steel",
        "finish": "Black Oxide",
        "barrel": "4.5 in / 114 mm",
        "img_right": "wp-content/uploads/2025/08/Star-Bolt-30-Right-1.webp",
        "img_left": "wp-content/uploads/2025/08/Star-Bolt-30-Left-1.webp",
        "tagline": "Bolt-action precision. Field-tested reliability.",
        "tags": [".30 Bore", "Field", "Reliable"],
    },
    {
        "slug": "star-max-32",
        "name": "Star Max 32",
        "sku": "MAX32",
        "caliber": ".32 Bore",
        "capacity": "7+1",
        "weight": "760 g",
        "action": "Semi-Automatic",
        "safety": "Triple Safety",
        "frame": "Forged Steel",
        "finish": "Premium Black",
        "barrel": "4.2 in / 107 mm",
        "img_right": "wp-content/uploads/2025/08/Star-Max-32-Right-1.webp",
        "img_left": "wp-content/uploads/2025/08/Star-Max-32-Left.webp",
        "tagline": "Premium-grade .32 with extended performance.",
        "tags": [".32 Bore", "Premium", "Extended"],
    },
    {
        "slug": "star-king-1911",
        "name": "Star King 1911",
        "sku": "K1911",
        "caliber": ".45 ACP",
        "capacity": "7+1",
        "weight": "880 g",
        "action": "Single Action, Semi-Auto",
        "safety": "Grip + Manual Safety",
        "frame": "Forged Steel, 1911 Platform",
        "finish": "Black Oxide",
        "barrel": "5.0 in / 127 mm",
        "img_right": "wp-content/uploads/2026/05/Star-King-1911-Right.png",
        "img_left": "wp-content/uploads/2026/05/Star-King-1911-Lift.png",
        "tagline": "The 1911 platform, perfected. Heritage meets precision.",
        "tags": [".45 ACP", "1911 Platform", "Premium"],
    },
    {
        "slug": "baaz-30",
        "name": "BAAZ 30",
        "sku": "BAAZ-30",
        "caliber": ".30 Bore",
        "capacity": "8+1",
        "weight": "850 g",
        "action": "Semi-Automatic",
        "safety": "Triple Independent Safety",
        "frame": "Forged Steel, Defence Grade",
        "finish": "Corrosion-Resistant Black",
        "barrel": "4.5 in / 114 mm",
        "img_right": "wp-content/uploads/2026/05/BAAZ-30-scaled.png",
        "img_left": "wp-content/uploads/2026/05/BAAZ-30-scaled.png",
        "tagline": "Defence grade. Three independent safeties. Steel lockup.",
        "tags": ["Defence Grade", ".30 Bore", "3x Safety", "Pro"],
    },
    {
        "slug": "star-fx-100",
        "name": "Star FX-100",
        "sku": "FX-100",
        "caliber": ".32 Bore",
        "capacity": "7+1",
        "weight": "720 g",
        "action": "Semi-Automatic",
        "safety": "Triple Safety",
        "frame": "Lightweight Alloy",
        "finish": "Tactical Matte",
        "barrel": "4.0 in / 102 mm",
        "img_right": "wp-content/uploads/2026/05/FX-100-Right.png",
        "img_left": "wp-content/uploads/2026/05/FX-100-Lift.png",
        "tagline": "Field-edition .32. Lightweight frame, tactical grip.",
        "tags": [".32 Bore", "Lightweight", "Tactical"],
    },
    {
        "slug": "star-30-original",
        "name": "Star 30 Original",
        "sku": "S30-OG",
        "caliber": ".30 Bore",
        "capacity": "8+1",
        "weight": "820 g",
        "action": "Semi-Automatic",
        "safety": "Triple Safety",
        "frame": "Forged Steel",
        "finish": "Black Oxide",
        "barrel": "4.5 in / 114 mm",
        "img_right": "wp-content/uploads/2026/05/Star-30-Original-Right-1.png",
        "img_left": "wp-content/uploads/2026/05/Star-30-Original-Lift.png",
        "tagline": "The classic. Decades of refinement, unchanged in spirit.",
        "tags": [".30 Bore", "Classic", "Heritage"],
    },
    {
        "slug": "star-ss-1911",
        "name": "Star SS 1911",
        "sku": "SS-1911",
        "caliber": ".45 ACP",
        "capacity": "7+1",
        "weight": "890 g",
        "action": "Single Action, Semi-Auto",
        "safety": "Grip + Manual Safety",
        "frame": "Stainless Steel, 1911 Platform",
        "finish": "Stainless / Match-Grade",
        "barrel": "5.0 in / 127 mm",
        "img_right": "wp-content/uploads/2026/05/Star-SS-1911-Right.png",
        "img_left": "wp-content/uploads/2026/05/Star-SS-1911-Left.png",
        "tagline": "Stainless 1911. Premium finish. Match-grade barrel.",
        "tags": [".45 ACP", "1911 Platform", "Stainless"],
    },
]

# -------------------------------------------------------------
# 3) Page-specific extra CSS (product hero, gallery, feature cards)
# -------------------------------------------------------------
EXTRA_CSS = """
/* ===== PRODUCT DETAIL PAGE ===== */
.prod-hero{
  padding-block:clamp(3rem,7vw,5.5rem);
  position:relative;overflow:hidden;
}
.prod-hero::before{
  content:'';position:absolute;top:-30%;right:-20%;width:80%;height:140%;
  background:radial-gradient(ellipse at center,rgba(209,30,58,0.10) 0%,transparent 65%);
  pointer-events:none;z-index:0;
}
.prod-hero-grid{
  display:grid;grid-template-columns:1.05fr 1fr;gap:clamp(2rem,5vw,4.5rem);
  align-items:center;position:relative;z-index:1;
}
@media(max-width:900px){.prod-hero-grid{grid-template-columns:1fr;}}

.gallery{display:flex;flex-direction:column;gap:1rem;}
.gallery-main{
  position:relative;aspect-ratio:4/3;border-radius:var(--radius-lg);
  background:
    radial-gradient(ellipse at center, rgba(209,30,58,0.12) 0%, transparent 60%),
    linear-gradient(135deg,var(--bg-2) 0%,var(--bg-1) 100%);
  border:var(--border);overflow:hidden;
  display:flex;align-items:center;justify-content:center;
}
.gallery-main::before{
  content:'';position:absolute;inset:0;
  background:
    linear-gradient(rgba(209,30,58,0.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(209,30,58,0.03) 1px,transparent 1px);
  background-size:32px 32px;
  pointer-events:none;
}
.gallery-main img{
  width:88%;height:88%;object-fit:contain;
  filter:drop-shadow(0 30px 60px rgba(0,0,0,0.85)) drop-shadow(0 0 25px rgba(209,30,58,0.18));
  animation:cdFloat 6s ease-in-out infinite;
  position:relative;z-index:1;
}
@keyframes cdFloat{0%,100%{transform:translateY(0);}50%{transform:translateY(-10px);}}
.gallery-thumbs{display:grid;grid-template-columns:repeat(2,1fr);gap:0.75rem;}
.thumb{
  height:90px;border-radius:var(--radius);background:var(--bg-2);border:var(--border);
  display:flex;align-items:center;justify-content:center;overflow:hidden;
  cursor:pointer;transition:border-color var(--transition),transform var(--transition);
  position:relative;
}
.thumb:hover{border-color:var(--red);transform:translateY(-2px);}
.thumb img{width:75%;height:75%;object-fit:contain;filter:drop-shadow(0 8px 18px rgba(0,0,0,0.7));}
.thumb-label{
  position:absolute;left:0.5rem;bottom:0.4rem;
  font-family:'JetBrains Mono',monospace;font-size:0.55rem;letter-spacing:0.14em;
  text-transform:uppercase;color:var(--ink-3);
}

.prod-meta .eyebrow{margin-bottom:1rem;}
.prod-meta h1{margin-bottom:1.25rem;font-size:clamp(2.4rem,5vw,4rem);}
.prod-tagline{color:var(--ink-1);font-size:1.05rem;line-height:1.75;max-width:480px;margin-bottom:2rem;}
.prod-quick{
  display:grid;grid-template-columns:repeat(3,1fr);gap:1px;
  background:rgba(247,246,243,0.05);border:1px solid rgba(247,246,243,0.05);
  border-radius:var(--radius);overflow:hidden;margin-bottom:2rem;
}
.prod-quick .qi{background:var(--bg-2);padding:0.9rem 1rem;}
.prod-quick .qi .k{font-family:'JetBrains Mono',monospace;font-size:0.58rem;letter-spacing:0.14em;text-transform:uppercase;color:var(--ink-3);margin-bottom:0.3rem;}
.prod-quick .qi .v{font-family:'Anton',sans-serif;font-size:1.15rem;letter-spacing:0.03em;color:var(--ink-0);}
.prod-ctas{display:flex;gap:0.75rem;flex-wrap:wrap;}

/* ===== DETAILED SPECS SECTION ===== */
.specs-block{background:var(--bg-1);border-block:var(--border);padding-block:clamp(4rem,8vw,6rem);}
.specs6{
  display:grid;grid-template-columns:repeat(6,1fr);gap:1px;
  background:rgba(247,246,243,0.05);border:1px solid rgba(247,246,243,0.05);
  border-radius:var(--radius-lg);overflow:hidden;margin-top:2.5rem;
}
.specs6 .sp{background:var(--bg-1);padding:1.5rem 1.2rem;transition:background var(--transition);}
.specs6 .sp:hover{background:var(--bg-2);}
.specs6 .sp .k{font-family:'JetBrains Mono',monospace;font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:var(--ink-3);margin-bottom:0.5rem;}
.specs6 .sp .v{font-family:'Anton',sans-serif;font-size:1.25rem;letter-spacing:0.03em;color:var(--ink-0);line-height:1.15;}
@media(max-width:900px){.specs6{grid-template-columns:repeat(3,1fr);}}
@media(max-width:520px){.specs6{grid-template-columns:repeat(2,1fr);}}

/* ===== FEATURE CARDS ===== */
.features-block{padding-block:clamp(4rem,8vw,6rem);}
.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(247,246,243,0.05);border:1px solid rgba(247,246,243,0.05);border-radius:var(--radius-lg);overflow:hidden;margin-top:2.5rem;}
.feat{background:var(--bg-1);padding:2rem 1.75rem;transition:background var(--transition);}
.feat:hover{background:var(--bg-2);}
.feat-ico{width:48px;height:48px;background:rgba(209,30,58,0.1);border-radius:var(--radius);display:flex;align-items:center;justify-content:center;color:var(--red);margin-bottom:1.25rem;}
.feat h3{font-family:'Anton',sans-serif;font-size:1.2rem;letter-spacing:0.04em;text-transform:uppercase;color:var(--ink-0);margin-bottom:0.6rem;}
.feat p{font-size:0.88rem;color:var(--ink-2);line-height:1.7;}
@media(max-width:780px){.feat-grid{grid-template-columns:1fr;}}

/* ===== RELATED PRODUCTS (3-up) ===== */
.related-block{background:var(--bg-1);border-block:var(--border);padding-block:clamp(4rem,8vw,6rem);}
.related-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(247,246,243,0.05);border:1px solid rgba(247,246,243,0.05);border-radius:var(--radius-lg);overflow:hidden;margin-top:2.5rem;}
@media(max-width:780px){.related-grid{grid-template-columns:1fr;}}
"""

# -------------------------------------------------------------
# 4) Build the HTML for a single product
# -------------------------------------------------------------
def page_head(prod):
    title = f"{prod['name']} &middot; Camstar Defence"
    desc = f"{prod['name']} &mdash; {prod['caliber']} sidearm, {prod['capacity']} capacity. {prod['tagline']}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Anton&amp;family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet"/>
<style>
{SHARED_CSS}
{EXTRA_CSS}
</style>
</head>
"""

UTIL_BAR = """<div class="util-bar">
  Licensed Firearms Manufacturer &middot; Made in India &middot; +91 9793 849 997 &middot; info@camstardefence.com
</div>
"""

# Nav uses ../ paths because product pages live in subfolders
NAV = """<nav class="nav">
  <div class="wrap nav-inner">
    <a href="../index.html" class="brand">
      <img src="../wp-content/uploads/2025/08/Logo-03-1-2.png" alt="Camstar Defence" style="height:42px;width:auto;filter:brightness(0) invert(1);"/>
      <div class="brand-text">
        <span class="name">Camstar</span>
        <span class="sub">Defence &middot; EST. 1997</span>
      </div>
    </a>
    <div class="nav-links">
      <a href="../index.html">Home</a>
      <a href="../about.html">About</a>
      <a href="../products.html" class="active">Arsenal</a>
      <a href="../contact.html">Contact</a>
    </div>
    <div class="nav-right">
      <a href="../contact.html" class="nav-cta">Get In Touch</a>
      <button class="nav-toggle" id="navToggle" aria-label="Toggle menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
  <div class="mobile-menu" id="mobileMenu">
    <a href="../index.html">Home</a>
    <a href="../about.html">About</a>
    <a href="../products.html" class="active">Arsenal</a>
    <a href="../contact.html">Contact</a>
    <a href="../contact.html">Get In Touch</a>
  </div>
</nav>
"""

def breadcrumb(prod):
    return f"""<div class="wrap" style="padding-top:2rem;padding-bottom:0.5rem;">
  <div class="section-num"><span>00</span> / <a href="../index.html" style="color:var(--ink-3);">Home</a> &nbsp;/&nbsp; <a href="../products.html" style="color:var(--ink-3);">Arsenal</a> &nbsp;/&nbsp; <span style="color:var(--red);">{prod['name']}</span></div>
</div>
"""

def hero(prod):
    return f"""<section class="prod-hero">
  <div class="wrap">
    <div class="prod-hero-grid">
      <div class="gallery reveal">
        <div class="gallery-main">
          <img src="../{prod['img_right']}" alt="{prod['name']}"/>
        </div>
        <div class="gallery-thumbs">
          <div class="thumb">
            <img src="../{prod['img_right']}" alt="{prod['name']} right view"/>
            <span class="thumb-label">Right</span>
          </div>
          <div class="thumb">
            <img src="../{prod['img_left']}" alt="{prod['name']} left view"/>
            <span class="thumb-label">Left</span>
          </div>
        </div>
      </div>
      <div class="prod-meta reveal">
        <span class="eyebrow">SKU: {prod['sku']} &middot; {prod['caliber']}</span>
        <h1 class="h-display">{prod['name']}</h1>
        <p class="prod-tagline">{prod['tagline']}</p>
        <div class="prod-quick">
          <div class="qi"><div class="k">Calibre</div><div class="v">{prod['caliber']}</div></div>
          <div class="qi"><div class="k">Capacity</div><div class="v">{prod['capacity']}</div></div>
          <div class="qi"><div class="k">Action</div><div class="v">{prod['action'].split(',')[0]}</div></div>
        </div>
        <div class="prod-ctas">
          <a href="../contact.html" class="btn-primary">
            <span>Request Quote</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          </a>
          <a href="../contact.html#dealers" class="btn-ghost">Find Dealer</a>
        </div>
      </div>
    </div>
  </div>
</section>
"""

def specs(prod):
    return f"""<section class="specs-block">
  <div class="wrap">
    <div class="section-head reveal">
      <div class="section-num"><span>01</span> / Specifications</div>
      <h2 class="h-display">Engineered to spec.</h2>
    </div>
    <div class="specs6 reveal">
      <div class="sp"><div class="k">Calibre</div><div class="v">{prod['caliber']}</div></div>
      <div class="sp"><div class="k">Capacity</div><div class="v">{prod['capacity']}</div></div>
      <div class="sp"><div class="k">Barrel</div><div class="v">{prod['barrel']}</div></div>
      <div class="sp"><div class="k">Weight</div><div class="v">{prod['weight']}</div></div>
      <div class="sp"><div class="k">Action</div><div class="v">{prod['action']}</div></div>
      <div class="sp"><div class="k">Safety</div><div class="v">{prod['safety']}</div></div>
      <div class="sp"><div class="k">Frame</div><div class="v">{prod['frame']}</div></div>
      <div class="sp"><div class="k">Finish</div><div class="v">{prod['finish']}</div></div>
      <div class="sp"><div class="k">Origin</div><div class="v">Kanpur, India</div></div>
      <div class="sp"><div class="k">Standard</div><div class="v">Arms Act 1959</div></div>
      <div class="sp"><div class="k">Warranty</div><div class="v">Lifetime Mfg.</div></div>
      <div class="sp"><div class="k">Status</div><div class="v">In Production</div></div>
    </div>
  </div>
</section>
"""

def features(prod):
    return f"""<section class="features-block">
  <div class="wrap">
    <div class="section-head reveal">
      <div class="section-num"><span>02</span> / What Makes It</div>
      <h2 class="h-display">Three pillars.<br/>One sidearm.</h2>
    </div>
    <div class="feat-grid reveal">
      <div class="feat">
        <div class="feat-ico">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>
        </div>
        <h3>Precision</h3>
        <p>Match-grade barrel, hand-fitted lockup and a trigger break tuned for the licensed marksman. Repeatable shot placement is engineered in &mdash; not adjusted later.</p>
      </div>
      <div class="feat">
        <div class="feat-ico">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12l9-9 9 9-9 9-9-9z"/><path d="M9 12h6M12 9v6"/></svg>
        </div>
        <h3>Build Quality</h3>
        <p>{prod['frame']} construction, {prod['finish'].lower()} finish, every internal surface inspected. Decades of refinement built into a sidearm that outlives its owner.</p>
      </div>
      <div class="feat">
        <div class="feat-ico">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3 6 6 1-4.5 4.5L18 20l-6-3-6 3 1.5-6.5L3 9l6-1 3-6z"/></svg>
        </div>
        <h3>Ergonomics</h3>
        <p>Grip geometry developed with sport shooters and defence professionals. Natural point-of-aim, comfortable for extended range sessions and ready in the field.</p>
      </div>
    </div>
  </div>
</section>
"""

def related(current_slug):
    """Pick 3 other products from the lineup."""
    others = [p for p in PRODUCTS if p["slug"] != current_slug]
    rng = random.Random(current_slug)  # deterministic per page
    picks = rng.sample(others, 3)
    cards = []
    for p in picks:
        tags_html = "".join(
            f'<span class="tag{" red" if i == 0 else ""}">{t}</span>'
            for i, t in enumerate(p["tags"][:3])
        )
        cards.append(f"""<a class="product" href="../{p['slug']}/index.html">
  <div class="product-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 5l7 7-7 7"/></svg></div>
  <div class="product-sku">SKU: {p['sku']}</div>
  <div class="product-name">{p['name']}</div>
  <div class="pad"><img src="../{p['img_right']}" alt="{p['name']}" class="product-photo" loading="lazy"/></div>
  <div class="product-desc">{p['tagline']}</div>
  <div class="product-tags">{tags_html}</div>
</a>""")
    return f"""<section class="related-block">
  <div class="wrap">
    <div class="section-head reveal">
      <div class="section-num"><span>03</span> / Also in the Arsenal</div>
      <h2 class="h-display">Continue exploring.</h2>
    </div>
    <div class="related-grid reveal">
      {"".join(cards)}
    </div>
    <div style="text-align:center;margin-top:2.5rem;">
      <a href="../products.html" class="btn-ghost">View Full Arsenal <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
    </div>
  </div>
</section>
"""

CTA = """<section class="cta">
  <div class="wrap">
    <span class="eyebrow center">04 / Enquire</span>
    <h2 class="h-display">Ready to acquire<br/>your sidearm?</h2>
    <p>Drop your email and our dealer-relations desk will be in touch within one business day. Or call our Kanpur facility directly.</p>
    <form class="cta-form" onsubmit="event.preventDefault();this.querySelector('button').textContent='Received';">
      <input type="email" placeholder="Your email address" required/>
      <button type="submit">Send &rarr;</button>
    </form>
  </div>
</section>
"""

FOOTER = """<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="../index.html" class="brand">
          <div class="brand-mark"><span>C</span></div>
          <div class="brand-text">
            <span class="name">Camstar</span>
            <span class="sub">Defence &middot; EST. 1997</span>
          </div>
        </a>
        <p>India's precision firearms manufacturer &mdash; engineering sidearms for marksmen, sport shooters and licensed professionals since 1997.</p>
      </div>
      <div>
        <h5>Arsenal</h5>
        <ul class="footer-list">
          <li><a href="../star-m45-ace-lite/index.html">Star M45 ACE Lite</a></li>
          <li><a href="../star-tt30/index.html">Star TT 30</a></li>
          <li><a href="../star-m32/index.html">Star M32</a></li>
          <li><a href="../baaz-30/index.html">BAAZ 30</a></li>
          <li><a href="../star-king-1911/index.html">Star King 1911</a></li>
          <li><a href="../products.html">View All &rarr;</a></li>
        </ul>
      </div>
      <div>
        <h5>Company</h5>
        <ul class="footer-list">
          <li><a href="../about.html">About Us</a></li>
          <li><a href="../about.html#heritage">Heritage</a></li>
          <li><a href="../contact.html#dealers">Dealer Network</a></li>
          <li><a href="../contact.html#training">Training Facility</a></li>
          <li><a href="../contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h5>Contact</h5>
        <address>
          <div class="row"><strong>Phone</strong>+91 9793 849 997</div>
          <div class="row"><strong>Email</strong>info@camstardefence.com</div>
          <div class="row"><strong>Address</strong>Camstar Defence Industries<br/>Kanpur, Uttar Pradesh<br/>India &mdash; 208 001</div>
          <div class="row"><strong>Hours</strong>Mon&ndash;Sat &middot; 11:00 &ndash; 19:00 IST</div>
        </address>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2025 Camstar Defence Industries Pvt. Ltd. All rights reserved.</span>
      <div class="socials">
        <a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="5"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg></a>
        <a href="#" aria-label="YouTube"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="5" width="20" height="14" rx="3"/><polygon points="10,9 16,12 10,15" fill="currentColor"/></svg></a>
        <a href="#" aria-label="WhatsApp"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 21l1.5-5.5A9 9 0 1 1 8.5 19.5L3 21z"/><path d="M9 12c.5 1 1.5 2 3 2.5"/></svg></a>
      </div>
    </div>
  </div>
</footer>
"""

SCRIPTS = """<script>
// Mobile nav toggle
const navToggle = document.getElementById('navToggle');
if (navToggle) {
  navToggle.addEventListener('click', () => {
    document.getElementById('mobileMenu').classList.toggle('open');
  });
}

// Scroll reveal
const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); revealObs.unobserve(e.target); } });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));

// Scroll progress bar
const bar = document.createElement('div');
bar.style.cssText = 'position:fixed;top:0;left:0;height:2px;width:0;background:linear-gradient(90deg,#d11e3a,#ff6060);z-index:9999;box-shadow:0 0 8px rgba(209,30,58,0.8);pointer-events:none;transition:width 0.1s linear';
document.body.appendChild(bar);
window.addEventListener('scroll', () => {
  const pct = window.scrollY / (document.body.scrollHeight - window.innerHeight) * 100;
  bar.style.width = pct + '%';
});

// Cursor glow
const cursor = document.createElement('div');
cursor.style.cssText = 'position:fixed;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(209,30,58,0.05) 0%,transparent 70%);pointer-events:none;z-index:0;transform:translate(-50%,-50%);transition:opacity 0.3s';
document.body.appendChild(cursor);
let gx = 0, gy = 0, gcx = 0, gcy = 0;
document.addEventListener('mousemove', e => { gx = e.clientX; gy = e.clientY; });
(function gc() { gcx += (gx-gcx)*0.08; gcy += (gy-gcy)*0.08; cursor.style.left=gcx+'px'; cursor.style.top=gcy+'px'; requestAnimationFrame(gc); })();

// Button hover glow
document.querySelectorAll('.btn-primary, .nav-cta, .cta-form button').forEach(btn => {
  btn.addEventListener('mouseenter', () => btn.style.boxShadow = '0 0 28px rgba(209,30,58,0.45)');
  btn.addEventListener('mouseleave', () => btn.style.boxShadow = '');
});

// Thumb click swap main image
document.querySelectorAll('.gallery-thumbs .thumb').forEach(t => {
  t.addEventListener('click', () => {
    const main = document.querySelector('.gallery-main img');
    const src = t.querySelector('img').src;
    if (main && src) main.src = src;
  });
});
</script>
</body>
</html>
"""

# -------------------------------------------------------------
# 5) Assemble and write
# -------------------------------------------------------------
def build_page(prod):
    return (
        page_head(prod)
        + '<body data-page="product">\n'
        + UTIL_BAR
        + NAV
        + breadcrumb(prod)
        + hero(prod)
        + specs(prod)
        + features(prod)
        + related(prod["slug"])
        + CTA
        + FOOTER
        + SCRIPTS
    )

def main():
    rebuilt = []
    issues = []
    for prod in PRODUCTS:
        folder = BASE / prod["slug"]
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
        index = folder / "index.html"
        # Backup existing
        if index.exists():
            backup = folder / "index-old.html"
            try:
                shutil.copy2(index, backup)
            except Exception as e:
                issues.append(f"{prod['slug']}: backup failed - {e}")
        try:
            html = build_page(prod)
            index.write_text(html, encoding="utf-8")
            rebuilt.append(prod["slug"])
        except Exception as e:
            issues.append(f"{prod['slug']}: write failed - {e}")

    print(f"Rebuilt {len(rebuilt)} product pages:")
    for s in rebuilt:
        print(f"  - {s}/index.html")
    if issues:
        print("\nIssues:")
        for i in issues:
            print(f"  ! {i}")
    else:
        print("\nNo issues.")

if __name__ == "__main__":
    main()
