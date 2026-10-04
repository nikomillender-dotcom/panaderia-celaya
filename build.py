#!/usr/bin/env python3
"""Panadería Celaya — Multi-Page Bilingual Static Site Generator.
Generates:
  - EN: /, /menu/, /cakes/, /about/, /visit/
  - ES: /es/, /es/menu/, /es/cakes/, /es/about/, /es/visit/
  - sitemap.xml, robots.txt, manifest.webmanifest, favicon.svg, 404.html
"""

import json
import os
import html
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE = os.environ.get("SITE_URL", "https://www.panaderiacelaya.com").rstrip("/")
ORDER_ENDPOINT = os.environ.get("ORDER_ENDPOINT", "")

PHONE_DISPLAY = "(972) 522-7939"
PHONE_RAW = "+19725227939"
PHONE_E164 = "+1-972-522-7939"
ADDR = dict(street="906 W Marshall Dr", city="Grand Prairie", state="TX", zip="75051")
MAPS_Q = "Panaderia+Celaya+906+W+Marshall+Dr+Grand+Prairie+TX+75051"
CITIES = ["Grand Prairie", "Dallas", "Arlington", "Fort Worth", "Irving", "Mansfield", "Cedar Hill", "DeSoto", "Duncanville", "Lancaster", "Midlothian", "Mesquite", "Carrollton", "Garland"]

menu = json.load(open(ROOT / "src/menu.json", encoding="utf-8"))
e = html.escape

LOGO_SVG = '<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="29" fill="#f8b414" stroke="#472717" stroke-width="4"/><path d="M12 36a20 20 0 0 1 40 0z" fill="#e8368a" stroke="#472717" stroke-width="3"/><path d="M22 36c0-8 2-12 4-15M32 36V19M42 36c0-8-2-12-4-15" stroke="#fff7e8" stroke-width="3" fill="none" stroke-linecap="round"/><rect x="10" y="36" width="44" height="9" rx="4.5" fill="#fff7e8" stroke="#472717" stroke-width="3"/></svg>'

JS_STR = {
    "emptyT": ("Your basket is empty", "Tu canasta está vacía"),
    "emptyP": ("Add pan dulce from the menu — ¡antójate!", "Agrega pan dulce del menú — ¡antójate!"),
    "less": ("Remove one", "Quitar uno"),
    "more": ("Add one", "Agregar uno"),
    "priceAtPickup": ("price at pickup", "precio en tienda"),
    "subtotal": ("Subtotal", "Subtotal"),
    "fineUnknown": ("Some items are priced in-store; we'll confirm your total.", "Algunos productos se cobran en tienda; te confirmamos el total."),
    "fineKnown": ("Pay at pickup. Taxes may apply.", "Pagas al recoger. Pueden aplicar impuestos."),
    "added": ("Added to your order! 🥐", "¡Agregado a tu pedido! 🥐"),
    "msgHead": ("🥐 NEW PICKUP ORDER — Panaderia Celaya", "🥐 NUEVO PEDIDO PARA RECOGER — Panadería Celaya"),
    "lblSub": ("Subtotal", "Subtotal"),
    "lblName": ("Name", "Nombre"),
    "lblPhone": ("Phone", "Teléfono"),
    "lblPickup": ("Pickup", "Recoger"),
    "lblCake": ("Cake", "Pastel"),
    "lblNotes": ("Notes", "Notas"),
    "eName": ("Please enter your name.", "Escribe tu nombre."),
    "ePhone": ("Enter a 10-digit phone number.", "Escribe un teléfono de 10 dígitos."),
    "eDate": ("Pick a pickup date.", "Elige una fecha."),
    "eCake": ("Custom cakes need 3 days' notice.", "Los pasteles necesitan 3 días de anticipación."),
    "copied": ("Order copied!", "¡Pedido copiado!"),
    "copyFail": ("Select & copy the text", "Selecciona y copia el texto"),
    "openNow": ("Open now · until 8:45 PM", "Abierto ahora · hasta las 8:45 PM"),
    "closedNow": ("Closed now · opens 6 AM", "Cerrado ahora · abre a las 6 AM"),
}

COMMON = {
    "brand_sub": ("Grand Prairie, TX · desde 2007", "Grand Prairie, TX · desde 2007"),
    "nav_home": ("Home", "Inicio"),
    "nav_menu": ("Menu & Order", "Menú y Pedidos"),
    "nav_cakes": ("Custom Cakes", "Pasteles"),
    "nav_about": ("Our Story", "Nuestra Historia"),
    "nav_visit": ("Visit & Hours", "Visítanos"),
    "cart": ("Cart", "Carrito"),
    "skip": ("Skip to main content", "Saltar al contenido principal"),
    "open_loading": ("Hours: 6:00 AM – 8:45 PM", "Horario: 6:00 AM – 8:45 PM"),
    "bulletin1": ("🥖 Fresh morning bakes warm from 6:00 AM", "🥖 Pan recién salido del horno cada mañana"),
    "bulletin2": ("🫔 Weekend Tamales & Barbacoa (Sat & Sun mornings)", "🫔 Tamales y barbacoa calientitos sábados y domingos"),
    "bulletin3": ("🎂 Custom Tres Leches & celebration cakes", "🎂 Pasteles de tres leches y celebración sobre pedido"),
    "call_us": ("Call", "Llamar"),
    "order_pickup": ("Order for pickup", "Ordenar para recoger"),
    "m_call": ("📞 Call", "📞 Llamar"),
    "m_order": ("🧺 Order", "🧺 Ordenar"),
    "foot_desc": (
        "Authentic Mexican panadería proudly serving Grand Prairie, Arlington, Dallas, and the entire DFW Metroplex since 2007. Family recipes, baked fresh from scratch every morning.",
        "Auténtica panadería mexicana sirviendo con orgullo a Grand Prairie, Arlington, Dallas y todo el Metroplex de DFW desde 2007. Recetas de familia horneadas desde la madrugada."
    ),
    "serving": ("Serving", "Sirviendo a"),
    "rights": ("All rights reserved.", "Todos los derechos reservados."),
    "cart_h": ("Your Order", "Tu Pedido"),
    "close": ("Close", "Cerrar"),
    "f_name": ("Your name", "Tu nombre"),
    "f_phone": ("Phone number", "Teléfono celular"),
    "f_date": ("Pickup date", "Fecha de recogida"),
    "f_time": ("Pickup time", "Hora de recogida"),
    "f_notes": ("Special notes (optional)", "Notas especiales (opcional)"),
    "f_notes_ph": ("Allergies, extra candles, packaging preferences...", "Alergias, velitas, empaque especial..."),
    "cake_h": ("🎂 Custom Cake Request", "🎂 Detalles del Pastel"),
    "f_size": ("Size / Servings", "Tamaño / Porciones"),
    "f_size_ph": ("e.g. 1/2 sheet, 30 people, 10-inch round", "ej. 1/2 plancha, 30 personas, redondo 10 pulg."),
    "f_flavor": ("Flavor & filling", "Sabor y relleno"),
    "f_flavor_ph": ("e.g. Tres leches with fresh strawberries", "ej. Tres leches con fresas naturales"),
    "f_msg": ("Inscription on cake", "Mensaje escrito en el pastel"),
    "f_msg_ph": ("e.g. ¡Feliz Cumpleaños Mamá!", "ej. ¡Feliz Cumpleaños Mamá!"),
    "cake_note": ("Custom decorated cakes require at least 3 days advance notice.", "Los pasteles personalizados requieren al menos 3 días de anticipación."),
    "place": ("Send Order to Bakery", "Enviar Pedido a la Panadería"),
    "place_note": ("No payment charged online. We confirm your order and total by phone or text; pay at pickup.", "No se cobra nada en línea. Confirmamos tu pedido y total por teléfono o texto; pagas al recoger."),
    "done_h": ("¡Casi Listo!", "¡Casi Listo!"),
    "done_p": ("Your order summary is ready! Send it directly to the bakery via SMS text or give us a quick phone call.", "¡El resumen de tu pedido está listo! Envíalo por mensaje de texto SMS o llámanos para confirmarlo."),
    "sent_ok": ("✅ Your order notification was also transmitted to our bakery staff.", "✅ Tu pedido también fue enviado a nuestro equipo."),
    "send_sms": ("💬 Text Order via SMS", "💬 Enviar Pedido por Mensaje de Texto"),
    "tel_call": ("📞 Call to Confirm (972) 522-7939", "📞 Llamar para Confirmar (972) 522-7939"),
    "copy": ("Copy Summary", "Copiar Resumen"),
    "clear": ("Start New Order", "Nuevo Pedido"),
    "price_pickup": ("Price at pickup", "Precio en tienda"),
    "add_btn": ("Add", "Agregar"),
}

