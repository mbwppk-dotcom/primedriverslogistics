#!/usr/bin/env python3
"""Generates the static HTML pages for the Prime Drivers Logistics site."""
import os

OUT = os.path.dirname(os.path.abspath(__file__))
PHONE = "+1 (279) 271-4680"
WA = "https://wa.me/12792714680"

def wa(msg):
    return WA + "?text=" + msg.replace(" ", "%20").replace("'", "%27")

WA_SVG = ('<svg class="wa-ico" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.4-1.5-.9-.8-1.5-1.8-1.6-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4C2.7 15.6 2.2 13.8 2.2 12 2.2 6.6 6.6 2.2 12 2.2c2.6 0 5.1 1 6.9 2.9 1.8 1.8 2.9 4.3 2.9 6.9 0 5.4-4.4 9.8-9.8 9.8zm8.4-18.2C18.1 1.3 15.2.1 12 .1 5.5.1.1 5.4.1 12c0 2.1.5 4.1 1.6 5.9L0 24l6.3-1.7c1.7.9 3.7 1.4 5.7 1.4 6.6 0 11.9-5.4 11.9-11.9 0-3.2-1.2-6.2-3.5-8.2z"/></svg>')

DISPATCH = [
    # slug, name, icon, short
    ("box-truck", "Box Truck", "📦", "Box Truck"),
    ("dry-van", "Dry Van", "🚚", "Dry Van"),
    ("reefer", "Reefer", "❄️", "Reefer"),
    ("power-only", "Power Only", "🔗", "Power Only"),
    ("hotshot", "Hotshot", "🔥", "Hotshot"),
    ("flatbed", "Flatbed / Step Deck", "🏗️", "Flatbed"),
]

# ------------------------------------------------------------------ partials

def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🚛</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<div id="loader"><div class="loader-inner"><div class="loader-truck">🚛</div><div class="loader-bar"><span></span></div></div></div>
"""

def header(active, topbar=True):
    def cls(name):
        return "nav-link active" if active == name else "nav-link"
    act = ' class="active"'
    dd = "\n".join(
        f'            <a href="dispatch-{s}.html"{act if active == "d-" + s else ""}><span>{i}</span>{n}</a>'
        for s, n, i, _ in DISPATCH
    )
    dispatch_active = "nav-link active" if active.startswith("d-") else "nav-link"
    tb = f"""<div class="topbar">
  <div class="container">
    <span><i class="dot"></i>Dispatching 24/7 across the USA</span>
    <span class="hide-sm">WhatsApp: {PHONE}</span>
  </div>
</div>
""" if topbar else ""
    return tb + f"""<header class="header">
  <div class="scroll-progress"></div>
  <div class="container">
    <a href="index.html" class="logo" aria-label="Prime Drivers Logistics home">
      <img src="images/logo.png" alt="Prime Drivers Logistics" class="logo-img">
    </a>
    <nav class="nav" aria-label="Main">
      <ul>
        <li><a href="index.html" class="{cls('home')}">Home</a></li>
        <li class="has-dropdown">
          <a href="#" class="{dispatch_active}">Dispatch <span class="caret">▼</span></a>
          <div class="dropdown">
{dd}
          </div>
        </li>
        <li><a href="services.html" class="{cls('services')}">Services</a></li>
        <li><a href="equipment.html" class="{cls('equipment')}">Equipment</a></li>
        <li><a href="about.html" class="{cls('about')}">About</a></li>
        <li><a href="contact.html" class="{cls('contact')}">Contact</a></li>
      </ul>
      <a href="{wa("Hi Prime Drivers, I'd like to start dispatch")}" target="_blank" rel="noopener" class="btn btn-wa btn-sm">{WA_SVG} Chat on WhatsApp</a>
    </nav>
    <button class="menu-toggle" aria-label="Open menu"><span></span></button>
  </div>
