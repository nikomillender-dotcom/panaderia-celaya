#!/usr/bin/env python3
"""Build the bilingual Panadería Celaya site.  Usage:  SITE_URL=https://yourdomain.com python3 build.py
Outputs: index.html (EN), es/index.html (ES), sitemap.xml, robots.txt, manifest.webmanifest, 404.html, favicon.svg
"""
import json, os, html, pathlib

ROOT = pathlib.Path(__file__).parent
# TODO: set to the real domain before launch (pancelaya.com did not resolve when this was built).
BASE = os.environ.get("SITE_URL", "https://www.panaderiacelaya.com").rstrip("/")
# TODO (optional): a Formspree/Basin/etc. endpoint so orders arrive by email automatically. Leave "" to use text/call flow.
ORDER_ENDPOINT = os.environ.get("ORDER_ENDPOINT", "")

PHONE_DISPLAY, PHONE_RAW, PHONE_E164 = "(972) 522-7939", "+19725227939", "+1-972-522-7939"
ADDR = dict(street="906 W Marshall Dr", city="Grand Prairie", state="TX", zip="75051")
MAPS_Q = "Panaderia+Celaya+906+W+Marshall+Dr+Grand+Prairie+TX+75051"
CITIES = ["Grand Prairie", "Dallas", "Arlington", "Fort Worth", "Irving", "Mansfield", "Cedar Hill", "DeSoto", "Duncanville", "Lancaster", "Midlothian", "Mesquite", "Carrollton", "Garland"]

menu = json.load(open(ROOT / "src/menu.json", encoding="utf-8"))
e = html.escape

