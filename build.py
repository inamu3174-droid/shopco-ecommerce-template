#!/usr/bin/env python3
"""Generates the static SHOP.CO pages into ./site. Run: python3 build.py"""
import html
from pathlib import Path

OUT = Path(__file__).parent / "site"
esc = html.escape

# ---------------------------------------------------------------- icons
def svg(path, cls="icon", vb="0 0 24 24", fill="none", stroke="currentColor", sw="1.8", extra=""):
    return (f'<svg class="{cls}" viewBox="{vb}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" {extra}>{path}</svg>')

I = {
    "search": svg('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>'),
    "cart": svg('<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.6 12.2a1 1 0 0 0 1 .8h8.8a1 1 0 0 0 1-.8L20 7H6"/>'),
    "user": svg('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="10" r="3"/><path d="M6.2 18.2c1.4-2.2 3.4-3.2 5.8-3.2s4.4 1 5.8 3.2"/>'),
    "menu": svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "close": svg('<path d="M6 6l12 12M18 6 6 18"/>', "icon-xs"),
    "chev": svg('<path d="m6 9 6 6 6-6"/>', "icon-sm chev"),
    "chev_f": svg('<path d="m6 9 6 6 6-6"/>', "icon-sm"),
    "mail": svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
    "tag": svg('<path d="M3 12V4h8l10 10-8 8L3 12Z"/><circle cx="7.5" cy="8.5" r="1.2"/>'),
    "trash": svg('<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13M10 11v6M14 11v6"/>', "icon", fill="none", stroke="currentColor"),
    "minus": svg('<path d="M5 12h14"/>', "icon-xs"),
    "plus": svg('<path d="M12 5v14M5 12h14"/>', "icon-xs"),
    "arrow_r": svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "arrow_l": svg('<path d="M19 12H5M11 6l-6 6 6 6"/>', "icon-xs"),
    "arrow_rr": svg('<path d="M5 12h14M13 6l6 6-6 6"/>', "icon-xs"),
    "check": svg('<path d="m5 12.5 4.5 4.5L19 7.5"/>', "", sw="2.4"),
    "filter": svg('<path d="M4 8h10M18 8h2M4 16h2M10 16h10"/><circle cx="16" cy="8" r="2"/><circle cx="8" cy="16" r="2"/>'),
    "dots": svg('<circle cx="5" cy="12" r="1.5" fill="currentColor"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/><circle cx="19" cy="12" r="1.5" fill="currentColor"/>', stroke="none"),
    "verified": svg('<circle cx="12" cy="12" r="10" fill="#01ab31" stroke="none"/><path d="m7.5 12.3 3 3 6-6.3" stroke="#fff" stroke-width="2"/>'),
    "twitter": svg('<path d="M22 5.9c-.7.3-1.5.6-2.3.7.8-.5 1.5-1.300 1.800-2.300-.8.5-1.700.8-2.600 1a4 4 0 0 0-6.900 3.600A11.400 11.400 0 0 1 3.700 4.700a4 4 0 0 0 1.200 5.400c-.7 0-1.300-.2-1.800-.5 0 2 1.400 3.600 3.200 4-.6.2-1.200.2-1.800.1.500 1.600 2 2.800 3.700 2.800A8.100 8.100 0 0 1 2 18.200 11.400 11.400 0 0 0 8.200 20c7.500 0 11.700-6.300 11.400-12 .8-.6 1.500-1.300 2-2.100Z" fill="currentColor" stroke="none"/>', "icon-sm"),
    "facebook": svg('<path d="M14 8h2.5V4.500H14a4 4 0 0 0-4 4V11H7.500v3.500H10V21h3.500v-6.500H16L16.500 11h-3V8.800c0-.5.200-.8.800-.8Z" fill="currentColor" stroke="none"/>', "icon-sm"),
    "instagram": svg('<rect x="3.500" y="3.500" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r=".9" fill="currentColor"/>', "icon-sm"),
    "github": svg('<path d="M12 2.500a9.500 9.500 0 0 0-3 18.500c.5.1.7-.2.7-.5v-1.800c-2.700.6-3.300-1.200-3.300-1.200-.4-1.100-1.100-1.400-1.100-1.400-.9-.6.100-.6.100-.6 1 .1 1.500 1 1.500 1 .9 1.500 2.300 1.100 2.900.8.1-.6.300-1.100.6-1.300-2.100-.2-4.300-1.100-4.300-4.700 0-1 .4-1.900 1-2.500-.1-.2-.4-1.200.1-2.500 0 0 .8-.3 2.600 1a9 9 0 0 1 4.800 0c1.800-1.200 2.600-1 2.600-1 .5 1.300.2 2.300.1 2.500.6.700 1 1.500 1 2.500 0 3.600-2.200 4.400-4.300 4.600.3.300.6.900.6 1.700V20c0 .3.200.6.700.5A9.500 9.500 0 0 0 12 2.500Z" fill="currentColor" stroke="none"/>', "icon-sm"),
    "spark": '<svg class="spark {c}" viewBox="0 0 100 100" aria-hidden="true"><path fill="currentColor" d="M50 0C52 28 72 48 100 50 72 52 52 72 50 100 48 72 28 52 0 50 28 48 48 28 50 0Z"/></svg>',
}
STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#ffc633" d="{d}"/></svg>'
STAR_FULL = "M12 1.5l3.1 6.800 7.400.8-5.500 5 1.600 7.300L12 17.600 5.400 22.400 7 15.100 1.500 10.100l7.400-.8L12 1.500Z"
STAR_HALF = "M12 1.500v16.100L5.400 22.400 7 15.100 1.500 10.100l7.400-.8L12 1.500Z"