</header>
"""

def road_ticker(ticker=True):
    items = ["RGN", "Dump", "Dry Van", "Reefer", "Flatbed", "Step Deck", "Power Only",
             "Hotshot", "Box Truck", "Conestoga", "Lowboy"]
    t = ""
    if ticker:
        spans = "".join(f"<span>{x}</span>" for x in items)
        t = f'<div class="ticker"><div class="ticker-track">{spans}</div></div>\n'
    return '<div class="road-wrap"><div class="road"></div></div>\n' + t

def section_head(eyebrow, title, sub=""):
    s = f'<p class="section-sub">{sub}</p>' if sub else ""
    return f"""<div class="section-head center reveal">
      <span class="eyebrow">{eyebrow}</span>
      <h2 class="section-title">{title}</h2>
      {s}
    </div>"""

def cards(items, cols=3, extra_cls=""):
    out = []
    for it in items:
        icon, title, text = it[:3]
        more = it[3] if len(it) > 3 else ""
        out.append(f"""      <div class="card {extra_cls} reveal">
        <div class="card-icon">{icon}</div>
        <h3>{title}</h3>
        <p>{text}</p>{more}
      </div>""")
    return f'<div class="grid grid-{cols}">\n' + "\n".join(out) + "\n    </div>"

def steps(items):
    out = []
    for n, (title, text) in enumerate(items, 1):
        out.append(f"""      <div class="card step reveal">
        <div class="step-num">{n}</div>
        <h3>{title}</h3>
        <p>{text}</p>
      </div>""")
    return '<div class="grid grid-4">\n' + "\n".join(out) + "\n    </div>"

def faq(items):
    out = []
    for q, a in items:
        out.append(f"""      <div class="faq-item reveal">
        <button class="faq-q" aria-expanded="false">{q}<span class="plus">+</span></button>
        <div class="faq-a"><p>{a}</p></div>
      </div>""")
    return '<div class="faq">\n' + "\n".join(out) + "\n    </div>"

def cta(title="Ready to Keep Your Truck Loaded?",
        text="Join hundreds of owner-operators who trust Prime Drivers Logistics. Onboard today and book your first load within 24 hours."):
    return f"""<section class="cta-wrap">
  <div class="container">
    <div class="cta reveal">
      <h2>{title}</h2>
      <p>{text}</p>
      <div class="btn-row">
        <a href="{wa("Hi Prime Drivers, I'm ready to get loaded")}" target="_blank" rel="noopener" class="btn btn-wa">{WA_SVG} Message {PHONE}</a>
        <a href="{wa("Hi, I'd like to discuss dispatch pricing")}" target="_blank" rel="noopener" class="btn btn-ghost">Discuss Pricing</a>
      </div>
    </div>
  </div>
</section>
"""

def footer(extra=""):
    dl = "\n".join(f'          <li><a href="dispatch-{s}.html">{n}</a></li>' for s, n, _, _ in DISPATCH)
    return f"""<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-about">
        <a href="index.html" class="logo" aria-label="Prime Drivers Logistics home">
          <img src="images/logo-white.png" alt="Prime Drivers Logistics" class="logo-img footer-logo">
        </a>
        <p>Full-service truck dispatching for owner-operators and fleets across the USA. We keep your wheels turning and your revenue growing — 24/7.</p>
      </div>
      <div>
        <h4>Dispatch</h4>
        <ul>
{dl}
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About Us</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="equipment.html">Equipment</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Get in Touch</h4>
        <ul>
          <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp: {PHONE}</a></li>
          <li>Serving USA</li>
          <li>24/7 Dispatch Support</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Prime Drivers Logistics. All rights reserved.</span>
      <span><a href="#">Privacy Policy</a> · <a href="#">Terms &amp; Conditions</a></span>
    </div>
  </div>
</footer>

<a href="{wa("Hi Prime Drivers!")}" target="_blank" rel="noopener" class="float-chat" aria-label="Chat with us on WhatsApp">{WA_SVG}<span>Chat with us</span></a>
{extra}
<script src="js/main.js"></script>
</body>
</html>
"""

def page_hero(crumb, title, text, btn_text, icon=""):
    ic = f"<span>{icon}</span>" if icon else ""
    return f"""<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / {crumb}</div>
    <h1>{ic}{title}</h1>
    <p>{text}</p>
    <a href="{wa("Hi Prime Drivers, I'd like to start dispatch")}" target="_blank" rel="noopener" class="btn btn-amber">🚀 {btn_text}</a>
  </div>
</section>
"""

def split(img, alt, eyebrow, title, body_html, checks, btn_text, btn_cls="btn-wa", reverse=False, dark=False, wrap_cls="section"):
    chk = ""
    if checks:
        chk = '<ul class="check-list">' + "".join(f"<li><span>{c}</span></li>" for c in checks) + "</ul>"
    rv = " reverse" if reverse else ""
    sec_cls = wrap_cls + (" dark" if dark else "")
    return f"""<section class="{sec_cls}">
  <div class="container split{rv}">
    <div class="split-media reveal reveal-left">
      <img src="images/{img}" alt="{alt}" loading="lazy">
    </div>
    <div class="reveal reveal-right">
      <span class="eyebrow">{eyebrow}</span>
      <h2>{title}</h2>
      {body_html}
      {chk}
      <a href="{wa("Hi Prime Drivers, I have a question")}" target="_blank" rel="noopener" class="btn {btn_cls}">{WA_SVG} {btn_text}</a>
    </div>
  </div>