def ct(k, l):
    return COMMON[k][0 if l == "en" else 1]

def get_links(current_page, lang):
    """Returns dict of links and asset prefix based on page and lang."""
    if lang == "en":
        if current_page == "home":
            pre_assets = "./"
            links = {
                "home": "./",
                "menu": "menu/",
                "cakes": "cakes/",
                "about": "about/",
                "visit": "visit/",
                "alt_lang": "es/"
            }
        else:
            pre_assets = "../"
            links = {
                "home": "../",
                "menu": "../menu/",
                "cakes": "../cakes/",
                "about": "../about/",
                "visit": "../visit/",
                "alt_lang": f"../es/{current_page}/"
            }
    else:  # es
        if current_page == "home":
            pre_assets = "../"
            links = {
                "home": "./",
                "menu": "menu/",
                "cakes": "cakes/",
                "about": "about/",
                "visit": "visit/",
                "alt_lang": "../"
            }
        else:
            pre_assets = "../../"
            links = {
                "home": "../",
                "menu": "../menu/",
                "cakes": "../cakes/",
                "about": "../about/",
                "visit": "../visit/",
                "alt_lang": f"../../{current_page}/"
            }
    return pre_assets, links

def render_item_card(it, l, pre_assets):
    name = it[l]
    desc = it["d" + l]
    p = it["price"]
    if it.get("img"):
        alt_text = f"{name} — Panadería Celaya Grand Prairie TX"
        ph = f'<div class="ph"><img src="{pre_assets}assets/img/{it["img"]}" alt="{e(alt_text)}" loading="lazy" width="400" height="300">'
        if it.get("note"):
            tag_text = ("Seasonal", "De temporada")[0 if l == "en" else 1] if it["note"] == "seasonal" else ("Sat & Sun", "Sáb y Dom")[0 if l == "en" else 1]
            ph += f'<span class="tag">{tag_text}</span>'
        ph += "</div>"
    else:
        ic = {"tamal-p": "🫔", "tamal-c": "🫔", "barbacoa": "🌮", "flan": "🍮", "gelatina": "🍧", "pudin": "🥛"}.get(it["id"], "🥐")
        n = sum(map(ord, it["id"])) % 3
        ph = f'<div class="ph emo e{n}" role="img" aria-label="{e(name)}">{ic}'
        if it.get("note"):
            tag_text = ("Seasonal", "De temporada")[0 if l == "en" else 1] if it["note"] == "seasonal" else ("Sat & Sun", "Sáb y Dom")[0 if l == "en" else 1]
            ph += f'<span class="tag">{tag_text}</span>'
        ph += "</div>"
    price = f'<span class="price">${p:.2f}</span>' if p is not None else f'<span class="price ask">{ct("price_pickup", l)}</span>'
    less_lbl = e(JS_STR["less"][0 if l == "en" else 1])
    more_lbl = e(JS_STR["more"][0 if l == "en" else 1])
    return (
        f'<article class="item" data-id="{it["id"]}">{ph}<div class="bd"><h4>{e(name)}</h4><p>{e(desc)}</p>'
        f'<div class="row">{price}<button class="add" type="button">+ {ct("add_btn", l)}</button>'
        f'<span class="step"><button type="button" data-d="-1" aria-label="{less_lbl}">–</button><output>0</output><button type="button" data-d="1" aria-label="{more_lbl}">+</button></span></div></div></article>'
    )

def render_layout(page_id, lang, title, desc, keywords, canonical_url, content_html, schema_json):
    pre_assets, links = get_links(page_id, lang)
    alt_lang = "es" if lang == "en" else "en"
    alt_url = f"{BASE}/" if (lang == "es" and page_id == "home") else (f"{BASE}/es/" if (lang == "en" and page_id == "home") else (f"{BASE}/es/{page_id}/" if lang == "en" else f"{BASE}/{page_id}/"))

    # Active nav class helper
    def nav_cls(target):
        return "nav-link active" if target == page_id else "nav-link"

    # Language toggle HTML
    if lang == "en":
        lang_toggle = f'<div class="lang" role="group" aria-label="Language selection"><span aria-current="true">EN</span><a href="{links["alt_lang"]}" hreflang="es" lang="es" title="Cambiar a Español">ES</a></div>'
    else:
        lang_toggle = f'<div class="lang" role="group" aria-label="Selección de idioma"><a href="{links["alt_lang"]}" hreflang="en" lang="en" title="Switch to English">EN</a><span aria-current="true">ES</span></div>'

    items_js = {it["id"]: {"name": it[lang], "price": it["price"], "cake": bool(it.get("cake"))} for it in menu["items"]}
    cfg = {
        "lang": lang,
        "items": items_js,
        "t": {k: v[0 if lang == "en" else 1] for k, v in JS_STR.items()},
        "phoneRaw": PHONE_RAW,
        "endpoint": ORDER_ENDPOINT
    }

    cities_str = ", ".join(CITIES)

    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(keywords)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="Panadería Celaya">
<meta name="theme-color" content="#1b4fb0">
<link rel="canonical" href="{canonical_url}">
<link rel="alternate" hreflang="{lang}" href="{canonical_url}">
<link rel="alternate" hreflang="{alt_lang}" href="{alt_url}">
<link rel="alternate" hreflang="x-default" href="{BASE}/">
<!-- Local Geographic SEO -->
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="Grand Prairie">
<meta name="geo.position" content="32.7459;-96.9978">
<meta name="ICBM" content="32.7459, -96.9978">
<meta name="format-detection" content="telephone=yes">
<!-- Open Graph & Social -->
<meta property="og:type" content="restaurant.restaurant">
<meta property="og:site_name" content="Panadería Celaya">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical_url}">
<meta property="og:locale" content="{"en_US" if lang == "en" else "es_US"}">
<meta property="og:locale:alternate" content="{"es_US" if lang == "en" else "en_US"}">
<meta property="og:image" content="{BASE}/assets/og-cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Panadería Celaya Pan Dulce y Pasteles en Grand Prairie, Texas">
<meta property="restaurant:contact_info:street_address" content="{ADDR["street"]}">
<meta property="restaurant:contact_info:locality" content="{ADDR["city"]}">
<meta property="restaurant:contact_info:region" content="TX">
<meta property="restaurant:contact_info:postal_code" content="{ADDR["zip"]}">
<meta property="restaurant:contact_info:phone_number" content="{PHONE_E164}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{BASE}/assets/og-cover.jpg">
<link rel="icon" href="{pre_assets}favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{pre_assets}manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bagel+Fat+One&family=Caveat:wght@600&family=Nunito:wght@400;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre_assets}assets/styles.css">
<script type="application/ld+json">{schema_json}</script>
</head>
<body>
<a class="skip" href="#mainContent">{ct("skip", lang)}</a>
<div class="picado" aria-hidden="true"></div>
<header class="top">
  <div class="wrap">
    <a class="logo" href="{links["home"]}" aria-label="Panadería Celaya Inicio">
      {LOGO_SVG}
      <span>Panadería Celaya<small>{ct("brand_sub", lang)}</small></span>
    </a>
    <nav class="main" aria-label="Navigation">
      <a class="{nav_cls("home")}" href="{links["home"]}">{ct("nav_home", lang)}</a>
      <a class="{nav_cls("menu")}" href="{links["menu"]}">{ct("nav_menu", lang)}</a>
      <a class="{nav_cls("cakes")}" href="{links["cakes"]}">{ct("nav_cakes", lang)}</a>
      <a class="{nav_cls("about")}" href="{links["about"]}">{ct("nav_about", lang)}</a>
      <a class="{nav_cls("visit")}" href="{links["visit"]}">{ct("nav_visit", lang)}</a>
      {lang_toggle}
      <button class="cart-btn" type="button" data-open-cart aria-label="{ct("cart", lang)}">
        🧺 <span class="t">{ct("cart", lang)}</span> <b class="cart-count">0</b>
      </button>
      <button class="nav-toggle" id="navToggle" type="button" aria-expanded="false" aria-controls="mobileDrawer" aria-label="Toggle menu">☰</button>
    </nav>
  </div>
  <div class="mobile-drawer" id="mobileDrawer">
    <a class="{ "active" if page_id == "home" else "" }" href="{links["home"]}">{ct("nav_home", lang)}</a>
    <a class="{ "active" if page_id == "menu" else "" }" href="{links["menu"]}">{ct("nav_menu", lang)}</a>
    <a class="{ "active" if page_id == "cakes" else "" }" href="{links["cakes"]}">{ct("nav_cakes", lang)}</a>
    <a class="{ "active" if page_id == "about" else "" }" href="{links["about"]}">{ct("nav_about", lang)}</a>
    <a class="{ "active" if page_id == "visit" else "" }" href="{links["visit"]}">{ct("nav_visit", lang)}</a>
  </div>