def stars(r):
    full = int(r)
    out = STAR.format(d=STAR_FULL) * full
    if r - full >= .5:
        out += STAR.format(d=STAR_HALF)
    return f'<span class="stars" role="img" aria-label="{r:g} out of 5 stars">{out}</span>'

def rating(r):
    return f'<div class="rating">{stars(r)}<span>{r:.1f}/<span class="of">5</span></span></div>'

def slug(name):
    return "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-").replace("--", "-")

def img(src, alt, **kw):
    attrs = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
    return f'<img src="{src}" alt="{esc(alt)}" loading="lazy" {attrs}>'

def product_img(name):
    return f"assets/img/products/{slug(name)}.png"

# ---------------------------------------------------------------- partials
def head(title, desc, extra_body_class=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="preconnect" href="https://api.fontshare.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Black&display=swap">
<link rel="stylesheet" href="css/style.css">
</head>
<body class="{extra_body_class}">
"""

def header(active=""):
    return f"""<div class="topbar" id="topbar">
  <p>Sign up and get 20% off to your first order. <a href="#newsletter">Sign Up Now</a></p>
  <button class="close" type="button" aria-label="Close banner" data-close-banner>{I['close']}</button>
</div>
<header class="header" id="header">
  <div class="wrap">
    <button class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" data-menu>{I['menu']}</button>
    <a class="logo" href="index.html">SHOP.CO</a>
    <nav class="nav" id="nav" aria-label="Main">
      <a href="category.html">Shop {I['chev_f'].replace('icon-sm','icon-sm')}</a>
      <a href="category.html?sale=1">On Sale</a>
      <a href="category.html?new=1">New Arrivals</a>
      <a href="index.html#brands">Brands</a>
    </nav>
    <form class="search" role="search" action="category.html" method="get">
      {I['search']}
      <input type="search" name="q" placeholder="Search for products..." aria-label="Search for products">
    </form>
    <div class="header-icons">
      <button class="search-btn" type="button" aria-label="Search" data-search-toggle>{I['search']}</button>
      <a class="cart-link" href="cart.html" aria-label="Cart">{I['cart']}<span class="cart-count" data-cart-count></span></a>
      <a href="#" aria-label="Account">{I['user']}</a>
    </div>
  </div>
</header>
"""

def newsletter():
    return f"""<section class="newsletter" id="newsletter">
  <div class="wrap">
    <div class="news-box">
      <h2 class="display">Stay upto date about our latest offers</h2>
      <form class="news-form" data-newsletter novalidate>
        <label>{I['mail']}<input type="email" name="email" placeholder="Enter your email address" aria-label="Email address" required></label>
        <button type="submit">Subscribe to Newsletter</button>
        <p class="news-msg" role="status"></p>
      </form>
    </div>
  </div>
</section>"""

FOOT_COLS = {
    "Company": ["About", "Features", "Works", "Career"],
    "Help": ["Customer Support", "Delivery Details", "Terms & Conditions", "Privacy Policy"],
    "FAQ": ["Account", "Manage Deliveries", "Orders", "Payments"],
    "Resources": ["Free eBooks", "Development Tutorial", "How to - Blog", "Youtube Playlist"],
}

def footer():
    cols = "".join(
        f'<div><h4>{k}</h4><ul>' + "".join(f'<li><a href="#">{v}</a></li>' for v in vs) + "</ul></div>"
        for k, vs in FOOT_COLS.items())
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer-main">
      <div class="about">
        <a class="logo" href="index.html">SHOP.CO</a>
        <p>We have clothes that suits your style and which you’re proud to wear. From women to men.</p>
        <div class="social">
          <a href="#" aria-label="Twitter">{I['twitter']}</a>
          <a href="#" aria-label="Facebook">{I['facebook']}</a>
          <a href="#" aria-label="Instagram">{I['instagram']}</a>
          <a href="#" aria-label="GitHub">{I['github']}</a>
        </div>
      </div>
      {cols}
    </div>
    <div class="footer-bottom">
      <span>Shop.co © 2000-2023, All Rights Reserved</span>
      <div class="pay" aria-label="Accepted payments">
        <span class="visa">VISA</span><span class="mc">MC</span><span class="pp">PayPal</span><span>Pay</span><span class="gp">G Pay</span>
      </div>
    </div>
  </div>
</footer>
<script src="js/main.js"></script>
</body>
</html>
"""

def card(p, href="product.html"):
    price = f'<span>${p["price"]}</span>'
    if p.get("old"):
        pct = p.get("off") or round((1 - p["price"] / p["old"]) * 100)
        price += f'<span class="old">${p["old"]}</span><span class="badge">-{pct}%</span>'
    return f"""<article class="card" data-name="{esc(p['name'])}" data-price="{p['price']}" data-rating="{p['rating']}">
  <a class="thumb" href="{href}" aria-label="{esc(p['name'])}">{img(product_img(p['name']), p['name'], onerror="this.remove()")}</a>
  <h3><a href="{href}">{esc(p['name'])}</a></h3>
  {rating(p['rating'])}
  <div class="price">{price}</div>
</article>"""

# ---------------------------------------------------------------- data
NEW = [
    dict(name="T-shirt with Tape Details", price=120, rating=4.5),
    dict(name="Skinny Fit Jeans", price=240, off=20, old=260, rating=3.5),
    dict(name="Checkered Shirt", price=180, rating=4.5),
    dict(name="Sleeve Striped T-shirt", price=130, off=30, old=160, rating=4.5),
]
TOP = [
    dict(name="Vertical Striped Shirt", price=212, off=20, old=232, rating=5.0),
    dict(name="Courage Graphic T-shirt", price=145, rating=4.0),
    dict(name="Loose Fit Bermuda Shorts", price=80, rating=3.0),
    dict(name="Faded Skinny Jeans", price=210, rating=4.5),
]
CAT = [
    dict(name="Gradient Graphic T-shirt", price=145, rating=3.5),
    dict(name="Polo with Tipping Details", price=180, rating=4.5),
    dict(name="Black Striped T-shirt", price=120, off=30, old=150, rating=5.0),
    dict(name="Skinny Fit Jeans", price=240, off=20, old=260, rating=3.5),
    dict(name="Checkered Shirt", price=180, rating=4.5),
    dict(name="Sleeve Striped T-shirt", price=130, off=30, old=160, rating=4.5),
    dict(name="Vertical Striped Shirt", price=212, off=20, old=232, rating=5.0),
    dict(name="Courage Graphic T-shirt", price=145, rating=4.0),
    dict(name="Loose Fit Bermuda Shorts", price=80, rating=3.0),
]
RELATED = [
    dict(name="Polo with Contrast Trims", price=212, off=20, old=242, rating=4.0),
    dict(name="Gradient Graphic T-shirt", price=145, rating=3.5),
    dict(name="Polo with Tipping Details", price=180, rating=4.5),
    dict(name="Black Striped T-shirt", price=120, off=30, old=150, rating=5.0),
]
HAPPY = [
    ("Sarah M.", "“I'm blown away by the quality and style of the clothes I received from Shop.co. From casual wear to elegant dresses, every piece I've bought has exceeded my expectations.”"),
    ("Alex K.", "“Finding clothes that align with my personal style used to be a challenge until I discovered Shop.co. The range of options they offer is truly remarkable, catering to a variety of tastes and occasions.”"),
    ("James L.", "“As someone who's always on the lookout for unique fashion pieces, I'm thrilled to have stumbled upon Shop.co. The selection of clothes is not only diverse but also on-point with the latest trends.”"),
    ("Mooen", "“Shop.co has become my go-to for everyday outfits. The quality is consistent, delivery is quick and the pieces always fit as expected.”"),
]
REVIEWS = [
    ("Samantha D.", 4.5, "“I absolutely love this t-shirt! The design is unique and the fabric feels so comfortable. As a fellow designer, I appreciate the attention to detail. It's become my favorite go-to shirt.”", "August 14, 2023"),
    ("Alex M.", 4, "“The t-shirt exceeded my expectations! The colors are vibrant and the print quality is top-notch. Being a UI/UX designer myself, I'm quite picky about aesthetics, and this t-shirt definitely gets a thumbs up from me.”", "August 15, 2023"),
    ("Ethan R.", 3.5, "“This t-shirt is a must-have for anyone who appreciates good design. The minimalistic yet stylish pattern caught my eye, and the fit is perfect. I can see the designer's touch in every aspect of this shirt.”", "August 16, 2023"),
    ("Olivia P.", 4, "“As a UI/UX enthusiast, I value simplicity and functionality. This t-shirt not only represents those principles but also feels great to wear. It's evident that the designer poured their creativity into making this t-shirt stand out.”", "August 17, 2023"),
    ("Liam K.", 4, "“This t-shirt is a fusion of comfort and creativity. The fabric is soft, and the design speaks volumes about the designer's skill. It's like wearing a piece of art that reflects my passion for both design and fashion.”", "August 18, 2023"),
    ("Ava H.", 4.5, "“I'm not just wearing a t-shirt; I'm wearing a piece of design philosophy. The intricate details and thoughtful layout of the design make this shirt a conversation starter.”", "August 19, 2023"),
]

def review_card(name, r, text, date, menu=True):
    dots = f'<button type="button" aria-label="More options" class="muted">{I["dots"]}</button>' if menu else ""
    return f"""<article class="review">
  <div class="head">{stars(r)}{dots}</div>
  <div class="who">{esc(name)}{I['verified']}</div>
  <p>{esc(text)}</p>
  {f'<time>Posted on {date}</time>' if date else ''}
</article>"""

# ---------------------------------------------------------------- pages
def page_home():
    return head("SHOP.CO — Find clothes that match your style", "Browse our diverse range of garments designed to bring out your individuality.") + header() + f"""
<main>
<section class="hero">
  <div class="wrap">
    <div>
      <h1 class="display">Find clothes that matches your style</h1>
      <p class="lead">Browse through our diverse range of meticulously crafted garments, designed to bring out your individuality and cater to your sense of style.</p>
      <a class="btn btn-dark" href="category.html">Shop Now</a>
      <div class="stats">
        <div><strong>200+</strong><span>International Brands</span></div><div class="sep"></div>
        <div><strong>2,000+</strong><span>High-Quality Products</span></div><div class="sep"></div>
        <div><strong>30,000+</strong><span>Happy Customers</span></div>
      </div>
    </div>
    <div class="hero-art">
      {I['spark'].format(c='s1')}{I['spark'].format(c='s2')}
      {img('assets/img/hero.png', 'Two models wearing the latest collection', onerror="this.remove()")}
    </div>
  </div>
</section>
<div class="brands" id="brands"><div class="wrap">
  <span class="b-versace">VERSACE</span><span class="b-zara">ZARA</span><span class="b-gucci">GUCCI</span><span class="b-prada">PRADA</span><span class="b-ck">Calvin Klein</span>
</div></div>

<section class="section"><div class="wrap">
  <h2 class="display section-title">New Arrivals</h2>
  <div class="grid-4">{''.join(card(p) for p in NEW)}</div>
  <div class="section-foot"><a class="btn btn-outline" href="category.html?new=1">View All</a></div>
  <hr class="divider">
</div></section>

<section class="section" style="padding-top:64px"><div class="wrap">
  <h2 class="display section-title">Top Selling</h2>
  <div class="grid-4">{''.join(card(p) for p in TOP)}</div>
  <div class="section-foot"><a class="btn btn-outline" href="category.html">View All</a></div>
</div></section>

<section class="wrap"><div class="dress">
  <h2 class="display section-title">Browse by dress style</h2>
  <div class="dress-grid">
    <a href="category.html?style=casual"><span>Casual</span>{img('assets/img/style-casual.png','Casual style', onerror="this.remove()")}</a>
    <a href="category.html?style=formal"><span>Formal</span>{img('assets/img/style-formal.png','Formal style', onerror="this.remove()")}</a>
    <a href="category.html?style=party"><span>Party</span>{img('assets/img/style-party.png','Party style', onerror="this.remove()")}</a>
    <a href="category.html?style=gym"><span>Gym</span>{img('assets/img/style-gym.png','Gym style', onerror="this.remove()")}</a>
  </div>
</div></section>

<section class="testimonials"><div class="wrap">
  <div class="t-head">
    <h2 class="display">Our happy customers</h2>
    <div class="t-arrows">
      <button type="button" aria-label="Previous" data-slide="-1">{I['arrow_l']}</button>
      <button type="button" aria-label="Next" data-slide="1">{I['arrow_rr']}</button>
    </div>
  </div>
  <div class="t-track" data-track>
    {''.join(review_card(n, 5, t, None, menu=False) for n, t in HAPPY)}
  </div>
</div></section>
</main>
""" + newsletter() + footer()


def page_category():
    colors = [("#00c12b", "Green"), ("#f50606", "Red"), ("#f5dd06", "Yellow"), ("#f57906", "Orange"), ("#06caf5", "Cyan"),
              ("#063af5", "Blue"), ("#7d06f5", "Purple"), ("#f506a4", "Pink"), ("#ffffff", "White"), ("#000000", "Black")]
    sw = "".join(
        f'<button type="button" class="swatch{" light" if c == "#ffffff" else ""}{" on" if n == "Blue" else ""}" '
        f'style="background:{c}" aria-label="{n}" aria-pressed="{"true" if n == "Blue" else "false"}">{I["check"]}</button>'
        for c, n in colors)
    sizes = ["XX-Small", "X-Small", "Small", "Medium", "Large", "X-Large", "XX-Large", "3X-Large", "4X-Large"]
    chips = "".join(f'<button type="button" class="chip{" on" if s == "Large" else ""}" aria-pressed="{"true" if s == "Large" else "false"}">{s}</button>' for s in sizes)
    def links(items):
        return '<ul class="f-links">' + "".join(f'<li><a href="#">{i}{I["chev"].replace("icon-sm chev","icon-sm")}</a></li>' for i in items) + "</ul>"
    def group(title, body, closed=False):
        return (f'<div class="f-group{" closed" if closed else ""}"><button class="f-title" type="button" aria-expanded="{"false" if closed else "true"}">{title}{I["chev_f"]}</button>'
                f'<div class="f-body">{body}</div></div>')
    pages = "".join(f'<a href="#"{" class=on" if i == 1 else ""}>{i}</a>' for i in (1, 2, 3)) + '<a href="#">…</a>' + "".join(f'<a href="#">{i}</a>' for i in (8, 9, 10))
    return head("Casual — SHOP.CO", "Browse casual clothing.") + header() + f"""
<main class="wrap">
  <ol class="breadcrumb"><li>Home {I['chev']}</li><li>Casual</li></ol>
  <div class="cat-layout" style="margin-top:28px">
    <aside class="filters" id="filters" aria-label="Filters">
      <div class="filters-head"><span>Filters</span>
        <span class="muted">{I['filter']}</span>
        <button class="close-filters" type="button" aria-label="Close filters" data-close-filters>{I['close']}</button></div>
      <div class="f-group" style="padding-top:24px"><div class="f-body" style="margin:0">{links(['T-shirts','Shorts','Shirts','Hoodie','Jeans'])}</div></div>
      {group('Price', '<div class="range" data-range><div class="track"></div><div class="fill"></div><input type="range" min="0" max="500" value="50" aria-label="Minimum price"><input type="range" min="0" max="500" value="200" aria-label="Maximum price"></div><div class="range-labels"><span data-min>$50</span><span data-max>$200</span></div>')}
      {group('Colors', f'<div class="swatches">{sw}</div>')}
      {group('Size', f'<div class="chips">{chips}</div>')}
      {group('Dress Style', links(['Casual','Formal','Party','Gym']))}
      <button class="btn btn-dark btn-block btn-sm" type="button" data-apply-filter>Apply Filter</button>
    </aside>
    <section aria-label="Products">
      <div class="cat-top">
        <h1 class="page-title">Casual</h1>
        <div class="tools">
          <span>Showing 1-10 of 100 Products</span>
          <span class="sort">Sort by: <select aria-label="Sort products" data-sort>
            <option value="popular">Most Popular</option><option value="low">Price: Low to High</option>
            <option value="high">Price: High to Low</option><option value="rating">Top Rated</option></select></span>
          <button class="filter-toggle" type="button" aria-label="Open filters" data-open-filters>{I['filter']}</button>
        </div>
      </div>
      <div class="cat-grid" data-grid>{''.join(card(p) for p in CAT)}</div>
      <nav class="pagination" aria-label="Pagination">
        <a class="page-btn" href="#">{I['arrow_l']}<span>Previous</span></a>
        <div class="page-nums">{pages}</div>
        <a class="page-btn" href="#"><span>Next</span>{I['arrow_rr']}</a>
      </nav>
    </section>
  </div>
</main>
<div class="scrim" data-scrim></div>
""" + newsletter() + footer()


def page_product():
    name = "One Life Graphic T-shirt"
    cols = [("#4f4631", "Olive"), ("#314f4a", "Green"), ("#31344f", "Navy")]
    sw = "".join(f'<button type="button" class="swatch{" on" if i == 0 else ""}" style="background:{c}" aria-label="{n}" aria-pressed="{"true" if i == 0 else "false"}" data-color="{n}">{I["check"]}</button>' for i, (c, n) in enumerate(cols))
    sizes = "".join(f'<button type="button" class="chip lg{" on" if s == "Large" else ""}" aria-pressed="{"true" if s == "Large" else "false"}">{s}</button>' for s in ["Small", "Medium", "Large", "X-Large"])
    thumbs = "".join(
        f'<button type="button" class="{"on" if i == 1 else ""}" data-thumb="{i}" aria-label="View image {i}">{img(f"assets/img/products/one-life-graphic-t-shirt-{i}.png", f"{name} view {i}", onerror="this.remove()")}</button>'
        for i in (1, 2, 3))
    revs = "".join(review_card(*r) for r in REVIEWS)
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in [
        ("How does the t-shirt fit?", "It has a regular fit. If you are between sizes, we recommend sizing up."),
        ("How should I wash it?", "Machine wash cold with similar colors and tumble dry low to keep the print looking fresh."),
        ("What is the return policy?", "You can return unworn items within 30 days of delivery for a full refund."),
    ])
    return head(f"{name} — SHOP.CO", "Graphic t-shirt crafted from a soft and breathable fabric.") + header() + f"""
<main class="wrap" data-product data-id="one-life-graphic-t-shirt" data-name="{name}" data-price="260">
  <ol class="breadcrumb"><li>Home {I['chev']}</li><li>Shop {I['chev']}</li><li>Men {I['chev']}</li><li>T-shirts</li></ol>
  <div class="pdp">
    <div class="thumbs">{thumbs}</div>
    <div class="main-img">{img('assets/img/products/one-life-graphic-t-shirt-1.png', name, onerror="this.remove()", id="main-img")}</div>
    <div class="info">
      <h1 class="display">{name}</h1>
      <div class="rating">{stars(4.5)}<span>4.5/<span class="of">5</span></span></div>
      <div class="price"><span>$260</span><span class="old">$300</span><span class="badge">-40%</span></div>
      <p class="desc">This graphic t-shirt which is perfect for any occasion. Crafted from a soft and breathable fabric, it offers superior comfort and style.</p>
      <div class="opt"><p>Select Colors</p><div class="swatches" data-colors>{sw}</div></div>
      <div class="opt"><p>Choose Size</p><div class="chips" data-sizes>{sizes}</div></div>
      <div class="buy">
        <div class="qty" data-qty><button type="button" aria-label="Decrease quantity" data-dec>{I['minus']}</button><span data-qty-val>1</span><button type="button" aria-label="Increase quantity" data-inc>{I['plus']}</button></div>
        <button class="btn btn-dark" type="button" data-add-to-cart>Add to Cart</button>
      </div>
      <p class="news-msg" role="status" data-add-msg style="margin-top:12px"></p>
    </div>
  </div>

  <div class="tabs" role="tablist">
    <button type="button" role="tab" data-tab="details">Product Details</button>
    <button type="button" role="tab" data-tab="reviews" class="on">Rating & Reviews</button>
    <button type="button" role="tab" data-tab="faq">FAQs</button>
  </div>
  <div class="tab-panel" id="tab-details" hidden>
    <ul class="detail-list"><li>Soft, breathable cotton blend</li><li>Regular fit, crew neck</li><li>Machine washable</li><li>Graphic print on the front</li></ul>
  </div>
  <div class="tab-panel" id="tab-reviews">
    <div class="rev-head">
      <h2>All Reviews <small>(451)</small></h2>
      <div class="rev-tools">
        <button class="pill round" type="button" aria-label="Filter reviews">{I['filter']}</button>
        <button class="pill" type="button">Latest {I['chev_f']}</button>
        <button class="pill dark" type="button">Write a Review</button>
      </div>
    </div>
    <div class="rev-grid">{revs}</div>
    <div class="rev-more"><button class="btn btn-outline" type="button">Load More Reviews</button></div>
  </div>
  <div class="tab-panel faq" id="tab-faq" hidden>{faq}</div>

  <section class="related">
    <h2 class="display">You might also like</h2>
    <div class="grid-4">{''.join(card(p) for p in RELATED)}</div>
  </section>
</main>
""" + newsletter() + footer()