# ---------------------------------------------------------------- copy (en, es)
X = {
 "title": ("Panaderia Celaya | Best Mexican Bakery in Grand Prairie & DFW — Pan Dulce, Tres Leches & Custom Cakes",
           "Panadería Celaya | Panadería Mexicana en Grand Prairie y DFW — Pan Dulce, Pasteles de Tres Leches y Pasteles Personalizados"),
 "desc": ("Fresh-baked Mexican pan dulce, conchas, bolillos, churros, tamales & tres leches cakes in Grand Prairie, TX. Serving Dallas–Fort Worth for 18 years. Order online for pickup.",
          "Pan dulce mexicano recién horneado, conchas, bolillos, churros, tamales y pasteles de tres leches en Grand Prairie, TX. Sirviendo a Dallas–Fort Worth por 18 años. Ordena en línea para recoger."),
 "keywords": ("panaderia celaya, mexican bakery grand prairie, panaderia grand prairie tx, bakery near me, panaderia near me, pan dulce dallas, pan dulce DFW, conchas, bolillos, tres leches cake dallas, custom cakes grand prairie, quinceanera cakes DFW, rosca de reyes dallas, tamales grand prairie, barbacoa grand prairie, churros, best bakery arlington tx, panaderia mexicana cerca de mi",
              "panadería celaya, panadería mexicana grand prairie, panadería en grand prairie tx, panadería cerca de mí, pan dulce dallas, pan dulce DFW, conchas, bolillos, pastel de tres leches dallas, pasteles personalizados grand prairie, pasteles de quinceañera DFW, rosca de reyes dallas, tamales grand prairie, barbacoa grand prairie, churros, panadería mexicana cerca de mí"),
 "nav_menu": ("Menu", "Menú"), "nav_cakes": ("Cakes", "Pasteles"), "nav_visit": ("Visit", "Visítanos"), "nav_faq": ("FAQ", "Preguntas"),
 "order": ("Order", "Ordenar"), "cart": ("Cart", "Carrito"), "skip": ("Skip to content", "Saltar al contenido"),
 "open_loading": ("Hours: 6 AM – 8:45 PM", "Horario: 6 AM – 8:45 PM"),
 "h1a": ("Warm", "Pan"), "h1b": ("pan dulce", "dulce"), "h1c": ("baked fresh every morning", "recién horneado cada mañana"),
 "lead": ("Conchas, bolillos, churros and the best tres leches in Grand Prairie — made with corazón for 18 years, right here in DFW.",
          "Conchas, bolillos, churros y el mejor tres leches de Grand Prairie — hecho con corazón por 18 años, aquí en DFW."),
 "cta1": ("Order for pickup", "Ordena para recoger"), "cta2": ("See the menu", "Ver el menú"),
 "stat1": ("years of sabor", "años de sabor"), "stat2": ("stars on Yelp", "estrellas en Yelp"), "stat3": ("daily, from 6 AM", "diario, desde las 6 AM"),
 "stk_a": ("18", "18"), "stk_a2": ("años", "años"), "stk_b": ("Fresh daily!", "¡Fresco diario!"),
 "alt_hero": ("Colorful Rosca de Reyes at Panaderia Celaya in Grand Prairie, Texas", "Rosca de Reyes colorida en Panadería Celaya, Grand Prairie, Texas"),
 "marq": (["¡Buenos días!", "Conchas", "Bolillos", "Churros", "Tres Leches", "Empanadas", "Tamales", "Pastel de Cumpleaños", "Buñuelos", "Marranitos", "¡Ven temprano!"],
          ["¡Buenos días!", "Conchas", "Bolillos", "Churros", "Tres Leches", "Empanadas", "Tamales", "Pastel de Cumpleaños", "Buñuelos", "Marranitos", "¡Ven temprano!"]),
 "why_h": ("Why DFW loves Celaya", "Por qué DFW ama Celaya"), "why_e": ("Hecho con amor", "Hecho con amor"),
 "why1t": ("Baked fresh, daily", "Horneado fresco, a diario"), "why1p": ("Warm bread hits the shelves every morning. Come early for the softest conchas — and the bolillos (they fly!).", "El pan caliente sale cada mañana. Ven temprano por las conchas más suaves — y por los bolillos (¡vuelan!)."),
 "why2t": ("Traditional & real", "Tradicional y auténtico"), "why2p": ("Real pumpkin in the empanadas, homemade-style buñuelos, marranitos and cortadillos. Just like abuela's.", "Empanadas con calabaza de verdad, buñuelos, marranitos y cortadillos como los de casa. Como los de la abuela."),
 "why3t": ("Cakes for every fiesta", "Pasteles para cada fiesta"), "why3p": ("Tres leches, birthdays, quinceañeras, graduations. Great prices — many treats under a dollar.", "Tres leches, cumpleaños, quinceañeras, graduaciones. Buenos precios — muchos antojitos a menos de un dólar."),
 "menu_h": ("Our menu", "Nuestro menú"), "menu_e": ("¡Antójate!", "¡Antójate!"),
 "menu_p": ("Tap + to build your order for pickup. Our selection changes daily — we'll confirm what's fresh when we reach out.", "Toca + para armar tu pedido y recogerlo. Nuestra selección cambia a diario — te confirmamos qué hay fresco."),
 "menu_note": ("🥐 Prices shown are today's listed prices. Items marked “price at pickup” are priced in the shop — we'll confirm your total. Tamales & barbacoa are weekends only.",
               "🥐 Los precios mostrados son los publicados. Los productos con “precio en tienda” se cobran al recoger — te confirmamos el total. Tamales y barbacoa solo en fin de semana."),
 "add": ("Add", "Agregar"), "ask": ("Price at pickup", "Precio en tienda"), "seasonal": ("Seasonal", "De temporada"), "weekend": ("Sat & Sun", "Sáb y Dom"),
 "cakes_e": ("Pasteles", "Pasteles"), "cakes_h": ("Cakes for your biggest moments", "Pasteles para tus momentos más especiales"),
 "cakes_p": ("From last-minute tres leches to custom birthday, quinceañera and wedding cakes — decorated with love. Call or order three days ahead for the very best.",
             "Desde un tres leches de último minuto hasta pasteles personalizados de cumpleaños, quinceañera y boda — decorados con cariño. Llama o pide con tres días de anticipación."),
 "cakes_l": (["Tres leches — with or without fresh fruit", "Birthday, quinceañera, graduation & wedding cakes", "Cheesecake, carrot cake, flan & more", "Custom messages & decorations"],
             ["Tres leches — con o sin fruta fresca", "Pasteles de cumpleaños, quinceañera, graduación y boda", "Cheesecake, pastel de zanahoria, flan y más", "Mensajes y decoraciones personalizadas"]),
 "cakes_cta": ("Order a cake", "Ordenar un pastel"),
 "alt_c1": ("Tres leches cake topped with fresh fruit", "Pastel de tres leches con fruta fresca"), "alt_c2": ("Decorated cake at Panaderia Celaya", "Pastel decorado en Panadería Celaya"),
 "story_e": ("Nuestra historia", "Nuestra historia"), "story_h": ("18 years of sabor y tradición", "18 años de sabor y tradición"),
 "story_p": ("For almost two decades Panaderia Celaya has brought a little taste of Mexico to Grand Prairie through its pan dulce. Every concha, every bolillo and every cake carries the dedication of a team that kneads, bakes and decorates with endless passion — a place where the smell of fresh bread means home.",
             "Por casi dos décadas Panadería Celaya ha traído un poquito del sabor mexicano a Grand Prairie a través de su pan dulce. Cada concha, cada bolillo y cada pastel lleva la dedicación de un equipo que amasa, hornea y decora con pasión. Un lugar donde el aroma a pan fresco es sinónimo de hogar."),
 "story_q": ("“Dieciocho años se dicen fácil, pero están llenos de madrugadas, de hornos calientes y, sobre todo, de mucho corazón… Gracias por su fidelidad.”",
             "“Dieciocho años se dicen fácil, pero están llenos de madrugadas, de hornos calientes y, sobre todo, de mucho corazón… Gracias por su fidelidad.”"),
 "story_s": ("— The Celaya family", "— La familia Celaya"),
 "cap1": ("Conchas!", "¡Conchas!"), "cap2": ("Fresh rolls", "Bolillos"), "cap3": ("Muffins", "Panquecitos"),
 "alt_p1": ("Plate of conchas and pan dulce", "Plato de conchas y pan dulce"), "alt_p2": ("Fresh bolillos on a baking tray", "Bolillos frescos en charola"), "alt_p3": ("Golden quesadilla de atole muffin", "Quesadilla de atole dorada"),
 "gal_e": ("Peek inside", "Échale un vistazo"), "gal_h": ("Welcome to the panadería", "Bienvenido a la panadería"),
 "alts": (["Racks of colorful pan dulce", "Trays of cinnamon pastries", "Display case full of pan dulce", "Pastry and muffin case", "Fresh churros and chocolate-dipped treats", "Panaderia Celaya storefront in Grand Prairie", "Cakes in the refrigerated case", "Tray of conchas, cuernitos and pan dulce"],
          ["Charolas de pan dulce colorido", "Charolas de pastelitos con canela", "Vitrina llena de pan dulce", "Vitrina de panqués y muffins", "Churros frescos y antojitos con chocolate", "Fachada de Panadería Celaya en Grand Prairie", "Pasteles en el refrigerador", "Charola de conchas, cuernitos y pan dulce"]),
 "rev_e": ("Lo que dicen", "Lo que dicen"), "rev_h": ("Our neighbors say it best", "Nuestros vecinos lo dicen mejor"),
 "yelp": ("on Yelp", "en Yelp"), "goog": ("on Google", "en Google"),
 "reviews": ([("Pan dulce heaven. Go early as it gets busy!", "Olivia D.", "Yelp"),
              ("The tres leches cake is always a hit. We were greeted with smiles and had quick toppings added to the cake.", "Sydney T.", "Yelp"),
              ("Hands down the best Mexican sweet bread in Grand Prairie. Employees are friendly. Don't change anything!", "Gracii L.", "Google"),
              ("Always fresh, soft and so satisfying. We pick up bread whenever we're in town.", "Brenda A.", "Google")],
             [("¡El cielo del pan dulce! Vayan temprano porque se llena.", "Olivia D.", "Yelp"),
              ("Amo el pan de aquí, siempre fresco, muy buenos precios y muy amables siempre las chicas que atienden.", "Linda A.", "Yelp"),
              ("Con mucha variedad de pan, buen servicio y personal muy amable y respetuoso.", "Alhondra R.", "Google"),
              ("Siempre fresco, suave y muy satisfactorio. Venimos por pan cada vez que estamos en la ciudad.", "Brenda A.", "Google")]),
 "faq_e": ("Preguntas", "Preguntas"), "faq_h": ("Good to know", "Bueno saber"),
 "faqs": ([("What are your hours?", "We're open every day from 6:00 AM to 8:45 PM. Bread comes out warm in the morning, and popular items (like bolillos) can sell out by the afternoon — come early!"),
           ("Where are you located?", "906 W Marshall Dr, Grand Prairie, TX 75051 — right off Marshall Drive, with free parking and a wheelchair-accessible entrance."),
           ("How do I order a custom cake?", "Add a cake to your order here, or call (972) 522-7939. For custom cakes please order at least 3 days ahead. Tres leches is often available same-day."),
           ("Do you have tamales and barbacoa?", "Yes! Hot tamales (pork and chicken) and barbacoa are available on Saturdays and Sundays. They sell out early, so come in the morning."),
           ("Do you sell Rosca de Reyes?", "Yes — our colorful Rosca de Reyes is made around Three Kings' Day in January. Order ahead so you don't miss out."),
           ("What payment do you accept?", "Cash, credit and debit cards, and mobile (NFC) payments."),
           ("Do you offer delivery?", "Pickup is easiest. For delivery or large event orders, please call us at (972) 522-7939.")],
          [("¿Cuál es su horario?", "Abrimos todos los días de 6:00 AM a 8:45 PM. El pan sale calientito por la mañana y los favoritos (como el bolillo) pueden agotarse en la tarde — ¡ven temprano!"),
           ("¿Dónde están ubicados?", "906 W Marshall Dr, Grand Prairie, TX 75051 — sobre Marshall Drive, con estacionamiento gratis y entrada accesible para sillas de ruedas."),
           ("¿Cómo ordeno un pastel personalizado?", "Agrega un pastel a tu pedido aquí, o llama al (972) 522-7939. Para pasteles personalizados pide con al menos 3 días de anticipación. El tres leches suele haber el mismo día."),
           ("¿Tienen tamales y barbacoa?", "¡Sí! Tamales calientes (de puerco y de pollo) y barbacoa los sábados y domingos. Se acaban temprano, así que ven por la mañana."),
           ("¿Venden Rosca de Reyes?", "Sí — nuestra colorida Rosca de Reyes se hace para el Día de Reyes en enero. Pídela con tiempo para no quedarte sin ella."),
           ("¿Qué formas de pago aceptan?", "Efectivo, tarjetas de crédito y débito, y pagos móviles (NFC)."),
           ("¿Hacen entregas a domicilio?", "Lo más fácil es recoger. Para entregas o pedidos grandes para eventos, llámanos al (972) 522-7939.")]),
 "visit_e": ("Ven a vernos", "Ven a vernos"), "visit_h": ("Visit the panadería", "Visita la panadería"),
 "hrs_h": ("Hours", "Horario"), "days": (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]),
 "hrs": ("6:00 AM – 8:45 PM", "6:00 AM – 8:45 PM"), "call": ("Call", "Llamar"), "dir": ("Get directions", "Cómo llegar"),
 "perks": (["Free parking", "Wheelchair accessible", "Cards & NFC accepted", "Takeout", "Dogs welcome"], ["Estacionamiento gratis", "Accesible", "Tarjetas y NFC", "Para llevar", "Perritos bienvenidos"]),
 "map_t": ("Map to Panaderia Celaya", "Mapa a Panadería Celaya"),
 "foot_p": ("Authentic Mexican bakery serving Grand Prairie and the Dallas–Fort Worth area since 2007.", "Panadería mexicana auténtica sirviendo a Grand Prairie y al área de Dallas–Fort Worth desde 2007."),
 "serving": ("Serving", "Sirviendo a"), "rights": ("All rights reserved.", "Todos los derechos reservados."),
 "m_order": ("🧺 Order", "🧺 Ordenar"), "m_call": ("📞 Call", "📞 Llamar"),
 # cart drawer
 "cart_h": ("Your order", "Tu pedido"), "close": ("Close", "Cerrar"),
 "f_name": ("Your name", "Tu nombre"), "f_phone": ("Phone", "Teléfono"), "f_date": ("Pickup date", "Fecha de recoger"), "f_time": ("Pickup time", "Hora de recoger"),
 "f_notes": ("Notes (optional)", "Notas (opcional)"), "f_notes_ph": ("Allergies, extra candles, etc.", "Alergias, velitas extra, etc."),
 "cake_h": ("🎂 Cake details", "🎂 Detalles del pastel"), "f_size": ("Size / servings", "Tamaño / porciones"), "f_size_ph": ("e.g. 1/2 sheet, 20 people", "ej. 1/2 charola, 20 personas"),
 "f_flavor": ("Flavor / filling", "Sabor / relleno"), "f_flavor_ph": ("e.g. tres leches with strawberries", "ej. tres leches con fresas"), "f_msg": ("Message on cake", "Mensaje en el pastel"), "f_msg_ph": ("e.g. ¡Feliz cumpleaños, Mami!", "ej. ¡Feliz cumpleaños, Mami!"),
 "cake_note": ("Custom cakes need 3 days' notice — earliest date set for you.", "Los pasteles personalizados necesitan 3 días de anticipación — ya elegimos la fecha más próxima."),
 "place": ("Send my order", "Enviar mi pedido"), "place_note": ("We'll confirm your order and total by phone or text. Nothing is charged online — you pay at pickup.", "Confirmamos tu pedido y total por teléfono o texto. No se cobra en línea — pagas al recoger."),
 "done_h": ("¡Casi listo!", "¡Casi listo!"), "done_p": ("Last step: send your order to the bakery. Tap below to text it (or call). We'll confirm it with you.", "Último paso: envía tu pedido a la panadería. Toca abajo para mandarlo por texto (o llamar). Te lo confirmamos."),
 "sent_ok": ("✅ Your order was also sent to our team.", "✅ Tu pedido también se envió a nuestro equipo."),
 "send_sms": ("💬 Text my order to the bakery", "💬 Mandar mi pedido por texto"), "copy": ("Copy order", "Copiar pedido"), "clear": ("Start over", "Empezar de nuevo"),
 "tel": ("📞 Call (972) 522-7939", "📞 Llamar (972) 522-7939"),
}
def t(k, l): v = X[k][0 if l == "en" else 1]; return v

