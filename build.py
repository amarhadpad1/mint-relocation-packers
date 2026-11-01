#!/usr/bin/env python3
"""Builds the Mint Relocation Packers demo site.  Usage:  python3 build.py
Edit site_data.py for phone numbers / addresses, then run this again."""
import os, shutil, json, html, urllib.parse
from site_data import *

OUT = os.environ.get("OUT", "site")
HERE = os.path.dirname(os.path.abspath(__file__))
esc = html.escape

ICON = {
 "phone":"M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24c1.12.37 2.33.57 3.57.57a1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1.02l-2.2 2.2z",
 "mail":"M20 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V6a2 2 0 00-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z",
 "pin":"M12 2a7 7 0 00-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 00-7-7zm0 9.5A2.5 2.5 0 119.5 9 2.5 2.5 0 0112 11.5z",
 "search":"M15.5 14h-.79l-.28-.27A6.47 6.47 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z",
 "up":"M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z",
 "clock":"M12 2a10 10 0 100 20 10 10 0 000-20zm.5 5v5.25l4.5 2.67-.75 1.23L11 13V7h1.5z",
 "fb":"M13 22v-8h3l.5-4H13V8c0-1.1.3-2 2-2h1.6V2.4C16.3 2.3 15.3 2.2 14.2 2.2 11.7 2.2 10 3.7 10 6.5V10H7v4h3v8h3z",
 "wa":"M12 2a10 10 0 00-8.6 15.1L2 22l5-1.3A10 10 0 1012 2zm5.2 14c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.2-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.2.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.3 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.2 1.4 2.5 1.5.3.1.4.1.6-.1l.8-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.8-.1 1.5z",
 "truck":"M20 8h-3V4H3a2 2 0 00-2 2v11h2a3 3 0 006 0h6a3 3 0 006 0h2v-5l-3-4zM6 18.5a1.5 1.5 0 110-3 1.5 1.5 0 010 3zm12 0a1.5 1.5 0 110-3 1.5 1.5 0 010 3zM17 12V9.5h2.5L21.46 12H17z",
 "box":"M21 8l-9-5-9 5v8l9 5 9-5V8zm-9-2.7L17.7 8.5 12 11.7 6.3 8.5 12 5.3zM5 9.8l6 3.3v6.6l-6-3.3V9.8zm8 9.9v-6.6l6-3.3v6.6l-6 3.3z",
 "home":"M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8h5z",
 "building":"M12 7V3H2v18h20V7H12zM6 19H4v-2h2v2zm0-4H4v-2h2v2zm0-4H4V9h2v2zm0-4H4V5h2v2zm4 12H8v-2h2v2zm0-4H8v-2h2v2zm0-4H8V9h2v2zm0-4H8V5h2v2zm10 12h-8v-2h2v-2h-2v-2h2v-2h-2V9h8v10z",
 "bars":"M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z",
}
def ic(n): return f'<svg class="svg" viewBox="0 0 24 24" aria-hidden="true"><path d="{ICON[n]}"/></svg>'
def tel(p): return f"tel:+91{p}"
def wa(p, text=""): return f"https://wa.me/91{p}" + (f"?text={urllib.parse.quote(text)}" if text else "")
def maps(q): return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)
def fmt(p): return f"{p[:5]} {p[5:]}"

# ---------- branch registry (slug -> info) ----------
BR = {}
for o in OFFICES: BR[o["slug"]] = dict(name=o["name"], area=o["area"], phone=o["phone"], addr=o["addr"])
for slug, area, label, ph in AREAS:
    if slug in BR:
        BR[slug]["label"] = label
        if ph: BR[slug]["phone"] = ph
    else:
        BR[slug] = dict(name=f"{area} Branch", area=area, phone=ph or HQ_PHONE, addr=None, label=label)
AREA_ORDER = [a[0] for a in AREAS]

SVC_ICON = {"corporate-relocation":"building","transportation-service":"truck","door-to-door-service":"home",
            "warehousing-storage":"box","household-moving":"home","commercial-movers":"building","residential-moves":"home"}
PROJECTS = ["Office Furniture Moving","Living Room","Moving Interstate","Cultural House","Beautiful House","Office Removals"]
def pslug(t): return t.lower().replace(" ","-")
def cslug(c): return c.lower()

PAGES = []   # (title, url) for site search
def reg(title, url): PAGES.append([title, url])

