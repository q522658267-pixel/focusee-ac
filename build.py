# -*- coding: utf-8 -*-
"""FOCUSEE portable air conditioner site generator."""
import json, os, re, html, sys, time
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'products.json'), encoding='utf-8'))

COMPANY   = 'Focusee Company Limited'
ADDRESS   = 'Factory House B, Changmingshui Industrial Park, Changyi Road, Wuguishan, Zhongshan City, Guangdong Province, China 528458'
SITE      = 'https://focuseetech.com/'
OG_IMAGE  = SITE + 'assets/img/og-cover.jpg'
LOGO_IMG  = SITE + 'assets/img/logo.png'
PEOPLE = [
    dict(name='Carol Luo', role='General Manager', email='carol.luo@focuseetech.com', wa='+86 133 7848 2598', wl='8613378482598'),
    dict(name='Robert Luo', role='Marketing Manager', email='Marketing@focuseetech.com', wa='+86 134 2565 1968', wl='8613425651968'),
]
CATS = ['Portable Air Con.', 'Dehumidifier', 'Air Purifier', 'Accessory']
CAT_SLUG = {'Portable Air Con.':'portable-air-conditioners','Dehumidifier':'dehumidifiers',
            'Air Purifier':'air-purifiers','Accessory':'accessories'}
CAT_DESC = {
 'Portable Air Con.':'Ductless, mobile and camping air conditioners from 1,000 to 24,000 BTU with R290 / R32 refrigerant.',
 'Dehumidifier':'Portable dehumidifiers handling 10 to 50 litres per day, with auto-defrost and continuous drain options.',
 'Air Purifier':'HEPA and carbon filtration units with high CADR for dust, odour and fine particle removal.',
 'Accessory':'Window kits, exhaust ducts, adaptors, filters and spare parts to complete the installation.',
}
# Longer SEO intro per category (used on category landing pages & meta description)
CAT_INTRO = {
 'Portable Air Con.':'Focusee portable air conditioners run from a 1,000 BTU camping unit to a 24,000 BTU floor-standing spot cooler. Every model is ductless, wheel-mounted and plug-and-play — no outdoor unit, no installation.',
 'Dehumidifier':'Focusee portable dehumidifiers extract 10 to 50 litres of moisture per day, with auto-defrost, continuous-drain and condensate-pump options for basements, warehouses, labs and comfort cooling.',
 'Air Purifier':'Focusee air purifiers combine true HEPA and activated-carbon filtration with high CADR for dust, odour, smoke and fine-particle removal in homes, offices and light-commercial spaces.',
 'Accessory':'Complete any installation with Focusee window kits, exhaust ducts, adaptors, filters and spare parts, engineered to fit our portable air conditioners and dehumidifiers.',
}
# Category-specific FAQ (real B2B buyer questions -> FAQPage rich result)
CAT_FAQ = {
 'Portable Air Con.':[
   ('Do portable air conditioners need an outdoor unit?',
    'No. Focusee portable air conditioners are self-contained: the compressor, condenser and evaporator sit in one wheel-mounted cabinet. You only route a flexible exhaust duct to a window or vent, then plug it in.'),
   ('Can I use a portable AC in a tent, RV or server room?',
    'Yes. Our 1,000 to 4,000 BTU units suit tents, RVs, cabins and small server rooms, while 12,000 to 24,000 BTU models handle halls, warehouses and industrial spot cooling.'),
   ('Do you customise voltage and plug for my market?',
    'Yes. Voltage (110V / 220V, 50 or 60 Hz), plug type and the user manual are configured to your destination market — Type G for the UK, Type F for the EU, Type I for AU / NZ and Type A/B for North America.'),
 ],
 'Dehumidifier':[
   ('Where should I place a portable dehumidifier?',
    'In the damp space itself — basement, warehouse corner, laundry room or storage area — with a few centimetres of clearance around the intake and exhaust. A continuous-drain hose lets it run unattended.'),
   ('What capacity dehumidifier do I need?',
    'Rough guide: 10 to 20 L/day for a flat or small basement, 20 to 35 L/day for a warehouse or light-commercial area, and 35 to 50 L/day for large or very damp spaces. We will size it with you.'),
   ('Do your dehumidifiers have auto-defrost?',
    'Yes. All models include auto-defrost, and most offer a continuous-drain or condensate-pump option so they keep working in cold basements without manual emptying.'),
 ],
 'Air Purifier':[
   ('What does HEPA filtration actually remove?',
    'True HEPA captures 99.97% of particles down to 0.3 microns — dust, pollen, smoke, pet dander and fine PM2.5 — while the activated-carbon layer absorbs odour and VOCs.'),
   ('How often should I replace the filter?',
    'Most filters last 6 to 12 months depending on air quality and runtime; the unit shows a filter-life indicator so you replace it only when needed.'),
   ('Are Focusee air purifiers quiet enough for bedrooms?',
    'Yes. A dedicated sleep mode drops fan speed and noise to bedroom-friendly levels while keeping air circulation going through the night.'),
 ],
 'Accessory':[
   ('Which window kit fits my portable AC?',
    'Our sliding-window adaptor kit (3 pieces per set) fits the standard exhaust-duct diameter used across the Focusee portable air conditioner range. Tell us your window type and we will match it.'),
   ('Can I get a longer exhaust duct?',
    'Yes. Exhaust ducts are available in 1.5 m, 2 m, 3 m and 4 m lengths, supplied separately or packed with the unit per your configuration.'),
 ],
}

# ------------------------------------------------------------------ helpers
def esc(s): return html.escape(str(s if s is not None else ''))
def esca(s):
    """Escape for use inside a double-quoted HTML attribute (keeps apostrophes literal)."""
    return (str(s if s is not None else '').replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))
def slug(s): return re.sub(r'[^a-z0-9]+','-',(s or '').lower()).strip('-') or 'product'
LOGO = '68ca51498f2ea.png'
# Google Search Console site-verification meta content. Paste the value from
# GSC ("HTML 标记" method) here, then rebuild; empty = no tag emitted.
GSC_VERIFY = ''
# Bing Webmaster Tools site-verification meta content (msvalidate.01).
BING_VERIFY = '3D0F53966638CB224E00DD2A93FE4BFC'
# English <-> French page pairs for hreflang annotations.
I18N = {
 'applications/france-distributor-oem.html': 'applications/fr-climatiseur-portable-oem.html',
 'applications/eu-ce-certification.html': 'applications/fr-certification-ce.html',
}
I18N_REV = {v: k for k, v in I18N.items()}
def gallery(p):
    g=[]
    for im in ([p.get('thumb')] + p.get('thumbs',[])):
        if not im or im == LOGO or im in g: continue
        g.append(im)
    return g[:6]

HEAD_T = '''<!DOCTYPE html>
<html lang="{{LANG}}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{T}}</title>
<meta name="description" content="{{D}}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="Focusee Company Limited">
{{GVERIFY}}
{{BVERIFY}}
<link rel="canonical" href="{{CANON}}">
{{ALTERNATES}}
<meta name="theme-color" content="#0B5CAB">
<meta property="og:type" content="{{OGT}}">
<meta property="og:site_name" content="Focusee Company Limited">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{{T}}">
<meta property="og:description" content="{{D}}">
<meta property="og:url" content="{{CANON}}">
<meta property="og:image" content="{{OGI}}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Focusee Company Limited - portable air conditioners and dehumidifiers">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{T}}">
<meta name="twitter:description" content="{{D}}">
<meta name="twitter:image" content="{{OGI}}">
<link rel="icon" href="{{R}}assets/img/logo.png">
<link rel="apple-touch-icon" href="{{R}}assets/img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{R}}assets/css/style.css">
{{JSONLD}}
</head>
<body>
'''
FOOT_T = '''
<script src="{{R}}assets/js/site.js"></script>
</body>
</html>'''

def topbar():
    return '''<div class="topbar"><div class="wrap">
  <div class="topbar-l">
    <a href="mailto:Marketing@focuseetech.com"><i>&#9993;</i>Marketing@focuseetech.com</a>
    <a href="https://wa.me/8613425651968"><i>&#9990;</i>+86 134 2565 1968</a>
  </div>
  <div class="topbar-l"><span>OEM &amp; ODM Portable Air Comfort &middot; Zhongshan, China</span></div>
</div></div>'''

def header(active='', r=''):
    def cls(k): return ' class="on"' if active == k else ''
    subs = ''.join(f'<a href="{r}{CAT_SLUG[c]}.html">{esc(c)}</a>' for c in CATS)
    return topbar() + f'''<header><div class="wrap">
  <a class="logo" href="{r}index.html">
    <img src="{r}assets/img/logo.png" alt="FOCUSEE">
    <span class="logo-txt"><b>Focusee Company Limited</b><span>Air Comfort Systems</span></span>
  </a>
  <nav class="main" id="navmain">
    <a href="{r}index.html"{cls('home')}>Home</a>
    <div class="has-sub"><a href="{r}products.html"{cls('products')}>Products</a>
      <div class="sub">{subs}<a href="{r}products.html">All Products</a></div></div>
    <a href="{r}about.html"{cls('about')}>About Us</a>
    <a href="{r}contact.html"{cls('contact')}>Contact</a>
  </nav>
  <div class="hd-cta">
    <a class="btn btn-grad btn-sm" href="{r}contact.html">Get a Quote</a>
    <button class="burger" id="burger" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</div></header>'''

def footer(r=''):
    return f'''<footer>
  <div class="wrap">
    <div class="f-grid">
      <div class="f-brand">
        <img src="{r}assets/img/logo.png" alt="FOCUSEE">
        <p>{COMPANY} is a manufacturer and exporter of portable air conditioners, dehumidifiers, air purifiers and accessories, serving importers, distributors and retail brands across Europe, North America, Australia and the Middle East.</p>
        <div class="socials"><a href="mailto:Marketing@focuseetech.com">@</a><a href="https://wa.me/8613425651968">WA</a></div>
      </div>
      <div><h4>Products</h4><ul>
        {''.join(f'<li><a href="{r}{CAT_SLUG[c]}.html">{esc(c)}</a></li>' for c in CATS)}
        <li><a href="{r}products.html">All Products</a></li>
      </ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="{r}about.html">About Us</a></li>
        <li><a href="{r}about.html#green">Sustainability</a></li>
        <li><a href="{r}contact.html">Contact</a></li>
        <li><a href="{r}contact.html">Request Catalogue</a></li>
      </ul></div>
      <div><h4>Resources</h4><ul>
        <li><a href="{r}applications/tent-camping-ac.html">Camping &amp; RV Cooling</a></li>
        <li><a href="{r}applications/server-room-cooling.html">Server Room Cooling</a></li>
        <li><a href="{r}blog/oem-private-label-guide.html">OEM &amp; Private Label</a></li>
        <li><a href="{r}applications/eu-ce-certification.html">EU CE / ErP Compliance</a></li>
        <li><a href="{r}applications/france-distributor-oem.html">France Market OEM</a></li>
        <li><a href="{r}blog/btu-sizing-guide.html">BTU Sizing Guide</a></li>
        <li><a href="{r}blog/dehumidifier-capacity-guide.html">Dehumidifier Capacity</a></li>
        <li><a href="{r}blog/server-room-heat-load.html">Server Room Heat Load</a></li>
        <li><a href="{r}blog/tent-rv-ac-power.html">Tent &amp; RV AC Power</a></li>
        <li><a href="{r}applications/fr-climatiseur-portable-oem.html">Climatiseur portable (FR)</a></li>
        <li><a href="{r}applications/fr-certification-ce.html">Certification CE (FR)</a></li>
      </ul></div>
      <div><h4>Contact</h4><ul>
        <li style="line-height:1.6">{esc(ADDRESS)}</li>
        <li><a href="mailto:carol.luo@focuseetech.com">carol.luo@focuseetech.com</a></li>
        <li><a href="mailto:Marketing@focuseetech.com">Marketing@focuseetech.com</a></li>
        <li><a href="https://wa.me/8613425651968">WhatsApp +86 134 2565 1968</a></li>
      </ul></div>
    </div>
    <div class="f-bot">
      <span>&copy; {COMPANY}. All rights reserved.</span>
      <span>Portable Air Conditioners &middot; Dehumidifiers &middot; Air Purifiers &middot; Accessories</span>
    </div>
  </div>
</footer>'''

def cta(r=''):
    return f'''<section class="cta">
  <div class="wrap">
    <div>
      <span class="eyebrow" style="color:#8FE6C9">Get in touch</span>
      <h2>Talk to our team about your next order</h2>
      <p>Send us your target specification, market and volume &mdash; we will reply with the right model, its certification status and a formal quotation.</p>
      <div class="cta-actions">
        <a class="btn btn-grad" href="mailto:Marketing@focuseetech.com">Email us</a>
        <a class="btn btn-ghost" href="https://wa.me/8613425651968">WhatsApp</a>
      </div>
    </div>
    <div class="contact-cards">
      {''.join(f'<div class="ccard"><span class="role">{esc(p["role"])}</span><b>{esc(p["name"])}</b><a href="mailto:{p["email"]}"><i>&#9993;</i>{p["email"]}</a><a href="https://wa.me/{p["wl"]}"><i>&#9990;</i>WhatsApp: {p["wa"]}</a></div>' for p in PEOPLE)}
    </div>
  </div>
</section>'''

# ------------------------------------------------------------------ image pipeline
WEBP = set()          # basenames of source images that have a .webp sibling
WEBP_MIN = 0          # convert everything: a partial set breaks the gallery switcher
DIMS = {}             # basename -> (width, height) of the ORIGINAL image
DIMS_FILE = ROOT + '/assets/img_dims.json'

def load_dims():
    """Real intrinsic sizes. Without them we must NOT emit width/height at all —
    a guessed size acts as a real CSS presentational hint and inflates the box."""
    if os.path.exists(DIMS_FILE):
        try:
            for k, v in json.load(open(DIMS_FILE, encoding='utf-8')).items():
                DIMS[k] = tuple(v)
        except Exception:
            pass

def save_dims():
    json.dump({k: list(v) for k, v in DIMS.items()},
              open(DIMS_FILE, 'w', encoding='utf-8'), ensure_ascii=False)

def ensure_webp(force=False):
    """Create .webp next to every source image. Runs once per build; skips fresh files."""
    try:
        from PIL import Image
    except ImportError:
        print('webp: Pillow not available, skipping')
        return
    d = ROOT + '/assets/img/'
    made = skipped = 0
    for fn in sorted(os.listdir(d)):
        if not fn.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        p = d + fn
        try:
            if os.path.getsize(p) < WEBP_MIN:
                continue
        except OSError:
            continue
        wp = os.path.splitext(p)[0] + '.webp'
        if (not force) and os.path.exists(wp) and os.path.getmtime(wp) >= os.path.getmtime(p):
            WEBP.add(fn); skipped += 1
            if fn not in DIMS:          # cached webp, but size still unknown -> read header only
                try:
                    with Image.open(p) as im: DIMS[fn] = im.size
                except Exception: pass
            continue
        try:
            im = Image.open(p)
            DIMS[fn] = im.size          # record before any resize
            im = im.convert('RGBA' if im.mode in ('RGBA', 'LA') or 'transparency' in im.info else 'RGB')
            if max(im.size) > 1100:
                im.thumbnail((1100, 1100), Image.LANCZOS)
            im.save(wp, 'WEBP', quality=82, method=6)
            WEBP.add(fn); made += 1
        except Exception as e:
            print('  webp skip', fn, e)
    print(f'webp: {made} new, {skipped} cached, {len(WEBP)} usable')