</header>

<div class="bulletin-bar" role="region" aria-label="Bakery Announcements">
  <div class="wrap">
    <span>{ct("bulletin1", lang)}</span>
    <span class="dot-sep" aria-hidden="true">✿</span>
    <span>{ct("bulletin2", lang)}</span>
    <span class="dot-sep" aria-hidden="true">✿</span>
    <span>{ct("bulletin3", lang)}</span>
  </div>
</div>

<main id="mainContent">
{content_html}
</main>

<footer>
  <div class="wrap">
    <div>
      <h3>Panadería Celaya</h3>
      <p>{ct("foot_desc", lang)}</p>
      <div class="footer-links">
        <a href="{links["home"]}">{ct("nav_home", lang)}</a>
        <a href="{links["menu"]}">{ct("nav_menu", lang)}</a>
        <a href="{links["cakes"]}">{ct("nav_cakes", lang)}</a>
        <a href="{links["about"]}">{ct("nav_about", lang)}</a>
        <a href="{links["visit"]}">{ct("nav_visit", lang)}</a>
      </div>
      <p style="margin-top: 1rem;">© <span id="yr">2026</span> Panadería Celaya. {ct("rights", lang)}</p>
    </div>
    <div>
      <address style="font-style: normal; line-height: 1.6;">
        <strong>Panadería Celaya</strong><br>
        {ADDR["street"]}<br>
        {ADDR["city"]}, {ADDR["state"]} {ADDR["zip"]}<br>
        <a href="tel:{PHONE_RAW}" style="font-size: 1.15rem; font-weight: 800;">{PHONE_DISPLAY}</a>
      </address>
      <p class="cities"><strong>{ct("serving", lang)}:</strong> {cities_str}.</p>
    </div>
  </div>
</footer>

<div class="mbar">
  <a class="btn alt" href="tel:{PHONE_RAW}">{ct("m_call", lang)}</a>
  <button class="btn" type="button" data-open-cart>
    {ct("m_order", lang)} <b class="cart-count" style="background: var(--marigold); color: var(--choc); border-radius: 99px; padding: 0 0.5rem; margin-left: 0.3rem;">0</b>
  </button>
</div>

<!-- Persistent Cart Drawer -->
<div class="scrim" id="scrim"></div>
<aside class="drawer" id="drawer" role="dialog" aria-modal="true" aria-labelledby="dh" aria-hidden="true">
  <header>
    <h2 id="dh">🧺 {ct("cart_h", lang)}</h2>
    <button class="x" id="drawerClose" type="button" aria-label="{ct("close", lang)}">✕</button>
  </header>
  <div class="dbody">
    <div id="cartView">
      <div id="cartLines"></div>
      <form class="order" id="orderForm" novalidate hidden>
        <label>{ct("f_name", lang)}<input id="f-name" autocomplete="name" required><span class="err" id="e-name" role="alert"></span></label>
        <label>{ct("f_phone", lang)}<input id="f-phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="(972) 555-0123" required><span class="err" id="e-phone" role="alert"></span></label>
        <div class="two">
          <label>{ct("f_date", lang)}<input id="f-date" type="date" required><span class="err" id="e-date" role="alert"></span></label>
          <label>{ct("f_time", lang)}<select id="f-time"></select></label>
        </div>
        <p class="fine" id="cakeNote" hidden>🎂 {ct("cake_note", lang)}</p>
        <div class="cakebox" id="cakeBox">
          <strong>{ct("cake_h", lang)}</strong>
          <label>{ct("f_size", lang)}<input id="f-size" placeholder="{e(ct("f_size_ph", lang))}"></label>
          <label>{ct("f_flavor", lang)}<input id="f-flavor" placeholder="{e(ct("f_flavor_ph", lang))}"></label>
          <label>{ct("f_msg", lang)}<input id="f-msg" placeholder="{e(ct("f_msg_ph", lang))}"></label>
        </div>
        <label>{ct("f_notes", lang)}<textarea id="f-notes" rows="2" placeholder="{e(ct("f_notes_ph", lang))}"></textarea></label>
        <button class="btn" type="submit">{ct("place", lang)}</button>
        <p class="fine">{ct("place_note", lang)}</p>
      </form>
    </div>
    <div id="doneView" class="done" hidden>
      <div class="big">🎉</div>
      <h3>{ct("done_h", lang)}</h3>
      <p>{ct("done_p", lang)}</p>
      <p class="fine" id="sentOk" hidden>{ct("sent_ok", lang)}</p>
      <pre id="doneMsg"></pre>
      <div class="btns">
        <a class="btn" id="smsBtn" href="#">{ct("send_sms", lang)}</a>
        <a class="btn blue" id="callBtn" href="#">{ct("tel_call", lang)}</a>
        <button class="btn alt sm" id="copyBtn" type="button">📋 {ct("copy", lang)}</button>
        <button class="btn alt sm" id="clearBtn" type="button">{ct("clear", lang)}</button>
      </div>
    </div>
  </div>
</aside>

<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
  window.CELAYA = {json.dumps(cfg, ensure_ascii=False)};
  document.getElementById("yr").textContent = new Date().getFullYear();