# ---------- layout ----------
def nav(r, active):
    def a(href, text, cls=""):
        return f'<a href="{href}"{(" class=%s" % chr(34)+cls+chr(34)) if cls else ""}>{text}</a>'
    on = lambda k: "active" if k == active else ""
    areas = "".join(f'<li><a href="{r}branches/{s}.html">{esc(BR[s]["label"])}</a></li>' for s in AREA_ORDER)
    areas += f'<li><a href="{r}bill-for-claim/hyderabad.html">Packers And Movers Bill For Claim In Hyderabad</a></li>'
    svcs = f'<li><a href="{r}services.html">All Services</a></li>' + "".join(f'<li><a href="{r}services/{s}.html">{esc(t)}</a></li>' for s,t,_,_ in SERVICES)
    cities = "".join(f'<li><a href="{r}bill-for-claim/{cslug(c)}.html">{c}</a></li>' for c in CITIES)
    car = '<span class="caret">▾</span>'
    return f'''<nav class="nav" id="nav" aria-label="Main menu"><ul>
<li>{a(r+"index.html","Home",on("home"))}</li>
<li class="has-sub"><a href="#" class="{on('branches')}" aria-haspopup="true">Branch Offices {car}</a>
 <ul class="sub lvl1"><li class="has-sub"><a href="#">Hyderabad</a><ul class="sub wide">{areas}</ul></li></ul></li>
<li>{a(r+"about-us.html","About Us",on("about"))}</li>
<li>{a(r+"quote-form.html","Quote Form",on("quote"))}</li>
<li class="has-sub"><a href="{r}projects.html" class="{on('projects')}">Projects {car}</a>
 <ul class="sub"><li><a href="{r}projects.html">Projects</a></li><li><a href="{r}projects/office-furniture-moving.html">Projects Single</a></li></ul></li>
<li class="has-sub"><a href="{r}services.html" class="{on('services')}">Services {car}</a><ul class="sub wide">{svcs}</ul></li>
<li>{a(r+"blog.html","Blog",on("blog"))}</li>
<li>{a(r+"contacts.html","Contacts",on("contacts"))}</li>
<li class="has-sub"><a href="{r}bill-for-claim/hyderabad.html" class="{on('bill')}">BILL FOR CLAIM {car}</a><ul class="sub right">{cities}</ul></li>
</ul></nav>'''

def footer(r):
    contact = f'''<div class="ph"><h4>24/7 Contact</h4><ul class="addr">
<li>Beeramguda Branch: <a href="{tel('7416001476')}">7416001476</a></li>
<li>Punjagutta Branch: <a href="{tel('9014963659')}">9014963659</a></li>
<li>Nagaram Branch: <a href="{tel('8019493600')}">8019493600</a></li>
<li>L.B Nagar Branch: <a href="{tel('9014963659')}">9014963659</a></li>
<li>Peerzadiguda Branch: <a href="{tel('8019493600')}">8019493600</a></li>
<li>Dilsukhnagar Branch: <a href="{tel('9014963659')}">9014963659</a></li>
<li>Chandanagar Branch: <a href="{tel('7569608447')}">7569608447</a></li></ul></div>'''
    addr = '<div><h4>Our Addresses</h4><ul class="addr">' + "".join(
        f'<li><b>{esc(o["name"])}:</b> {esc(o["addr"])}</li>' for o in OFFICES) + '</ul></div>'
    mail = f'<div><h4>E-mail</h4><p><a href="mailto:{EMAIL}">{EMAIL}</a></p><h4 style="margin-top:26px">Working Hours</h4><p>{HOURS}</p></div>'
    cats = "".join(f'<li><a href="{r}blog.html#{c.replace(" ","-")}">{c}</a></li>' for c in BLOG_CATS)
    return f'''<footer class="footer">
<div class="container contact">{contact}{addr}{mail}</div>
<div class="container cols">
 <div><a class="logo" href="{r}index.html"><img src="{r}assets/img/logo.png" alt="Mint Relocation Packers"></a>
 <p style="margin-top:18px">We provide expert packers and movers service for seamless relocation. Our team handles everything from packing to unloading, ensuring a stress-free move.</p>
 <p><a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook" style="display:inline-flex;gap:8px;align-items:center">{ic("fb")} Follow us on Facebook</a></p></div>
 <div><h4>Categories</h4><ul>{cats}</ul></div>
 <div><h4>Newsletter</h4><p>Stay stress-free during your move with our reliable and efficient packers and movers services - subscribe to our newsletter for exclusive tips and offers.</p>
 <form class="subscribe" novalidate><label class="sr" for="nl-{id(r)}">Email</label><input id="nl-{id(r)}" name="email" type="email" placeholder="Your email address"><button type="submit">Subscribe</button></form>
 <p class="sub-msg form-note" style="color:#cfcfcf;margin-top:8px"></p></div>
</div>
<div class="copy"><div class="container">Copyright © 2023, Mint Relocation Packers. All rights reserved.</div></div>
</footer>'''