</section>
"""

# ------------------------------------------------------------------ shared content

SERVICES_HOME = [
    ("🎯", "High-Paying Load Sourcing", "We work the load boards, broker relationships and lanes you prefer to lock in the best rate-per-mile — every single day."),
    ("🤝", "Broker Negotiation", "Our dispatchers negotiate hard on your behalf and verify every broker's credit and reputation before you commit."),
    ("🗺️", "Route &amp; Trip Planning", "Smart routing around weather, traffic and construction with fuel-efficient stops planned A to Z."),
    ("📄", "Paperwork &amp; Compliance", "Rate cons, BOLs, carrier packets and FMCSA compliance — all set up and filed so nothing slows you down."),
    ("💵", "Billing &amp; Factoring", "We submit invoices and factoring docs the moment you deliver, so you get paid faster and chase nothing."),
    ("🛟", "24/7 Driver Support", "Breakdown, detention or a last-minute reroute? Your dispatcher answers day or night, weekends included."),
]

EQUIPMENT = [
    ("📦", "Box Truck", "26'+ box trucks with lift gate — local &amp; regional freight.", "box-truck"),
    ("🚚", "Dry Van", "48'–53' vans, the backbone of OTR freight.", "dry-van"),
    ("❄️", "Reefer", "Temperature-controlled loads with premium rates.", "reefer"),
    ("🏗️", "Flatbed / Step Deck", "Open-deck freight, tarps and securement handled.", "flatbed"),
    ("🔥", "Hotshot", "40'+ hotshot loads moving fast and frequent.", "hotshot"),
    ("🔗", "Power Only", "Day cabs &amp; OTR units pulling drop trailers.", "power-only"),
    ("🚛", "Conestoga / Lowboy", "Specialized and oversized — permits coordinated.", None),
    ("⚙️", "RGN / Heavy Haul", "Machinery and heavy equipment, route-surveyed.", None),
]

STEPS = [
    ("Say Hi on WhatsApp", "Message us your equipment, authority and preferred lanes. No long forms."),
    ("Quick Setup", "We complete your carrier packet and broker setups — usually same day."),
    ("We Book Your Loads", "Your dispatcher sources, negotiates and sends rates for your approval."),
    ("You Drive &amp; Get Paid", "You haul, we handle paperwork and factoring so payment lands fast."),
]

FAQ_HOME = [
    ("How much does dispatch cost?", "We charge a flat percentage of the gross load rate — no setup fees, no hidden charges and no long-term contracts. Message us on WhatsApp for a quote tailored to your truck."),
    ("Do I have to accept every load?", "Never. There's no forced dispatch. We send you the details and rate of every load and you approve it before we book."),
    ("What do I need to get started?", "Your active MC/DOT authority, a current certificate of insurance (COI), your W-9 and your equipment details. That's it."),
    ("Which states do you cover?", "All 48 contiguous states. We plan lanes around your home time — local, regional or OTR."),
    ("Can you help with factoring?", "Yes. We work with trusted factoring partners and submit your paperwork right after delivery so you get paid fast."),
]

def equip_cards(link=True):
    items = []
    for icon, name, text, slug in EQUIPMENT:
        more = f'<a class="card-link" href="dispatch-{slug}.html">Learn more →</a>' if (link and slug) else ""
        items.append((icon, name, text, more))
    return cards(items, cols=4, extra_cls="equip-card")

VIDEO_MODAL = """<div class="modal" id="videoModal" role="dialog" aria-modal="true" aria-label="Video">
  <div class="modal-box">
    <button class="modal-close" aria-label="Close">×</button>
    <iframe src="" title="Prime Drivers video" allow="autoplay; encrypted-media; fullscreen" allowfullscreen></iframe>
  </div>
</div>"""

# ------------------------------------------------------------------ pages

def page_index():
    h = head("Prime Drivers Logistics | Truck Dispatch Services USA",
             "Full-service truck dispatch for owner-operators. High-paying loads, broker negotiation, paperwork and 24/7 support.")
    h += header("home", topbar=False)
    h += f"""