def dims(src):
    """width/height attribute pair for an image, or '' when the real size is unknown."""
    wh = DIMS.get(src)
    return f' width="{wh[0]}" height="{wh[1]}"' if wh else ''

def pic(src, alt, r='', lazy=True, extra=''):
    """Responsive-safe <picture> with WebP + original fallback."""
    a = esc(alt)
    load = 'lazy' if lazy else 'eager'
    pr = '' if lazy else ' fetchpriority="high"'
    wh = dims(src)
    orig = f'{r}assets/img/{src}'
    if src in WEBP:
        wb = f'{r}assets/img/{os.path.splitext(src)[0]}.webp'
        return (f'<picture><source srcset="{wb}" type="image/webp">'
                f'<img src="{orig}" alt="{a}"{wh} loading="{load}"{pr}{extra}></picture>')
    return f'<img src="{orig}" alt="{a}"{wh} loading="{load}"{pr}{extra}>'

def webp_src(src, r=''):
    """Preferred single src for JS-driven gallery switching."""
    if src in WEBP:
        return f'{r}assets/img/{os.path.splitext(src)[0]}.webp'
    return f'{r}assets/img/{src}'

# ------------------------------------------------------------------ SEO helpers
def ld(obj):
    """Serialize a JSON-LD graph node into a safe <script> block."""
    s = json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
    s = s.replace('</', '<\\/').replace('\u2028', ' ').replace('\u2029', ' ')
    return '<script type="application/ld+json">' + s + '</script>'

ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": SITE + "#organization",
    "name": COMPANY,
    "url": SITE,
    "logo": {"@type": "ImageObject", "url": LOGO_IMG},
    "image": OG_IMAGE,
    "description": "Manufacturer and exporter of portable air conditioners, dehumidifiers, humidifiers and air purifiers. OEM and ODM private label supply for importers, distributors and retail brands.",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Factory House B, Changmingshui Industrial Park, Changyi Road, Wuguishan",
        "addressLocality": "Zhongshan City",
        "addressRegion": "Guangdong",
        "postalCode": "528458",
        "addressCountry": "CN",
    },
    "contactPoint": [
        {"@type": "ContactPoint", "contactType": "sales", "name": "Carol Luo",
         "jobTitle": "General Manager", "email": "carol.luo@focuseetech.com",
         "telephone": "+86-133-7848-2598", "availableLanguage": ["en", "zh"]},
        {"@type": "ContactPoint", "contactType": "sales", "name": "Robert Luo",
         "jobTitle": "Marketing Manager", "email": "Marketing@focuseetech.com",
         "telephone": "+86-134-2565-1968", "availableLanguage": ["en", "zh"]},
    ],
    "areaServed": ["Europe", "United Kingdom", "North America", "Australia", "New Zealand", "Middle East", "South East Asia"],
    "knowsAbout": ["portable air conditioner", "dehumidifier", "air purifier", "R290 refrigerant", "OEM manufacturing"],
}

def org_ld():
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": SITE + "#website",
        "url": SITE,
        "name": COMPANY,
        "publisher": {"@id": SITE + "#organization"},
        "inLanguage": "en",
    }
    return ld(ORG) + '\n' + ld(website)

def breadcrumb_ld(items):
    """items: list of (name, url). Last one may have url=None."""
    els = []
    for i, (n, u) in enumerate(items):
        node = {"@type": "ListItem", "position": i + 1, "name": n}
        if u: node["item"] = u
        els.append(node)
    return ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": els})

def itemlist_ld(name, items):
    els = []
    for i, it in enumerate(items):
        u = it["url"]
        if not u.startswith('http'):  # 已是绝对地址则不再拼 SITE，防止域名重复
            u = SITE + u
        els.append({"@type": "ListItem", "position": i + 1,
                    "name": it["name"], "url": u})
    return ld({"@context": "https://schema.org", "@type": "ItemList",
               "name": name, "numberOfItems": len(els), "itemListElement": els})

def detail_faq_html(cat):
    """Render category-specific buyer FAQ on each product page (drives FAQPage rich result)."""
    faqs = CAT_FAQ.get(cat, [])
    if not faqs:
        return ''
    return ''.join(
        f'<details{" open" if i == 0 else ""}><summary>{esc(q)}</summary>'
        f'<div class="faq-a"><p>{esc(a)}</p></div></details>'
        for i, (q, a) in enumerate(faqs))

def detail_faq_ld(cat):
    faqs = CAT_FAQ.get(cat, [])
    if not faqs:
        return ''
    return ld({"@context": "https://schema.org", "@type": "FAQPage",
               "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}}
                             for q, a in faqs]})

def product_ld(p):
    img = p['g'][0] if p.get('g') else 'logo.png'
    imgs = [SITE + 'assets/img/' + i for i in p['g']] or [LOGO_IMG]
    bl = [re.sub(r'\s+', ' ', b).strip(' ;,') for b in p.get('bullets', [])[:4]]
    desc = (p.get('desc') or '; '.join(bl)
            or f"{p['name']} {CATEGORY_WORD.get(p['cat'], 'unit')} from Focusee Company Limited")
    node = {
        "@context": "https://schema.org",
        "@type": "Product",
        "@id": SITE + 'product-' + p['slug'] + '.html#product',
        "name": p['name'],
        "description": str(desc)[:500],
        "sku": p['name'],
        "mpn": p['name'],
        "category": CATEGORY_WORD.get(p['cat'], 'Portable air conditioner'),
        "brand": {"@type": "Brand", "name": "Focusee"},
        "manufacturer": {"@id": SITE + "#organization"},
        "image": imgs,
        "url": SITE + 'product-' + p['slug'] + '.html',
        # No "offers" node on purpose: prices are quoted per order, never published.
        # Emitting a priceCurrency without a price is worse than emitting none.
    }
    if p.get('bullets'):
        node["additionalProperty"] = [
            {"@type": "PropertyValue", "name": "Key specification",
             "value": re.sub(r'\s+', ' ', b).strip(' ;,')} for b in p['bullets'][:6]]
    return ld(node)

CATEGORY_WORD = {
    'Portable Air Con.': 'Portable air conditioner',
    'Dehumidifier': 'Dehumidifier',
    'Air Purifier': 'Air purifier',
    'Accessory': 'Air conditioner accessory',
}

def page(fname, title, desc, body, active='', r='', canon=None, ogt='website', ogi=None, jsonld='', path=None, lang='en'):
    """path: URL path relative to SITE, e.g. 'products.html'. Used for canonical."""
    if canon is None:
        canon = SITE + (path or fname)
    # hreflang alternates for paired EN/FR pages
    alt = ''
    if fname in I18N or fname in I18N_REV:
        en = SITE + (I18N_REV.get(fname, fname) if fname in I18N_REV else fname)
        fr = SITE + (I18N.get(fname, fname) if fname in I18N else I18N_REV[fname])
        alt = (f'<link rel="alternate" hreflang="en" href="{en}">\n'
               f'<link rel="alternate" hreflang="fr" href="{fr}">\n'
               f'<link rel="alternate" hreflang="x-default" href="{en}">')
    h = (HEAD_T.replace('{{T}}', esca(title))
               .replace('{{D}}', esca(desc))
               .replace('{{R}}', r)
               .replace('{{LANG}}', lang)
               .replace('{{CANON}}', esca(canon))
               .replace('{{OGT}}', ogt)
               .replace('{{OGI}}', esca(ogi or OG_IMAGE))
               .replace('{{GVERIFY}}',
                         ('<meta name="google-site-verification" content="%s">' % esca(GSC_VERIFY))
                         if GSC_VERIFY else '')
               .replace('{{BVERIFY}}',
                         ('<meta name="msvalidate.01" content="%s">' % esca(BING_VERIFY))
                         if BING_VERIFY else '')
               .replace('{{ALTERNATES}}', alt)
               .replace('{{JSONLD}}', jsonld))
    htmlout = h + header(active, r) + body + footer(r) + FOOT_T.replace('{{R}}', r)
    dest = os.path.join(ROOT, fname)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w', encoding='utf-8').write(htmlout)
    return fname

def alt_of(p, i=0):
    """Descriptive alt text — plain words, no keyword stuffing."""
    return f"{p['name']} {CATEGORY_WORD.get(p['cat'], 'portable air comfort unit').lower()}, view {i+1}"

def card(p, n, r='', eager=False):
    g = gallery(p)
    img = g[0] if g else 'logo.png'
    txt = p.get('bullets', [])
    sub = txt[0] if txt else p.get('desc', '')[:70]
    return f'''<a class="card" href="{r}product-{slug(p['name'])}.html" data-cat="{CAT_SLUG.get(p['cat'],'')}">
  <div class="card-img"><span class="card-cat">{esc(p['cat'].replace('Portable Air Con.','Portable AC'))}</span>
    {pic(img, alt_of(p), r, lazy=not eager)}</div>
  <div class="card-body"><h3>{esc(p['name'])}</h3><p>{esc(sub)}</p>
    <span class="card-more">View details</span></div>
</a>'''

# ------------------------------------------------------------------ prepare data
BAD = ('CONTACT US', 'GREEN MASTER', 'mk-jenny', 'Zhongshan Liangchang', 'mail-airmaster')
def clean_tables(ts):
    out = []
    for t in ts:
        rows = [r for r in t if not any(any(b in c for b in BAD) for c in r)]
        rows = [r for r in rows if any(c.strip() for c in r)]
        if rows: out.append(rows)
    return out
for p in DATA:
    p['tables'] = clean_tables(p.get('tables', []))
    p['bullets'] = [b for b in p.get('bullets', []) if not any(x in b for x in BAD)]
DATA.sort(key=lambda x: (CATS.index(x['cat']) if x['cat'] in CATS else 9))
CATS = [c for c in CATS if any(x['cat'] == c for x in DATA)]
for i, p in enumerate(DATA):
    p['slug'] = slug(p['name'])
    p['prev'] = {'name': DATA[i-1]['name'], 'slug': slug(DATA[i-1]['name'])} if i > 0 else None
    p['next'] = {'name': DATA[i+1]['name'], 'slug': slug(DATA[i+1]['name'])} if i < len(DATA)-1 else None
    p['g'] = gallery(p)