def page(path, title, body, active="", desc="", crumbs=None, h1=None, bar=True):
    """path = file path relative to site root, e.g. 'branches/x.html'"""
    depth = path.count("/"); r = "../" * depth
    full_title = f"{title} - Mint Relocation Packers"
    crumb_html = ""
    if bar:
        trail = [("Home", r+"index.html")] + (crumbs or [])
        cr = '<span class="sep">›</span>'.join(f'<a href="{u}">{esc(t)}</a>' for t,u in trail) + f'<span class="sep">›</span>{esc(h1 or title)}'
        crumb_html = f'<div class="titlebar"><div class="container"><h1>{esc(h1 or title)}</h1><div class="crumbs">{cr}</div></div></div>'
    top = f'''<div class="topbar"><div class="container">
<ul class="soc"><li><a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">{ic("fb")}</a></li></ul>
<ul><li>{ic("phone")}<a href="{tel(HQ_PHONE)}">(+91) {HQ_PHONE}</a></li>
<li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li>{ic("pin")}<a href="{maps(BR['beeramguda']['addr'])}" target="_blank" rel="noopener">365 Shirdi Colony, Beeramguda, TS</a></li></ul></div></div>'''
    header = f'''<header class="site-header"><div class="container hdr">
<a class="logo" href="{r}index.html" aria-label="Mint Relocation Packers - home"><img src="{r}assets/img/logo.png" alt="Mint Relocation Packers" width="150" height="60"></a>
{nav(r, active)}
<div class="hdr-right"><button class="search-btn" aria-label="Search the site">{ic("search")}</button>
<a class="btn" href="{r}quote-form.html">Get a free quote</a>
<button class="menu-toggle" aria-label="Open menu" aria-expanded="false">{ic("bars")}</button></div></div></header>'''
    extra = f'''<div class="search-ov" role="dialog" aria-label="Search"><button class="x" aria-label="Close search">×</button>
<div class="box"><input type="search" placeholder="Type to search - e.g. Madhapur, services, bill" aria-label="Search"><ul></ul></div></div>
<div class="floatc"><a class="c" href="{tel(HQ_PHONE)}" aria-label="Call us">{ic("phone")}<span>Call now</span></a><a class="w" href="{wa(HQ_PHONE)}" target="_blank" rel="noopener" aria-label="WhatsApp us">{ic("wa")}<span>WhatsApp</span></a></div>
<button class="totop" aria-label="Back to top">{ic("up")}</button>'''
    doc = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full_title)}</title><meta name="description" content="{esc(desc or 'Mint Relocation Packers and Movers - reliable packing and moving services in Hyderabad and across India.')}">
<link rel="icon" href="{r}assets/img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Biryani:wght@300;400;600;700;800&family=Nunito+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/style.css"></head>
<body data-root="{r}">
{top}{header}
<main>{crumb_html}{body}</main>
{footer(r)}{extra}
<script src="{r}assets/js/data.js"></script><script src="{r}assets/js/main.js"></script>
</body></html>'''
    fp = os.path.join(OUT, path); os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(doc)
    return doc

# ---------- reusable blocks ----------
def quote_form(compact=False, branch="beeramguda", dark=False, idp="q"):
    opts = "".join(f'<option value="{s}"{" selected" if s==branch else ""}>{esc(BR[s]["name"] if BR[s].get("addr") else BR[s]["area"])} - {BR[s]["phone"]}</option>'
                   for s in list(BR.keys()))
    svc = '<option value="">Select a service</option>' + "".join(f'<option>{esc(t)}</option>' for _,t,_,_ in SERVICES) + "<option>Bill for Claim</option><option>Other / Not sure yet</option>"
    cls = "dark-form" if dark else "formbox"
    return f'''<form class="{cls}" data-quote novalidate>