</script>
<script src="{pre_assets}assets/app.js" defer></script>
</body>
</html>'''

# ==================== PAGE BUILDERS ====================

def build_home(lang):
    pre_assets, links = get_links("home", lang)
    if lang == "en":
        title = "Panaderia Celaya | Authentic Mexican Bakery in Grand Prairie & DFW"
        desc = "Fresh-baked Mexican pan dulce, conchas, bolillos, churros & tres leches cakes in Grand Prairie, TX. 18 years of artisan baking. Order online for pickup."
        keywords = "panaderia celaya, mexican bakery grand prairie, pan dulce dallas, conchas dallas, bolillos dfw, tres leches cake grand prairie, bakery near me"
        h1_a, h1_b, h1_c = "Traditional Mexican", "pan dulce,", "baked fresh daily"
        lead = "For 18 years, Panadería Celaya has brought the authentic flavors of Mexico to Grand Prairie and the DFW Metroplex — kneaded by hand before sunrise and baked with corazón."
        btn_menu = "Explore Full Menu"
        btn_cake = "Custom Cakes"
        stat1_t, stat1_l = "18 Years", "of Family Tradition"
        stat2_t, stat2_l = "4.8★", "Yelp Customer Rating"
        stat3_t, stat3_l = "6:00 AM", "Doors Open Every Day"
        seal_top, seal_bot = "18 Años", "Grand Prairie, TX"
        fresh_tag = "Baked Fresh Daily"
        
        # Ritual
        rit_eye = "The Authentic Experience"
        rit_h2 = "How to Panadería: Grab Your Tray & Tongs"
        rit_desc = "Stepping into Panadería Celaya is a beloved neighborhood tradition. Here is how our bakery works every single morning:"
        s1_h = "1. Grab Tray & Tongs"
        s1_p = "Take a metal tray (charola) and tongs at the entrance. Walk along our wooden glass cases and select your favorite conchas, bolillos, marranitos, and empanadas."
        s1_f = "Self-serve bakery display cases"
        s2_h = "2. Baked Fresh from 4:00 AM"
        s2_p = "Our bakers arrive hours before dawn to mix authentic doughs and fire the ovens. Warm bolillos and pillowy conchas hit the trays starting at 6:00 AM."
        s2_f = "Warm morning bakes guaranteed"
        s3_h = "3. Weekend Specials"
        s3_p = "Every Saturday and Sunday morning, we serve steaming authentic tamales (pork & chicken) and tender barbacoa by the pound. Come early before they sell out!"
        s3_f = "Saturdays & Sundays starting at 6 AM"

        # Featured
        feat_eye = "Bakery Highlights"
        feat_h2 = "Neighborhood Favorites"
        feat_desc = "A glimpse of what our bakers bring warm out of the ovens today."
        see_all = "See Complete 30+ Item Menu →"

        # Cake banner
        cake_eye = "Celebrations & Parties"
        cake_h2 = "Custom Cakes for Life's Sweetest Moments"
        cake_p = "From our celebrated Tres Leches cake adorned with fresh seasonal fruit to custom multi-tiered birthday and quinceañera cakes crafted with pride."
        cake_btn = "Explore Cake Options & Inquire"

        # Story snippet
        story_eye = "From the Owners"
        story_q = "“Eighteen years are easy to say, but they are filled with early dawns, hot ovens, and above all, a whole lot of heart. Our mission from day one has remained the same: to offer you the finest quality and a place where the aroma of fresh bread means home.”"
        story_sig = "— The Celaya Family"
        story_link = "Read Our Full 18-Year Story →"
        alt_hero = "Colorful Rosca de Reyes at Panaderia Celaya"
    else:
        title = "Panadería Celaya | Panadería Mexicana en Grand Prairie y DFW"
        desc = "Pan dulce mexicano recién horneado, conchas, bolillos, churros y pasteles de tres leches en Grand Prairie, TX. 18 años de tradición. Ordena para recoger."
        keywords = "panadería celaya, panadería mexicana grand prairie, pan dulce dallas, conchas dallas, bolillos dfw, pastel tres leches grand prairie, panadería cerca de mí"
        h1_a, h1_b, h1_c = "Pan dulce", "tradicional,", "recién horneado al día"
        lead = "A lo largo de 18 años, Panadería Celaya ha brindado el sabor auténtico de México a Grand Prairie y a todo el Metroplex de DFW — amasado antes del amanecer y horneado con mucho corazón."
        btn_menu = "Ver Menú Completo"
        btn_cake = "Pasteles para Eventos"
        stat1_t, stat1_l = "18 Años", "de Tradición Familiar"
        stat2_t, stat2_l = "4.8★", "Calificación en Yelp"
        stat3_t, stat3_l = "6:00 AM", "Abierto Todos los Días"
        seal_top, seal_bot = "18 Años", "Grand Prairie, TX"
        fresh_tag = "Horneado Fresco al Día"

        # Ritual
        rit_eye = "La Experiencia Auténtica"
        rit_h2 = "El Ritual de la Panadería: Charola y Pinzas"
        rit_desc = "Visitar Panadería Celaya es una tradición de barrio que une a las familias. Así se vive nuestra panadería cada mañana:"
        s1_h = "1. Toma tu Charola y Pinzas"
        s1_p = "Al entrar, toma tu charola de metal y tus pinzas. Recorre nuestras vitrinas de madera y elige a tu gusto conchas, bolillos, marranitos, cortadillos y empanadas."
        s1_f = "Vitrinas tradicionales de autoservicio"
        s2_h = "2. Horneado Desde las 4:00 AM"
        s2_p = "Nuestros panaderos comienzan su jornada de madrugada para amasar y calentar los hornos. El pan sale caliente y listo para llevar desde que abrimos a las 6:00 AM."
        s2_f = "Pan calientito garantizado por la mañana"
        s3_h = "3. Fin de Semana Tradicional"
        s3_p = "Cada sábado y domingo por la mañana tenemos tamales calientes (de puerco y pollo) y barbacoa por libra. ¡Llega temprano porque se acaban rápido!"
        s3_f = "Sábados y domingos desde las 6:00 AM"

        # Featured
        feat_eye = "Especialidades de la Casa"
        feat_h2 = "Los Consentidos de la Panadería"
        feat_desc = "Una probadita de lo que sale caliente de nuestros hornos cada mañana."
        see_all = "Ver Menú Completo (Más de 30 Variedades) →"

        # Cake banner
        cake_eye = "Celebraciones y Fiestas"
        cake_h2 = "Pasteles Hechos a Mano para tus Mejores Momentos"
        cake_p = "Desde nuestro legendario pastel de Tres Leches decorado con fruta natural fresca hasta pasteles personalizados para quinceañeras, bodas y cumpleaños."
        cake_btn = "Ver Diseños y Opciones de Pasteles"

        # Story snippet
        story_eye = "Mensaje de la Familia"
        story_q = "“Dieciocho años se dicen fácil, pero están llenos de madrugadas, de hornos calientes y, sobre todo, de mucho corazón. Desde el primer día nuestra misión ha sido ofrecerles la mejor calidad, siendo un lugar donde el aroma a pan fresco es sinónimo de hogar.”"
        story_sig = "— La Familia Celaya"
        story_link = "Conoce Nuestra Historia de 18 Años →"
        alt_hero = "Rosca de Reyes tradicional en Panadería Celaya"

    # Featured items cards (6 highlights)
    featured_ids = ["concha-v", "bolillo", "churro-c", "tres-leches", "marranito", "empanada"]
    feat_cards = "".join(render_item_card(it, lang, pre_assets) for it in menu["items"] if it["id"] in featured_ids)

    canonical_url = f"{BASE}/" if lang == "en" else f"{BASE}/es/"

    schema_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["Bakery", "LocalBusiness", "FoodEstablishment"],
                "@id": f"{BASE}/#bakery",
                "name": "Panaderia Celaya",
                "alternateName": ["Panadería Celaya", "Panaderia Celaya Grand Prairie"],
                "description": desc,
                "url": canonical_url,
                "telephone": PHONE_E164,
                "priceRange": "$",
                "servesCuisine": ["Mexican", "Bakery", "Pan Dulce"],
                "foundingDate": "2007",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": ADDR["street"],
                    "addressLocality": ADDR["city"],
                    "addressRegion": ADDR["state"],
                    "postalCode": ADDR["zip"],
                    "addressCountry": "US"
                },
                "openingHoursSpecification": [{
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    "opens": "06:00",
                    "closes": "20:45"
                }],
                "paymentAccepted": "Cash, Credit Card, Debit Card, NFC Mobile Payments",
                "areaServed": [{"@type": "City", "name": c + ", TX"} for c in CITIES]
            },
            {
                "@type": "WebSite",
                "@id": f"{BASE}/#website",
                "url": f"{BASE}/",
                "name": "Panaderia Celaya",
                "inLanguage": ["en", "es"]
            }
        ]
    }

    content_html = f'''
<section class="hero">
  <div class="wrap">
    <div>
      <span class="pill" id="openPill"><span class="dot"></span><span class="txt">{ct("open_loading", lang)}</span></span>
      <h1>{h1_a} <em>{h1_b}</em><br><span class="u">{h1_c}</span></h1>
      <p class="lead">{lead}</p>
      <div class="cta-group">
        <a class="btn" href="{links["menu"]}">🥐 {btn_menu}</a>
        <a class="btn alt" href="{links["cakes"]}">🎂 {btn_cake}</a>
      </div>
      <div class="hero-stats">
        <div><strong>{stat1_t}</strong><span>{stat1_l}</span></div>
        <div><strong>{stat2_t}</strong><span>{stat2_l}</span></div>
        <div><strong>{stat3_t}</strong><span>{stat3_l}</span></div>
      </div>
    </div>
    <div class="hero-visual">
      <div class="hero-frame">
        <img src="{pre_assets}assets/img/rosca.webp" alt="{e(alt_hero)}" width="440" height="550" fetchpriority="high">
      </div>
      <div class="artisan-seal">
        <strong>{seal_top}</strong>
        <span>{seal_bot}</span>
      </div>
      <div class="fresh-tag">✓ {fresh_tag}</div>
    </div>
  </div>
</section>