JS_STR = {  # strings used by app.js
 "emptyT": ("Your basket is empty", "Tu canasta está vacía"), "emptyP": ("Add some pan dulce from the menu — ¡antójate!", "Agrega pan dulce del menú — ¡antójate!"),
 "less": ("Remove one", "Quitar uno"), "more": ("Add one", "Agregar uno"), "priceAtPickup": ("price at pickup", "precio en tienda"), "subtotal": ("Subtotal", "Subtotal"),
 "fineUnknown": ("Some items are priced in-store; we'll confirm your total.", "Algunos productos se cobran en tienda; te confirmamos el total."), "fineKnown": ("Pay at pickup. Taxes may apply.", "Pagas al recoger. Pueden aplicar impuestos."),
 "added": ("Added to your order! 🥐", "¡Agregado a tu pedido! 🥐"), "msgHead": ("🥐 NEW PICKUP ORDER — Panaderia Celaya", "🥐 NUEVO PEDIDO PARA RECOGER — Panadería Celaya"),
 "lblSub": ("Subtotal", "Subtotal"), "lblName": ("Name", "Nombre"), "lblPhone": ("Phone", "Teléfono"), "lblPickup": ("Pickup", "Recoger"), "lblCake": ("Cake", "Pastel"), "lblNotes": ("Notes", "Notas"),
 "eName": ("Please enter your name.", "Escribe tu nombre."), "ePhone": ("Enter a 10-digit phone number.", "Escribe un teléfono de 10 dígitos."), "eDate": ("Pick a pickup date.", "Elige una fecha."),
 "eCake": ("Custom cakes need 3 days' notice.", "Los pasteles necesitan 3 días de anticipación."),
 "copied": ("Order copied!", "¡Pedido copiado!"), "copyFail": ("Select & copy the text", "Selecciona y copia el texto"),
 "openNow": ("Open now · until 8:45 PM", "Abierto ahora · hasta las 8:45 PM"), "closedNow": ("Closed now · opens 6 AM", "Cerrado ahora · abre a las 6 AM"),
}