<h3>{"Get a free quote" if compact else "Tell us about your move"}</h3>
<p class="form-note" style="{'color:#ddd' if dark else ''}">We will reply on WhatsApp or by phone. Fields marked * are required.</p>
<div class="f">
<div><label for="{idp}-name">Your name *</label><input id="{idp}-name" name="name" autocomplete="name"><div class="err" data-err="name"></div></div>
<div><label for="{idp}-phone">Phone number *</label><input id="{idp}-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel"><div class="err" data-err="phone"></div></div>
<div><label for="{idp}-from">Moving from *</label><input id="{idp}-from" name="from" placeholder="Area / city"><div class="err" data-err="from"></div></div>
<div><label for="{idp}-to">Moving to *</label><input id="{idp}-to" name="to" placeholder="Area / city"><div class="err" data-err="to"></div></div>
<div><label for="{idp}-service">Service</label><select id="{idp}-service" name="service">{svc}</select></div>
<div><label for="{idp}-date">Moving date</label><input id="{idp}-date" name="date" type="date"></div>
<div class="full"><label for="{idp}-branch">Nearest branch</label><select id="{idp}-branch" name="branch">{opts}</select></div>
<div class="full"><label for="{idp}-email">Email (optional)</label><input id="{idp}-email" name="email" type="email" autocomplete="email"></div>
{'' if compact else f'<div class="full"><label for="{idp}-msg">Message (optional)</label><textarea id="{idp}-msg" name="message" rows="4"></textarea></div>'}
<div class="full" style="display:flex;gap:12px;flex-wrap:wrap"><button class="btn wa" type="submit">{ic("wa")} Send on WhatsApp</button>
<button class="btn dark" type="button" data-email>{ic("mail")} Send by email</button></div>
</div><div class="ok" role="status" aria-live="polite"></div></form>'''

def band(r, text="Ready to move? <b>Get a free quote today.</b>", phone=HQ_PHONE):
    return f'''<section class="band"><div class="container"><h2>{text}</h2><div class="acts">
<a class="btn dark" href="{r}quote-form.html">Get a free quote</a><a class="btn line" href="{tel(phone)}">{ic("phone")} Call {fmt(phone)}</a></div></div></section>'''

def office_card(slug, r):
    b = BR[slug]; msg = f"Hello Mint Relocation Packers ({b['name']}), I would like a free quote."
    return f'''<div class="off"><h3>{esc(b["name"])}</h3>
<div class="row">{ic("pin")}<span>{esc(b["addr"])}</span></div>
<div class="row">{ic("phone")}<a href="{tel(b["phone"])}"><b>{fmt(b["phone"])}</b></a></div>
<div class="row">{ic("clock")}<span>{HOURS}</span></div>
<div class="acts"><a class="btn sm" href="{tel(b["phone"])}">Call</a><a class="btn sm wa" href="{wa(b["phone"], msg)}" target="_blank" rel="noopener">WhatsApp</a>
<a class="btn sm line" href="{maps(b["addr"])}" target="_blank" rel="noopener">Directions</a></div></div>'''

# ---------- static assets ----------
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "assets/img"), exist_ok=True)
shutil.copytree(os.path.join(HERE, "static/css"), os.path.join(OUT, "assets/css"))
shutil.copytree(os.path.join(HERE, "static/js"), os.path.join(OUT, "assets/js"))
for f in os.listdir(os.path.join(HERE, "static/img")): shutil.copy(os.path.join(HERE, "static/img", f), os.path.join(OUT, "assets/img", f))

# ---------- HOME ----------
r = ""
svc_cards = "".join(f'''<article class="svc"><div class="ico">{ic(SVC_ICON[s])}</div><h3>{esc(t)}</h3><p>{esc(d)}</p><a class="more" href="services/{s}.html">Read more</a></article>''' for s,t,d,_ in SERVICES[:6])
home = f'''
<section class="hero"><div class="container"><div>
<span class="eyebrow">Packers and Movers in Hyderabad</span>
<h1>The best move <b>you will ever make.</b></h1>
<p>Reliable and professional packing and moving services in Hyderabad and across India, with direct customer support and over 5 years of trusted experience.</p>
<div class="cta"><a class="btn" href="quote-form.html">Get a free quote</a><a class="btn line" href="{tel(HQ_PHONE)}">{ic("phone")} Call {fmt(HQ_PHONE)}</a></div>
<div class="tags"><span>Careful packing</span><span>Safe transport</span><span>On-time delivery</span></div></div>
<div class="ph"><img src="assets/img/photo-boxes.jpg" alt="Happy couple holding moving boxes in their new home" width="584" height="300"></div></div></section>

<section class="sec gray"><div class="container center"><span class="eyebrow">We moving safely</span>
<h2 class="h2">Safe Moving <b>Procedures.</b></h2>
<div class="grid g3 steps" style="text-align:left">
<div class="step"><span class="no">01</span><h3>Make your <b>reservation</b></h3><p>Call us, message us on WhatsApp or fill in the quote form with your moving date and addresses.</p></div>
<div class="step"><span class="no">02</span><h3>Load your <b>container</b></h3><p>Our team packs your belongings with quality material and loads them carefully into the vehicle.</p></div>
<div class="step"><span class="no">03</span><h3>We'll take it from <b>there</b></h3><p>We transport, unload and place your goods at the new address, so you can settle in without stress.</p></div>
</div></div></section>