def page_cart():
    return head("Your cart — SHOP.CO", "Review the items in your cart.") + header() + f"""
<main class="wrap">
  <ol class="breadcrumb"><li>Home {I['chev']}</li><li>Cart</li></ol>
  <h1 class="display cart-title">Your cart</h1>
  <div class="cart-layout">
    <section class="panel" id="cart-items" aria-label="Cart items"></section>
    <aside class="panel summary" aria-label="Order summary">
      <h2>Order Summary</h2>
      <div class="sum-rows">
        <div class="sum-row"><span>Subtotal</span><strong data-subtotal>$0</strong></div>
        <div class="sum-row disc"><span>Discount (-20%)</span><strong data-discount>-$0</strong></div>
        <div class="sum-row"><span>Delivery Fee</span><strong data-delivery>$0</strong></div>
      </div>
      <div class="sum-total"><span>Total</span><strong data-total>$0</strong></div>
      <form class="promo" data-promo novalidate>
        <label>{I['tag']}<input type="text" name="code" placeholder="Add promo code" aria-label="Promo code"></label>
        <button type="submit">Apply</button>
      </form>
      <p class="promo-msg" role="status" data-promo-msg></p>
      <a class="btn btn-dark btn-block" href="#" data-checkout>Go to Checkout {I['arrow_r']}</a>
    </aside>
  </div>
</main>
""" + newsletter() + footer()


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    pages = {"index.html": page_home, "category.html": page_category, "product.html": page_product, "cart.html": page_cart}
    for fn, f in pages.items():
        (OUT / fn).write_text(f(), encoding="utf-8")
        print("wrote", fn)