<section class="hero">
  <div class="container">
    <div class="reveal">
      <span class="badge">⭐ Trusted by 700+ owner-operators</span>
      <h1>Keep Your Wheels Turning &amp; Your Revenue Growing</h1>
      <p class="lead">Prime Drivers Logistics is your full-service truck dispatch partner. We find the high-paying loads, negotiate with brokers, plan your routes and handle the paperwork — so you stay focused on the road.</p>
      <div class="btn-row">
        <a href="{wa("Hi Prime Drivers, I'd like to start dispatch")}" target="_blank" rel="noopener" class="btn btn-amber">🚀 Start Dispatch on WhatsApp</a>
        <a href="services.html" class="btn btn-ghost">Explore Services →</a>
      </div>
    </div>
    <div class="glass-card reveal">
      <span class="live-pill"><i></i>Live dispatch desk · 24/7</span>
      <div class="glass-icon">🚚</div>
      <h3>Get Loaded in 24 Hours</h3>
      <ul class="check-list">
        <li>No forced dispatch — you approve every load</li>
        <li>Dedicated dispatcher &amp; broker negotiation</li>
        <li>Paperwork, billing &amp; factoring handled</li>
        <li>Best rate-per-mile on every lane</li>
      </ul>
      <a href="{wa("Hi Prime Drivers, I'd like to get loaded")}" target="_blank" rel="noopener" class="btn btn-wa btn-block">{WA_SVG} Start on WhatsApp</a>
      <p class="rating">⭐ 4.9/5 from owner-operators across the USA</p>
    </div>
  </div>
</section>
{road_ticker()}
<section class="section">
  <div class="container">
    {section_head("What We Do", "Everything Dispatch, Handled End-to-End", "One dedicated dispatcher. Zero forced dispatch. Full transparency on every load you run.")}
    {cards(SERVICES_HOME)}
    <div class="center" style="margin-top:44px"><a href="services.html" class="btn btn-blue">See All Services</a></div>
  </div>
</section>
"""
    h += split("scania.jpg", "Semi truck on a highway", "Why Outsource Dispatch",
               "More Loaded Miles. Less Office Stress.",
               "<p>Running the back office alone burns hours you could spend earning. We become your logistics department for a flat percentage — no salaries, no software, no overhead.</p>",
               ["<strong>Earn more per mile</strong> — dedicated negotiation on every load.",
                "<strong>Zero downtime</strong> — your next load is booked before you deliver the current one.",
                "<strong>No forced dispatch</strong> — you approve every rate before we book.",
                "<strong>Transparent percentage</strong> — no setup fees, cancel anytime."],
               "Ask Us on WhatsApp", wrap_cls="section soft")
    h += f"""
<section class="section">
  <div class="container">
    {section_head("Equipment We Dispatch", "Whatever You Drive, We Keep It Loaded", "From 26' box trucks to RGN heavy-haul — our dispatchers know the lanes and rates for your equipment.")}
    {equip_cards()}
  </div>
</section>

<section class="stats">
  <div class="container grid grid-4">
    <div class="reveal"><div class="stat-num" data-count="618" data-suffix="+">0</div><div class="stat-label">Owner-Operators Onboard</div></div>
    <div class="reveal"><div class="stat-num" data-count="15891" data-suffix="+">0</div><div class="stat-label">Loads Booked</div></div>
    <div class="reveal"><div class="stat-num" data-count="2.8" data-suffix="$/mi">0</div><div class="stat-label">Avg. Rate Secured</div></div>
    <div class="reveal"><div class="stat-num" data-count="86" data-suffix="%">0</div><div class="stat-label">Driver Retention</div></div>
  </div>
</section>

<section class="video-band">
  <div class="container reveal">
    <button class="play-btn" data-video="YOUR_YOUTUBE_EMBED_URL" aria-label="Play video">▶</button>
    <span class="eyebrow">On the Move 24/7</span>
    <h2>Your Freight, Always Rolling Forward</h2>
    <p>While you drive, our dispatch desk is booking your next load, confirming your paperwork and tracking your delivery in real time.</p>
    <a href="{wa("Hi Prime Drivers, I'd like to start dispatch")}" target="_blank" rel="noopener" class="btn btn-amber">🚀 Start Dispatch Today</a>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("How It Works", "From Sign-Up to Loaded in 24 Hours", "Onboarding is fast, paperless and built around your preferences.")}
    {steps(STEPS)}
  </div>
</section>