<section class="sec"><div class="container split">
<div class="ph"><img src="assets/img/photo-plans.jpg" alt="Couple planning their move with a floor plan" width="584" height="400"></div>
<div><span class="eyebrow">Why Mint Relocation</span>
<h2 class="h2">Get full <b>control of your shipment.</b></h2>
<p class="lead">Reliable and professional packing and moving services in Hyderabad and across India, with direct customer support and over 5 years of trusted experience.</p>
<div class="feat"><div><h4>Innovative systems</h4><p>High-tech innovations are helping the packers and movers improve their service quality and efficiency, locally as well as domestically.</p></div>
<div><h4>Compare prices</h4><p>The approximate price of packers and movers in India for local household shifting is around Rs 5,000 to Rs 20,000. Intercity moves cost more, so ask us for an exact quote.</p></div></div>
<div class="bar"><div class="l"><span>Road freight</span><span>90%</span></div><div class="t"><div class="f" data-w="90"></div></div></div>
<p style="margin-top:28px"><a class="btn" href="about-us.html">About us</a></p></div></div></section>

<section class="sec gray"><div class="container"><div class="center"><span class="eyebrow">What we do</span><h2 class="h2">Our <b>Services</b></h2></div>
<div class="grid g3">{svc_cards}</div><p class="center" style="margin-top:34px"><a class="btn dark" href="services.html">View all services</a></p></div></section>

<section class="counters"><div class="container"><div class="grid">
<div><div class="n"><span data-to="750">750</span><sup>+</sup></div><p>Customers choose our movers</p></div>
<div><div class="n"><span data-to="870">870</span><sup>+</sup></div><p>Boxes successfully moved</p></div>
<div><div class="n"><span data-to="320">320</span><sup>+</sup></div><p>Customers satisfied with our service</p></div></div></div></section>

<section class="sec"><div class="container"><div class="center"><span class="eyebrow">Find us</span><h2 class="h2">Our <b>Branches</b></h2>
<p class="lead">Call the branch nearest to you - each office has its own number.</p></div>
<div class="grid g3">{"".join(office_card(o["slug"], "") for o in OFFICES[:6])}</div>
<p class="center" style="margin-top:34px"><a class="btn dark" href="contacts.html">All branches &amp; contacts</a></p></div></section>
{band("")}'''
page("index.html", "Packers and Movers in Hyderabad", home, "home", "Mint Relocation Packers and Movers - packing, moving and transport services in Hyderabad and across India.", bar=False)
reg("Home", "index.html")

# ---------- ABOUT ----------
about = f'''<section class="sec"><div class="container split"><div><span class="eyebrow">Our company</span>
<h2 class="h2">We are one of the <b>Top Packers And Movers Company</b></h2>
<p class="lead">Our main aim is to provide top-notch packing and moving services with high standard material.</p>
<ul class="tick"><li>Careful packing with quality material</li><li>Trained team for loading, transport and unloading</li><li>Local, intercity and interstate moves</li><li>Proper GST bill for claim on request</li></ul>
<a class="btn" href="quote-form.html">Get a free quote</a></div>
<div><img src="assets/img/photo-plans.jpg" alt="Planning a move" width="584" height="400"></div></div></section>
<section class="counters"><div class="container"><div class="center" style="margin-bottom:34px"><span class="eyebrow" style="color:#fff">Fun facts</span><h2 class="h2" style="color:#fff">Counters <b>Numbers Speak</b></h2></div>
<div class="grid"><div><div class="n"><span data-to="750">750</span><sup>+</sup></div><p>Customers choose our movers</p></div>
<div><div class="n"><span data-to="870">870</span><sup>+</sup></div><p>Boxes successfully moved</p></div>
<div><div class="n"><span data-to="320">320</span><sup>+</sup></div><p>Customers satisfied with our service</p></div></div></div></section>
<section class="sec gray"><div class="container center"><span class="eyebrow">Our clients say</span><h2 class="h2">We love our clients <b>and they love us</b></h2>
<p class="lead">Read what our customers say about us on Google.</p>
<a class="btn dark" target="_blank" rel="noopener" href="{maps('Mint Relocation Packers and Movers Hyderabad')}">See Google reviews</a></div></section>{band("")}'''
page("about-us.html", "About Us", about, "about", crumbs=[]); reg("About Us","about-us.html")

# ---------- QUOTE ----------
quote = f'''<section class="sec"><div class="container layout"><div>{quote_form(idp="q")}</div>
<aside class="side"><div class="card"><h3>Prefer to talk?</h3><p>Call us any time - we are available 24/7.</p>
<p><a class="btn" href="{tel(HQ_PHONE)}">{ic("phone")} {fmt(HQ_PHONE)}</a></p><p><a class="btn wa" href="{wa(HQ_PHONE)}" target="_blank" rel="noopener">{ic("wa")} WhatsApp us</a></p></div>
<div class="card"><h3>What happens next?</h3><ul class="tick"><li>You send your details</li><li>We call back to confirm the requirement</li><li>You get a clear estimate</li></ul></div></aside></div></section>'''
page("quote-form.html", "Quote Form", quote, "quote", "Request a free packers and movers quote."); reg("Quote Form","quote-form.html")

# ---------- SERVICES ----------
cards = "".join(f'''<article class="svc"><div class="ico">{ic(SVC_ICON[s])}</div><h3>{esc(t)}</h3><p>{esc(d)}</p><a class="more" href="services/{s}.html">Read more</a></article>''' for s,t,d,_ in SERVICES)
page("services.html", "Services", f'<section class="sec"><div class="container"><div class="grid g3">{cards}</div></div></section>{band("")}', "services"); reg("Services","services.html")
for s,t,d,items in SERVICES:
    side = "".join(f'<a href="{x}.html"{" class=cur" if x==s else ""}>{esc(tt)}</a>' for x,tt,_,_ in SERVICES)
    body = f'''<section class="sec"><div class="container layout"><div class="prose"><img src="../assets/img/photo-boxes.jpg" alt="{esc(t)}" width="584" height="300" style="width:100%;margin-bottom:26px">