LOGO = '<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="29" fill="#f8b414" stroke="#472717" stroke-width="4"/><path d="M12 36a20 20 0 0 1 40 0z" fill="#e8368a" stroke="#472717" stroke-width="3"/><path d="M22 36c0-8 2-12 4-15M32 36V19M42 36c0-8-2-12-4-15" stroke="#fff7e8" stroke-width="3" fill="none" stroke-linecap="round"/><rect x="10" y="36" width="44" height="9" rx="4.5" fill="#fff7e8" stroke="#472717" stroke-width="3"/></svg>'
EMO = {"salado": ["🫔", "🌮", "🥖"], "frio": ["🍮", "🍧", "🥛"]}

def item_card(it, l):
    name = it[l]; desc = it["d" + l]; p = it["price"]
    if it.get("img"):
        pre = "" if l == "en" else "../"
        alt = f"{name} — Panaderia Celaya Grand Prairie TX"
        ph = f'<div class="ph"><img src="{pre}assets/img/{it["img"]}" alt="{e(alt)}" loading="lazy" width="400" height="300">'
        if it.get("note"): ph += f'<span class="tag">{t(it["note"], l)}</span>'
        ph += "</div>"
    else:
        ic = {"tamal-p": "🫔", "tamal-c": "🫔", "barbacoa": "🌮", "flan": "🍮", "gelatina": "🍧", "pudin": "🥛"}.get(it["id"], "🥐")
        n = sum(map(ord, it["id"])) % 3
        ph = f'<div class="ph emo e{n}" role="img" aria-label="{e(name)}">{ic}'
        if it.get("note"): ph += f'<span class="tag">{t(it["note"], l)}</span>'
        ph += "</div>"
    price = f'<span class="price">${p:.2f}</span>' if p is not None else f'<span class="price ask">{t("ask", l)}</span>'
    return (f'<article class="item" data-id="{it["id"]}">{ph}<div class="bd"><h4>{e(name)}</h4><p>{e(desc)}</p>'
            f'<div class="row">{price}<button class="add" type="button">+ {t("add", l)}</button>'
            f'<span class="step"><button type="button" data-d="-1" aria-label="{e(JS_STR["less"][0 if l=="en" else 1])}">–</button><output>0</output><button type="button" data-d="1" aria-label="{e(JS_STR["more"][0 if l=="en" else 1])}">+</button></span></div></div></article>')