<section style="background: var(--white); border-block: 3px solid var(--choc);">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">{rit_eye}</span>
      <h2>{rit_h2}</h2>
      <p>{rit_desc}</p>
    </div>
    <div class="ritual-grid">
      <div class="ritual-card">
        <div class="step-num">Paso 1</div>
        <h3>{s1_h}</h3>
        <p>{s1_p}</p>
        <div class="card-footer">✓ {s1_f}</div>
      </div>
      <div class="ritual-card">
        <div class="step-num">Paso 2</div>
        <h3>{s2_h}</h3>
        <p>{s2_p}</p>
        <div class="card-footer">✓ {s2_f}</div>
      </div>
      <div class="ritual-card">
        <div class="step-num">Paso 3</div>
        <h3>{s3_h}</h3>
        <p>{s3_p}</p>
        <div class="card-footer">✓ {s3_f}</div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">{feat_eye}</span>
      <h2>{feat_h2}</h2>
      <p>{feat_desc}</p>
    </div>
    <div class="item-grid">{feat_cards}</div>
    <div style="text-align: center; margin-top: 2.5rem;">
      <a class="btn blue" href="{links["menu"]}">{see_all}</a>
    </div>
  </div>
</section>

<section style="background: var(--pink); color: #fff; border-block: 3px solid var(--choc);">
  <div class="wrap" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2.5rem; align-items: center;">
    <div>
      <span class="eyebrow" style="color: var(--marigold-l);">{cake_eye}</span>
      <h2 style="color: #fff;">{cake_h2}</h2>
      <p style="font-size: 1.15rem; margin: 1rem 0 1.8rem; line-height: 1.6;">{cake_p}</p>
      <a class="btn yel" href="{links["cakes"]}">🎂 {cake_btn}</a>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
      <img src="{pre_assets}assets/img/cake-fruit.webp" alt="Pastel de tres leches con fruta fresca" style="border: 4px solid var(--choc); border-radius: var(--r); aspect-ratio: 1; object-fit: cover; box-shadow: 8px 8px 0 var(--choc);">
      <img src="{pre_assets}assets/img/cake-love.webp" alt="Pastel de corazón artesanal" style="border: 4px solid var(--choc); border-radius: var(--r); aspect-ratio: 1; object-fit: cover; box-shadow: 8px 8px 0 var(--choc); margin-top: 1.5rem;">
    </div>
  </div>
</section>

<section>
  <div class="wrap" style="max-width: 52rem; text-align: center;">
    <span class="eyebrow">{story_eye}</span>
    <blockquote class="story-quote" style="text-align: left; margin: 1.2rem 0;">
      <p>{story_q}</p>
      <div class="sign" style="text-align: right;">{story_sig}</div>
    </blockquote>
    <a class="btn sm alt" href="{links["about"]}">{story_link}</a>
  </div>
</section>
'''
    return render_layout("home", lang, title, desc, keywords, canonical_url, content_html, json.dumps(schema_data, ensure_ascii=False))


def build_menu(lang):
    pre_assets, links = get_links("menu", lang)
    if lang == "en":
        title = "Pan Dulce Menu & Pickup Ordering | Panadería Celaya Grand Prairie"
        desc = "Complete Mexican bakery menu: conchas, bolillos, churros, marranitos, empanadas, tamales, and pasteles. Fresh daily. Build your pickup order online."
        keywords = "panaderia celaya menu, mexican sweet bread prices, conchas grand prairie, bolillo pickup, churros dfw, tres leches menu"
        banner_eye = "Baked Fresh Daily"
        banner_h1 = "Our Bakery Menu & Pickup Orders"
        banner_desc = "Select your favorite sweet breads, savory weekend specialties, and desserts. Add items to your basket and submit your pickup order."
        all_lbl = "All Varieties"
        note = "🥐 Prices shown reflect current in-shop listings. Items noted as 'price at pickup' are priced at the counter. Tamales & barbacoa are available weekends only (Saturdays & Sundays)."
    else:
        title = "Menú de Pan Dulce y Pedidos para Recoger | Panadería Celaya Grand Prairie"
        desc = "Menú completo de panadería mexicana: conchas, bolillos, churros, marranitos, empanadas, tamales y pasteles. Fresco a diario. Arma tu pedido para recoger."
        keywords = "menú panadería celaya, precios pan dulce, conchas grand prairie, bolillos dfw, churros cajeta, menú tres leches"
        banner_eye = "Horneado Fresco Cada Mañana"
        banner_h1 = "Menú de Panadería y Pedidos para Recoger"
        banner_desc = "Selecciona tus piezas favoritas de pan dulce, antojitos de fin de semana y pasteles. Agrega a tu canasta y envía tu pedido para recoger."
        all_lbl = "Todo el Menú"
        note = "🥐 Los precios mostrados corresponden a los publicados en tienda. Los productos con 'precio en tienda' se confirman al momento. Tamales y barbacoa disponibles únicamente fines de semana."

    filter_buttons = f'<button class="filter-btn active" type="button" data-cat="all">✿ {all_lbl}</button>'
    for c in menu["cats"]:
        filter_buttons += f'<button class="filter-btn" type="button" data-cat="{c["id"]}">{c["icon"]} {e(c[lang])}</button>'

    sections_html = ""
    for c in menu["cats"]:
        cards = "".join(render_item_card(it, lang, pre_assets) for it in menu["items"] if it["cat"] == c["id"])
        sections_html += f'''
<div class="cat-section" id="cat-{c["id"]}">
  <h3 class="cat-title"><span>{c["icon"]}</span> {e(c[lang])}</h3>
  <div class="item-grid">{cards}</div>
</div>'''

    canonical_url = f"{BASE}/menu/" if lang == "en" else f"{BASE}/es/menu/"

    schema_sections = []
    for c in menu["cats"]:
        items_schema = []
        for it in menu["items"]:
            if it["cat"] == c["id"]:
                m_obj = {"@type": "MenuItem", "name": it[lang], "description": it["d" + lang]}
                if it["price"] is not None:
                    m_obj["offers"] = {"@type": "Offer", "price": f'{it["price"]:.2f}', "priceCurrency": "USD"}
                items_schema.append(m_obj)
        schema_sections.append({"@type": "MenuSection", "name": c[lang], "hasMenuItem": items_schema})

    schema_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Menu",
                "@id": f"{canonical_url}#menu",
                "name": "Panaderia Celaya Menu",
                "url": canonical_url,
                "hasMenuSection": schema_sections
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Menu", "item": canonical_url}
                ]
            }
        ]
    }

    content_html = f'''
<div class="page-banner">
  <div class="wrap">
    <div class="breadcrumb">
      <a href="{links["home"]}">{ct("nav_home", lang)}</a>
      <span>/</span>
      <span>{ct("nav_menu", lang)}</span>
    </div>
    <span class="eyebrow">{banner_eye}</span>
    <h1>{banner_h1}</h1>
    <p class="banner-desc">{banner_desc}</p>
  </div>
</div>

<div class="menu-controls">
  <div class="wrap">
    <div class="menu-filters">{filter_buttons}</div>
  </div>
</div>

<section style="padding-top: 1rem;">
  <div class="wrap">
    {sections_html}
    <div class="weekend-alert" style="margin-top: 2rem;">
      <p>{note}</p>
    </div>
  </div>