<section class="section soft">
  <div class="container">
    {section_head("Drivers Love Us", "Real Words From the Road", "Owner-operators across the country trust Prime Drivers to keep their trucks moving.")}
    <p class="sample-note">Sample testimonials — replace with your clients' real reviews.</p>
    <div class="grid grid-3">
      <div class="card testi reveal">
        <div class="stars">★★★★★</div>
        <blockquote>"My weekly gross went up almost 30% in the first month. They actually fight for the rate instead of taking the first offer — and I never feel pushed into a load."</blockquote>
        <div class="person"><span class="avatar">MJ</span><div><strong>Marcus J.</strong><small>Owner-Operator · Dry Van</small></div></div>
      </div>
      <div class="card testi reveal">
        <div class="stars">★★★★★</div>
        <blockquote>"Running two reefers used to mean I was on the phone all day. Now my dispatcher handles brokers, paperwork and factoring. Payments land on time — no more chasing a claim for me."</blockquote>
        <div class="person"><span class="avatar">RS</span><div><strong>Ravi S.</strong><small>Reefer · 2 trucks</small></div></div>
      </div>
      <div class="card testi reveal">
        <div class="stars">★★★★★</div>
        <blockquote>"Hotshot is all about speed and these guys get it. Loads are booked before I'm even empty and they answer WhatsApp at 2 AM. Best decision I've made for my business."</blockquote>
        <div class="person"><span class="avatar">DC</span><div><strong>Diego C.</strong><small>Hotshot Owner-Operator</small></div></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("On the Road With Us", "Built Around the Trucking Life")}
    <div class="gallery reveal">
      <figure><img src="images/gallery-1.jpg" alt="Semi truck on a wet highway at sunset" loading="lazy"></figure>
      <figure class="tall"><img src="images/gallery-2.jpg" alt="Dark semi truck on the road" loading="lazy"></figure>
      <figure><img src="images/gallery-3.jpg" alt="Truck on a mountain road" loading="lazy"></figure>
      <figure><img src="images/gallery-4.jpg" alt="Distribution warehouse" loading="lazy"></figure>
      <figure><img src="images/gallery-5.jpg" alt="Warehouse aisle" loading="lazy"></figure>
      <figure><img src="images/gallery-7.jpg" alt="Container port from above" loading="lazy"></figure>
      <figure><img src="images/gallery-8.jpg" alt="White truck on a highway" loading="lazy"></figure>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="container">
    {section_head("Good to Know", "Questions Drivers Ask Us")}
    {faq(FAQ_HOME)}
  </div>
