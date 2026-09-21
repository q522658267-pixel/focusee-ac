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

# ------------------------------------------------------------------ helpers
def esc(s): return html.escape(str(s if s is not None else ''))
def esca(s):
    """Escape for use inside a double-quoted HTML attribute (keeps apostrophes literal)."""
    return (str(s if s is not None else '').replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))
def slug(s): return re.sub(r'[^a-z0-9]+','-',(s or '').lower()).strip('-') or 'product'
LOGO = '68ca51498f2ea.png'
def gallery(p):
    g=[]
    for im in ([p.get('thumb')] + p.get('thumbs',[])):
        if not im or im == LOGO or im in g: continue
        g.append(im)
    return g[:6]

HEAD_T = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{T}}</title>
<meta name="description" content="{{D}}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="Focusee Company Limited">
<link rel="canonical" href="{{CANON}}">
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
    subs = ''.join(f'<a href="{r}products.html#{CAT_SLUG[c]}">{esc(c)}</a>' for c in CATS)
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
        {''.join(f'<li><a href="{r}products.html#{CAT_SLUG[c]}">{esc(c)}</a></li>' for c in CATS)}
        <li><a href="{r}products.html">All Products</a></li>
      </ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="{r}about.html">About Us</a></li>
        <li><a href="{r}about.html#green">Sustainability</a></li>
        <li><a href="{r}contact.html">Contact</a></li>
        <li><a href="{r}contact.html">Request Catalogue</a></li>
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
        els.append({"@type": "ListItem", "position": i + 1,
                    "name": it["name"], "url": SITE + it["url"]})
    return ld({"@context": "https://schema.org", "@type": "ItemList",
               "name": name, "numberOfItems": len(els), "itemListElement": els})

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

def page(fname, title, desc, body, active='', r='', canon=None, ogt='website', ogi=None, jsonld='', path=None):
    """path: URL path relative to SITE, e.g. 'products.html'. Used for canonical."""
    if canon is None:
        canon = SITE + (path or fname)
    h = (HEAD_T.replace('{{T}}', esca(title))
               .replace('{{D}}', esca(desc))
               .replace('{{R}}', r)
               .replace('{{CANON}}', esca(canon))
               .replace('{{OGT}}', ogt)
               .replace('{{OGI}}', esca(ogi or OG_IMAGE))
               .replace('{{JSONLD}}', jsonld))
    htmlout = h + header(active, r) + body + footer(r) + FOOT_T.replace('{{R}}', r)
    open(os.path.join(ROOT, fname), 'w', encoding='utf-8').write(htmlout)
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
        cat_tiles += f'''<a class="cat-tile" href="products.html#{CAT_SLUG[c]}">
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
    ]
    faq_html = ''.join(
        f'<details{" open" if i == 0 else ""}><summary>{q}</summary><div class="faq-a"><p>{a}</p></div></details>'
        for i, (q, a) in enumerate(faqs))
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
                               (p['name'], None)]))
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
    for p in DATA:
        urls.append((f'product-{p["slug"]}.html', '0.8', 'monthly'))
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
for p in DATA:
    files.append(build_detail(p))
build_sitemap(); build_robots()
print('og cover:', build_og_cover())
print('pages written:', len(files))