</section>
'''
    return render_layout("menu", lang, title, desc, keywords, canonical_url, content_html, json.dumps(schema_data, ensure_ascii=False))


def build_cakes(lang):
    pre_assets, links = get_links("cakes", lang)
    if lang == "en":
        title = "Custom Cakes & Tres Leches | Panadería Celaya Grand Prairie TX"
        desc = "Traditional fruit-topped Tres Leches, custom birthday cakes, quinceañera cakes & celebration sheets in Grand Prairie. Order 3 days ahead."
        keywords = "tres leches cake grand prairie, custom cakes dallas, quinceanera cake dfw, birthday cake grand prairie, panaderia celaya cakes"
        banner_eye = "Celebrations & Special Moments"
        banner_h1 = "Custom Cakes & Legendary Tres Leches"
        banner_desc = "Baked with traditional sponge, soaked in our rich three-milk blend, and decorated with love for your birthdays, quinceañeras, weddings, and anniversaries."
        g1_h = "Signature Tres Leches"
        g1_p = "Our most beloved cake. Light, airy sponge cake soaked to perfection in our traditional tres leches recipe and topped with fresh fruit (strawberries, peaches, kiwi)."
        g1_items = ["Tres Leches con Fruta Natural", "Tres Leches Tradicional Chantilly", "Tres Leches con Fresa / Durazno"]
        g2_h = "Birthdays & Quinceañeras"
        g2_p = "Custom sheet cakes and tiered celebration cakes tailored with your colors, personalized inscriptions, and festive decorations."
        g2_items = ["Custom Inscriptions & Themes", "Round Cakes (8\", 10\", 12\")", "1/4 Sheet, 1/2 Sheet & Full Sheet"]
        g3_h = "How to Order Your Cake"
        g3_p = "Ready-to-go round tres leches cakes are stocked daily in our chilled display case. For custom themes and large sizes, please order at least 3 days in advance."
        g3_items = ["3 Days Advance Notice for Custom Orders", "Same-Day Round Tres Leches in Display Case", "Order Online or Call (972) 522-7939"]
        order_btn = "Request / Order a Cake Now"
        gal_h2 = "Real Cakes from Our Kitchen"
    else:
        title = "Pasteles Personalizados y Tres Leches | Panadería Celaya Grand Prairie TX"
        desc = "Tradicional pastel de Tres Leches con fruta natural, pasteles de cumpleaños, quinceañeras y bodas en Grand Prairie. Pide con 3 días de anticipación."
        keywords = "pastel tres leches grand prairie, pasteles personalizados dallas, pasteles quinceañera dfw, pastel cumpleaños grand prairie, pasteles panadería celaya"
        banner_eye = "Celebraciones y Momentos Especiales"
        banner_h1 = "Pasteles Personalizados y Tres Leches Tradicional"
        banner_desc = "Elaborados con pan esponja tradicional, humedecidos en nuestra receta secreta de tres leches y decorados con esmero para tus fiestas y reuniones."
        g1_h = "Tres Leches Inolvidable"
        g1_p = "El favorito de nuestras familias. Pan esponjoso perfectamente humedecido en leche, cubierto con crema chantilly y coronado con fruta natural fresca."
        g1_items = ["Tres Leches con Fruta Natural Fresca", "Tres Leches Tradicional de Vainilla", "Rellenos de Fresa, Durazno o Cajeta"]
        g2_h = "Cumpleaños y Quinceañeras"
        g2_p = "Pasteles de plancha y pisos personalizados con tu temática, dedicatorias especiales y decoraciones al gusto."
        g2_items = ["Dedicatoria Personalizada", "Pasteles Redondos (8\", 10\", 12\")", "1/4 de Plancha, 1/2 Plancha y Plancha Entera"]
        g3_h = "Cómo Encargar tu Pastel"
        g3_p = "Contamos con pasteles redondos de tres leches listos para llevar en nuestra vitrina fría todos los días. Para pedidos especiales y personalizados, encarga con 3 días."
        g3_items = ["3 Días de Anticipación para Personalizados", "Pasteles Listos para Llevar el Mismo Día", "Pide en Línea o Llama al (972) 522-7939"]
        order_btn = "Hacer Pedido de Pastel"
        gal_h2 = "Pasteles Reales Salidos de Nuestra Pastelería"

    canonical_url = f"{BASE}/cakes/" if lang == "en" else f"{BASE}/es/cakes/"

    schema_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Product",
                "name": "Panaderia Celaya Custom & Tres Leches Cakes",
                "description": desc,
                "url": canonical_url,
                "image": [f"{BASE}/assets/img/cake-fruit.webp", f"{BASE}/assets/img/cake-love.webp"],
                "offers": {
                    "@type": "AggregateOffer",
                    "priceCurrency": "USD",
                    "lowPrice": "15.00",
                    "highPrice": "120.00",
                    "offerCount": "10"
                }
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Cakes", "item": canonical_url}
                ]
            }
        ]
    }

    content_html = f'''
<div class="page-banner">
  <div class="wrap">
    <div class="breadcrumb">
      <a href="{links["home"]}">{ct("nav_home", lang)}</a>
      <span>/</span>
      <span>{ct("nav_cakes", lang)}</span>
    </div>
    <span class="eyebrow">{banner_eye}</span>
    <h1>{banner_h1}</h1>
    <p class="banner-desc">{banner_desc}</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="cake-guide-grid">
      <div class="guide-card">
        <h3>{g1_h}</h3>
        <p>{g1_p}</p>
        <ul>{"".join(f"<li>{x}</li>" for x in g1_items)}</ul>
      </div>
      <div class="guide-card">
        <h3>{g2_h}</h3>
        <p>{g2_p}</p>
        <ul>{"".join(f"<li>{x}</li>" for x in g2_items)}</ul>
      </div>
      <div class="guide-card">
        <h3>{g3_h}</h3>
        <p>{g3_p}</p>
        <ul>{"".join(f"<li>{x}</li>" for x in g3_items)}</ul>
      </div>
    </div>
    
    <div style="text-align: center; margin-bottom: 3.5rem;">
      <button class="btn yel" type="button" data-cake-order style="font-size: 1.2rem; padding: 0.9rem 2.2rem;">🎂 {order_btn}</button>
    </div>

    <div class="sec-head">
      <span class="eyebrow">Galería de Pastelería</span>
      <h2>{gal_h2}</h2>
    </div>
    <div class="cake-gallery-grid">
      <figure>
        <img src="{pre_assets}assets/img/cake-fruit.webp" alt="Pastel de Tres Leches con Fruta Natural Fresca" loading="lazy">
        <figcaption>Pastel de Tres Leches con Fruta Fresca</figcaption>
      </figure>
      <figure>
        <img src="{pre_assets}assets/img/cake-love.webp" alt="Pastel de Celebración con Decoración Elegante" loading="lazy">
        <figcaption>Pastel de Cumpleaños / Aniversario</figcaption>
      </figure>
      <figure>
        <img src="{pre_assets}assets/img/cakes-fridge.webp" alt="Vitrinas con pasteles listos para llevar" loading="lazy">
        <figcaption>Vitrina de Pasteles Listos para Llevar</figcaption>
      </figure>
      <figure>
        <img src="{pre_assets}assets/img/anniv.webp" alt="Pastel de Aniversario Panadería Celaya" loading="lazy">
        <figcaption>Pastel Conmemorativo de la Familia</figcaption>
      </figure>
    </div>
  </div>