</section>
<div class="soft">{cta()}</div>
"""
    h += footer(VIDEO_MODAL)
    return h


DISPATCH_DETAIL = {
    "box-truck": dict(
        hero="Tired of hunting for decent freight and drowning in paperwork between runs? Our box truck dispatch service removes the daily headaches so your 26'+ straight truck stays loaded and profitable — you drive, we handle the rest.",
        title="Experts Who Keep Your Box Truck Loaded",
        p1="Box trucks — also called straight trucks — offer better maneuverability and lower running costs than semis, making them perfect for local and regional runs. But local moving and delivery demand can be sporadic, and empty days eat into your income.",
        p2="Prime Drivers Logistics keeps your box truck earning by pairing your local work with steady long-haul and regional loads. We work with non-local box truck owners running 26' or more with a lift gate, handling every back-office task so you never deadhead or chase brokers again.",
        img="box-truck.jpg"),
    "dry-van": dict(
        hero="Dry van freight is everywhere — but so is the competition. We cut through cheap load-board offers and lock in consistent, well-paying freight for your 48'–53' van.",
        title="Dry Van Dispatch That Pays What You're Worth",
        p1="Dry vans haul the bulk of America's consumer goods, which means freight is plentiful but rates are tight. Without a strategy, it's easy to end up running cheap miles just to stay busy.",
        p2="Our dispatchers build lane strategies around high-demand markets, negotiate every rate and plan your reloads ahead of time, so you're running profitable miles — not just miles.",
        img="gallery-2.jpg"),
    "reefer": dict(
        hero="Reefer loads pay a premium — when they're dispatched right. We source temperature-controlled freight, verify every detail and keep your unit cold and loaded.",
        title="Reefer Dispatch With Zero Room for Error",
        p1="Produce, meat, pharmaceuticals and frozen goods move on tight appointment windows and strict temperature requirements. One missed detail can mean a rejected load.",
        p2="We confirm temps, pulp requirements, appointment times and lumper details before you roll, and we target seasonal produce lanes to keep your reefer earning top dollar year-round.",
        img="gallery-1.jpg"),
    "power-only": dict(
        hero="No trailer? No problem. We match your day cab or OTR tractor with drop-trailer and power-only freight from carriers and shippers nationwide.",
        title="Power Only Dispatch for Tractors Without Trailers",
        p1="Power only lets you haul without the cost of owning a trailer — you hook up to preloaded trailers from shippers, brokers and big carriers' drop yards.",
        p2="We secure power-only programs and spot loads, handle onboarding with the large networks and keep your tractor moving with minimal downtime between hooks.",
        img="gallery-8.jpg"),
    "hotshot": dict(
        hero="Hotshot freight moves fast — so should your dispatcher. We book expedited, time-sensitive loads that fit your pickup and gooseneck and keep you rolling.",
        title="Hotshot Dispatch Built for Speed",
        p1="Hotshot carriers run 40'+ gooseneck and flatbed trailers on urgent, partial and LTL loads — construction equipment, oilfield parts, machinery and more.",
        p2="We know the hotshot boards and direct shippers, stack partials for full-truck pay and plan routes that respect your weight limits and DOT requirements.",
        img="gallery-3.jpg"),
    "flatbed": dict(
        hero="Open-deck freight demands experience. We dispatch flatbed and step deck loads with the right securement, tarp and permit details sorted before you roll.",
        title="Flatbed &amp; Step Deck Dispatch Done Right",
        p1="Lumber, steel, building materials and machinery pay well on open decks — but they come with tarping, chains, straps, oversize rules and tricky load-outs.",
        p2="Our dispatchers confirm dimensions, weights, securement and tarp pay up front, coordinate permits when needed and keep high-paying open-deck freight flowing to your trailer.",
        img="gallery-4.jpg"),
}

def page_dispatch(slug, name, icon, short):
    d = DISPATCH_DETAIL[slug]
    h = head(f"{name} Dispatch Service | Prime Drivers Logistics",
             f"Professional {name.lower()} dispatch for owner-operators — loads, rates, paperwork and 24/7 support.")
    h += header("d-" + slug)
    h += page_hero(f"Dispatch / {name}", f"{name} Dispatch Service", d["hero"], "Start Dispatch on WhatsApp", icon)
    h += road_ticker(ticker=False)
    h += split(d["img"], f"{name} on the road", f"{short} Dispatch", d["title"],
               f"<p>{d['p1']}</p><p>{d['p2']}</p>", [], f"Talk to a {short} Dispatcher")
    feats = [
        ("🎯", "Goal-Oriented Load Search", f"We learn your lanes, home time and income targets, then book loads that move you toward them."),
        ("👤", "Your Dedicated Dispatcher", f"A single point of contact who knows your {short.lower()} and your preferences — not a rotating call center."),
        ("💰", "Best Loads &amp; Rates", f"We mine the boards and our broker network daily for the highest-paying {short.lower()} freight available."),
        ("📄", "Paperwork &amp; Billing", "Rate confirmations, BOLs, invoices and carrier packets — all prepared and submitted for you."),
        ("🛡️", "Broker Credit Checks", "Every broker is screened for credit and payment history so you never haul for someone who won't pay."),
        ("🛟", "24/7 Support", "Detention, breakdowns, lumper issues — your dispatcher is reachable around the clock."),
    ]
    h += f"""
<section class="section soft">
  <div class="container">
    {section_head("What You Get", f"Full-Service {short} Dispatching", "Everything handled end-to-end so you can keep your eyes on the road.")}
    {cards(feats)}
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("How It Works", "From Sign-Up to Loaded in 24 Hours", "Onboarding is fast, paperless and built around your preferences.")}
    {steps(STEPS)}
  </div>
</section>

<section class="section soft">
  <div class="container">
    {section_head("Good to Know", f"{short} Dispatch FAQs")}
    {faq(FAQ_HOME[:4])}
  </div>