<h2 style="margin-top:0">{esc(t)}</h2><p class="lead">{esc(d)}</p><h3>What you get</h3><ul class="tick">{"".join(f"<li>{esc(i)}</li>" for i in items)}</ul>
<p>Tell us your requirement and the nearest branch will call you back with a clear estimate.</p><p><a class="btn" href="../quote-form.html?service={urllib.parse.quote(t)}">Get a free quote</a></p></div>
<aside class="side"><div class="card"><h3>Our services</h3><div class="side-nav">{side}</div></div>
<div class="card"><h3>Need help?</h3><p><a class="btn" href="{tel(HQ_PHONE)}">{ic("phone")} {fmt(HQ_PHONE)}</a></p></div></aside></div></section>'''
    page(f"services/{s}.html", t, body, "services", d, crumbs=[("Services","../services.html")]); reg(t, f"services/{s}.html")

# ---------- BRANCH PAGES ----------
def branch_page(slug):
    b = BR[slug]; area = b["area"]; ph = b["phone"]
    h1 = f"Packers And Movers in {area}, Hyderabad"
    others = "".join(f'<a href="{s}.html"{" class=cur" if s==slug else ""}>{esc(BR[s]["area"])}</a>' for s in sorted(BR, key=lambda k: BR[k]["area"]))
    addr = f'<div class="row" style="display:flex;gap:10px;margin:14px 0">{ic("pin")}<span><b>Address:</b> {esc(b["addr"])}<br><a class="more" target="_blank" rel="noopener" href="{maps(b["addr"])}">Get directions</a></span></div>' if b.get("addr") else \
           f'<p>We serve {esc(area)} and nearby areas of Hyderabad. Call us and we will arrange a pick-up from your doorstep.</p>'
    msg = f"Hello Mint Relocation Packers ({b['name']}), I would like a free quote."
    body = f'''<section class="sec"><div class="container layout"><div class="prose">