</section>
'''
    return render_layout("cakes", lang, title, desc, keywords, canonical_url, content_html, json.dumps(schema_data, ensure_ascii=False))


def build_about(lang):
    pre_assets, links = get_links("about", lang)
    if lang == "en":
        title = "Our Story & 18 Years of Tradition | Panadería Celaya Grand Prairie"
        desc = "Since 2007, Panadería Celaya has crafted authentic Mexican sweet bread from scratch in Grand Prairie, TX. Read about our 18-year baking heritage."
        keywords = "about panaderia celaya, history panaderia celaya, grand prairie mexican bakery tradition, authentic pan dulce dallas"
        banner_eye = "Heritage & Dedication"
        banner_h1 = "18 Years of Sabor, Tradition & Family"
        banner_desc = "From 4:00 AM dough preparation to the warmth of our ovens on West Marshall Drive — celebrating nearly two decades of baking for our community."
        p1 = "For nearly 18 years, Panadería Celaya has been a warm gathering place for families across Grand Prairie, Arlington, Dallas, and the wider DFW Metroplex. What started with a commitment to authentic Mexican baking has grown into a cherished neighborhood landmark."
        p2 = "From day one, our mission has been simple: never cut corners. We bake the pillowy conchas that remind our guests of home, crusty bolillos for the family dinner table, real pumpkin-filled empanadas, handmade buñuelos, and sweet marranitos seasoned with genuine piloncillo."
        p3 = "Every piece of bread that leaves our display case carries the dedication of our bakery team, who arrive hours before dawn to knead, proof, bake, and decorate with tireless passion."
        quote_body = "“Eighteen years are easy to say, but they are filled with early dawns, hot ovens, and above all, a whole lot of heart. The real reason we are here, standing proud and grateful, is you, our customers. Thank you for making Panadería Celaya a place where the aroma of fresh bread means home.”"
        quote_sig = "— The Celaya Family"
        gal_h2 = "Inside the Panadería"
    else:
        title = "Nuestra Historia y 18 Años de Tradición | Panadería Celaya Grand Prairie"
        desc = "Desde 2007, Panadería Celaya elabora pan dulce mexicano artesanal en Grand Prairie, TX. Conoce nuestra historia de 18 años de hornos calientes."
        keywords = "historia panadería celaya, tradición panadería celaya grand prairie, pan dulce auténtico dallas, panadería mexicana artesanal"
        banner_eye = "Herencia y Dedicación"
        banner_h1 = "18 Años de Sabor, Tradición y Familia"
        banner_desc = "Desde las madrugadas preparando la masa hasta el calor de nuestros hornos en West Marshall Drive — celebrando casi dos décadas junto a nuestra comunidad."
        p1 = "A lo largo de casi 18 años, Panadería Celaya ha sido un punto de encuentro para familias de Grand Prairie, Arlington, Dallas y todo el Metroplex de DFW. Lo que comenzó como un sueño de compartir el auténtico sabor del pan dulce mexicano se ha convertido en una casa para todos."
        p2 = "Desde el primer día, nuestra misión ha sido la misma: ofrecerles la más alta calidad sin atajos. Horneamos esas ricas conchas que tanto les encantan, el crujiente y noble bolillo para la mesa de cada día, empanadas con relleno de calabaza de verdad y buñuelos como los que hacía la abuela."
        p3 = "Cada pieza, desde la más sencilla hasta el pastel más elaborado, lleva consigo el cariño de un equipo que amasa, hornea y decora con una pasión inagotable antes de que salga el sol."
        quote_body = "“Dieciocho años se dicen fácil, pero están llenos de madrugadas, de hornos calientes y, sobre todo, de mucho corazón. La verdadera razón de que estemos aquí, firmes y felices, son ustedes, nuestros clientes. Gracias por su fidelidad y por permitirnos ser parte de sus mesas.”"
        quote_sig = "— La Familia Celaya"
        gal_h2 = "Rincones de Nuestra Panadería"

    canonical_url = f"{BASE}/about/" if lang == "en" else f"{BASE}/es/about/"

    schema_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "AboutPage",
                "@id": f"{canonical_url}#about",
                "name": "About Panaderia Celaya",
                "description": desc,
                "url": canonical_url
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "About", "item": canonical_url}
                ]
            }
        ]
    }

    content_html = f'''
<div class="page-banner">
  <div class="wrap">
    <div class="breadcrumb">
      <a href="{links["home"]}">{ct("nav_home", lang)}</a>
      <span>/</span>
      <span>{ct("nav_about", lang)}</span>
    </div>
    <span class="eyebrow">{banner_eye}</span>
    <h1>{banner_h1}</h1>
    <p class="banner-desc">{banner_desc}</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="story-split">
      <div class="story-text">
        <p>{p1}</p>
        <p>{p2}</p>
        <p>{p3}</p>
        <blockquote class="story-quote">
          <p>{quote_body}</p>
          <div class="sign">{quote_sig}</div>
        </blockquote>
      </div>
      <div>
        <img src="{pre_assets}assets/img/interior.webp" alt="Vitrinas de madera en Panadería Celaya" style="border: 4px solid var(--choc); border-radius: var(--r-lg); box-shadow: 12px 12px 0 var(--cobalt); width: 100%;">
      </div>
    </div>

    <div class="sec-head">
      <span class="eyebrow">Nuestras Raíces</span>
      <h2>{gal_h2}</h2>
    </div>
    <div class="gallery-grid">
      <img src="{pre_assets}assets/img/storefront.webp" alt="Fachada exterior de Panadería Celaya en Grand Prairie" loading="lazy">
      <img src="{pre_assets}assets/img/conchas-rack.webp" alt="Charolas de conchas recién horneadas" loading="lazy">
      <img src="{pre_assets}assets/img/bolillos.webp" alt="Bolillos calientes en la charola" loading="lazy">
      <img src="{pre_assets}assets/img/churros.webp" alt="Churros frescos y antojitos" loading="lazy">
      <img src="{pre_assets}assets/img/tray.webp" alt="Charola surtida de pan dulce" loading="lazy">
      <img src="{pre_assets}assets/img/case.webp" alt="Vitrina de panadería tradicional" loading="lazy">
    </div>
  </div>
</section>
'''
    return render_layout("about", lang, title, desc, keywords, canonical_url, content_html, json.dumps(schema_data, ensure_ascii=False))


def build_visit(lang):
    pre_assets, links = get_links("visit", lang)
    if lang == "en":
        title = "Visit Us, Hours & Weekend Specials | Panadería Celaya Grand Prairie TX"
        desc = "Visit Panadería Celaya at 906 W Marshall Dr, Grand Prairie TX. Open 6:00 AM – 8:45 PM daily. Weekend hot tamales and fresh barbacoa. Directions & map."
        keywords = "panaderia celaya hours, panaderia celaya address, bakery grand prairie tx, tamales grand prairie saturday sunday, barbacoa grand prairie"
        banner_eye = "We Look Forward to Seeing You"
        banner_h1 = "Visit Panadería Celaya in Grand Prairie"
        banner_desc = "Conveniently located on West Marshall Drive with free parking and wheelchair accessibility. Come early for warm morning breads!"
        hours_h = "Store Hours"
        dir_btn = "Get Google Maps Directions"
        call_btn = "Call the Bakery"
        wknd_h = "Weekend Specials: Hot Tamales & Barbacoa"
        wknd_p = "Every Saturday and Sunday starting at 6:00 AM, we offer hot pork & chicken tamales and savory barbacoa by the pound. They sell out fast — come early in the morning!"
        faq_eye = "Frequently Asked Questions"
        faq_h2 = "Helpful Visitor Information"
        days_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        faqs = [
            ("What time does warm bread come out?", "Our bakers begin at 4:00 AM, and the first warm trays of conchas and bolillos hit the cases when doors open at 6:00 AM."),
            ("Where are you located and is there parking?", "We are at 906 W Marshall Dr, Grand Prairie, TX 75051. We have a dedicated free customer parking lot with easy wheelchair access."),
            ("What payment methods do you accept?", "We accept cash, Visa, MasterCard, Discover, Amex, and NFC mobile payments (Apple Pay, Google Pay)."),
            ("How do weekend tamales and barbacoa work?", "They are available Saturday and Sunday mornings only. Due to high demand, they often sell out by 9:00 AM, so morning arrival is strongly encouraged.")
        ]
        perks = ["Free Customer Parking", "Wheelchair Accessible Entrance", "Cards & Contactless NFC Accepted", "Takeout Available", "Dogs Welcome Outside"]
    else:
        title = "Visítanos, Horarios y Especiales de Fin de Semana | Panadería Celaya"
        desc = "Visita Panadería Celaya en 906 W Marshall Dr, Grand Prairie TX. Abierto de 6:00 AM a 8:45 PM diario. Tamales y barbacoa los fines de semana. Mapa y ubicación."
        keywords = "horario panadería celaya, dirección panadería celaya grand prairie, tamales grand prairie fin de semana, barbacoa grand prairie texas"
        banner_eye = "Te Esperamos con Gusto"
        banner_h1 = "Visita Panadería Celaya en Grand Prairie"
        banner_desc = "Ubicados sobre West Marshall Drive con estacionamiento gratuito y acceso para sillas de ruedas. ¡Llega temprano para disfrutar el pan caliente!"
        hours_h = "Horario de Atención"
        dir_btn = "Cómo Llegar en Google Maps"
        call_btn = "Llamar a la Panadería"
        wknd_h = "Especiales de Fin de Semana: Tamales y Barbacoa"
        wknd_p = "Todos los sábados y domingos a partir de las 6:00 AM tenemos tamales calientes (de puerco y pollo) y deliciosa barbacoa por libra. ¡Se agotan rápido, llega por la mañana!"
        faq_eye = "Preguntas Frecuentes"
        faq_h2 = "Información Útil para tu Visita"
        days_names = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        faqs = [
            ("¿A qué hora sale el pan calientito?", "Comenzamos a hornear desde las 4:00 AM. El pan dulce y los bolillos calientes salen en sus charolas a partir de las 6:00 AM."),
            ("¿Dónde están ubicados y hay estacionamiento?", "Estamos en 906 W Marshall Dr, Grand Prairie, TX 75051. Contamos con estacionamiento gratuito y rampa para sillas de ruedas."),
            ("¿Qué métodos de pago reciben?", "Aceptamos efectivo, tarjetas de crédito y débito (Visa, Mastercard, Amex) y pagos móviles NFC (Apple Pay y Google Pay)."),
            ("¿Cómo funciona la venta de tamales y barbacoa?", "Se venden exclusivamente sábados y domingos por la mañana. Por su alta demanda, suelen agotarse alrededor de las 9:00 AM.")
        ]
        perks = ["Estacionamiento Gratis", "Entrada Accesible para Sillas de Ruedas", "Tarjetas y Pagos Móviles NFC", "Servicio para Llevar", "Perritos Bienvenidos"]

    hours_rows = "".join(f'<tr><td>{d}</td><td>6:00 AM – 8:45 PM</td></tr>' for d in days_names)
    perks_html = "".join(f'<span>✓ {p}</span>' for p in perks)
    faqs_html = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faqs)

    canonical_url = f"{BASE}/visit/" if lang == "en" else f"{BASE}/es/visit/"

    schema_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["Place", "LocalBusiness"],
                "@id": f"{canonical_url}#place",
                "name": "Panaderia Celaya Grand Prairie",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": ADDR["street"],
                    "addressLocality": ADDR["city"],
                    "addressRegion": ADDR["state"],
                    "postalCode": ADDR["zip"],
                    "addressCountry": "US"
                },
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": 32.7459,
                    "longitude": -96.9978
                },
                "telephone": PHONE_E164,
                "hasMap": f"https://www.google.com/maps/search/?api=1&query={MAPS_Q}"
            },
            {
                "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Visit", "item": canonical_url}
                ]
            }
        ]
    }

    content_html = f'''