</section>
<div class="soft">{cta(f"Get Your {short} Loaded This Week")}</div>
"""
    h += footer()
    return h


def page_services():
    h = head("Dispatch Services | Prime Drivers Logistics",
             "Load sourcing, rate negotiation, route planning, paperwork, factoring coordination and 24/7 driver support.")
    h += header("services")
    h += page_hero("Services", "Dispatch Services That Drive Revenue",
                   "From finding the load to getting you paid, our dispatchers run your entire back office — so every mile you drive is a mile that pays.",
                   "Start Dispatch on WhatsApp")
    h += road_ticker(ticker=False)
    items = [
        ("🎯", "Load Sourcing", "We mine premium load boards, direct broker relationships and our private lane network to find the highest rate-per-mile for your equipment and location — refreshed all day, every day."),
        ("🤝", "Rate Negotiation", "Our dispatchers negotiate aggressively on every load and screen brokers for credit and payment history, so you never haul for someone who won't pay."),
        ("🗺️", "Route &amp; Trip Planning", "Efficient routing that dodges weather, construction and traffic, with planned fuel and rest stops that maximize your hours and minimize deadhead."),
        ("📄", "Paperwork &amp; Compliance", "Carrier packets, rate cons, BOLs, IFTA support and FMCSA compliance reminders — organized and filed so audits never slow you down."),
        ("💵", "Factoring Coordination", "Through trusted factoring partners we help you turn delivered loads into cash fast — paperwork uploaded to the portal for you."),
        ("🛟", "24/7 Driver Support", "Breakdowns, detention, reroutes or broker disputes — your dispatcher is reachable day or night, weekends and holidays included."),
        ("📈", "Business Growth", "Lane analysis, rate trends and planning to help you add trucks and scale your authority into a profitable fleet."),
        ("🧾", "Broker Setup", "We handle broker onboarding and carrier packets so you're approved and ready to haul with top brokers fast."),
        ("📊", "Weekly Reports", "Clear weekly summaries of gross revenue, rate-per-mile and miles driven so you always know where your business stands."),
    ]
    h += f"""
<section class="section">
  <div class="container">
    {section_head("What We Do", "Everything Your Truck Needs to Earn", "One dedicated dispatcher handling the full back office — transparently, on a flat percentage.")}
    {cards(items)}
  </div>
</section>
"""
    h += split("warehouse.jpg", "Warehouse aisle", "A True Partner", "We Run the Office. You Run the Road.",
               "<p>Every Prime Drivers client gets a single, dedicated dispatcher who learns your preferences, your home time and your goals — not a rotating call center.</p>",
               ["<strong>Dedicated dispatcher</strong> who knows your truck and your lanes.",
                "<strong>Real-time updates</strong> on every load and payment.",
                "<strong>Transparent pricing</strong> — flat percentage, no hidden fees.",
                "<strong>No contracts</strong> — stay because it works, not because you're locked in."],
               "Talk to a Dispatcher", wrap_cls="section soft")
    h += f"""
<section class="section">
  <div class="container">
    {section_head("How It Works", "Four Steps to Loaded", "Onboarding is fast, paperless and built around your preferences.")}
    {steps(STEPS)}
  </div>
</section>
<div>{cta()}</div>
"""
    h += footer()
    return h


def page_equipment():
    h = head("Equipment We Dispatch | Prime Drivers Logistics",
             "Box truck, dry van, reefer, flatbed, step deck, hotshot, power only, conestoga, lowboy and RGN dispatch.")
    h += header("equipment")
    h += page_hero("Equipment", "Equipment We Dispatch",
                   "From 26' box trucks to RGN heavy-haul — our dispatchers know the lanes, rates and requirements for your exact setup.",
                   "Tell Us What You Drive")
    h += road_ticker()
    h += f"""
<section class="section">
  <div class="container">
    {section_head("Whatever You Drive", "We Keep It Loaded", "Pick your equipment to see how we dispatch it.")}
    {equip_cards()}
  </div>
</section>
"""
    h += split("gallery-1.jpg", "Semi truck at sunset", "Specialized Freight", "Oversize, Heavy-Haul &amp; Open-Deck Experts",
               "<p>Specialized freight pays the most — and demands the most planning. We coordinate permits, route surveys, escorts and securement details so your Conestoga, lowboy or RGN runs smoothly.</p>",
               ["<strong>Permits coordinated</strong> state by state.",
                "<strong>Dimensions &amp; weights verified</strong> before you commit.",
                "<strong>Tarp and securement pay</strong> negotiated up front."],
               "Talk to a Dispatcher", wrap_cls="section soft")
    h += f"<div class='soft'>{cta()}</div>"
    h += footer()
    return h


def page_about():
    h = head("About Us | Prime Drivers Logistics",
             "Prime Drivers Logistics is a US truck dispatch company built to keep owner-operators loaded and profitable.")
    h += header("about")
    h += page_hero("About", "Built by People Who Know Trucking",
                   "We started Prime Drivers Logistics with one goal: give owner-operators the back-office muscle of a big carrier without giving up their independence.",
                   "Chat With Our Team")
    h += road_ticker(ticker=False)
    h += split("gallery-3.jpg", "Truck on a mountain highway", "Our Story", "Your Truck. Your Rules. Our Hustle.",
               "<p>Too many drivers were losing money to cheap loads, slow payments and endless paperwork. We built a dispatch desk that treats every truck like its own business — because it is.</p><p>Today we dispatch hundreds of owner-operators and small fleets across all 48 states, with a dedicated dispatcher for every client and support around the clock.</p>",
               ["<strong>Driver-first</strong> — you approve every load.",
                "<strong>Transparent</strong> — flat percentage, no surprises.",
                "<strong>Always on</strong> — 24/7 WhatsApp support."],
               "Talk to Our Team")
    h += f"""