<h2 style="margin-top:0">Mint Relocation Packers and Movers - {esc(area)}</h2>
<p class="lead">Moving home or office in or around {esc(area)}? Our team packs, loads, transports and unloads your belongings with care, so you do not have to worry about a thing.</p>
{addr}<h3>Services available in {esc(area)}</h3><ul class="tick">{"".join(f'<li><a href="../services/{s}.html">{esc(t)}</a></li>' for s,t,_,_ in SERVICES)}</ul>
<h3>How to book</h3><ul class="tick"><li>Call <a href="{tel(ph)}"><b>{fmt(ph)}</b></a> or message us on WhatsApp</li><li>Tell us your moving date and addresses</li><li>Get a clear estimate and confirm your booking</li></ul>
<p style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="{tel(ph)}">{ic("phone")} Call {fmt(ph)}</a><a class="btn wa" target="_blank" rel="noopener" href="{wa(ph,msg)}">{ic("wa")} WhatsApp</a>
<a class="btn dark" href="../quote-form.html?branch={slug}">Get a free quote</a></p></div>
<aside class="side"><div class="card"><h3>Call this branch</h3><p style="font-size:26px;font-family:Biryani,Arial;font-weight:800;margin:0"><a href="{tel(ph)}">{fmt(ph)}</a></p><p class="form-note">{HOURS}</p></div>
<div class="card"><h3>All branches</h3><div class="side-nav" style="max-height:340px;overflow:auto">{others}</div></div></aside></div></section>{band("../", phone=ph)}'''
    page(f"branches/{slug}.html", h1, body, "branches", f"Packers and movers in {area}, Hyderabad. Call {ph}.", crumbs=[("Branch Offices","../contacts.html")])
    reg(h1, f"branches/{slug}.html")
for slug in BR: branch_page(slug)

# ---------- BILL FOR CLAIM ----------
KW = ["Packers and Movers Bill Format for Claim in {c}","Claiming Insurance with Packers and Movers Bill in {c}","{c} Packers and Movers Bill Sample for Insurance Claim",
      "Packers and Movers Bill for Reimbursement in {c}","Mint Relocation Packers and Movers Bill for Claim in {c}","{c} Packers and Movers Bill Template for Claim",
      "How to Get Packers and Movers Bill for Claim in {c}","Claiming Relocation Expenses with Packers and Movers Bill in {c}","Insurance Claim Process with Packers and Movers Bill in {c}",
      "Packers and Movers Bill Verification for Claim in {c}"]
for c in CITIES:
    side = "".join(f'<a href="{cslug(x)}.html"{" class=cur" if x==c else ""}>{x}</a>' for x in CITIES)
    body = f'''<section class="sec"><div class="container layout"><div class="prose">
<h2 style="margin-top:0">Packers And Movers Bill For Claim {c} - Call Now - <a href="{tel(CLAIM_PHONE)}">{CLAIM_PHONE}</a></h2>
<p><b>Packers and Movers in {c} GST Bills For Claim - GST TAX INVOICE.</b></p>
<p>Mint packers and movers bill for claim in {c} serves as a crucial document for individuals or businesses seeking reimbursement or insurance coverage for their relocation expenses. This document outlines the details of the services provided by Mint Relocation Packers and Movers and is essential for facilitating a smooth claims process.</p>
<p>Typically, the bill includes important information such as:</p>
<ul class="tick"><li><b>Company Details:</b> the name, address, contact information and GSTIN of Mint Relocation Packers and Movers.</li>
<li><b>Customer Details:</b> the customer's name, address and contact details, to establish the recipient of the services.</li>
<li><b>Service Details:</b> a breakdown of the services provided, such as packing, loading, transportation, unloading and unpacking, along with their respective costs.</li>
<li><b>Date and Duration:</b> the date of service initiation and completion, and the duration of the relocation process.</li>
<li><b>Cost Breakdown:</b> labour charges, transportation fees, packing material costs and any additional charges.</li>
<li><b>GST Details:</b> the Goods and Services Tax applied to the total bill amount, along with the applicable tax rate and GSTIN.</li>
<li><b>Terms and Conditions:</b> payment terms, insurance coverage and liability clauses, for clarity and transparency.</li>
<li><b>Signature and Seal:</b> the bill is signed by an authorised representative and stamped with the company's official seal for authenticity.</li></ul>
<p>By providing a comprehensive packers and movers bill for claim in {c}, Mint Relocation aims to facilitate a transparent and hassle-free claims process for its customers, ensuring peace of mind during the relocation journey.</p>
<h3>Your search ends here!</h3><ul class="tick">{"".join(f"<li>{k.format(c=c)}</li>" for k in KW)}</ul>
<p><b>One solution for all the above details.</b></p>
<p style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="{tel(CLAIM_PHONE)}">{ic("phone")} Call {fmt(CLAIM_PHONE)}</a><a class="btn dark" href="../quote-form.html?service=Bill%20for%20Claim">Get a free quote today</a></p></div>
<aside class="side"><div class="card"><h3>Bill for claim in other cities</h3><div class="side-nav">{side}</div></div></aside></div></section>'''
    t = f"Packers And Movers Bill For Claim In {c}"
    page(f"bill-for-claim/{cslug(c)}.html", t, body, "bill", f"Packers and movers GST bill for claim in {c}. Call {CLAIM_PHONE}.", crumbs=[("Bill for Claim","hyderabad.html")])
    reg(t, f"bill-for-claim/{cslug(c)}.html")

# ---------- PROJECTS ----------
IMGS = ["photo-boxes.jpg", "photo-plans.jpg"]
pc = "".join(f'<a class="proj" href="projects/{pslug(p)}.html"><img src="assets/img/{IMGS[i%2]}" alt="{p}" loading="lazy"><div><small>Project</small><h3>{p}</h3></div></a>' for i,p in enumerate(PROJECTS))
page("projects.html", "Projects", f'<section class="sec"><div class="container"><div class="grid g3">{pc}</div></div></section>{band("")}', "projects"); reg("Projects","projects.html")
for i,p in enumerate(PROJECTS):
    prev = PROJECTS[i-1]; nxt = PROJECTS[(i+1)%len(PROJECTS)]
    det = '<div class="dl"><div class="k">Category</div><div>Interior</div><div class="k">Date</div><div>December 29, 2018</div></div>' if p=="Office Furniture Moving" else ""
    body = f'''<section class="sec"><div class="container layout"><div class="prose"><img src="../assets/img/{IMGS[i%2]}" alt="{p}" style="width:100%;margin-bottom:24px">