<div class="page-banner">
  <div class="wrap">
    <div class="breadcrumb">
      <a href="{links["home"]}">{ct("nav_home", lang)}</a>
      <span>/</span>
      <span>{ct("nav_visit", lang)}</span>
    </div>
    <span class="eyebrow">{banner_eye}</span>
    <h1>{banner_h1}</h1>
    <p class="banner-desc">{banner_desc}</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="weekend-alert">
      <strong>🫔 {wknd_h}</strong>
      <p>{wknd_p}</p>
    </div>

    <div class="visit-layout">
      <div>
        <div class="visit-box">
          <h3>📍 {ADDR["street"]}, {ADDR["city"]}, {ADDR["state"]} {ADDR["zip"]}</h3>
          <p style="margin: 0.4rem 0 1.2rem;"><a href="tel:{PHONE_RAW}" style="font-weight: 800; font-size: 1.2rem;">{PHONE_DISPLAY}</a></p>
          
          <h4 style="font-family: var(--display); font-size: 1.25rem;">🕒 {hours_h}</h4>
          <table class="hours-table" id="hoursTbl">{hours_rows}</table>
          
          <div style="display: flex; gap: 0.8rem; flex-wrap: wrap; margin-top: 1.4rem;">
            <a class="btn sm blue" href="https://www.google.com/maps/dir/?api=1&destination={MAPS_Q}" target="_blank" rel="noopener">🧭 {dir_btn}</a>
            <a class="btn sm alt" href="tel:{PHONE_RAW}">📞 {call_btn}</a>
          </div>

          <div class="perks-list">{perks_html}</div>
        </div>
      </div>
      
      <div class="map-frame">
        <iframe title="Ubicación de Panadería Celaya en Grand Prairie Texas" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={MAPS_Q}&output=embed"></iframe>
      </div>
    </div>
  </div>
</section>

<section style="background: var(--white); border-top: 3px solid var(--choc);">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">{faq_eye}</span>
      <h2>{faq_h2}</h2>
    </div>
    <div class="faq-box">{faqs_html}</div>
  </div>
</section>
'''
    return render_layout("visit", lang, title, desc, keywords, canonical_url, content_html, json.dumps(schema_data, ensure_ascii=False))


# ==================== MAIN EXECUTION ====================

def main():
    # Make directories
    for path_str in ["", "menu", "cakes", "about", "visit", "es", "es/menu", "es/cakes", "es/about", "es/visit"]:
        (ROOT / path_str).mkdir(parents=True, exist_ok=True)

    # 1. English Pages
    (ROOT / "index.html").write_text(build_home("en"), encoding="utf-8")
    (ROOT / "menu/index.html").write_text(build_menu("en"), encoding="utf-8")
    (ROOT / "cakes/index.html").write_text(build_cakes("en"), encoding="utf-8")
    (ROOT / "about/index.html").write_text(build_about("en"), encoding="utf-8")
    (ROOT / "visit/index.html").write_text(build_visit("en"), encoding="utf-8")

    # 2. Spanish Pages
    (ROOT / "es/index.html").write_text(build_home("es"), encoding="utf-8")
    (ROOT / "es/menu/index.html").write_text(build_menu("es"), encoding="utf-8")
    (ROOT / "es/cakes/index.html").write_text(build_cakes("es"), encoding="utf-8")
    (ROOT / "es/about/index.html").write_text(build_about("es"), encoding="utf-8")
    (ROOT / "es/visit/index.html").write_text(build_visit("es"), encoding="utf-8")

    # 3. Sitemap.xml (all 10 pages with proper alternates)
    pages_list = ["", "menu/", "cakes/", "about/", "visit/"]
    sitemap_entries = ""
    for p in pages_list:
        en_loc = f"{BASE}/{p}"
        es_loc = f"{BASE}/es/{p}"
        sitemap_entries += f'''  <url>
    <loc>{en_loc}</loc>
    <changefreq>weekly</changefreq>
    <priority>{"1.0" if p == "" else "0.9"}</priority>
    <xhtml:link rel="alternate" hreflang="en" href="{en_loc}"/>
    <xhtml:link rel="alternate" hreflang="es" href="{es_loc}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{en_loc}"/>
  </url>
  <url>
    <loc>{es_loc}</loc>
    <changefreq>weekly</changefreq>
    <priority>{"1.0" if p == "" else "0.9"}</priority>
    <xhtml:link rel="alternate" hreflang="en" href="{en_loc}"/>
    <xhtml:link rel="alternate" hreflang="es" href="{es_loc}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{en_loc}"/>
  </url>
'''

    (ROOT / "sitemap.xml").write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
{sitemap_entries}</urlset>
''', encoding="utf-8")

    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")

    (ROOT / "manifest.webmanifest").write_text(json.dumps({
        "name": "Panadería Celaya",
        "short_name": "Celaya",
        "description": "Authentic Mexican bakery in Grand Prairie TX. Fresh pan dulce daily.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#fff7e8",
        "theme_color": "#1b4fb0",
        "icons": [{"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"}]
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    (ROOT / "favicon.svg").write_text(LOGO_SVG.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" '), encoding="utf-8")

    (ROOT / "404.html").write_text('''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>404 — Panadería Celaya</title>
<style>
  body { font-family: system-ui, sans-serif; text-align: center; padding: 4rem 1.5rem; background: #fff7e8; color: #472717; }
  h1 { font-size: 2.2rem; margin-top: 1rem; }
  p { font-size: 1.2rem; max-width: 32rem; margin: 1rem auto; }
  a { display: inline-block; margin: 0.5rem; padding: 0.6rem 1.2rem; background: #e8368a; color: #fff; text-decoration: none; border-radius: 99px; font-weight: bold; }
</style>
</head>
<body>
  <div style="font-size: 5rem;">🥐</div>
  <h1>¡Ay! Esta página se acabó, como el bolillo de las 4 PM.</h1>
  <p>No pudimos encontrar la página que buscas. Regresa a nuestro inicio para ver todo nuestro pan dulce recién horneado.</p>
  <a href="/">Ir a Inicio (English)</a>
  <a href="/es/">Ir a Inicio (Español)</a>
</body>
</html>''', encoding="utf-8")

    print(f"Successfully generated 10 bilingual pages and SEO assets for {BASE}")

if __name__ == "__main__":
    main()