def schema(l):
    by = {c["id"]: c for c in menu["cats"]}
    sections = []
    for c in menu["cats"]:
        its = []
        for it in menu["items"]:
            if it["cat"] != c["id"]: continue
            m = {"@type": "MenuItem", "name": it[l], "description": it["d" + l]}
            if it["price"] is not None: m["offers"] = {"@type": "Offer", "price": f'{it["price"]:.2f}', "priceCurrency": "USD"}
            its.append(m)
        sections.append({"@type": "MenuSection", "name": c[l], "hasMenuItem": its})
    imgs = [f"{BASE}/assets/img/{n}.webp" for n in ["rosca", "storefront", "conchas-rack", "cake-fruit", "interior"]]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    bakery = {
        "@type": ["Bakery", "LocalBusiness", "FoodEstablishment"], "@id": f"{BASE}/#bakery",
        "name": "Panaderia Celaya", "alternateName": ["Panadería Celaya", "Panaderia Celaya Grand Prairie", "Celaya Bakery"],
        "description": t("desc", l), "url": f"{BASE}/" + ("" if l == "en" else "es/"), "image": imgs, "logo": f"{BASE}/favicon.svg",
        "telephone": PHONE_E164, "priceRange": "$", "servesCuisine": ["Mexican", "Bakery", "Pan Dulce"], "foundingDate": "2007",
        "slogan": "Pan dulce mexicano recién horneado desde 2007", "inLanguage": ["en", "es"],
        "address": {"@type": "PostalAddress", "streetAddress": ADDR["street"], "addressLocality": ADDR["city"], "addressRegion": ADDR["state"], "postalCode": ADDR["zip"], "addressCountry": "US"},
        "hasMap": f"https://www.google.com/maps/search/?api=1&query={MAPS_Q}",
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": days, "opens": "06:00", "closes": "20:45"}],
        "paymentAccepted": "Cash, Credit Card, Debit Card, NFC Mobile Payments", "currenciesAccepted": "USD",
        "areaServed": [{"@type": "City", "name": c + ", TX"} for c in CITIES] + [{"@type": "AdministrativeArea", "name": "Dallas–Fort Worth Metroplex"}],
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in ["Free parking", "Wheelchair accessible entrance", "Wheelchair accessible parking", "Takeout", "Credit cards accepted"]],
        "knowsAbout": ["Pan dulce", "Conchas", "Bolillos", "Tres leches cake", "Rosca de Reyes", "Churros", "Tamales", "Custom cakes", "Quinceañera cakes"],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Product", "name": it[l]}} for it in menu["items"] if it["id"] in ("tres-leches", "birthday", "rosca", "concha-v", "bolillo")],
        "potentialAction": {"@type": "OrderAction", "target": {"@type": "EntryPoint", "urlTemplate": f"{BASE}/" + ("" if l == "en" else "es/") + "#order", "actionPlatform": ["http://schema.org/DesktopWebPlatform", "http://schema.org/MobileWebPlatform"]}, "deliveryMethod": "http://purl.org/goodrelations/v1#DeliveryModePickUp"},
        "hasMenu": {"@type": "Menu", "name": "Panaderia Celaya Menu", "hasMenuSection": sections},
    }
    faq = {"@type": "FAQPage", "@id": f"{BASE}/#faq-{l}", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in X["faqs"][0 if l == "en" else 1]]}
    site = {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": "Panaderia Celaya", "inLanguage": ["en", "es"], "publisher": {"@id": f"{BASE}/#bakery"}}
    return json.dumps({"@context": "https://schema.org", "@graph": [bakery, faq, site]}, ensure_ascii=False, separators=(",", ":"))

def page(l):
    o = "es" if l == "en" else "en"
    pre = "" if l == "en" else "../"
    url = f"{BASE}/" + ("" if l == "en" else "es/")
    other = ("es/" if l == "en" else "../")
    i = lambda k: t(k, l)
    items_js = {it["id"]: {"name": it[l], "price": it["price"], "cake": bool(it.get("cake"))} for it in menu["items"]}
    cfg = {"lang": l, "items": items_js, "t": {k: v[0 if l == "en" else 1] for k, v in JS_STR.items()}, "phoneRaw": PHONE_RAW, "endpoint": ORDER_ENDPOINT}

    chips = "".join(f'<a class="chip" href="#cat-{c["id"]}">{c["icon"]} {e(c[l])}</a>' for c in menu["cats"])
    cats = ""
    for c in menu["cats"]:
        cards = "".join(item_card(it, l) for it in menu["items"] if it["cat"] == c["id"])
        cats += f'<div class="cat" id="cat-{c["id"]}"><h3><span aria-hidden="true">{c["icon"]}</span> {e(c[l])}</h3><div class="grid">{cards}</div></div>'
    mq = "".join(f"<span>{e(w)}</span><i>✿</i>" for w in X["marq"][0 if l == "en" else 1])
    cake_li = "".join(f"<li>{e(x)}</li>" for x in X["cakes_l"][0 if l == "en" else 1])
    gal = ["case", "rolls-rack", "rack-color", "muffin", "churros", "storefront2", "cakes-fridge", "tray"]
    gal_html = "".join(f'<img src="{pre}assets/img/{g}.webp" alt="{e(a)}" loading="lazy">' for g, a in zip(gal, X["alts"][0 if l == "en" else 1]))
    revs = "".join(f'<figure class="rev"><div class="st" aria-label="5 stars">★★★★★</div><blockquote><p>“{e(q)}”</p></blockquote><figcaption><cite>{e(n)}</cite> · {src}</figcaption></figure>' for q, n, src in X["reviews"][0 if l == "en" else 1])
    faqs = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in X["faqs"][0 if l == "en" else 1])
    hours = "".join(f"<tr><td>{d}</td><td>{i('hrs')}</td></tr>" for d in X["days"][0 if l == "en" else 1])
    perks = "".join(f"<span>{e(p)}</span>" for p in X["perks"][0 if l == "en" else 1])
    cities = ", ".join(CITIES)
    toggle = (f'<div class="lang" role="group" aria-label="Language / Idioma"><span aria-current="true">EN</span><a href="{other}" hreflang="es" lang="es" title="Español">ES</a></div>' if l == "en"
              else f'<div class="lang" role="group" aria-label="Language / Idioma"><a href="{other}" hreflang="en" lang="en" title="English">EN</a><span aria-current="true">ES</span></div>')
    pri = lambda k: e(JS_STR[k][0 if l == "en" else 1])

    return f'''<!doctype html>
<html lang="{l}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(i("title"))}</title>
<meta name="description" content="{e(i("desc"))}">
<meta name="keywords" content="{e(i("keywords"))}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="Panaderia Celaya">
<meta name="theme-color" content="#1b4fb0">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{BASE}/">
<link rel="alternate" hreflang="es" href="{BASE}/es/">
<link rel="alternate" hreflang="x-default" href="{BASE}/">
<!-- Local SEO -->
<meta name="geo.region" content="US-TX"><meta name="geo.placename" content="Grand Prairie"><meta name="ICBM" content="32.7459, -96.9978">
<meta name="format-detection" content="telephone=yes">
<!-- Open Graph / Social -->
<meta property="og:type" content="restaurant.restaurant"><meta property="og:site_name" content="Panaderia Celaya">
<meta property="og:title" content="{e(i("title"))}"><meta property="og:description" content="{e(i("desc"))}">
<meta property="og:url" content="{url}"><meta property="og:locale" content="{"en_US" if l == "en" else "es_US"}"><meta property="og:locale:alternate" content="{"es_US" if l == "en" else "en_US"}">
<meta property="og:image" content="{BASE}/assets/og-cover.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{e(i("alt_hero"))}">
<meta property="restaurant:contact_info:street_address" content="{ADDR["street"]}"><meta property="restaurant:contact_info:locality" content="{ADDR["city"]}"><meta property="restaurant:contact_info:region" content="TX"><meta property="restaurant:contact_info:postal_code" content="{ADDR["zip"]}"><meta property="restaurant:contact_info:phone_number" content="{PHONE_E164}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(i("title"))}"><meta name="twitter:description" content="{e(i("desc"))}"><meta name="twitter:image" content="{BASE}/assets/og-cover.jpg">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml"><link rel="manifest" href="{pre}manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="image" href="{pre}assets/img/rosca.webp">
<link href="https://fonts.googleapis.com/css2?family=Bagel+Fat+One&family=Caveat:wght@600&family=Nunito:wght@400;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/styles.css">
<script type="application/ld+json">{schema(l)}</script>
</head>
<body>
<a class="skip" href="#main">{i("skip")}</a>
<div class="picado" aria-hidden="true"></div>
<header class="top"><div class="wrap">
  <a class="logo" href="{"./" if l == "en" else "./"}" aria-label="Panadería Celaya">{LOGO}<span>Panadería Celaya<small>Grand Prairie, TX · desde 2007</small></span></a>
  <nav class="main" aria-label="Main">
    <a href="#menu">{i("nav_menu")}</a><a href="#cakes">{i("nav_cakes")}</a><a href="#visit">{i("nav_visit")}</a><a href="#faq">{i("nav_faq")}</a>
    {toggle}
    <button class="cart-btn keep" type="button" data-open-cart aria-label="{i("cart")}">🧺 <span class="t">{i("cart")}</span> <b class="cart-count">0</b></button>
  </nav>
</div></header>
<main id="main">
<section class="hero"><div class="wrap">
  <div>
    <span class="pill" id="openPill"><span class="dot"></span><span class="txt">{i("open_loading")}</span></span>
    <h1>{i("h1a")} <em>{i("h1b")}</em><br><span class="u">{i("h1c")}</span></h1>
    <p class="lead">{i("lead")}</p>
    <div class="cta"><a class="btn" href="#menu">🥐 {i("cta1")}</a><a class="btn alt" href="tel:{PHONE_RAW}">📞 {PHONE_DISPLAY}</a></div>
    <div class="mini"><div><strong>18</strong>{i("stat1")}</div><div><strong>4.8★</strong>{i("stat2")}</div><div><strong>6 AM</strong>{i("stat3")}</div></div>
  </div>
  <div class="arch"><div class="frame"><img src="{pre}assets/img/rosca.webp" alt="{e(i("alt_hero"))}" width="430" height="538" fetchpriority="high"></div>
    <div class="sticker a"><span><b>{i("stk_a")}</b>{i("stk_a2")}</span></div><div class="sticker b">{i("stk_b")}</div><div class="sticker c" aria-hidden="true">🥐</div></div>
</div></section>
<div class="marquee" aria-hidden="true"><div>{mq}{mq}</div></div>

<section><div class="wrap">
  <div class="head"><span class="eyebrow">{i("why_e")}</span><h2>{i("why_h")}</h2></div>
  <div class="why">
    <div class="card"><div class="ico">🥖</div><h3>{i("why1t")}</h3><p>{i("why1p")}</p></div>
    <div class="card"><div class="ico">🧡</div><h3>{i("why2t")}</h3><p>{i("why2p")}</p></div>
    <div class="card"><div class="ico">🎂</div><h3>{i("why3t")}</h3><p>{i("why3p")}</p></div>
  </div>
</div></section>
<div class="tiles" aria-hidden="true"></div>

<section class="menu-sec" id="menu"><div class="wrap">
  <div class="head"><span class="eyebrow">{i("menu_e")}</span><h2>{i("menu_h")}</h2><p>{i("menu_p")}</p></div>
  <nav class="chips" aria-label="{i("menu_h")}">{chips}</nav>
  {cats}
  <p class="menu-note">{i("menu_note")}</p>
</div></section>
<div class="tiles" aria-hidden="true"></div>

<section class="cakes" id="cakes"><div class="wrap">
  <div><span class="eyebrow">{i("cakes_e")}</span><h2>{i("cakes_h")}</h2><p>{i("cakes_p")}</p><ul>{cake_li}</ul>
    <button class="btn yel" type="button" data-open-cart>🎂 {i("cakes_cta")}</button></div>
  <div class="cake-photos"><img src="{pre}assets/img/cake-fruit.webp" alt="{e(i("alt_c1"))}" loading="lazy"><img src="{pre}assets/img/cake-love.webp" alt="{e(i("alt_c2"))}" loading="lazy"></div>
</div></section>

<section class="story"><div class="wrap">
  <div class="polaroids">
    <figure><img src="{pre}assets/img/concha-plate.webp" alt="{e(i("alt_p1"))}" loading="lazy"><figcaption>{i("cap1")}</figcaption></figure>
    <figure><img src="{pre}assets/img/bolillos.webp" alt="{e(i("alt_p2"))}" loading="lazy"><figcaption>{i("cap2")}</figcaption></figure>
    <figure><img src="{pre}assets/img/muffin.webp" alt="{e(i("alt_p3"))}" loading="lazy"><figcaption>{i("cap3")}</figcaption></figure>
  </div>
  <div><span class="eyebrow">{i("story_e")}</span><h2>{i("story_h")}</h2><p style="margin-top:.8rem">{i("story_p")}</p>
    <blockquote lang="es">{i("story_q")}<div class="sign">{i("story_s")}</div></blockquote></div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="head"><span class="eyebrow">{i("gal_e")}</span><h2>{i("gal_h")}</h2></div>
  <div class="gallery">{gal_html}</div>
</div></section>

<section class="reviews"><div class="wrap">
  <div class="head"><span class="eyebrow" style="color:var(--choc)">{i("rev_e")}</span><h2>{i("rev_h")}</h2></div>
  <div class="rate"><span class="pill"><b>4.8★</b> {i("yelp")}</span><span class="pill"><b>4.4★</b> {i("goog")}</span></div>
  <div class="grid">{revs}</div>
</div></section>

<section id="faq"><div class="wrap">
  <div class="head"><span class="eyebrow">{i("faq_e")}</span><h2>{i("faq_h")}</h2></div>
  <div class="faq">{faqs}</div>
</div></section>

<section class="visit" id="visit"><div class="wrap">
  <div>
    <span class="eyebrow">{i("visit_e")}</span><h2>{i("visit_h")}</h2>
    <div class="vbox" style="margin-top:1.2rem">
      <h3>📍 {ADDR["street"]}, {ADDR["city"]}, {ADDR["state"]} {ADDR["zip"]}</h3>
      <p><a href="tel:{PHONE_RAW}">{PHONE_DISPLAY}</a></p>
      <h3 style="margin-top:1rem">🕒 {i("hrs_h")}</h3>
      <table class="hours" id="hoursTbl">{hours}</table>
      <div class="cta"><a class="btn sm blue" href="https://www.google.com/maps/dir/?api=1&destination={MAPS_Q}" target="_blank" rel="noopener">🧭 {i("dir")}</a><a class="btn sm alt" href="tel:{PHONE_RAW}">📞 {i("call")}</a></div>
      <div class="perks">{perks}</div>
    </div>
  </div>
  <div class="map"><iframe title="{e(i("map_t"))}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={MAPS_Q}&output=embed"></iframe></div>
</div></section>
</main>
<footer><div class="wrap">
  <div><h3>Panadería Celaya</h3><p>{i("foot_p")}</p><p>© <span id="yr">2026</span> Panaderia Celaya. {i("rights")}</p></div>
  <div><address style="font-style:normal">{ADDR["street"]}<br>{ADDR["city"]}, {ADDR["state"]} {ADDR["zip"]}<br><a href="tel:{PHONE_RAW}">{PHONE_DISPLAY}</a></address>
    <p class="cities"><strong>{i("serving")}:</strong> {cities}.</p></div>
</div></footer>

<div class="mbar"><a class="btn alt" href="tel:{PHONE_RAW}">{i("m_call")}</a><button class="btn" type="button" data-open-cart>{i("m_order")} <b class="cart-count" style="background:var(--marigold);color:var(--choc);border-radius:99px;padding:0 .5rem">0</b></button></div>

<div class="scrim" id="scrim"></div>
<aside class="drawer" id="drawer" role="dialog" aria-modal="true" aria-labelledby="dh" aria-hidden="true">
  <header><h2 id="dh">🧺 {i("cart_h")}</h2><button class="x" id="drawerClose" type="button" aria-label="{i("close")}">✕</button></header>
  <div class="dbody">
    <div id="cartView">
      <div id="cartLines"></div>
      <form class="order" id="orderForm" novalidate hidden>
        <label>{i("f_name")}<input id="f-name" autocomplete="name" required><span class="err" id="e-name" role="alert"></span></label>
        <label>{i("f_phone")}<input id="f-phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="(972) 555-0123" required><span class="err" id="e-phone" role="alert"></span></label>
        <div class="two"><label>{i("f_date")}<input id="f-date" type="date" required><span class="err" id="e-date" role="alert"></span></label><label>{i("f_time")}<select id="f-time"></select></label></div>
        <p class="fine" id="cakeNote" hidden>🎂 {i("cake_note")}</p>
        <div class="cakebox" id="cakeBox"><strong>{i("cake_h")}</strong>
          <label>{i("f_size")}<input id="f-size" placeholder="{e(i("f_size_ph"))}"></label>
          <label>{i("f_flavor")}<input id="f-flavor" placeholder="{e(i("f_flavor_ph"))}"></label>
          <label>{i("f_msg")}<input id="f-msg" placeholder="{e(i("f_msg_ph"))}"></label></div>
        <label>{i("f_notes")}<textarea id="f-notes" rows="2" placeholder="{e(i("f_notes_ph"))}"></textarea></label>
        <button class="btn" type="submit">{i("place")}</button>
        <p class="fine">{i("place_note")}</p>
      </form>
    </div>
    <div id="doneView" class="done" hidden>
      <div class="big">🎉</div><h3>{i("done_h")}</h3><p>{i("done_p")}</p>
      <p class="fine" id="sentOk" hidden>{i("sent_ok")}</p>
      <pre id="doneMsg"></pre>
      <div class="btns"><a class="btn" id="smsBtn" href="#">{i("send_sms")}</a><a class="btn blue" id="callBtn" href="#">{i("tel")}</a>
        <button class="btn alt sm" id="copyBtn" type="button">📋 {i("copy")}</button><button class="btn alt sm" id="clearBtn" type="button">{i("clear")}</button></div>
    </div>
  </div>
</aside>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>window.CELAYA={json.dumps(cfg, ensure_ascii=False)};document.getElementById("yr").textContent=new Date().getFullYear();</script>
<script src="{pre}assets/app.js" defer></script>
</body>
</html>'''