<h2 style="margin-top:0">{p}</h2><p class="lead">We are an India-based top mover company.</p>{det}
<p style="display:flex;justify-content:space-between;gap:20px;margin-top:30px;flex-wrap:wrap"><a class="more" href="{pslug(prev)}.html">← {prev}</a><a class="more" href="{pslug(nxt)}.html">{nxt} →</a></p></div>
<aside class="side"><div class="card"><h3>Related projects</h3><div class="side-nav">{"".join(f'<a href="{pslug(x)}.html">{x}</a>' for x in PROJECTS if x!=p)}</div></div>
<div class="card"><h3>Plan your move</h3><p><a class="btn" href="../quote-form.html">Get a free quote</a></p></div></aside></div></section>'''
    page(f"projects/{pslug(p)}.html", p, body, "projects", crumbs=[("Projects","../projects.html")]); reg(p, f"projects/{pslug(p)}.html")

# ---------- BLOG ----------
chips = '<button class="chip on" data-cat="all">All</button>' + "".join(f'<button class="chip" data-cat="{c}">{c}</button>' for c in BLOG_CATS)
posts = "".join(f'<article class="post" data-cat="{c}"><span class="meta">{c} · {tag}</span><h3>{esc(t)}</h3><p>{esc(txt[:110].rsplit(" ",1)[0])}…</p><div class="full"><p>{esc(txt)}</p></div><button type="button">Read more</button></article>' for t,c,tag,txt in BLOG)
page("blog.html", "Blog", f'<section class="sec"><div class="container"><div class="chips">{chips}</div><div class="grid g2">{posts}</div></div></section>{band("")}', "blog"); reg("Blog","blog.html")

# ---------- CONTACTS ----------
contacts = f'''<section class="sec"><div class="container"><div class="center"><span class="eyebrow">Here when you need us</span><h2 class="h2">Contact <b>our branches</b></h2>
<p class="lead">Call the branch nearest to you, or write to <a href="mailto:{EMAIL}"><b>{EMAIL}</b></a></p></div>
<div class="grid g3">{"".join(office_card(o["slug"], "") for o in OFFICES)}</div></div></section>
<section class="sec gray"><div class="container layout"><div>{quote_form(idp="c")}</div><aside class="side"><div class="card"><h3>Working hours</h3><p>{HOURS}</p><p>Call or WhatsApp any time - we respond as soon as possible.</p></div>
<div class="card"><h3>Email</h3><p><a href="mailto:{EMAIL}"><b>{EMAIL}</b></a></p></div></aside></div></section>'''
page("contacts.html", "Contacts", contacts, "contacts", "Contact Mint Relocation Packers and Movers branches in Hyderabad."); reg("Contacts","contacts.html")

# ---------- data.js ----------
data = dict(email=EMAIL, hq=HQ_PHONE, pages=PAGES,
            branches={k: dict(name=v["name"] if v.get("addr") else v["area"] + " Branch", phone=v["phone"]) for k,v in BR.items()})
open(os.path.join(OUT, "assets/js/data.js"), "w").write("window.SITE=" + json.dumps(data, ensure_ascii=False) + ";")
print("built", sum(len(f) for _,_,f in os.walk(OUT)), "files in", OUT)