<section class="stats">
  <div class="container grid grid-4">
    <div class="reveal"><div class="stat-num" data-count="618" data-suffix="+">0</div><div class="stat-label">Owner-Operators Onboard</div></div>
    <div class="reveal"><div class="stat-num" data-count="15891" data-suffix="+">0</div><div class="stat-label">Loads Booked</div></div>
    <div class="reveal"><div class="stat-num" data-count="48">0</div><div class="stat-label">States Covered</div></div>
    <div class="reveal"><div class="stat-num" data-count="86" data-suffix="%">0</div><div class="stat-label">Driver Retention</div></div>
  </div>
</section>
<section class="section">
  <div class="container">
    {section_head("Our Values", "What Drives Us")}
    {cards([
        ("🤝", "Honesty", "Every rate, every fee, every broker detail — shared openly with you before you commit."),
        ("⚡", "Speed", "Loads booked before you're empty, paperwork filed the moment you deliver."),
        ("💪", "Advocacy", "We negotiate like it's our own money on the line — because your success is our business."),
    ])}
  </div>
</section>
<div>{cta()}</div>
"""
    h += footer()
    return h


def page_contact():
    h = head("Contact Us | Prime Drivers Logistics",
             "Talk to a Prime Drivers dispatcher on WhatsApp — 24/7 support for owner-operators across the USA.")
    h += header("contact")
    h += page_hero("Contact", "Let's Get You Loaded",
                   "Skip the forms. Message a real dispatcher on WhatsApp and we'll have you set up and booking loads the same day.",
                   "Message Us on WhatsApp")
    h += road_ticker(ticker=False)
    h += f"""
<section class="section">
  <div class="container">
    {cards([
        ("💬", "WhatsApp", "The fastest way to reach us. Message anytime, day or night.", f'<div class="big"><a href="{WA}" target="_blank" rel="noopener">{PHONE}</a></div>'),
        ("💵", "Pricing", "No fixed tables — we tailor a rate to your truck. Ask us on WhatsApp.", f'<a class="card-link" href="{wa("Hi, I would like a custom dispatch quote")}" target="_blank" rel="noopener">Get a Custom Quote →</a>'),
        ("🌎", "Coverage &amp; Hours", "Serving owner-operators &amp; fleets across the USA.", '<div class="big">24/7 Dispatch Support</div>'),
    ])}
  </div>
</section>
"""
    h += split("office.jpg", "Prime Drivers dispatch office", "Why WhatsApp?", "Real People. Instant Answers.",
               "<p>We skipped the contact forms on purpose. When your truck is sitting or a broker is stalling, you don't want to fill out a form and wait — you want a dispatcher on the line. One tap and you're talking to us.</p>",
               ["<strong>Reply in minutes</strong>, not business days.",
                "<strong>Send photos</strong> of your COI, authority or rate con instantly.",
                "<strong>Same-day setup</strong> once we have your details."],
               "Start the Conversation", reverse=True, dark=True)
    send = [("Authority", "Your active MC/DOT number."),
            ("Insurance", "A current certificate of insurance (COI)."),
            ("Equipment", "Truck/trailer type and preferred lanes."),
            ("Goals", "Home time, target rate and any preferences.")]
    h += f"""
<section class="section">
  <div class="container">
    {section_head("Quick Start", "What to Send Us", "Have these ready and we'll have you booking loads the same day.")}
    {steps(send)}
    <div class="center" style="margin-top:44px">
      <a href="{wa("Hi Prime Drivers! Here are my details: MC/DOT: , Equipment: , Preferred lanes: ")}" target="_blank" rel="noopener" class="btn btn-amber">🚀 Send My Details on WhatsApp</a>
    </div>
  </div>
</section>
"""
    h += footer()
    return h


def main():
    pages = {
        "index.html": page_index(),
        "services.html": page_services(),
        "equipment.html": page_equipment(),
        "about.html": page_about(),
        "contact.html": page_contact(),
    }
    for slug, name, icon, short in DISPATCH:
        pages[f"dispatch-{slug}.html"] = page_dispatch(slug, name, icon, short)
    for fn, html in pages.items():
        with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
            f.write(html)
    print("wrote", len(pages), "pages")

if __name__ == "__main__":
    main()