(ROOT / "es").mkdir(exist_ok=True)
(ROOT / "index.html").write_text(page("en"), encoding="utf-8")
(ROOT / "es/index.html").write_text(page("es"), encoding="utf-8")

# ---- SEO support files
(ROOT / "sitemap.xml").write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url><loc>{BASE}/</loc><changefreq>weekly</changefreq><priority>1.0</priority>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE}/"/><xhtml:link rel="alternate" hreflang="es" href="{BASE}/es/"/><xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/"/></url>
  <url><loc>{BASE}/es/</loc><changefreq>weekly</changefreq><priority>1.0</priority>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE}/"/><xhtml:link rel="alternate" hreflang="es" href="{BASE}/es/"/><xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/"/></url>
</urlset>
''')
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
(ROOT / "manifest.webmanifest").write_text(json.dumps({"name": "Panadería Celaya", "short_name": "Celaya", "description": t("desc", "en"), "start_url": "/", "display": "standalone", "background_color": "#fff7e8", "theme_color": "#1b4fb0", "icons": [{"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"}]}, ensure_ascii=False, indent=1))
(ROOT / "favicon.svg").write_text(LOGO.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" '))
(ROOT / "404.html").write_text('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>404 · Panadería Celaya</title><meta name="viewport" content="width=device-width,initial-scale=1"><body style="font-family:system-ui;text-align:center;padding:4rem;background:#fff7e8;color:#472717"><div style="font-size:5rem">🥐</div><h1>¡Ay! This page ran out, like the bolillos.</h1><p><a href="/">Back to Panadería Celaya</a> · <a href="/es/">Volver al inicio</a></p>')
print("built", BASE)