json.dump(DATA, open(ROOT + '/assets/products.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('products:', len(DATA), 'cats:', CATS)

# ------------------------------------------------------------------ INDEX
def build_index():
    picks = {'Portable Air Con.':6, 'Dehumidifier':4, 'Air Purifier':2, 'Accessory':1}
    feat = []
    for c in CATS:
        feat += [x for x in DATA if x['cat'] == c][:picks.get(c, 3)]
    feat = feat[:12]
    cat_tiles = ''
    for c in CATS:
        n = len([x for x in DATA if x['cat'] == c])
        cat_tiles += f'''<a class="cat-tile" href="{CAT_SLUG[c]}.html">
  <div class="n">{n:02d}</div><h3>{esc(c)}</h3><p>{esc(CAT_DESC[c])}</p>
  <span class="card-more">Browse range</span></a>'''
    cards = '\n'.join(card(p, i) for i, p in enumerate(feat))
    why = [
      ('Smart Control', 'WiFi app and infrared remote control. Tuya ecosystem, timer 0&ndash;24H, sleep mode and self-diagnosis as standard.', 'M12 2a7 7 0 0 1 7 7c0 3-2 5-4 7l-1 3H10l-1-3c-2-2-4-4-4-7a7 7 0 0 1 7-7zm-2 19h4'),
      ('Eco Refrigerant', 'R290 and R32 low-GWP refrigerant options, RoHS compliant materials throughout the supply chain.', 'M12 3v18M5 8l14 8M19 8L5 16'),
      ('Energy Efficient', 'EU ERP Class A efficiency, Energy Star options for the United States and MEPS-ready models for Australia.', 'M13 2 4 14h6l-1 8 9-12h-6z'),
      ('All-in-One Comfort', 'Cooling, heating, dehumidifying, purifying and ventilating in a single portable unit, with self-evaporating drain-free operation.', 'M12 3a9 9 0 1 0 9 9M12 3v9h9'),
      ('True Mobile Design', 'Ductless and wheel-mounted. No installation, no outdoor unit &mdash; plug in and move it from room to room.', 'M5 12h14M13 6l6 6-6 6'),
      ('OEM &amp; ODM', 'Private label, custom housing colour, control panel, packaging and voltage / plug configuration for your market.', 'M4 7h16v13H4zM9 7V4h6v3'),
      ('Certified for Your Market', 'GS / CE, ETL, RoHS, REACH and MEPS documentation available. Test reports released with every order.', 'M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z'),
      ('Container Loading Support', 'Full documentation on MOQ, carton dimensions and 20&prime; / 40&prime;GP / 40&prime;HQ loading quantities for every model.', 'M3 7l9-4 9 4-9 4-9-4zm0 0v10l9 4 9-4V7'),
    ]
    why_html = ''.join(f'''<div class="why-card"><div class="why-ico"><svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></svg></div><h3>{t}</h3><p>{x}</p></div>''' for t, x, d in why)

    body = f'''<section class="hero"><div class="wrap">
  <div>
    <span class="hero-tag">Portable Air Comfort Specialist</span>
    <h1>Cooling comfort that <em>moves with you</em></h1>
    <p class="lead">Focusee Company Limited designs and manufactures portable air conditioners, dehumidifiers, air purifiers and accessories for importers, distributors and retail brands worldwide. Ductless by design, eco-refrigerant ready, certified for your market.</p>
    <div class="hero-actions">
      <a class="btn btn-grad" href="products.html">Explore products</a>
      <a class="btn btn-ghost" href="contact.html">Request a quote</a>
    </div>
    <div class="hero-stats">
      <div><b>{len(DATA)}+</b><span>Models available</span></div>
      <div><b>{len(CATS)}</b><span>Product categories</span></div>
      <div><b>1k&ndash;24k</b><span>BTU range</span></div>
      <div><b>OEM</b><span>&amp; private label</span></div>
    </div>
  </div>
  <div class="hero-visual">
    {pic(DATA[3]['g'][0] if len(DATA) > 3 and DATA[3]['g'] else 'logo.png',
         'Focusee portable air conditioner with WiFi app control', lazy=False)}
    <div class="hero-badge"><i>WiFi</i><div><b>Smart app control</b><span>Tuya eco-system &middot; 0&ndash;24H timer</span></div></div>
  </div>
</div></section>

<div class="strip"><div class="wrap">
  <div><em></em>CE / GS &mdash; EU &amp; UK</div>
  <div><em></em>Energy Star options &mdash; US</div>
  <div><em></em>MEPS ready &mdash; AU / NZ</div>
  <div><em></em>R290 &amp; R32 refrigerant</div>
  <div><em></em>RoHS compliant materials</div>
</div></div>

<section>
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Product range</span>
      <h2>{len(CATS)} product families, one supply chain</h2>
      <p>From a 1,000 BTU camping unit to a 24,000 BTU floor-standing air conditioner &mdash; a complete portable air comfort programme from a single factory.</p>
    </div>
    <div class="cats">{cat_tiles}</div>
  </div>
</section>

<section class="alt" id="featured">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow g">Featured models</span>
      <h2>Popular portable air conditioners</h2>
      <p>Every model below is available for OEM / private label with your own brand, packaging and voltage configuration.</p>
    </div>
    <div class="filters" id="filters">
      <button class="on" data-f="all">All</button>
      {''.join(f'<button data-f="{CAT_SLUG[c]}">{esc(c)}</button>' for c in CATS)}
    </div>
    <div class="grid" id="grid">{cards}</div>
    <div style="text-align:center;margin-top:44px"><a class="btn btn-line" href="products.html">View all {len(DATA)} products</a></div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Why Focusee</span>
      <h2>Built for importers and retail brands</h2>
      <p>Engineering, certification support and export documentation &mdash; handled by one team that speaks your market's language.</p>
    </div>
    <div class="why">{why_html}</div>
  </div>
</section>

<section class="alt" id="green">
  <div class="wrap split">
    <div class="split-text">
      <span class="eyebrow g">About Focusee</span>
      <h2>Experienced pioneers in portable home appliances</h2>
      <p>Focusee specialises in portable air conditioners, dehumidifiers, humidifiers and air purifiers. Our engineering team comes from the home appliance industry, and we build around one idea: follow the user&rsquo;s lifestyle and remove the complexity of daily operation.</p>
      <p>One unit, many needs &mdash; cooling, heating, dehumidifying and purifying &mdash; instead of five machines competing for the same corner of the room.</p>
      <ul class="ticks">
        <li>Self-detection and conditioning of temperature, humidity and timing</li>
        <li>Low-GWP refrigerant and RoHS certified materials</li>
        <li>HEPA filtration with high CADR and efficient air changes per hour</li>
        <li>EU Class A, Energy Star and Grade 1 efficiency achievements</li>
      </ul>
      <div style="margin-top:30px"><a class="btn btn-line" href="about.html">More about us</a></div>
    </div>
    <div class="split-visual">
      <div class="frame">{pic(DATA[2]['g'][0], 'Focusee portable air conditioner with R290 refrigerant')}</div>
      <div class="float-card a"><b>R290 / R32</b><span>Low-GWP refrigerant</span></div>
      <div class="float-card b"><b>0&ndash;24H</b><span>Timer &amp; sleep mode</span></div>
    </div>
  </div>
</section>

<div class="band"><div class="wrap">
  <div><b>{len(DATA)}+</b><span>Models in the catalogue</span></div>
  <div><b>{len(CATS)}</b><span>Product categories</span></div>
  <div><b>OEM</b><span>Private label &amp; ODM</span></div>
  <div><b>FOB</b><span>Zhongshan / Shenzhen</span></div>
</div></div>

{cta()}
'''
    # ---- FAQ (content + FAQPage rich result)
    faqs = [
        ('What is the minimum order quantity?',
         'MOQ is quoted per model and is normally one 40&#8242;HQ container, mixed models accepted. The exact piece count is printed on every product page together with carton dimensions and 20&#8242; / 40&#8242;GP / 40&#8242;HQ loading quantities.'),
        ('Do you supply OEM and private label?',
         'Yes. We build to your brand: housing colour, control panel layout, logo placement, packaging artwork, manual language, plus voltage and plug configuration for your destination market.'),
        ('Which certifications can you provide?',
         'GS / CE for the EU and UK, ETL for North America, RoHS and REACH material documentation, and MEPS-ready models for Australia and New Zealand. Test reports are released with the order.'),
        ('Which refrigerant do you use?',
         'R290 and R32 low-GWP refrigerant, selected per model and per market regulation. Full refrigerant documentation is available for import clearance.'),
        ('What is the lead time?',
         'Typically 30 to 45 days after deposit and artwork approval, depending on model and season. Repeat orders of existing models are usually faster.'),
        ('Can you ship mixed containers?',
         'Yes. Portable air conditioners, dehumidifiers, air purifiers and accessories can be combined in one container, and we will work out the loading plan for you.'),
        ('What is your warranty and after-sales policy?',
         'We provide a standard 12-month limited warranty on portable air conditioners and dehumidifiers, with spare-parts support and technical documentation. Extended warranty and local service arrangements can be discussed for volume OEM programmes.'),
        ('What are your payment terms?',
         'Typical terms are T/T with a 30% deposit and 70% against a copy of the bill of lading, or an irrevocable L/C at sight for established buyers. Exact terms are confirmed per order.'),
        ('Can I order a sample or prototype before a container?',
         'Yes. We can ship a sample unit or a small trial batch so you can verify build quality, performance and packaging before committing to a full container. Sample cost is credited against your first container order.'),
        ('Do you customise voltage and plug for my market?',
         'Yes. Voltage (110V / 220V, 50 or 60 Hz), plug type and the full user manual are configured for your destination market — Type G for the UK, Type F for the EU, Type I for AU / NZ and Type A/B for North America.'),
    ]
    faq_html = ''.join(
        f'<details{" open" if i == 0 else ""}><summary>{q}</summary><div class="faq-a"><p>{a}</p></div></details>'
        for i, (q, a) in enumerate(faqs))
    res_tiles = ''.join(
        f'''<a class="cat-tile" href="{s['path']}">
  <div class="n">{i+1:02d}</div><h3>{esc(t)}</h3><p>{esc(d)}</p>
  <span class="card-more">Read more</span></a>'''
        for i, (t, d, s) in enumerate([
            ('Camping, tent & RV cooling',
             'How to size 1,800-9,000 BTU units for tents, caravans and motorhomes, and how to power them on site.',
             APP_PAGES[0]),
            ('Server room & cabinet cooling',
             'Working out the heat load from equipment watts, and directing cold air where it is needed.',
             APP_PAGES[1]),
            ('OEM & private label guide',
             'ODM versus OEM, what can be customised, certification by market, tooling, MOQ and lead times.',
             APP_PAGES[2]),
        ]))
    body += f'''
<section id="resources">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Guides &amp; applications</span>
      <h2>Sizing, certification and private-label guides</h2>
      <p>Technical background for the questions that come up before an order &mdash; written for importers and retail buyers rather than end users.</p>
    </div>
    <div class="cats">{res_tiles}</div>
  </div>
</section>
'''
    body += f'''
<section class="alt" id="faq">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow g">Buyer questions</span>
      <h2>Frequently asked questions</h2>
      <p>The six things importers ask us first &mdash; answered plainly.</p>
    </div>
    <div class="faq">{faq_html}</div>
  </div>
</section>
'''
    faq_ld = ld({"@context": "https://schema.org", "@type": "FAQPage",
                 "mainEntity": [{"@type": "Question", "name": re.sub(r'<[^>]+>', '', q),
                                 "acceptedAnswer": {"@type": "Answer",
                                                    "text": re.sub(r'<[^>]+>', '', a).replace('&#8242;', "'")}}
                                for q, a in faqs]})
    return page('index.html',
                'Focusee Company Limited | Portable Air Conditioner & Dehumidifier Manufacturer',
                'Focusee Company Limited manufactures portable air conditioners, dehumidifiers, air purifiers and accessories for importers and retail brands. OEM & ODM, R290 / R32, CE / GS certified, MOQ and container loading published.',
                body, 'home', canon=SITE,
                jsonld=org_ld() + '\n' + faq_ld)

# ------------------------------------------------------------------ PRODUCTS
def build_products():
    groups = ''
    for c in CATS:
        items = [p for p in DATA if p['cat'] == c]
        if not items: continue
        groups += f'''<div class="pgroup" data-cat="{CAT_SLUG[c]}" id="{CAT_SLUG[c]}" style="margin-top:56px">
  <div class="sec-head left" style="margin-bottom:26px"><span class="eyebrow g">{len(items)} models</span><h2 style="font-size:27px">{esc(c)}</h2>
  <p style="margin-top:10px">{esc(CAT_DESC[c])}</p></div>
  <div class="grid">{''.join(card(p, i) for i, p in enumerate(items))}</div>
</div>'''
    body = f'''<section class="phead"><div class="wrap">
  <h1>Products</h1>
  <div class="crumb"><a href="index.html">Home</a><span class="sep">/</span><span>Products</span></div>
</div></section>

<section style="padding-top:56px">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Full catalogue</span>
      <h2>{len(DATA)} portable air comfort models</h2>
      <p>Portable air conditioners, dehumidifiers, air purifiers and accessories &mdash; all available for OEM / private label. Specifications, MOQ and container loading data are published on every product page.</p>
    </div>
    <div class="filters" id="filters">
      <button class="on" data-f="all">All categories</button>
      {''.join(f'<button data-f="{CAT_SLUG[c]}">{esc(c)}</button>' for c in CATS)}
    </div>
    <div id="groups">{groups}</div>
  </div>
</section>

{cta()}
'''
    items = [{'name': p['name'], 'url': 'product-' + p['slug'] + '.html'} for p in DATA]
    return page('products.html', f'Products | {len(DATA)} Portable Air Conditioners & Dehumidifiers — Focusee',
                f'Browse {len(DATA)} portable air conditioners, dehumidifiers, air purifiers and accessories from Focusee Company Limited. Specifications, MOQ and container loading data included.',
                body, 'products',
                jsonld=breadcrumb_ld([('Home', SITE), ('Products', None)]) + '\n'
                       + itemlist_ld('Focusee portable air comfort catalogue', items))

# ------------------------------------------------------------------ CATEGORY
def build_category(c):
    items = [p for p in DATA if p['cat'] == c]
    if not items:
        return None
    n = len(items)
    slug_c = CAT_SLUG[c]
    fname = slug_c + '.html'
    intro = CAT_INTRO.get(c, CAT_DESC[c])
    cat_title = {'Portable Air Con.': 'Portable Air Conditioners', 'Dehumidifier': 'Dehumidifiers',
                 'Air Purifier': 'Air Purifiers', 'Accessory': 'Accessories'}.get(c, c)
    cards = '\n'.join(card(p, i) for i, p in enumerate(items))
    faqs = CAT_FAQ.get(c, [])
    faq_html = ''.join(
        f'<details{" open" if i == 0 else ""}><summary>{q}</summary>'
        f'<div class="faq-a"><p>{a}</p></div></details>'
        for i, (q, a) in enumerate(faqs))
    desc_full = intro + (' Browse %d %s models with published specifications, MOQ and container loading data. OEM / ODM, certified for your market.'
                         % (n, c.lower()))
    desc = desc_full if len(desc_full) <= 158 else desc_full[:155].rstrip() + '…'
    body = f'''<section class="phead"><div class="wrap">
  <h1>{esc(cat_title)}</h1>
  <div class="crumb"><a href="index.html">Home</a><span class="sep">/</span><a href="products.html">Products</a><span class="sep">/</span><span>{esc(c)}</span></div>
</div></section>

<section style="padding-top:40px"><div class="wrap">
  <div class="sec-head">
    <span class="eyebrow">{n} models</span>
    <h2>{esc(c)} for importers and retail brands</h2>
    <p>{esc(intro)}</p>
  </div>
  <div class="grid">{cards}</div>
  <div style="text-align:center;margin-top:34px"><a class="btn btn-line" href="products.html">View the full catalogue</a></div>
</div></section>

<section class="alt" id="faq"><div class="wrap">
  <div class="sec-head">
    <span class="eyebrow g">Buyer questions</span>
    <h2>{esc(cat_title)} — frequently asked questions</h2>
  </div>
  <div class="faq">{faq_html}</div>
</div></section>
'''
    faq_ld = ld({"@context": "https://schema.org", "@type": "FAQPage",
                 "mainEntity": [{"@type": "Question", "name": re.sub(r'<[^>]+>', '', q),
                                "acceptedAnswer": {"@type": "Answer",
                                                   "text": re.sub(r'<[^>]+>', '', a)}}
                               for q, a in faqs]}) if faqs else ''
    items_ld = [{'name': p['name'], 'url': SITE + 'product-' + p['slug'] + '.html'} for p in items]
    jsonld = (breadcrumb_ld([('Home', SITE), ('Products', SITE + 'products.html'), (c, None)])
              + '\n' + itemlist_ld(f'Focusee {c} catalogue', items_ld))
    if faq_ld:
        jsonld += '\n' + faq_ld
    return page(fname,
                f'{cat_title} | Focusee Company Limited — OEM & Private Label',
                desc, body, 'products', ogt='product', ogi=OG_IMAGE, jsonld=jsonld)

# --------------------------------------------------- APPLICATION / GUIDE PAGES
def prod_by_name(n):
    for p in DATA:
        if p['name'] == n:
            return p
    return None

def render_blocks(blocks):
    """Render a list of content blocks: p / note / ul / table."""
    out = []
    for b in blocks:
        k = b[0]
        if k == 'p':
            out.append(f'<p>{esc(b[1])}</p>')
        elif k == 'note':
            out.append(f'<div class="note">{esc(b[1])}</div>')
        elif k == 'ul':
            out.append('<ul>' + ''.join(f'<li>{esc(x)}</li>' for x in b[1]) + '</ul>')
        elif k == 'table':
            head = ''.join(f'<th>{esc(x)}</th>' for x in b[1])
            rows = ''.join('<tr>' + ''.join(f'<td>{esc(c)}</td>' for c in row) + '</tr>'
                           for row in b[2])
            out.append(f'<div class="tbl"><table><thead><tr>{head}</tr></thead>'
                       f'<tbody>{rows}</tbody></table></div>')
    return '\n'.join(out)

APP_PAGES = [
 dict(
  fname='applications/tent-camping-ac.html',
  path='applications/tent-camping-ac.html',
  title='Camping, Tent & RV Air Conditioning | Focusee Ductless Portable AC',
  desc='Ductless portable air conditioners from 1,800 to 9,000 BTU for tents, caravans, RVs and cabins - no outdoor unit, 230 V campsite or off-grid options, OEM available.',
  h1='Cooling for tents, caravans and RVs',
  eyebrow='Application',
  lede='A ductless portable air conditioner cools a tent, caravan or motorhome without an outdoor condenser - one exhaust duct out of a window or vent sleeve, running from a campsite hook-up or a small generator.',
  blocks=[
   ('h2', 'Why ductless cooling suits camping and RV use'),
   ('p', 'Campgrounds, caravan parks and RV sites rarely allow an outdoor condenser, and a split system needs refrigerant pipework that cannot be installed on a temporary pitch. A portable unit needs no outdoor equipment: the compressor sits inside the casing and only the exhaust duct has to leave the space.'),
   ('ul', [
     'No outdoor unit and no refrigerant work - nothing to mount on the pitch or the vehicle',
     'One exhaust duct out of a window, roof vent or purpose-made tent sleeve',
     'Wheel-mounted and typically 20-35 kg, so it moves between tent, caravan and awning',
     'Runs from a standard 230-240 V campsite hook-up',
   ]),
   ('note', 'Portable units in this class must be vented. Sealed no-duct spot coolers exist, but they need a far larger power supply and are rarely available below 12,000 BTU.'),
   ('h2', 'Sizing: how many BTU for a tent, caravan or RV?'),
   ('p', 'Capacity has to cover the heat coming through the walls and roof plus the heat the occupants generate. Canvas and thin fibreglass hold far less heat out than an insulated caravan, so two similar-sized spaces can need very different units.'),
   ('table', ['Space', 'Typical capacity', 'Notes'], [
     ['2-4 person tent', '1,000 - 2,000 BTU', 'Night-time use, vented through a window flap or tent sleeve'],
     ['Large tent / glamping unit', '2,000 - 4,000 BTU', 'Higher load when the sun hits the canvas directly'],
     ['Caravan or small camper', '4,000 - 7,000 BTU', 'Insulated walls; allow more if the roof is unshaded'],
     ['Large caravan / motorhome', '7,000 - 12,000 BTU', 'Check the site hook-up amperage before choosing'],
   ]),
   ('p', 'As a rule of thumb, add capacity for direct sun, for more than two occupants, and for a space used as a daytime living area rather than for sleep only.'),
   ('h2', 'Power: campsite hook-ups, generators and 12 V'),
   ('ul', [
     'EU and UK campsite hook-ups are normally 230-240 V at 6 A or 16 A - confirm the site amperage before selecting a model',
     'Compact units draw roughly 400-700 W; mid-size camping units 700-1,200 W',
     'Off-grid users pair a compact DC unit with a 12 V / 24 V battery bank and inverter, or run an AC unit from a small generator',
     'Voltage, plug type and frequency are configured at assembly for the destination market',
   ]),
   ('h2', 'Exhaust, condensate and noise'),
   ('p', 'The exhaust duct carries the heat out of the space, so the shorter and straighter the run, the better the performance. A window kit is normally included; for tents and caravans a sleeve or vent panel keeps the duct in place.'),
   ('p', 'Most camping-range units are self-evaporating, so water from the evaporator is reused to cool the condenser. Larger units collect condensate in a tank or can run on a continuous drain hose - useful for a longer stay.'),
   ('p', 'Night-time noise matters more in a tent or a caravan than in a room, so quiet-mode fans and low-vibration mounts are the two specification points buyers ask about most in this segment.'),
   ('h2', 'What buyers in this segment usually specify'),
   ('ul', [
     'Carry handles and a moulded case for transport',
     'Remote control and a sleep or quiet mode',
     'Auto-restart after a power interruption',
     'Colour and retail carton to match the brand',
     'CE / UKCA marking for EU and UK sales',
   ]),
  ],
  faqs=[
   ('Can a portable air conditioner really cool a tent?',
    'Yes, provided the exhaust duct is routed outside through a window flap or a tent vent sleeve. Without venting, the heat the unit removes is pushed straight back into the tent. A 1,000-2,000 BTU unit is enough for a two to four person tent at night.'),
   ('Will a camping air conditioner run from a battery?',
    'Compact DC models can run from a 12 V or 24 V battery bank through a suitable inverter. AC units generally need a campsite hook-up or a small generator, because start-up current is several times the running current.'),
   ('How many BTU do I need for a caravan?',
    'A well-insulated caravan usually needs 4,000-7,000 BTU and a larger motorhome 7,000-12,000 BTU. Add capacity for an unshaded roof and for daytime use.'),
   ('Does the unit have to sit outside?',
    'No. The unit stays inside the space and only the exhaust duct goes outside. Keep the duct run as short as is practical.'),
   ('Can we order these units under our own brand?',
    'Yes. Both the compact camping units and the caravan-range models are available for private label, with your carton, rating label and manual.'),
  ],
  models=['PCX5R-18MA', 'PC-LMA', 'PC20S-22MA'],
  models_head='Compact models suited to tents, caravans and RVs',
 ),
 dict(
  fname='applications/server-room-cooling.html',
  path='applications/server-room-cooling.html',
  title='Server Room & Electrical Cabinet Cooling | Focusee Spot Coolers',
  desc='Portable spot coolers from 11,000 to 30,000 BTU for server rooms, comms cabinets and switchgear rooms - no outdoor unit, condensate pump option, OEM available.',
  h1='Cooling for server rooms, comms cabinets and switchgear',
  eyebrow='Application',
  lede='Where a split system cannot be installed - rented premises, temporary sites, or a cabinet added after the room was built - a portable spot cooler is the fastest way to remove heat from IT and electrical equipment.',
  blocks=[
   ('h2', 'Why spot cooling instead of a split system'),
   ('ul', [
     'No outdoor condenser, so no landlord approval, façade penetration or planning delay',
     'No refrigerant pipework to install or commission',
     'Moveable - one unit can cover a cabinet today and a rack room next month',
     'Provides standby capacity for equipment that cannot be taken offline',
     'Installed and running the same day',
   ]),
   ('h2', 'Sizing the heat load'),
   ('p', 'Electrical equipment converts almost all of its input power into heat, so the load is calculated directly from the power draw:'),
   ('note', 'BTU/h = equipment watts x 3.412'),
   ('p', 'Add a margin of 20-30 % for solar gain through windows, lighting, people and duct losses, then round up to the nearest available capacity.'),
   ('table', ['Installation', 'Typical IT / electrical load', 'Suggested capacity'], [
     ['Wall-mounted comms cabinet', '0.5 - 1.5 kW', '4,000 - 7,000 BTU'],
     ['Small rack (1-3 racks)', '2 - 4 kW', '12,000 - 18,000 BTU'],
     ['Server room / switchgear room', '5 - 8 kW', '24,000 - 30,000 BTU'],
   ]),
   ('note', 'Example: a 3 kW rack generates 3 x 3.412 = about 10,240 BTU/h. With a 25 % margin that is roughly 12,800 BTU/h, so a 14,000 BTU unit is the smallest sensible choice.'),
   ('h2', 'Directing cold air where it matters'),
   ('p', 'A spot cooler is only as good as the air path. Point the supply louvre at the intake of the equipment, or use a cold-air duct kit to deliver air to the front of a rack. Avoid blowing cold air at the ceiling or into a corner, where it will short-cycle back into the unit.'),
   ('ul', [
     'Deliver air to the equipment intake, not to the room in general',
     'Keep return air away from the cold supply to avoid short-cycling',
     'Blank unused rack space so cold air is not lost straight through',
     'Keep the exhaust duct run short and prefer a window kit to an open doorway',
   ]),
   ('h2', 'Condensate and continuous operation'),
   ('p', 'Dehumidification produces water continuously. For a cabinet or a short-term job the internal tank is usually enough. For round-the-clock duty, specify a condensate pump or a gravity drain hose so the unit does not stop on a full tank.'),
   ('p', 'Units used in this way run for long periods, so washable or replaceable filters and a serviceable coil matter more than in domestic use.'),
   ('h2', 'Standby and maintenance'),
   ('p', 'Many operators buy a spot cooler purely as standby capacity: it sits unused until the primary air conditioning fails, then holds the room within limits while a repair is arranged. For that duty look for auto-restart after power failure, a permanent drain connection and controls that any member of staff can operate.'),
  ],
  faqs=[
   ('Can a portable air conditioner keep a server room cool?',
    'For small and mid-size loads, yes. A portable spot cooler handles a comms cabinet or a small rack room well. Once the load goes beyond roughly 8-10 kW a dedicated precision cooling system is the right answer, and the portable unit becomes the standby.'),
   ('How do I work out the BTU for a server room?',
    'Multiply the equipment wattage by 3.412 to get BTU/h, then add a 20-30 % margin. A 3 kW rack therefore needs roughly 12,000-14,000 BTU of cooling.'),
   ('Does the unit need a drain?',
    'The internal tank is fine for short jobs. For continuous operation choose the condensate pump or gravity-drain option so the unit does not shut down when the tank fills.'),
   ('Can it run continuously?',
    'Yes. The models used for this application are built for long-duty operation, though the filters should be cleaned at the interval given in the manual and the coil serviced periodically.'),
   ('Can the cold air be ducted into a rack?',
    'Yes. A cold-air duct kit lets you deliver air from the supply louvre directly to the front of the rack, which is far more effective than cooling the whole room.'),
  ],
  models=['PCI35R-25MAS', 'PC-MMA', 'PC90R-MMA'],
  models_head='Higher-capacity models for room and equipment loads',
 ),
 dict(
  fname='blog/oem-private-label-guide.html',
  path='blog/oem-private-label-guide.html',
  title='OEM & Private Label Air Conditioners: A Buyer\u2019s Guide | Focusee',
  desc='How to launch a private-label portable air conditioner, dehumidifier or air purifier: ODM vs OEM, customisation, certification by market, MOQ, tooling and lead times.',
  h1='OEM and private label: a practical buyer\u2019s guide',
  eyebrow='Guide',
  lede='Taking a portable air conditioner or dehumidifier to market under your own brand is a project with a fixed sequence of steps. This guide sets out what each step involves, what drives cost, and where first-time importers most often lose time.',
  blocks=[
   ('h2', 'ODM, OEM and private label - what the words actually mean'),
   ('table', ['Route', 'What changes', 'Tooling', 'Typical minimum'], [
     ['Private label (ODM)', 'Your brand on an existing model: logo, carton, rating label, manual', 'None', 'Lowest - can share a mixed container'],
     ['Customised ODM', 'Existing platform with a modified colour, control panel or fascia', 'Light tooling', 'Mid - set by model and by change'],
     ['Full OEM', 'Your own industrial design, moulds, PCB and specification', 'Full tooling', 'Highest - set by tooling and line setup'],
   ]),
   ('p', 'Most first programmes start as private label on a proven platform, because the certification and the reliability are already established and the only changes are cosmetic and documentary.'),
   ('h2', 'The seven steps of a private-label programme'),
   ('ul', [
     'Brief - target market, capacity range, price point, channels and volumes',
     'Model selection - an existing platform that matches the brief, or a proposal from us',
     'Sample and sign-off - a working sample is approved before any artwork or tooling starts',
     'Artwork - retail carton, rating label, user manual and remote-control overlay',
     'Certification - testing and documentation for the destination market',
     'Pilot order - production, pre-shipment inspection and shipping documents',
     'Repeat orders - loading plan across models, plus any seasonal forecast you can give us',
   ]),
   ('h2', 'What can be customised, and what it costs in time'),
   ('table', ['Item', 'Customisable?', 'Effect on lead time'], [
     ['Logo on the unit', 'Yes - printing or nameplate', 'None to minor'],
     ['Retail carton', 'Yes - full artwork', 'Adds 5-10 days before print approval'],
     ['Rating label and manual', 'Yes - and required in many markets', 'Included in the artwork stage'],
     ['Voltage, plug and frequency', 'Yes - set at assembly', 'None'],
     ['Colour or fascia change', 'Yes - on selected platforms', 'Light tooling, adds several weeks'],
     ['New industrial design', 'Yes - full OEM', 'Tooling typically 25-45 days'],
   ]),
   ('h2', 'Certification by destination market'),
   ('p', 'Market access is the step that most often delays a launch, because testing can only start once the final specification and artwork are frozen. Plan it early and treat it as a critical-path item.'),
   ('table', ['Market', 'Typically required'], [
     ['European Union', 'CE marking, EMC and safety testing, energy label and refrigerant documentation'],
     ['United Kingdom', 'UKCA marking alongside the equivalent safety and EMC testing'],
     ['Australia / New Zealand', 'Electrical safety and EMC, plus MEPS registration for the model'],
     ['GCC', 'G-Mark and destination-specific conformity documentation'],
     ['North America', 'Safety listing for the model and market-specific electrical configuration'],
   ]),
   ('note', 'Testing is arranged with accredited laboratories against the final bill of materials and artwork. Because requirements change, confirm the current list for your market before tooling is committed.'),
   ('h2', 'Minimum order, lead time and payment'),
   ('ul', [
     'The minimum is set per model and per change - a private-label run on an existing platform is far lower than a full-OEM programme',
     'Production normally starts after sample approval, artwork sign-off and deposit',
     'Typical production lead time after approval is 30-45 days, plus transit',
     'Mixed containers are possible - air conditioners, dehumidifiers and purifiers can be combined with a loading plan',
     'Payment is usually by T/T with a deposit and balance against documents; L/C terms can be discussed for larger orders',
   ]),
   ('h2', 'Inspection and quality control'),
   ('p', 'A pre-shipment inspection on a defined sampling plan is standard for a first order, and third-party inspection is welcome. Ask for the test reports for the batch, not only for the sample, and keep a signed golden sample with both parties.'),
   ('ul', [
     'Pre-shipment inspection on an agreed AQL sampling plan',
     'Batch test reports for cooling performance, electrical safety and leak checks',
     'A sealed golden sample retained by both sides',
     'Carton drop and transit testing for the retail pack',
   ]),
   ('h2', 'Five mistakes that cost first-time importers time'),
   ('ul', [
     'Starting certification after tooling - the specification has to be final first',
     'Sizing for the wrong climate - a unit chosen for a mild market is undersized in a hot one',
     'Forgetting the energy label and refrigerant paperwork for the EU',
     'Approving tooling before the working sample is signed off',
     'Leaving too little time between production and the retail season',
   ]),
  ],
  faqs=[
   ('What is the minimum order for a private-label air conditioner?',
    'It depends on the route. A private-label run on an existing platform has the lowest minimum and can be combined with other models in a mixed container. A full-OEM programme with new tooling carries a much higher minimum because of the tooling and line setup.'),
   ('Can you certify the unit for my market?',
    'Certification is arranged per project: testing is carried out by accredited laboratories against your final specification and artwork for the destination market. We will confirm exactly which tests and documents your market requires before the programme starts.'),
   ('How long does tooling take?',
    'Light changes such as a colour or fascia modification take several weeks. A completely new industrial design typically needs 25-45 days for tooling before trial production.'),
   ('Who owns the tooling?',
    'Tooling paid for by the buyer is owned by the buyer. Ownership, storage and transfer terms are set out in the supply agreement.'),
   ('Can I mix models in one container?',
    'Yes. Air conditioners, dehumidifiers and air purifiers can be combined in a single container, and we will work out the loading plan so the space is used properly.'),
   ('Do you supply the retail packaging?',
    'Yes. We produce the carton, rating label, manual and remote overlay to your artwork, and you approve proofs before printing.'),
  ],
  models=[],
  models_head='',
 ),
 # ---- EU / France market (targets Fnac Darty, Boulanger, Leroy Merlin, Electro Dépôt, Cdiscount) ----
 dict(
  fname='applications/eu-ce-certification.html',
  path='applications/eu-ce-certification.html',
  title='CE, ERP & F-Gas Compliance for EU Portable AC Importers | Focusee',
  desc='What EU importers need to place portable air conditioners, dehumidifiers and air purifiers on the market: CE marking, ErP energy label, F-Gas refrigerant rules, technical file and documentation, supplied by Focusee.',
  h1='Placing portable air conditioners on the EU market',
  eyebrow='EU compliance',
  lede='Selling a portable air conditioner, dehumidifier or air purifier in the European Union means meeting CE marking, the ErP energy-labelling rules and the F-Gas refrigerant requirements. This page sets out what the documentation covers and how we support EU importers and private-label brands through conformity.',
  blocks=[
   ('h2', 'CE marking: the baseline for the EU market'),
   ('p', 'Every unit placed on the EU market must carry a valid CE mark backed by a technical file: the EU Declaration of Conformity, the applicable harmonised standards for electrical safety and electromagnetic compatibility, and the test reports behind them. The mark is the importer\u2019s statement that the product meets the relevant EU legislation.'),
   ('ul', [
     'Low Voltage Directive (LVD) \u2013 electrical safety',
     'EMC Directive \u2013 electromagnetic compatibility',
     'RoHS \u2013 restriction of hazardous substances',
     'REACH \u2013 chemical substance documentation',
     'Ecodesign and energy-labelling requirements',
   ]),
   ('h2', 'ErP energy labelling'),
   ('p', 'Portable air conditioners and dehumidifiers fall under the EU ecodesign and energy-labelling rules. A compliant product ships with the correct energy label and product information sheet, and the seasonal efficiency values are recorded in the technical file. Private-label buyers receive label artwork and the fiche text in the languages of the markets they sell into.'),
   ('h2', 'F-Gas and refrigerant choice'),
   ('p', 'The F-Gas Regulation restricts high-GWP refrigerants. Focusee builds portable units with R290 (propane) and R32 low-GWP refrigerants selected per model and per market, with the refrigerant charge and documentation needed for import clearance. Choosing the right refrigerant is part of the model selection, not an afterthought.'),
   ('note', 'Refrigerant rules change. Confirm the current GWP limits and any model-specific restrictions for your target member states before the bill of materials is frozen.'),
   ('h2', 'The technical file and what the importer holds'),
   ('p', 'The importer is responsible for the product on the EU market. Keep the technical documentation, the Declaration of Conformity and the test reports on file, and make sure the rated values on the label match the tested unit. We release the batch test reports with the order so the file is complete at shipment.'),
   ('h2', 'UKCA alongside CE'),
   ('p', 'For Great Britain the equivalent mark is UKCA. Many EU models can be prepared for both markets; tell us if you sell into the UK as well as the EU so the documentation covers both routes.'),
   ('h2', 'How Focusee supports EU importers'),
   ('ul', [
     'CE marking with a complete technical file and EU Declaration of Conformity',
     'ErP energy label and product fiche artwork per market language',
     'R290 / R32 low-GWP refrigerant selection and documentation',
     'Batch test reports released with the shipment',
     'Voltage, plug (Type F / Schuko) and manual language set for the EU',
   ]),
  ],
  faqs=[
   ('What does CE marking actually require for a portable air conditioner?',
    'A valid CE mark is backed by a technical file: the EU Declaration of Conformity plus the test reports for electrical safety (LVD), electromagnetic compatibility (EMC), RoHS and the applicable ecodesign rules. The importer holds this file and must be able to present it on request.'),
   ('Do I need an energy label for the EU?',
    'Yes, for portable air conditioners and dehumidifiers. The product ships with the correct EU energy label and product information sheet, and the seasonal efficiency values are recorded in the technical file. Label artwork and fiche text are supplied in the market languages you sell into.'),
   ('Which refrigerant do you use for the EU?',
    'We build with R290 and R32 low-GWP refrigerants, chosen per model and per market to meet the F-Gas Regulation. The refrigerant charge and supporting documentation are provided for import clearance.'),
   ('Can one model be sold in both the EU and the UK?',
    'Often yes. The EU uses CE marking and Great Britain uses UKCA; many models can be prepared for both. Tell us if you sell into both so the documentation covers each route.'),
   ('What documents do I receive with the shipment?',
    'The batch test reports, the Declaration of Conformity and the labelling artwork are released with the order so your technical file is complete at the time of shipment.'),
   ('Can I order these under my own brand for the EU?',
    'Yes. Private-label units are delivered with your carton, rating label, manual and energy-label artwork, all prepared for EU conformity.'),
  ],
  models=['PCX5R-18MA', 'PC-LMA', 'PC20S-22MA'],
  models_head='EU-ready portable models for private label',
 ),
 dict(
  fname='applications/france-distributor-oem.html',
  path='applications/france-distributor-oem.html',
  title='Portable Air Conditioner OEM for the French Market | Focusee',
  desc='Private-label and OEM portable air conditioners for French retailers and distributors: 230 V / 50 Hz Type F plug, French manual and energy label, ErP compliance, mixed-container supply and lead times.',
  h1='Portable air conditioners for the French market',
  eyebrow='France',
  lede='The French retail and distribution channel \u2014 specialist appliances, DIY and electronics \u2014 buys portable air conditioners as a seasonal, private-label and own-brand category. This page covers the configuration and documentation French buyers expect, and how we supply them.',
  blocks=[
   ('h2', 'What the French market expects'),
   ('p', 'French buyers specify 230 V / 50 Hz with a Type F (Schuko) plug, a French-language user manual and rating label, and the EU energy label. Seasonal demand peaks before summer, so lead time and a planned repeat programme matter as much as the unit itself.'),
   ('ul', [
     '230 V / 50 Hz with Type F (Schuko) plug',
     'French-language manual, rating label and packaging text',
     'EU energy label and product fiche for France',
     'CE marking with a complete technical file',
     'R290 / R32 low-GWP refrigerant for the EU',
   ]),
   ('h2', 'Channels we supply'),
   ('p', 'Focusee supplies importers, distributors and retail brands across the French market. Whether the destination is a specialist appliance chain, a DIY and home-improvement retailer, or an online marketplace, the model selection and the packaging are prepared to the channel.'),
   ('h2', 'Private label and own-brand'),
   ('p', 'Most French programmes run as private label on a proven platform: your logo, retail carton, rating label and manual, with voltage, plug and refrigerant set for France. A full OEM programme with bespoke industrial design is available for buyers with the volume to support tooling.'),
   ('h2', 'Capacity range for France'),
   ('p', 'French apartments and smaller homes drive demand for compact 7,000\u201312,000 BTU units, while larger flats and town houses take 12,000\u201324,000 BTU. We cover the full range and can recommend the mix for a first order based on your customer profile.'),
   ('h2', 'Logistics and lead time'),
   ('ul', [
     'Mixed containers \u2013 portable AC, dehumidifiers and purifiers combined',
     'Typical production 30\u201345 days after sample and artwork approval',
     'FOB or CIF to a French port, with documentation for clearance',
     'Repeat orders planned ahead of the spring build-up',
   ]),
   ('note', 'Plan the first order well before the seasonal peak. Certification and artwork are on the critical path, and production slots tighten from late winter.'),
  ],
  faqs=[
   ('What voltage and plug do French buyers require?',
    '230 V / 50 Hz with a Type F (Schuko) plug, a French-language manual and rating label, and the EU energy label. We configure voltage, plug and manual at assembly for the French market.'),
   ('Can you supply our own brand for the French market?',
    'Yes. Private-label units ship with your carton, rating label, manual and energy-label artwork, all prepared for EU conformity and the French language.'),
   ('Which capacities sell in France?',
    'Compact 7,000\u201312,000 BTU units lead for apartments, with 12,000\u201324,000 BTU for larger homes. We can recommend a first-order mix from your customer profile.'),
   ('What is the lead time for a French order?',
    'Typically 30\u201345 days after sample and artwork approval, plus transit. Because seasonal demand peaks before summer, plan the first order ahead of the spring build-up.'),
   ('Can models be mixed in one container to France?',
    'Yes. Portable air conditioners, dehumidifiers and air purifiers can be combined in a single container with a loading plan, which suits a multi-category French assortment.'),
   ('Do you handle CE and ErP documentation?',
    'Yes. We supply CE marking with the technical file, the EU energy label and fiche, and the refrigerant documentation needed for French import.'),
  ],
  models=['PCX5R-18MA', 'PC-LMA', 'PC20S-22MA'],
  models_head='Compact-to-mid models suited to the French market',
 ),
 # ---- Blog: buyer guides (tool-type, link-worthy) ----
 dict(
  fname='blog/btu-sizing-guide.html',
  path='blog/btu-sizing-guide.html',
  title='How to Size a Portable Air Conditioner by BTU and Room | Focusee',
  desc='A practical BTU sizing guide for portable air conditioners: convert room square metres to BTU, adjust for sun, ceiling height and occupancy, and avoid the two mistakes that leave a unit underpowered.',
  h1='Sizing a portable air conditioner: a BTU guide',
  eyebrow='Guide',
  lede='Choosing the right portable air conditioner starts with cooling capacity, measured in BTU. Size it too small and the room never reaches temperature; too large and the unit short-cycles. This guide turns room dimensions into a sensible BTU range.',
  blocks=[
   ('h2', 'Start with the floor area'),
   ('p', 'Cooling capacity for a room is usually estimated from the floor area. A practical starting point for a standard ceiling height of about 2.5 m is roughly 20 BTU per square foot, or about 215 BTU per square metre. Use it as a first pass, then adjust for the factors below.'),
   ('table', ['Room', 'Area', 'Suggested capacity'], [
     ['Small bedroom', '10 \u2013 15 m\u00b2', '7,000 \u2013 9,000 BTU'],
     ['Large bedroom / office', '15 \u2013 25 m\u00b2', '9,000 \u2013 12,000 BTU'],
     ['Living room', '25 \u2013 35 m\u00b2', '12,000 \u2013 14,000 BTU'],
     ['Open-plan / large space', '35 \u2013 50 m\u00b2', '14,000 \u2013 24,000 BTU'],
   ]),
   ('note', 'Example: a 20 m\u00b2 room \u00d7 215 BTU \u2248 4,300 BTU as a base \u2014 but a living room with sun and two occupants should be rounded up well past the 9,000 BTU mark.'),
   ('h2', 'Adjust for the real conditions'),
   ('p', 'Floor area alone under-specifies most rooms. Add capacity for the things that load the space with heat:'),
   ('ul', [
     'Direct sun or a west-facing window \u2013 add 10\u201320 %',
     'High ceilings (above 2.7 m) \u2013 add roughly 10 % per extra 30 cm',
     'More than two occupants \u2013 each person adds heat',
     'Heat-producing equipment \u2013 computers, kitchen, servers',
     'Top-floor rooms \u2013 the roof adds gain',
   ]),
   ('h2', 'Two mistakes that leave a unit underpowered'),
   ('p', 'The first is ignoring the sun and rounding down to the nearest catalogue size. The second is forgetting that a portable unit must exhaust heat through a duct, so a poorly sealed window lets cooled air escape and forces the unit to work harder. Seal the vent panel and keep the duct run short.'),
   ('h2', 'Single-hose vs dual-hose'),
   ('p', 'A single-hose unit draws room air to cool the condenser and pushes it out through the same duct, which pulls warm air back in. A dual-hose unit uses outside air for the condenser, so it cools more efficiently in the same space. For rooms above about 25 m\u00b2, dual-hose is worth specifying.'),
   ('h2', 'Match capacity to the market'),
   ('p', 'Voltage and plug are set for the destination market, but capacity is set by the room. Tell us the room types and sizes you sell into and we will propose the BTU spread for the line, with the models and MOQ to match.'),
  ],
  faqs=[
   ('How many BTU do I need per square metre?',
    'As a first pass, about 215 BTU per square metre for a standard 2.5 m ceiling, then add capacity for sun, high ceilings, occupants and equipment. A 20 m\u00b2 room is roughly a 9,000 BTU starting point before adjustments.'),
   ('Should I round up or down?',
    'Round up. An underpowered unit never reaches temperature on a hot day and runs continuously; a slightly larger unit reaches setpoint and cycles off, which is easier on the compressor.'),
   ('Does a portable AC need venting?',
    'Yes. The heat removed from the room is pushed out through an exhaust duct. Seal the window vent panel and keep the duct run short so cooled air is not lost.'),
   ('Single-hose or dual-hose?',
    'Dual-hose is more efficient in the same space because it uses outside air for the condenser instead of pulling room air through the unit. For rooms above about 25 m\u00b2 it is worth specifying.'),
   ('Can I size by room type instead of maths?',
    'A rule-of-thumb table by room size is a good shortcut, but always adjust upward for sun and occupancy. Send us your room profile and we will propose the capacity spread for the line.'),
  ],
  models=[],
  models_head='',
 ),
 dict(
  fname='blog/dehumidifier-capacity-guide.html',
  path='blog/dehumidifier-capacity-guide.html',
  title='Choosing a Dehumidifier Capacity (Litres/Day) | Focusee',
  desc='How to pick dehumidifier capacity in litres per day: match extraction rate to room size, dampness level and use \u2014 basement, warehouse, laundry or comfort \u2014 plus auto-defrost and drain options.',
  h1='Choosing a dehumidifier capacity',
  eyebrow='Guide',
  lede='Dehumidifier capacity is rated in litres of water removed per day. Pick too low and the space stays damp; pick by litres alone and you can still miss the job if the room is cold or needs continuous drain. This guide matches capacity to the situation.',
  blocks=[
   ('h2', 'Capacity is litres per day, not tank size'),
   ('p', 'The headline number \u2014 10 L/day, 20 L/day, 50 L/day \u2014 is the extraction rate at a standard test condition. It is not the tank volume. A larger tank just means less frequent emptying; the litres/day figure is what decides whether the room dries.'),
   ('table', ['Space', 'Typical capacity', 'Notes'], [
     ['Flat / small basement', '10 \u2013 20 L/day', 'Comfort and light dampness'],
     ['Warehouse / light-commercial', '20 \u2013 35 L/day', 'Larger air volume, longer run time'],
     ['Large / very damp space', '35 \u2013 50 L/day', 'Flood recovery, storage, production'],
   ]),
   ('h2', 'Match capacity to how damp it is'),
   ('p', 'The same room needs more capacity if it is genuinely wet rather than merely humid. A laundry room or a basement after rain loads the air far more than a mildly humid living room, so size for the worst week, not the average day.'),
   ('ul', [
     'Mild humidity \u2013 occasional condensation on windows',
     'Moderate damp \u2013 musty smell, visible moisture',
     'Severe \u2013 standing water, flooding, storage at risk',
   ]),
   ('h2', 'Cold spaces need auto-defrost'),
   ('p', 'Below about 15 \u00b0C a dehumidifier\u2019s coil can ice up. Basements and unheated stores run cold, so auto-defrost is the specification point that keeps the unit working through winter. All Focusee dehumidifiers include auto-defrost.'),
   ('h2', 'Continuous drain vs tank'),
   ('p', 'For unattended or round-the-clock duty \u2014 a warehouse, a storage room, a flood recovery \u2014 a continuous-drain hose or condensate pump removes water without anyone emptying the tank. For a bedroom or office, the internal tank is usually enough.'),
   ('h2', 'Picking the line'),
   ('p', 'Decide the capacity band from the room and the dampness, then choose drain and defrost options from how it will be used. Tell us the spaces and duty cycle and we will propose the models and MOQ for the range.'),
  ],
  faqs=[
   ('How many litres per day do I need?',
    'A flat or small basement typically needs 10\u201320 L/day, a warehouse or light-commercial space 20\u201335 L/day, and a large or very damp space 35\u201350 L/day. Size for the worst week, not the average day.'),
   ('Is the litres/day number the tank size?',
    'No. Litres/day is the extraction rate at standard test conditions; the tank only sets how often you empty it. The extraction rate is what dries the room.'),
   ('Do I need auto-defrost?',
    'If the space runs below about 15 \u00b0C \u2014 a basement or unheated store \u2014 yes. The coil can ice up without it. All Focusee dehumidifiers include auto-defrost.'),
   ('Tank or continuous drain?',
    'A tank suits a bedroom or office. For unattended or continuous duty such as a warehouse or flood recovery, choose the continuous-drain hose or condensate pump so the unit never stops on a full tank.'),
   ('Can these be private labelled?',
    'Yes. Dehumidifiers are available for private label with your carton, rating label and manual, and the capacity and drain options set for your market.'),
  ],
  models=[],
  models_head='',
 ),
 # ---- French-language market pages (hreflang fr, targets French-language search) ----
 dict(
  fname='applications/fr-climatiseur-portable-oem.html',
  path='applications/fr-climatiseur-portable-oem.html',
  lang='fr',
  title='Climatiseur portable en marque blanche pour le marché français | Focusee',
  desc='Climatiseurs portables en OEM et marque blanche pour les revendeurs et distributeurs français : 230 V / 50 Hz prise Type F, notice en français et étiquette énergie, conformité ErP, conteneurs mixtes et délais.',
  h1='Climatiseurs portables pour le marché français',
  eyebrow='France',
  lede='Le canal de distribution français — magasins d’appareils, bricolage et électronique — achète le climatiseur portable comme une catégorie saisonnière et en marque propre. Cette page présente la configuration et la documentation attendues par les acheteurs français, et la façon dont nous les livrons.',
  blocks=[
   ('h2', 'Ce qu’attend le marché français'),
   ('p', 'Les acheteurs français spécifient 230 V / 50 Hz avec une prise Type F (Schuko), une notice utilisateur et une étiquette en français, ainsi que l’étiquette énergie UE. La demande est saisonnière et culmine avant l’été, aussi le délai et un programme de réapprovisionnement planifié comptent autant que l’appareil lui-même.'),
   ('ul', [
     '230 V / 50 Hz avec prise Type F (Schuko)',
     'Notice, étiquette et texte d’emballage en français',
     'Étiquette énergie et fiche produit UE pour la France',
     'Marquage CE avec dossier technique complet',
     'Réfrigérant à faible PRG R290 / R32 pour l’UE',
   ]),
   ('h2', 'Les canaux que nous servons'),
   ('p', 'Focusee fournit importateurs, distributeurs et marques de retail sur le marché français. Qu’il s’agisse d’une enseigne d’appareils, d’un distributeur bricolage ou d’une place de marché en ligne, la sélection des modèles et l’emballage sont préparés pour le canal.'),
   ('h2', 'Marque blanche et propre'),
   ('p', 'La plupart des programmes français fonctionnent en marque blanche sur une plateforme éprouvée : votre logo, carton, étiquette et notice, avec tension, prise et réfrigérant paramétrés pour la France. Un programme OEM complet avec design industriel propre est possible pour les acheteurs ayant le volume nécessaire.'),
   ('h2', 'Gammes de puissance pour la France'),
   ('p', 'Les appartements et petites maisons françaises favorisent les modèles compacts de 7 000 à 12 000 BTU, tandis que les grands appartements et maisons de ville prennent 12 000 à 24 000 BTU. Nous couvrons toute la gamme et pouvons recommander le mix d’une première commande selon votre clientèle.'),
   ('h2', 'Logistique et délais'),
   ('ul', [
     'Conteneurs mixtes — climatiseurs, déshumidificateurs et purificateurs combinés',
     'Production typique de 30 à 45 jours après validation échantillon et BAT',
     'FOB ou CIF vers un port français, avec documents de dédouanement',
     'Commandes répétées planifiées avant la montée de printemps',
   ]),
   ('note', 'Planifiez la première commande bien avant le pic saisonnier. La certification et le BAT sont sur le chemin critique, et les créneaux de production se resserrent à partir de la fin de l’hiver.'),
  ],
  faqs=[
   ('Quelle tension et prise les acheteurs français exigent-ils ?',
    '230 V / 50 Hz avec prise Type F (Schuko), notice et étiquette en français, et étiquette énergie UE. Nous paramétrons tension, prise et notice à l’assemblage pour le marché français.'),
   ('Pouvez-vous livrer sous notre propre marque pour la France ?',
    'Oui. Les unités en marque blanche sont livrées avec votre carton, étiquette, notice et étiquette énergie, le tout préparé pour la conformité UE et la langue française.'),
   ('Quelles puissances se vendent en France ?',
    'Les modèles compacts 7 000 à 12 000 BTU dominent pour les appartements, et 12 000 à 24 000 BTU pour les grandes habitations. Nous pouvons recommander un mix de première commande selon votre clientèle.'),
   ('Quel est le délai pour une commande française ?',
    'Typiquement 30 à 45 jours après validation échantillon et BAT, plus le transport. Comme la demande est saisonnière, planifiez la première commande avant la montée de printemps.'),
   ('Peut-on mélanger les modèles dans un conteneur vers la France ?',
    'Oui. Climatiseurs, déshumidificateurs et purificateurs peuvent être combinés dans un seul conteneur avec un plan de chargement, ce qui convient à un assortiment français multi-catégories.'),
   ('Gérez-vous les documents CE et ErP ?',
    'Oui. Nous fournissons le marquage CE avec le dossier technique, l’étiquette énergie UE et la fiche, ainsi que la documentation réfrigérant nécessaire à l’importation française.'),
  ],
  models=['PCX5R-18MA', 'PC-LMA', 'PC20S-22MA'],
  models_head='Modèles compacts à moyens adaptés au marché français',
 ),
 dict(
  fname='applications/fr-certification-ce.html',
  path='applications/fr-certification-ce.html',
  lang='fr',
  title='Conformité CE, ErP et F-Gas pour l’importateur UE | Focusee',
  desc='Ce dont les importateurs UE ont besoin pour vendre climatiseurs portables, déshumidificateurs et purificateurs : marquage CE, étiquette énergie ErP, règles F-Gas sur le réfrigérant, dossier technique et documents, fournis par Focusee.',
  h1='Mettre un climatiseur portable sur le marché de l’UE',
  eyebrow='Conformité UE',
  lede='Vendre un climatiseur portable, un déshumidificateur ou un purificateur dans l’Union européenne implique le marquage CE, les règles d’étiquetage énergétique ErP et les exigences F-Gas sur le réfrigérant. Cette page décrit la documentation et la façon dont nous soutenons les importateurs et marques UE.',
  blocks=[
   ('h2', 'Le marquage CE : le socle du marché UE'),
   ('p', 'Chaque unité mise sur le marché UE doit porter un marquage CE valide, appuyé par un dossier technique : la Déclaration de conformité UE, les normes harmonisées applicables pour la sécurité électrique et la CEM, et les rapports d’essai correspondants. Le marquage est l’affirmation de l’importateur que le produit respecte la législation UE.'),
   ('ul', [
     'Directive Basse Tension (LVD) — sécurité électrique',
     'Directive CEM — compatibilité électromagnétique',
     'RoHS — restriction des substances dangereuses',
     'REACH — documentation sur les substances chimiques',
     'Exigences éco-conception et étiquetage énergétique',
   ]),
   ('h2', 'Étiquetage énergétique ErP'),
   ('p', 'Les climatiseurs portables et déshumidificateurs relèvent des règles UE d’éco-conception et d’étiquetage. Un produit conforme est livré avec l’étiquette énergie correcte et la fiche produit, et les valeurs de rendement saisonnier sont consignées au dossier technique.'),
   ('h2', 'F-Gas et choix du réfrigérant'),
   ('p', 'Le règlement F-Gas restreint les réfrigérants à fort PRG. Focusee construit des unités portables avec les réfrigérants à faible PRG R290 (propane) et R32, choisis par modèle et par marché, avec la charge et la documentation nécessaires au dédouanement.'),
   ('note', 'Les règles sur les réfrigérants évoluent. Confirmez les limites de PRG en vigueur et les restrictions par État membre avant de figer la nomenclature.'),
   ('h2', 'Le dossier technique'),
   ('p', 'L’importateur est responsable du produit sur le marché UE. Conservez la documentation technique, la Déclaration de conformité et les rapports d’essai, et vérifiez que les valeurs de l’étiquette correspondent à l’unité testée. Nous remettons les rapports de lot avec la commande.'),
   ('h2', 'UKCA conjointement au CE'),
   ('p', 'Pour la Grande-Bretagne, la marque équivalente est UKCA. De nombreux modèles UE peuvent être préparés pour les deux marchés ; dites-nous si vous vendez aussi au Royaume-Uni.'),
   ('h2', 'Comment Focusee soutient les importateurs UE'),
   ('ul', [
     'Marquage CE avec dossier technique complet et Déclaration UE',
     'Étiquette énergie ErP et fiche produit par langue de marché',
     'Choix et documentation du réfrigérant R290 / R32 à faible PRG',
     'Rapports d’essai de lot remis avec l’expédition',
     'Tension, prise (Type F) et langue de notice paramétrées pour l’UE',
   ]),
  ],
  faqs=[
   ('Que requiert concrètement le marquage CE pour un climatiseur portable ?',
    'Un CE valide s’appuie sur un dossier technique : la Déclaration de conformité UE plus les rapports d’essai pour la sécurité électrique (LVD), la CEM, la RoHS et les règles d’éco-conception applicables. L’importateur détient ce dossier et doit pouvoir le présenter.'),
   ('Une étiquette énergie est-elle nécessaire pour l’UE ?',
    'Oui, pour les climatiseurs portables et déshumidificateurs. Le produit est livré avec l’étiquette UE correcte et la fiche produit, et les valeurs de rendement saisonnier sont consignées au dossier technique.'),
   ('Quel réfrigérant utilisez-vous pour l’UE ?',
    'Nous construisons avec les réfrigérants à faible PRG R290 et R32, choisis par modèle et par marché pour respecter le règlement F-Gas. La charge et la documentation sont fournies pour le dédouanement.'),
   ('Un même modèle peut-il être vendu en UE et au Royaume-Uni ?',
    'Souvent oui. L’UE utilise le CE et la Grande-Bretagne l’UKCA ; de nombreux modèles peuvent être préparés pour les deux. Précisez-nous si vous vendez sur les deux marchés.'),
   ('Quels documents recevez-vous avec l’expédition ?',
    'Les rapports d’essai de lot, la Déclaration de conformité et les visuels d’étiquetage sont remis avec la commande afin que votre dossier soit complet au moment de l’expédition.'),
   ('Puis-je commander ces produits sous ma propre marque pour l’UE ?',
    'Oui. Les unités en marque blanche sont livrées avec votre carton, étiquette, notice et étiquette énergie, tous préparés pour la conformité UE.'),
  ],
  models=[],
  models_head='',
 ),
 # ---- More English buyer-guide blog posts (long-tail) ----
 dict(
  fname='blog/server-room-heat-load.html',
  path='blog/server-room-heat-load.html',
  title='How to Calculate Server Room Cooling Load (Watts × 3.412) | Focusee',
  desc='A practical server-room heat-load calculation: convert equipment watts to BTU/h, add margin for solar gain and people, and size a portable spot cooler to the room.',
  h1='Calculating a server room cooling load',
  eyebrow='Guide',
  lede='Electrical equipment turns almost all of its input power into heat, so a server room’s cooling load can be calculated directly from its wattage. This guide turns that wattage into a BTU figure and a sensible spot-cooler size.',
  blocks=[
   ('h2', 'The core conversion'),
   ('p', 'Because IT and electrical equipment convert input power almost entirely to heat, the load is simply the equipment wattage. Convert it to cooling units with the factor:'),
   ('note', 'BTU/h = equipment watts × 3.412'),
   ('p', 'Example: a 3 kW rack draws 3,000 W. 3,000 × 3.412 = 10,236 BTU/h. That is the heat the cooler must remove before any extra gains.'),
   ('h2', 'Add margin for the room'),
   ('p', 'The raw equipment load is only the start. Add 20-30 % for solar gain through windows, lighting, people in the room and duct losses, then round up to the nearest available capacity.'),
   ('table', ['Installation', 'Typical IT / electrical load', 'Suggested capacity'], [
     ['Wall-mounted comms cabinet', '0.5 - 1.5 kW', '4,000 - 7,000 BTU'],
     ['Small rack (1-3 racks)', '2 - 4 kW', '12,000 - 18,000 BTU'],
     ['Server room / switchgear room', '5 - 8 kW', '24,000 - 30,000 BTU'],
   ]),
   ('h2', 'Why a portable spot cooler fits'),
   ('p', 'Where a split system cannot be installed — rented premises, a cabinet added after the room was built, or standby capacity for equipment that cannot go offline — a portable spot cooler is the fastest way to remove heat. No outdoor condenser, no refrigerant pipework, running the same day.'),
   ('h2', 'Deliver the cold air where it matters'),
   ('p', 'Point the supply louvre at the equipment intake, or use a cold-air duct kit to reach the front of a rack. Keep return air away from the cold supply to avoid short-cycling, and blank unused rack space so cold air is not lost.'),
   ('h2', 'Continuous operation'),
   ('p', 'For round-the-clock duty specify a condensate pump or gravity drain so the unit does not stop on a full tank. The models used here are built for long duty, but filters should be cleaned at the interval in the manual.'),
  ],
  faqs=[
   ('How do I convert server watts to BTU?',
    'Multiply the equipment wattage by 3.412 to get BTU/h. A 3 kW rack therefore needs roughly 10,200 BTU/h before any extra margin for solar gain or people.'),
   ('How much margin should I add?',
    'Add 20-30 % for windows, lighting, occupants and duct losses, then round up to the nearest available capacity. A 3 kW rack typically lands at a 12,000-14,000 BTU unit.'),
   ('Can a portable unit cool a server room?',
    'For small and mid-size loads, yes. A spot cooler handles a comms cabinet or small rack room well; beyond roughly 8-10 kW a dedicated precision system is the right answer and the portable becomes standby.'),
   ('Does it need a drain?',
    'The internal tank is fine for short jobs. For continuous operation choose the condensate pump or gravity-drain option so the unit does not shut down when the tank fills.'),
   ('Can I duct cold air to a rack?',
    'Yes. A cold-air duct kit delivers air from the supply louvre directly to the front of the rack, which is far more effective than cooling the whole room.'),
  ],
  models=[],
  models_head='',
 ),
 dict(
  fname='blog/tent-rv-ac-power.html',
  path='blog/tent-rv-ac-power.html',
  title='Powering a Tent or RV Air Conditioner: Hook-ups, Generators, 12V | Focusee',
  desc='How to power a portable air conditioner in a tent, caravan or motorhome: campsite hook-up amperage, generator sizing, 12 V battery and inverter options, and voltage configured for your market.',
  h1='Powering a tent or RV air conditioner',
  eyebrow='Guide',
  lede='A portable air conditioner is only useful if the pitch or vehicle can power it. This guide covers campsite hook-ups, generators, 12 V options and the start-up current that catches first-time buyers out.',
  blocks=[
   ('h2', 'Campsite hook-ups'),
   ('p', 'EU and UK campsite hook-ups are normally 230-240 V at 6 A or 16 A. Confirm the site amperage before selecting a model, because a unit that draws more than the supply allows will trip the post.'),
   ('ul', [
     'Compact units draw roughly 400-700 W',
     'Mid-size camping units 700-1,200 W',
     'Always check the hook-up rating, not just the voltage',
   ]),
   ('h2', 'Generators'),
   ('p', 'Off-grid users run an AC unit from a small generator. Size the generator for the unit’s start-up current, which is several times the running current for the first second, not for the running watts alone.'),
   ('h2', '12 V and battery banks'),
   ('p', 'Compact DC units can run from a 12 V or 24 V battery bank through a suitable inverter. AC units generally need a hook-up or a generator because start-up current is too high for a small battery alone.'),
   ('h2', 'Voltage and market'),
   ('p', 'Voltage, plug type and frequency are configured at assembly for the destination market — Type F for the EU, Type G for the UK, Type I for AU / NZ and Type A/B for North America. Tell us where the unit will be used and we set it.'),
   ('note', 'Start-up (locked-rotor) current is the figure that trips breakers. Size supply and cabling for that, not the running wattage.'),
  ],
  faqs=[
   ('Will a camping air conditioner run from a battery?',
    'Compact DC models can run from a 12 V or 24 V battery bank through a suitable inverter. AC units generally need a campsite hook-up or a generator because start-up current is several times the running current.'),
   ('What campsite amperage do I need?',
    'EU and UK hook-ups are typically 6 A or 16 A at 230-240 V. Confirm the site rating before choosing a model so the unit does not trip the supply.'),
   ('How big a generator do I need?',
    'Size it for the start-up current, which is several times the running current for the first moment, not the running watts alone.'),
   ('Can you configure voltage for my market?',
    'Yes. Voltage, plug type and frequency are set at assembly — Type F for the EU, Type G for the UK, Type I for AU / NZ, Type A/B for North America.'),
   ('Why does my breaker trip on start-up?',
    'The compressor draws several times its running current for a moment at start-up. Size the supply and cabling for that locked-rotor current, not the running wattage.'),
  ],
  models=[],
  models_head='',
 ),
]

def build_app(spec):
    r = '../'
    blocks = []
    for b in spec['blocks']:
        if b[0] == 'h2':
            blocks.append(f'<h2>{esc(b[1])}</h2>')
        else:
            blocks.append(render_blocks([b]))
    article = '\n'.join(blocks)
    faqs = spec.get('faqs', [])
    faq_html = ''.join(
        f'<details{" open" if i == 0 else ""}><summary>{esc(q)}</summary>'
        f'<div class="faq-a"><p>{esc(a)}</p></div></details>'
        for i, (q, a) in enumerate(faqs))
    # related models
    rel = ''
    picks = [prod_by_name(n) for n in spec.get('models', [])]
    picks = [p for p in picks if p]
    if picks:
        rel = (f'<section class="alt"><div class="wrap">'
               f'<div class="sec-head"><span class="eyebrow g">Related models</span>'
               f'<h2>{esc(spec["models_head"])}</h2></div>'
               f'<div class="grid">'
               + '\n'.join(card(p, i, r) for i, p in enumerate(picks))
               + '</div>'
               f'<div style="text-align:center;margin-top:34px">'
               f'<a class="btn btn-line" href="{r}products.html">View the full catalogue</a></div>'
               f'</div></section>')
    else:
        links = ''.join(
            f'<li><a href="{r}{CAT_SLUG[c]}.html">{esc(c)}</a></li>' for c in CATS)
        rel = (f'<section class="alt"><div class="wrap">'
               f'<div class="sec-head"><span class="eyebrow g">Where to start</span>'
               f'<h2>Browse the product lines we build under private label</h2></div>'
               f'<div class="prose"><ul>{links}</ul>'
               f'<p>Send us a brief - target market, capacity range and volumes - and we will come back '
               f'with the platforms that fit and the tooling or artwork that each one needs.</p></div>'
               f'</div></section>')
    body = f'''<section class="phead"><div class="wrap">
  <h1>{esc(spec['h1'])}</h1>
  <div class="crumb"><a href="{r}index.html">Home</a><span class="sep">/</span>
  <a href="{r}index.html#resources">Resources</a><span class="sep">/</span><span>{esc(spec['eyebrow'])}</span></div>
</div></section>

<section style="padding-top:44px"><div class="wrap">
  <div class="prose">
    <p class="lede" style="font-size:17px;color:var(--ink)">{esc(spec['lede'])}</p>
    {article}
  </div>
  <div class="prose"><div class="art-cta">
    <div><h3>Need pricing or a specification sheet?</h3>
    <p>Send us the capacity, market and volume you have in mind and we will reply with models, MOQ and lead time.</p></div>
    <a class="btn btn-grad" href="{r}contact.html">Get a Quote</a>
  </div></div>
</div></section>

<section class="alt" id="faq"><div class="wrap">
  <div class="sec-head">
    <span class="eyebrow g">Buyer questions</span>
    <h2>Frequently asked questions</h2>
  </div>
  <div class="faq">{faq_html}</div>
</div></section>

{rel}
'''
    faq_ld = ld({"@context": "https://schema.org", "@type": "FAQPage",
                 "mainEntity": [{"@type": "Question", "name": q,
                                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                                for q, a in faqs]}) if faqs else ''
    jsonld = breadcrumb_ld([('Home', SITE), ('Resources', None), (spec['h1'], None)])
    if faq_ld:
        jsonld += '\n' + faq_ld
    return page(spec['fname'], spec['title'], spec['desc'], body,
                active='', r=r, canon=SITE + spec['path'],
                ogt='article', ogi=OG_IMAGE, jsonld=jsonld, path=spec['path'],
                lang=spec.get('lang', 'en'))

# ------------------------------------------------------------------ DETAIL
def spec_tables(tables):
    specs=[]; funcs=[]
    for t in tables:
        if not t: continue
        if len(t[0]) == 1: specs.append(t)
        else: funcs.append(t)
    return specs, funcs

def build_detail(p):
    g = p['g']
    main = g[0] if g else 'logo.png'
    thumbs = ''
    for i, im in enumerate(g):
        wattr = ' data-webp="%s"' % webp_src(im) if im in WEBP else ''
        on = ' class="on"' if i == 0 else ' class=""'
        thumbs += ('<button%s data-src="assets/img/%s"%s>%s</button>'
                   % (on, im, wattr, pic(im, alt_of(p, i))))
    bl = ''.join(f'<li>{esc(b)}</li>' for b in p['bullets'][:6])
    specs, funcs = spec_tables(p['tables'])
    spec_html = ''
    for t in specs:
        head = t[0][0]
        rows = ''
        for r in t[1:]:
            if len(r) == 1:
                rows += f'<tr><td colspan="9" style="background:#E8F1FA;color:var(--navy-2);font-weight:700">{esc(r[0])}</td></tr>'
            else:
                rows += '<tr>' + ''.join(f'<td>{esc(c)}</td>' for c in r) + '</tr>'
        spec_html += f'''<div style="margin-bottom:28px">
  <h3 style="font-size:16px;margin-bottom:12px;color:var(--navy-2)">{esc(head)} &mdash; Specification</h3>
  <div class="tbl-wrap"><table class="spec"><tbody><tr><td colspan="9" style="text-align:center;font-weight:700">{esc(head)}</td></tr>{rows}</tbody></table></div>
</div>'''
    func_html = ''
    for t in funcs:
        cells = ''
        for r in t:
            if len(r) < 2: continue
            key, val = r[0], r[1]
            na = val.strip() in ('N/A', 'No', '-', '')
            cells += f'<div class="func" style="{"opacity:.45" if na else ""}"><span>{esc(key)}</span><b style="margin-left:auto;font-weight:600;color:{"var(--muted)" if na else "var(--blue)"};font-size:12.5px">{esc(val) if val.strip() else "&ndash;"}</b></div>'
        func_html += f'<div class="func-grid" style="margin-bottom:22px">{cells}</div>'
    if not func_html:
        func_html = '<p style="color:var(--muted)">Function list available on request.</p>'
    # quick highlights: try to read BTU + refrigerant from spec
    hi = ''
    flat = ' '.join(' | '.join(r) for r in sum(specs, []))
    m = re.search(r'([\d,]{3,7})\s*/\s*[\d,]{3,7}(?:\s*/\s*[\d,]{3,7})*\s*(?:BTU)?', flat)
    btu = ''
    for r in sum(specs, []):
        if len(r) > 1 and 'BTU' in r[0].upper():
            btu = ' / '.join(r[1:]); break
    ref = ''
    for r in sum(specs, []):
        if len(r) > 1 and 'Refrigerant' in r[0]:
            ref = ' / '.join(dict.fromkeys(r[1:])); break
    moq = ' &middot; '
    moq = next((b for b in p['bullets'] if b.lower().startswith('moq')), '')
    if btu: hi += f'<div><b>{esc(btu)}</b><span>COOLING CAPACITY (BTU)</span></div>'
    if ref: hi += f'<div><b>{esc(ref)}</b><span>REFRIGERANT</span></div>'
    if moq: hi += f'<div><b>{esc(moq.replace("MOQ:","").strip())}</b><span>MINIMUM ORDER</span></div>'
    hi_html = f'<div class="pd-high">{hi}</div>' if hi else ''
    prev = f'<a href="product-{p["prev"]["slug"]}.html"><span>Previous</span>{esc(p["prev"]["name"])}</a>' if p['prev'] else '<span></span>'
    nxt = f'<a href="product-{p["next"]["slug"]}.html" style="text-align:right"><span>Next</span>{esc(p["next"]["name"])}</a>' if p['next'] else '<span></span>'
    related = [x for x in DATA if x['cat'] == p['cat'] and x['slug'] != p['slug']][:4]
    rel_html = ''.join(card(x, i) for i, x in enumerate(related))
    body = f'''<section class="phead" style="padding-bottom:8px"><div class="wrap">
  <div class="crumb"><a href="index.html">Home</a><span class="sep">/</span><a href="products.html">Products</a><span class="sep">/</span><a href="products.html#{CAT_SLUG.get(p['cat'],'')}">{esc(p['cat'])}</a><span class="sep">/</span><span>{esc(p['name'])}</span></div>
</div></section>

<div class="wrap"><div class="pd-top">
  <div class="pd-gallery">
    <div class="pd-main">{pic(main, alt_of(p), lazy=False, extra=' id="pdmain"')}</div>
    <div class="pd-thumbs">{thumbs}</div>
  </div>
  <div class="pd-info">
    <span class="pd-cat">{esc(p['cat'])}</span>
    <h1>{esc(p['name'])}</h1>
    {f'<p class="pd-slogan">{esc(p["desc"])}</p>' if p['desc'] else ''}
    <ul class="pd-bullets">{bl}</ul>
    {hi_html}
    <div class="pd-actions">
      <a class="btn btn-grad" href="mailto:Marketing@focuseetech.com?subject=Quotation%20request%20-%20{esc(p['name'])}">Request quotation</a>
      <a class="btn btn-line" href="https://wa.me/8613425651968">Enquire on WhatsApp</a>
    </div>
    <p style="margin-top:22px;font-size:13px;color:var(--muted)">Sold to importers, distributors and retail brands. OEM / private label welcome. Voltage, plug type and packaging configured to your market.</p>
  </div>
</div></div>

<div class="wrap"><div class="pd-sec">
  <h2>Specification</h2>
  {spec_html or '<p style="color:var(--muted)">Detailed specification available on request.</p>'}
</div></div>

<div class="wrap"><div class="pd-sec">
  <h2>Functions</h2>
  {func_html}
</div></div>

<div class="wrap"><div class="pager">{prev}{nxt}</div></div>

<section class="alt"><div class="wrap">
  <div class="sec-head left" style="margin-bottom:30px"><span class="eyebrow g">Related models</span><h2 style="font-size:27px">More {esc(p['cat'])}</h2></div>
  <div class="grid">{rel_html}</div>
</div></section>

<section class="alt" id="faq" style="background:#fff"><div class="wrap">
  <div class="sec-head">
    <span class="eyebrow g">Buyer questions</span>
    <h2>{esc(p['cat'])} — frequently asked questions</h2>
  </div>
  <div class="faq">{detail_faq_html(p['cat'])}</div>
</div></section>

{cta()}
'''
    word = CATEGORY_WORD.get(p['cat'], 'portable air comfort unit')
    short = (p.get('desc') or '; '.join(re.sub(r'\s+', ' ', b).strip(' ;,') for b in p['bullets'][:3])).strip()
    short = re.sub(r'\s+', ' ', short)[:150].rstrip(' ,;')
    desc = (f'{p["name"]} {word} from Focusee Company Limited. {short}. '
            f'Specification table, function list, MOQ and container loading data for OEM and private label orders.')
    ogimg = SITE + 'assets/img/' + (g[0] if g else 'logo.png')
    jsonld = (product_ld(p) + '\n'
              + breadcrumb_ld([('Home', SITE), ('Products', SITE + 'products.html'),
                               (p['cat'], SITE + 'products.html#' + CAT_SLUG.get(p['cat'], '')),
                               (p['name'], None)])
              + ('\n' + detail_faq_ld(p['cat']) if detail_faq_ld(p['cat']) else ''))
    return page(f'product-{p["slug"]}.html',
                f'{p["name"]} {word} | Focusee Company Limited',
                desc, body, ogt='product', ogi=ogimg, jsonld=jsonld)

# ------------------------------------------------------------------ ABOUT
def build_about():
    body = f'''<section class="phead"><div class="wrap">
  <h1>About Focusee</h1>
  <div class="crumb"><a href="index.html">Home</a><span class="sep">/</span><span>About Us</span></div>
</div></section>

<section>
  <div class="wrap split">
    <div class="split-text">
      <span class="eyebrow g">Who we are</span>
      <h2>Portable air comfort, engineered in Zhongshan</h2>
      <p>{COMPANY} is a manufacturer and exporter of portable air conditioners, dehumidifiers, humidifiers and air purifiers. Our engineering team comes from the home appliance industry, and we specialise in building compact, ductless units that combine several functions in one chassis.</p>
      <p>We work with importers, distributors, retail chains and private-label brands. Projects are handled end to end: model selection, control panel and housing customisation, certification documentation, packaging artwork and container loading.</p>
      <ul class="ticks">
        <li>Ductless, wheel-mounted units &mdash; no installation required</li>
        <li>Self-evaporating technology, free from drainage while cooling</li>
        <li>WiFi app and infrared remote control as standard on most models</li>
        <li>MOQ, carton and container loading data published for every model</li>
      </ul>
    </div>
    <div class="split-visual">
      <div class="frame">{pic(DATA[0]['g'][0], 'Focusee portable dehumidifier on the production line')}</div>
      <div class="float-card a"><b>{len(DATA)}+</b><span>Models in catalogue</span></div>
      <div class="float-card b"><b>{len(CATS)}</b><span>Product families</span></div>
    </div>
  </div>
</section>

<div class="band"><div class="wrap">
  <div><b>Simple</b><span>Self-detection &amp; conditioning</span></div>
  <div><b>Smart</b><span>WiFi, app &amp; remote control</span></div>
  <div><b>Silent</b><span>From 38 dB operating noise</span></div>
  <div><b>Green</b><span>R290 / R32, low GWP</span></div>
</div></div>

<section id="green">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow g">Sustainability</span>
      <h2>Go green, go sustainable</h2>
      <p>We believe our industry can influence the environment deeply &mdash; and that we have a responsibility to change. Four green principles guide how we design, source and manufacture.</p>
    </div>
    <div class="vals">
      <div class="val"><span class="k">01 &middot; Green Policy</span><h3>Reduce the damage and the waste</h3>
        <p>All materials are RoHS certified, including our upstream and downstream supply chain. We adopt environmentally friendly refrigerant alternatives with lower GWP, and we keep improving efficiency so users reach comfort without wasting time or electricity.</p></div>
      <div class="val"><span class="k">02 &middot; Green Product</span><h3>Reuse the resource</h3>
        <p>Water is precious, so we use every drop. Condensate can be reused to humidify the room, and exhaust air is filtered and sterilised before it leaves the unit &mdash; no more emission, just fresh air released.</p></div>
      <div class="val"><span class="k">03 &middot; Green Process</span><h3>Rescue the creatures and the habitat</h3>
        <p>Everyone has the right to drink water and breathe fresh air. We keep developing products that deliver clean water and clean air for households in regions where both are scarce.</p></div>
      <div class="val"><span class="k">04 &middot; Green Partner</span><h3>Repurpose the needs and usage of products</h3>
        <p>Do we really need an air conditioner, a heater, a clothes dryer and a dehumidifier at home for such limited use? A 6-in-1 portable unit solves the same problems through different seasons &mdash; one machine, far fewer resources consumed.</p></div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Product concept</span>
      <h2>Smart living &amp; simple living</h2>
      <p>Four commitments we design into every portable unit we ship.</p>
    </div>
    <div class="why">
      <div class="why-card"><div class="why-ico"><svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a9 9 0 1 0 9 9"/><path d="M12 7v5l3 3"/></svg></div>
        <h3>Simple life</h3><p>Self-detection and conditioning of temperature, humidity and timing &mdash; easy to operate and soothing, all in one unit.</p></div>
      <div class="why-card"><div class="why-ico"><svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18M5 8l14 8M19 8L5 16"/></svg></div>
        <h3>Resource reusing</h3><p>Waste recycle and reuse, condensate sterilisation, exhaust purification and low-GWP refrigerant adoption.</p></div>
      <div class="why-card"><div class="why-ico"><svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h18M12 3v18"/><circle cx="12" cy="12" r="9"/></svg></div>
        <h3>Quality air</h3><p>Constant temperature and humidity with HEPA filtration, high CADR, efficient ACH and powerful odour and dust reduction.</p></div>
      <div class="why-card"><div class="why-ico"><svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h6l-1 8 9-12h-6z"/></svg></div>
        <h3>Energy saving</h3><p>Best-in-class EER achievements: EU Class A++, US Energy Star certified, Taiwan Grade 1 &mdash; strong performance, lower consumption.</p></div>
    </div>
  </div>
</section>

{cta()}
'''
    return page('about.html', 'About Us | Focusee Company Limited — Portable Air Comfort Manufacturer',
                'Focusee Company Limited is a Zhongshan-based manufacturer of portable air conditioners, dehumidifiers and air purifiers, supplying importers, distributors and private-label brands worldwide.',
                body, 'about',
                jsonld=breadcrumb_ld([('Home', SITE), ('About Us', None)]))

# ------------------------------------------------------------------ CONTACT
def build_contact():
    cards = ''
    for p in PEOPLE:
        cards += f'''<div class="c-card">
  <span class="role">{esc(p['role'])}</span>
  <h3>{esc(p['name'])}</h3>
  <div class="c-row"><i>&#9993;</i><a href="mailto:{p['email']}">{p['email']}</a></div>
  <div class="c-row"><i>&#9990;</i><a href="https://wa.me/{p['wl']}">WhatsApp: {p['wa']}</a></div>
</div>'''
    body = f'''<section class="phead"><div class="wrap">
  <h1>Contact us</h1>
  <div class="crumb"><a href="index.html">Home</a><span class="sep">/</span><span>Contact</span></div>
</div></section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow g">Sales &amp; enquiries</span>
      <h2>Your contacts at Focusee</h2>
      <p>Tell us the product, market and target volume &mdash; we will come back with the model, certification status, MOQ and a formal quotation.</p>
    </div>
    <div class="c-grid">{cards}</div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Factory &amp; office</span>
      <h2>Where we are</h2>
    </div>
    <div class="info-grid">
      <div class="c-card"><h4>Address</h4><p>{esc(ADDRESS)}</p></div>
      <div class="c-card"><h4>Business</h4><p>OEM &amp; ODM portable air conditioners, dehumidifiers, air purifiers and accessories. Export documentation, certification support and private-label packaging.</p></div>
      <div class="c-card"><h4>Markets</h4><p>Europe, United Kingdom, North America, Australia &amp; New Zealand, the Middle East and South East Asia.</p></div>
    </div>
  </div>
</section>

{cta()}
'''
    contact_ld = ld({
        "@context": "https://schema.org", "@type": "ContactPage",
        "name": "Contact Focusee Company Limited",
        "url": SITE + "contact.html",
        "mainEntity": {"@id": SITE + "#organization"},
    })
    return page('contact.html', 'Contact | Focusee Company Limited — Portable Air Conditioner Manufacturer',
                'Contact Focusee Company Limited for portable air conditioner, dehumidifier and air purifier enquiries. Carol Luo, General Manager and Robert Luo, Marketing Manager.',
                body, 'contact',
                jsonld=breadcrumb_ld([('Home', SITE), ('Contact', None)]) + '\n' + contact_ld)

# ------------------------------------------------------------------ JS
JS = '''/* FOCUSEE site scripts */
(function(){
  var b=document.getElementById('burger'), n=document.getElementById('navmain');
  if(b&&n){ b.addEventListener('click',function(){ n.classList.toggle('open'); }); }
  document.querySelectorAll('.has-sub > a').forEach(function(a){
    a.addEventListener('click',function(e){
      if(window.innerWidth<=900){ e.preventDefault(); a.parentNode.classList.toggle('open'); }
    });
  });

  /* product filters */
  var fw=document.getElementById('filters');
  if(fw){
    fw.addEventListener('click',function(e){
      var btn=e.target.closest('button'); if(!btn) return;
      var f=btn.dataset.f;
      fw.querySelectorAll('button').forEach(function(x){ x.classList.toggle('on', x===btn); });
      var groups=document.querySelectorAll('.pgroup');
      if(groups.length){
        groups.forEach(function(g){ g.style.display = (f==='all'||g.dataset.cat===f)?'':'none'; });
      }
      var grid=document.getElementById('grid');
      if(grid){
        grid.querySelectorAll('.card').forEach(function(c){
          var ok = f==='all' || (c.dataset.cat===f);
          c.style.display = ok?'':'none';
        });
      }
    });
  }

  /* product gallery — keeps <picture><source type=webp> in sync with <img> */
  var m=document.getElementById('pdmain');
  if(m){
    var wrap=m.parentNode, sp=(wrap && wrap.tagName==='PICTURE') ? wrap.querySelector('source') : null;
    document.querySelectorAll('.pd-thumbs button').forEach(function(b){
      b.addEventListener('click',function(){
        document.querySelectorAll('.pd-thumbs button').forEach(function(x){x.classList.remove('on');});
        b.classList.add('on');
        var w=b.getAttribute('data-webp');
        if(sp){
          if(w){
            /* re-attach if a previous switch had to detach the webp source */
            if(!sp.parentNode) wrap.insertBefore(sp, m);
            sp.setAttribute('srcset', w);
          } else if(sp.parentNode){
            /* this image has no webp sibling: drop the source or the old one keeps winning */
            sp.parentNode.removeChild(sp);
          }
        }
        m.src=b.dataset.src;
      });
    });
  }

  /* header shadow on scroll */
  var hd=document.querySelector('header');
  if(hd){ window.addEventListener('scroll',function(){
    hd.style.boxShadow = window.scrollY>10 ? '0 6px 24px rgba(10,25,41,.08)' : 'none';
  }); }
})();
'''

# ------------------------------------------------------------------ 404
def build_404():
    body = f'''<section class="phead"><div class="wrap">
  <h1>Page not found</h1>
  <div class="crumb"><a href="index.html">Home</a><span class="sep">/</span><span>404</span></div>
</div></section>
<section><div class="wrap" style="text-align:center;padding:40px 0 60px">
  <p style="font-size:17px;color:var(--muted);max-width:640px;margin:0 auto 28px">
    That page does not exist. Start from the catalogue, or tell us what you are looking for and we will point you to the right model.
  </p>
  <div class="hero-actions" style="justify-content:center">
    <a class="btn btn-grad" href="products.html">Browse all products</a>
    <a class="btn btn-ghost" href="index.html">Back to home</a>
  </div>
</div></section>
{cta()}
'''
    return page('404.html', 'Page Not Found | Focusee Company Limited',
                'The page you were looking for does not exist. Browse the Focusee portable air conditioner and dehumidifier catalogue instead.',
                body, '', jsonld=breadcrumb_ld([('Home', SITE), ('404', None)]))

# ------------------------------------------------------------------ sitemap / robots
def build_sitemap():
    today = time.strftime('%Y-%m-%d')
    urls = [('', '1.0', 'weekly'), ('products.html', '0.9', 'weekly'),
            ('about.html', '0.6', 'monthly'), ('contact.html', '0.7', 'monthly')]
    for c in CATS:
        urls.append((CAT_SLUG[c] + '.html', '0.7', 'weekly'))
    for p in DATA:
        urls.append((f'product-{p["slug"]}.html', '0.8', 'monthly'))
    for spec in APP_PAGES:
        urls.append((spec['path'], '0.6', 'monthly'))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, pri, cf in urls:
        out.append(f'  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod>'
                   f'<changefreq>{cf}</changefreq><priority>{pri}</priority></url>')
    out.append('</urlset>')
    open(ROOT + '/sitemap.xml', 'w', encoding='utf-8').write('\n'.join(out) + '\n')

def build_robots():
    txt = f'''User-agent: *
Allow: /

Sitemap: {SITE}sitemap.xml
'''
    open(ROOT + '/robots.txt', 'w', encoding='utf-8').write(txt)

# ------------------------------------------------------------------ OG cover image
def build_og_cover(force=False):
    """1200x630 social share card. Rebuild only when missing (or force=True)."""
    path = ROOT + '/assets/img/og-cover.jpg'
    if os.path.exists(path) and not force:
        return 'exists'
    try:
        from PIL import Image, ImageDraw, ImageFont
        W, H = 1200, 630
        im = Image.new('RGB', (W, H), (10, 58, 110))
        d = ImageDraw.Draw(im)
        # diagonal navy -> blue -> teal wash
        c0, c1 = (9, 46, 92), (16, 110, 150)
        for x in range(W):
            t = x / W
            col = tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))
            d.line([(x, 0), (x, H)], fill=col)
        # soft teal glow bottom-right
        glow = Image.new('L', (W, H), 0)
        gd = ImageDraw.Draw(glow)
        gd.ellipse([W - 520, H - 420, W + 180, H + 160], fill=70)
        glow = glow.filter(__import__('PIL.ImageFilter', fromlist=['ImageFilter']).GaussianBlur(90))
        im = Image.composite(Image.new('RGB', (W, H), (23, 185, 138)), im, glow)
        d = ImageDraw.Draw(im)

        def font(sz, bold=False):
            for p in ((r'C:\Windows\Fonts\seguisb.ttf' if bold else r'C:\Windows\Fonts\segoeui.ttf'),
                      (r'C:\Windows\Fonts\arialbd.ttf' if bold else r'C:\Windows\Fonts\arial.ttf')):
                if os.path.exists(p):
                    try: return ImageFont.truetype(p, sz)
                    except Exception: pass
            return ImageFont.load_default()

        def fit(text, maxw, start, bold=False, min_sz=20):
            sz = start
            while sz > min_sz:
                f = font(sz, bold)
                if d.textlength(text, font=f) <= maxw:
                    return f
                sz -= 2
            return font(min_sz, bold)

        # logo top-left
        try:
            lp = Image.open(ROOT + '/assets/img/logo.png').convert('RGB')
            lp.thumbnail((400, 88))
            im.paste(lp, (70, 62))
        except Exception:
            pass

        M = 70
        avail = W - M * 2
        f1 = fit('Portable Air Conditioners', avail, 68, bold=True)
        f2 = fit('Dehumidifiers  ·  Air Purifiers  ·  Accessories', avail, 34)
        f3 = fit('OEM & ODM manufacturer  ·  R290 / R32  ·  CE / GS  ·  MEPS', avail, 26)
        d.text((M, 214), 'Portable Air Conditioners', font=f1, fill=(255, 255, 255))
        d.text((M, 312), 'Dehumidifiers  ·  Air Purifiers  ·  Accessories', font=f2, fill=(158, 232, 208))
        d.text((M, 380), 'OEM & ODM manufacturer  ·  R290 / R32  ·  CE / GS  ·  MEPS', font=f3, fill=(203, 224, 244))
        # accent rule
        d.rectangle([M, 470, M + 110, 476], fill=(23, 185, 138))
        f4 = fit('Focusee Company Limited  ·  Zhongshan, China  ·  focuseetech.com', avail, 26)
        d.text((M, 508), 'Focusee Company Limited  ·  Zhongshan, China  ·  focuseetech.com',
               font=f4, fill=(255, 255, 255))
        im.save(path, 'JPEG', quality=88, optimize=True)
        return 'created'
    except Exception as e:
        print('og cover skipped:', e)
        return 'skipped'

# ------------------------------------------------------------------ run
os.makedirs(ROOT + '/assets/js', exist_ok=True)
load_dims()            # real image sizes -> correct width/height attributes
ensure_webp()          # must run before any page is rendered
save_dims()
open(ROOT + '/assets/js/site.js','w',encoding='utf-8').write(JS)
files = [build_index(), build_products(), build_about(), build_contact(), build_404()]
for c in CATS:
    f = build_category(c)
    if f: files.append(f)
for p in DATA:
    files.append(build_detail(p))
for spec in APP_PAGES:
    files.append(build_app(spec))
build_sitemap(); build_robots()
print('og cover:', build_og_cover())
print('pages written:', len(files))
