# -*- coding: utf-8 -*-
"""FOCUSEE portable air conditioner site generator."""
import json, os, re, html, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'products.json'), encoding='utf-8'))

COMPANY   = 'Focusee Company Limited'
ADDRESS   = 'Factory House B, Changmingshui Industrial Park, Changyi Road, Wuguishan, Zhongshan City, Guangdong Province, China 528458'
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
<meta name="keywords" content="portable air conditioner, dehumidifier manufacturer, OEM portable AC, R290 air conditioner, portable AC supplier China, Focusee">
<link rel="icon" href="{{R}}assets/img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{R}}assets/css/style.css">
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

def page(fname, title, desc, body, active='', r=''):
    htmlout = HEAD_T.replace('{{T}}', esc(title)).replace('{{D}}', esc(desc)).replace('{{R}}', r)
    htmlout += header(active, r) + body + footer(r) + FOOT_T.replace('{{R}}', r)
    open(os.path.join(ROOT, fname), 'w', encoding='utf-8').write(htmlout)
    return fname

def card(p, n, r=''):
    g = gallery(p)
    img = g[0] if g else 'logo.png'
    txt = p.get('bullets', [])
    sub = txt[0] if txt else p.get('desc', '')[:70]
    return f'''<a class="card" href="{r}product-{slug(p['name'])}.html">
  <div class="card-img"><span class="card-cat">{esc(p['cat'].replace('Portable Air Con.','Portable AC'))}</span>
    <img src="{r}assets/img/{img}" alt="{esc(p['name'])}" loading="lazy"></div>
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
    <img src="assets/img/{DATA[3]['g'][0] if len(DATA)>3 and DATA[3]['g'] else 'logo.png'}" alt="FOCUSEE portable air conditioner">
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
      <div class="frame"><img src="assets/img/{DATA[2]['g'][0]}" alt="Focusee portable air conditioner"></div>
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
    return page('index.html', 'Focusee Company Limited | Portable Air Conditioners, Dehumidifiers & Air Purifiers',
                'Focusee Company Limited manufactures portable air conditioners, dehumidifiers, air purifiers and accessories for importers and retail brands. OEM & ODM, R290 / R32, CE / GS certified.',
                body, 'home')

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
    return page('products.html', f'Products | {len(DATA)} Portable Air Conditioners & Dehumidifiers — Focusee',
                f'Browse {len(DATA)} portable air conditioners, dehumidifiers, air purifiers and accessories from Focusee Company Limited. Specifications, MOQ and container loading data included.',
                body, 'products')

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
    thumbs = ''.join(f'<button class="{"on" if i==0 else ""}" data-src="assets/img/{im}"><img src="assets/img/{im}" alt="{esc(p["name"])} view {i+1}"></button>' for i, im in enumerate(g))
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
    <div class="pd-main"><img id="pdmain" src="assets/img/{main}" alt="{esc(p['name'])}"></div>
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
    return page(f'product-{p["slug"]}.html',
                f'{p["name"]} | {p["cat"]} &mdash; Focusee Company Limited',
                f'{p["name"]} {p["cat"]} from Focusee Company Limited. {p["desc"]}. Specifications, MOQ and container loading data.',
                body)

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
      <div class="frame"><img src="assets/img/{DATA[0]['g'][0]}" alt="Focusee portable air conditioner"></div>
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
                body, 'about')

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
    return page('contact.html', 'Contact | Focusee Company Limited — Portable Air Conditioner Manufacturer',
                'Contact Focusee Company Limited for portable air conditioner, dehumidifier and air purifier enquiries. Carol Luo, General Manager and Robert Luo, Marketing Manager.',
                body, 'contact')

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

  /* product gallery */
  var m=document.getElementById('pdmain');
  if(m){
    document.querySelectorAll('.pd-thumbs button').forEach(function(b){
      b.addEventListener('click',function(){
        document.querySelectorAll('.pd-thumbs button').forEach(function(x){x.classList.remove('on');});
        b.classList.add('on');
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

# ------------------------------------------------------------------ run
os.makedirs(ROOT + '/assets/js', exist_ok=True)
open(ROOT + '/assets/js/site.js','w',encoding='utf-8').write(JS)
files = [build_index(), build_products(), build_about(), build_contact()]
for p in DATA:
    files.append(build_detail(p))
print('pages written:', len(files))
