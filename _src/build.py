#!/usr/bin/env python3
"""Builds the site's pages: English at the repo root, Spanish in /es.

    python3 _src/build.py

Every piece of copy is written once, as t("English", "Español"). Edit it here,
rebuild, and commit the generated .html files (GitHub Pages serves them as-is;
Jekyll ignores this _src folder).

Photos: each photo(...) call names a file under assets/img/. Until that file
exists the page shows a framed placeholder; drop the image in and rebuild.
  assets/img/portrait.jpg                 hero portrait, 4:5
  assets/img/projects/minisumo-pcb.jpg    engineering card, macro on the PCB
  assets/img/projects/minisumo.jpg        Minisumo on the dohyo
  assets/img/projects/robomatrix.jpg      Minisumo & RoboFut at Robomatrix
  assets/img/travel/oaxaca-landscape.jpg  Oaxaca hero + hospitality card, 16:9
  assets/img/travel/field-architecture.jpg, field-table.jpg,
  assets/img/travel/field-craft.jpg, field-guests.jpg, field-landscape.jpg
  assets/img/certificates/<name>.pdf + <name>.jpg  (preview image; see certs_*())
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://alejandrofavero.github.io/"
EMAIL = "alex@travelinoaxaca.com"
PHOTOGRAPHER = ("Douglas Favero", "https://douglasfavero.com")


def credit(link=True):
    name, url = PHOTOGRAPHER
    label = t("Photo", "Foto")
    if link:
        return f'{label}: <a href="{url}" target="_blank" rel="noopener">{name}</a>'
    return f"{label}: {name}"
L = "en"  # language currently being built


def t(en, es):
    return en if L == "en" else es


def pre():
    """Prefix from the current page to the site root."""
    return "" if L == "en" else "../"


NAV = [
    ("projects.html", "Work", "Proyectos"),
    ("about.html", "About", "Perfil"),
    ("certificates.html", "Recognition", "Reconocimientos"),
    ("travel.html", "Oaxaca", "Oaxaca"),
]

ICON_MOON = '<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>'
ICON_SUN = '<svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
ICON_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><path d="M3 8h18M3 16h18"/></svg>'


# ---- Building blocks --------------------------------------------------------

def photo(path, label, note="", alt="", h=None, fig=None, cls="", pos=None, by=None):
    style = f' style="--h: {h}px;"' if h else ""
    if os.path.exists(os.path.join(ROOT, path)):
        css = (f"--h: {h}px; " if h else "") + (f"object-position: {pos};" if pos else "")
        img_style = f' style="{css.strip()}"' if css else ""
        inner = f'<img src="{pre()}{path}" alt="{alt or label}" loading="lazy"{img_style}>'
    else:
        note_html = f'<span class="note">{note}</span>' if note else ""
        inner = (f'<!-- photo: add {path} and rebuild -->\n'
                 f'<div class="ph" role="img" aria-label="{alt or label}"{style}><span class="lbl">{label}</span>{note_html}</div>')
    cap = ""
    if by and os.path.exists(os.path.join(ROOT, path)):
        cap = f'\n<figcaption class="credit lbl">{by}</figcaption>'
    if fig:
        cap = f'\n<figcaption class="fig"><span class="lbl accent">{fig[0]}</span><span class="lbl faint">{fig[1]}</span></figcaption>'
    return f'<figure class="photo {cls}">\n{inner}{cap}\n</figure>'


def spec(rows):
    out = []
    for k, v, *flag in rows:
        cls = ' class="result"' if flag else ""
        out.append(f'<div><dt class="lbl">{k}</dt><dd{cls}>{v}</dd></div>')
    return '<dl class="spec">\n' + "\n".join(out) + "\n</dl>"


def section_head(label, title, aside=""):
    return f'''<div class="section-head">
<div>
<span class="lbl accent">{label}</span>
<h2 class="section-title">{title}</h2>
</div>
{aside}
</div>'''


def record(kind, title, detail, when):
    return f'''<div class="record">
<span class="lbl faint">{kind}</span>
<div><h3 class="title">{title}</h3><p class="detail">{detail}</p></div>
<span class="lbl accent">{when}</span>
</div>'''


def languages_panel():
    rows = [(t("Spanish", "Español"), t("Native", "Nativo"), 100),
            (t("English", "Inglés"), "C1", 83),
            (t("French", "Francés"), "A2", 33)]
    gauges = "\n".join(
        f'<div class="gauge"><div class="row"><span class="name">{n}</span><span class="lbl faint">{lvl}</span></div>'
        f'<div class="bar"><span style="width: {w}%;"></span></div></div>' for n, lvl, w in rows)
    return f'''<aside class="panel">
<span class="lbl accent">{t("Working languages", "Idiomas")}</span>
{gauges}
<hr>
<span class="lbl accent">{t("Toolkit", "Herramientas")}</span>
<p class="body">{t("PCB design · 3D printing · Soldering &amp; assembly · Arduino / ESP32 · C / C++ · Data structures in C · WordPress",
                  "Diseño de PCB · Impresión 3D · Soldadura y ensamble · Arduino / ESP32 · C / C++ · Estructuras de datos en C · WordPress")}</p>
</aside>'''


# ---- Page shell -------------------------------------------------------------

def head(page, title, desc):
    canon = "" if page == "index.html" else page
    here = BASE + ("" if L == "en" else "es/") + canon
    return f'''<!doctype html>
<html lang="{L}" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{here}">
<link rel="alternate" hreflang="en" href="{BASE}{canon}">
<link rel="alternate" hreflang="es" href="{BASE}es/{canon}">
<link rel="alternate" hreflang="x-default" href="{BASE}{canon}">
<meta name="theme-color" content="#0C0F13">
<script>try{{var s=localStorage.getItem("theme");if(s==="light"||s==="dark")document.documentElement.setAttribute("data-theme",s)}}catch(e){{}}</script>
<link rel="icon" type="image/svg+xml" href="{pre()}assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&amp;family=Instrument+Sans:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre()}assets/css/style.css">
</head>'''


def header(page, coords):
    items = []
    for href, en, es in NAV:
        cur = ' aria-current="page"' if href == page else ""
        items.append(f'<li><a class="lbl" href="{href}"{cur}>{en if L == "en" else es}</a></li>')
    en_href = page if L == "en" else "../" + page
    es_href = "es/" + page if L == "en" else page
    en_cur = ' aria-current="true"' if L == "en" else ""
    es_cur = ' aria-current="true"' if L == "es" else ""
    return f'''<a class="skip-link lbl" href="#main">{t("Skip to content", "Saltar al contenido")}</a>
<header class="site-header">
<div class="wrap header-bar">
<a class="brand" href="index.html">
<span class="monogram" aria-hidden="true">AF</span>
<span class="brand-name lbl">Alejandro Favero</span>
</a>
<nav class="site-nav" id="primary-nav" aria-label="{t("Primary", "Principal")}">
<ul>
{chr(10).join(items)}
</ul>
</nav>
<div class="header-tools">
<span class="coords lbl">{coords}</span>
<div class="lang-switch" role="group" aria-label="Language / Idioma">
<a href="{en_href}" hreflang="en" lang="en" aria-label="English"{en_cur}>EN</a>
<a href="{es_href}" hreflang="es" lang="es" aria-label="Español"{es_cur}>ES</a>
</div>
<button class="icon-btn theme-toggle" type="button" data-theme-toggle aria-label="{t("Switch between light and dark theme", "Cambiar entre tema claro y oscuro")}">{ICON_MOON}{ICON_SUN}</button>
<button class="icon-btn nav-toggle" type="button" data-nav-toggle aria-controls="primary-nav" aria-expanded="false" aria-label="{t("Menu", "Menú")}">{ICON_MENU}</button>
</div>
</div>
</header>'''


def footer_grand():
    return f'''<footer class="site-footer">
<div class="wrap">
<div class="footer-grand">
<div>
<span class="lbl accent">{t("Correspondence", "Contacto")}</span>
<h2>{t("Let’s talk engineering<br><em>— or Oaxaca.</em>", "Hablemos de ingeniería<br><em>— o de Oaxaca.</em>")}</h2>
<div class="btn-row" style="margin-top: 40px;">
<a class="btn btn-primary" href="mailto:{EMAIL}">{t("Write to me", "Escríbeme")} <span aria-hidden="true">→</span></a>
</div>
</div>
<div class="footer-links">
<a href="mailto:{EMAIL}">{EMAIL} <span class="lbl" aria-hidden="true">→</span></a>
<a href="https://linkedin.com/in/alejandro-manuel-favero-cruz" target="_blank" rel="noopener">LinkedIn <span class="lbl" aria-hidden="true">↗</span></a>
<a href="https://github.com/AlejandroFavero" target="_blank" rel="noopener">GitHub <span class="lbl" aria-hidden="true">↗</span></a>
<a href="https://travelinoaxaca.com" target="_blank" rel="noopener">travelinoaxaca.com <span class="lbl" aria-hidden="true">↗</span></a>
</div>
</div>
<div class="footer-bottom">
<span class="lbl">© 2026 Alejandro Manuel Favero Cruz</span>
<span class="lbl">CDMX — 19.4326° N 99.1332° W</span>
<span class="lbl">Oaxaca — 17.0732° N 96.7266° W</span>
</div>
</div>
</footer>'''


def footer_slim():
    return f'''<footer class="site-footer">
<div class="wrap footer-slim">
<span class="lbl">© 2026 Alejandro Manuel Favero Cruz</span>
<nav aria-label="{t("Elsewhere", "En otros sitios")}">
<a class="lbl" href="mailto:{EMAIL}">{t("Email", "Correo")} →</a>
<a class="lbl" href="https://linkedin.com/in/alejandro-manuel-favero-cruz" target="_blank" rel="noopener">LinkedIn ↗</a>
<a class="lbl" href="https://github.com/AlejandroFavero" target="_blank" rel="noopener">GitHub ↗</a>
</nav>
<span class="lbl">Oaxaca — 17.0732° N 96.7266° W</span>
</div>
</footer>'''


def page(name, title, desc, main, body_cls="", coords="19.43° N · 99.13° W", footer=footer_grand):
    cls = f' class="{body_cls}"' if body_cls else ""
    return f'''{head(name, title, desc)}
<body{cls}>
{header(name, coords)}
<main id="main">
{main}
</main>
{footer()}
<script src="{pre()}assets/js/main.js"></script>
</body>
</html>
'''


# ---- Shared content ---------------------------------------------------------

def feature_minisumo():
    return f'''<article class="feature">
{photo("assets/img/projects/minisumo.jpg", t("Photo — Minisumo on the dohyo", "Foto — Minisumo en el dohyo"),
       t("Three-quarter view, low angle", "Vista a tres cuartos, ángulo bajo"),
       alt=t("The Minisumo robot that placed 3rd at Roboduca 2026: custom PCB on a 3D-printed chassis",
             "El robot minisumo que obtuvo el 3.er lugar en Roboduca 2026: PCB propia sobre chasis impreso en 3D"),
       pos="50% 55%")}
<div class="feature-copy">
<span class="lbl accent">{t("No. 01 — Current", "No. 01 — Actual")}</span>
<h3>{t("Minisumo Competition Robot", "Robot de competencia Minisumo")}</h3>
<span class="lbl faint">{t("CROFI Robotics Club · Faculty of Engineering, UNAM", "Club de Robótica CROFI · Facultad de Ingeniería, UNAM")}</span>
<p class="body">{t("Designed and fabricated from scratch: a custom PCB, a 3D-printed chassis, and embedded Arduino firmware.",
                   "Diseñado y fabricado desde cero: PCB propia, chasis impreso en 3D y firmware embebido en Arduino.")}</p>
{spec([(t("Electronics", "Electrónica"), t("Custom PCB", "PCB propia")),
       (t("Chassis", "Chasis"), t("3D-printed", "Impreso en 3D")),
       ("Firmware", "Arduino · C++"),
       (t("Result", "Resultado"), t("3rd place, Roboduca 2026", "3.er lugar, Roboduca 2026"), True),
       (t("Status", "Estado"), t("Open-source release in preparation", "Publicación open source en preparación"))])}
</div>
</article>'''


def feature_robomatrix():
    return f'''<article class="feature reverse">
{photo("assets/img/projects/robomatrix.jpg", t("Photo — Robomatrix", "Foto — Robomatrix"),
       t("Both robots, competition day", "Ambos robots, día de competencia"),
       alt=t("The Minisumo and RoboFut robots at Robomatrix", "Los robots Minisumo y RoboFut en Robomatrix"))}
<div class="feature-copy">
<span class="lbl accent">{t("No. 02 — High school", "No. 02 — Bachillerato")}</span>
<h3>Minisumo &amp; RoboFut</h3>
<span class="lbl faint">{t("Robotics Club · CBTIS 26", "Club de Robótica · CBTIS 26")}</span>
<p class="body">{t("The Minisumo placed 3rd regionally and 4th continentally at Robomatrix, competing against university-level teams. RoboFut, a remote-controlled robot, competed at the same event.",
                   "El Minisumo obtuvo el 3.er lugar regional y el 4.º continental en Robomatrix, compitiendo contra equipos universitarios. RoboFut, un robot a control remoto, compitió en el mismo evento.")}</p>
{spec([(t("Result", "Resultado"), t("3rd regional · 4th continental", "3.º regional · 4.º continental"), True),
       (t("Disciplines", "Disciplinas"), t("PCB design · Remote control", "Diseño de PCB · Control remoto"))])}
</div>
</article>'''


def certs_competition():
    return [
        dict(kind=t("Competition", "Competencia"), title="Roboduca 2026 — Minisumo",
             detail=t("3rd place · CROFI Robotics Club, UNAM", "3.er lugar · Club de Robótica CROFI, UNAM"),
             when="2026", file="roboduca-2026"),
        dict(kind=t("Competition", "Competencia"), title="Robomatrix Oaxaca 2024 — Minisumo",
             detail=t("3rd regional · 4th continental with the robot Zeus · CBTIS 26, against university-level teams",
                      "3.º regional · 4.º continental con el robot Zeus · CBTIS 26, contra equipos universitarios"),
             when="2024", file="robomatrix-2024",
             doc=t("Qualified for the Robomatrix Continental Master — the top 3 advance", "Clasificación al Robomatrix Continental Master — avanzan los 3 primeros lugares")),
    ]


def certs_coursework():
    anthropic = t("Anthropic · Certificate of completion", "Anthropic · Certificado de finalización")
    return [
        dict(kind=t("Coursework", "Curso"), title="AI Fluency: Framework &amp; Foundations", detail=anthropic,
             when=t("Jul. 2026", "Jul. 2026"), file="anthropic-ai-fluency"),
        dict(kind=t("Coursework", "Curso"),
             title=t("Introduction to AI Engineering — Phase I", "Introducción a la Ingeniería en Inteligencia Artificial — Fase I"),
             detail=t("Iberoamerican Technology Foundation, with support from the Salesforce Foundation",
                      "Iberoamerican Technology Foundation, con apoyo de Fundación Salesforce"),
             when=t("May 2026", "May. 2026"), file="itf-intro-ai-engineering"),
        dict(kind=t("Coursework", "Curso"), title="Claude Code 101", detail=anthropic,
             when=t("Apr. 2026", "Abr. 2026"), file="anthropic-claude-code-101"),
        dict(kind=t("Coursework", "Curso"), title="Claude 101", detail=anthropic,
             when=t("Apr. 2026", "Abr. 2026"), file="anthropic-claude-101"),
    ]


def cert_pdf(c):
    path = f"assets/img/certificates/{c['file']}.pdf"
    return path if os.path.exists(os.path.join(ROOT, path)) else None


def records(items):
    return "\n".join(record(c["kind"], c["title"], c["detail"], c["when"]) for c in items)


def cert_card(c):
    pdf = cert_pdf(c)
    jpg = f"assets/img/certificates/{c['file']}.jpg"
    if pdf and os.path.exists(os.path.join(ROOT, jpg)):
        thumb = (f'<a class="cert-thumb" href="{pre()}{pdf}" target="_blank" rel="noopener">'
                 f'<img src="{pre()}{jpg}" alt="{t("Certificate", "Certificado")}: {c["title"]}" loading="lazy"></a>')
        link = f'<a class="lbl text-link" href="{pre()}{pdf}" target="_blank" rel="noopener">{t("View certificate", "Ver certificado")} ↗</a>'
    else:
        thumb = f'<div class="cert-thumb ph"><span class="lbl">{c["title"]}</span><span class="note">{c["detail"].split(" · ")[0]}</span></div>'
        link = ""
    doc = f'<p class="lbl faint">{c["doc"]}</p>' if c.get("doc") else ""
    return f'''<article class="cert">
{thumb}
<div class="cert-meta"><span class="lbl faint">{c["kind"]}</span><span class="lbl accent">{c["when"]}</span></div>
<h3>{c["title"]}</h3>
<p class="body">{c["detail"]}</p>
{doc}
{link}
</article>'''


# ---- Pages ------------------------------------------------------------------

def index():
    main = f'''<div class="wrap">
<section class="hero">
<div class="hero-copy">
<span class="eyebrow lbl">{t("Engineering · Robotics · Hospitality", "Ingeniería · Robótica · Hospitalidad")}</span>
<h1 class="display">Alejandro<br><em>Favero</em></h1>
<p class="tagline">{t("Engineer. Builder. Founder.", "Ingeniero. Constructor. Fundador.")}</p>
<p class="lede">{t("Electrical &amp; Electronics Engineering student at UNAM, designing competition robots from bare PCBs — and running Travel in Oaxaca, a travel blog started in 2020 that has grown into a DMC and luxury travel concierge. Headed toward graduate research in physics, mathematics, or robotics.",
                   "Estudiante de Ingeniería Eléctrica Electrónica en la UNAM que diseña robots de competencia desde la PCB — y dirige Travel in Oaxaca, un blog de viajes nacido en 2020 que hoy es una DMC y concierge de viajes de lujo. Rumbo a un posgrado de investigación en física, matemáticas o robótica.")}</p>
<div class="btn-row">
<a class="btn btn-primary" href="projects.html">{t("View selected work", "Ver proyectos")} <span aria-hidden="true">→</span></a>
<a class="btn btn-secondary" href="travel.html">Travel in Oaxaca</a>
</div>
</div>
{photo("assets/img/portrait.jpg", t("Portrait", "Retrato"), t("4 : 5 · natural light, dark backdrop", "4 : 5 · luz natural, fondo oscuro"),
       alt=t("Alejandro Favero on the beach at sunset", "Alejandro Favero en la playa al atardecer"),
       fig=("Fig. 01", credit()), pos="50% 22%")}
</section>

<section class="stats" aria-label="{t("At a glance", "En resumen")}">
<div class="stat"><span class="n">9.4<small> / 10</small></span><span class="lbl">{t("GPA · UNAM Electrical &amp; Electronics Eng.", "Promedio · Ing. Eléctrica Electrónica, UNAM")}</span></div>
<div class="stat"><span class="n">3<sup>{t("rd", "er")}</sup></span><span class="lbl">Minisumo · Roboduca 2026</span></div>
<div class="stat"><span class="n">4<sup>{t("th", "º")}</sup></span><span class="lbl">{t("Continental · Robomatrix Minisumo", "Continental · Minisumo Robomatrix")}</span></div>
<div class="stat"><span class="n">2020</span><span class="lbl">{t("Travel in Oaxaca, started as a blog", "Travel in Oaxaca, nace como blog")}</span></div>
</section>
</div>

<section class="section">
<div class="wrap">
{section_head(t("§ 01 — Practice", "§ 01 — Práctica"),
              t('Two disciplines,<br><em class="soft">one standard of care.</em>', 'Dos disciplinas,<br><em class="soft">un mismo nivel de cuidado.</em>'),
              f'<p class="body">{t("Both start from first principles and are carried end to end — a robot from bare board to competition, a trip from first inquiry to the last day in Oaxaca.", "Ambas parten de primeros principios y se llevan de principio a fin — un robot, de la placa desnuda a la competencia; un viaje, de la primera consulta al último día en Oaxaca.")}</p>')}
<div class="duo">
<a class="duo-card" href="projects.html">
{photo("assets/img/projects/minisumo-pcb.jpg", t("Photo — Minisumo robot", "Foto — Robot minisumo"), t("Macro on the custom PCB", "Macro sobre la PCB propia"),
       alt=t("Close-up of the Minisumo robot's custom PCB", "Detalle de la PCB propia del robot minisumo"))}
<div class="row"><span class="lbl accent">{t("I. Engineering", "I. Ingeniería")}</span><span class="lbl faint">UNAM · CROFI</span></div>
<h3>{t("Robots from bare components.", "Robots desde cero.")}</h3>
<p class="body">{t("Custom PCB layout, 3D-printed chassis and embedded firmware in C/C++ — designed, fabricated and programmed without kits.",
                   "Diseño de PCB propio, chasis impreso en 3D y firmware embebido en C/C++ — diseñados, fabricados y programados sin kits.")}</p>
<span class="lbl go">{t("Selected work →", "Proyectos →")}</span>
</a>
<a class="duo-card" href="travel.html">
{photo("assets/img/travel/oaxaca-landscape.jpg", t("Photo — Oaxaca", "Foto — Oaxaca"), t("Landscape or architecture, golden hour", "Paisaje o arquitectura, hora dorada"),
       alt=t("Stone fretwork of the Palace of Mitla, Oaxaca", "Grecas de piedra del Palacio de Mitla, Oaxaca"),
       by=t("Mitla · ", "Mitla · ") + credit(link=False))}
<div class="row"><span class="lbl accent">{t("II. Hospitality", "II. Hospitalidad")}</span><span class="lbl faint">{t("Oaxaca · Since 2020", "Oaxaca · Desde 2020")}</span></div>
<h3>{t("Oaxaca, handled with care.", "Oaxaca, con todo cuidado.")}</h3>
<p class="body">{t("Travel in Oaxaca — started as a blog in 2020, then tours after the pandemic; today a DMC and luxury travel concierge, run while studying engineering full time.",
                   "Travel in Oaxaca — nació como blog en 2020, después de la pandemia llegaron los tours; hoy es una DMC y concierge de viajes de lujo, dirigida mientras estudio ingeniería de tiempo completo.")}</p>
<span class="lbl go">Travel in Oaxaca →</span>
</a>
</div>
</div>
</section>

<section class="section" id="work">
<div class="wrap">
{section_head(t("§ 02 — Selected work", "§ 02 — Proyectos"),
              t("Built from <em>first principles.</em>", "Construido desde <em>primeros principios.</em>"),
              f'<a class="lbl text-link" href="projects.html">{t("All projects →", "Todos los proyectos →")}</a>')}
{feature_minisumo()}
</div>
</section>

<section class="section raised">
<div class="wrap">
{section_head(t("§ 03 — The route so far", "§ 03 — El recorrido"),
              t("From Oaxaca <em>to the lab.</em>", "De Oaxaca <em>al laboratorio.</em>"),
              f'<span class="lbl faint">{t("Solid — completed · Dashed — next", "Continua — completado · Punteada — siguiente")}</span>')}
<ol class="route">
<li class="stop"><span class="node" aria-hidden="true"></span><span class="lbl accent">{t("Oct. 2020", "Oct. 2020")}</span><span class="place">Oaxaca</span><p>{t("Started Travel in Oaxaca as a travel blog — today a DMC and luxury concierge.", "Inicié Travel in Oaxaca como blog de viajes — hoy una DMC y concierge de lujo.")}</p></li>
<li class="stop"><span class="node" aria-hidden="true"></span><span class="lbl accent">{t("High school", "Bachillerato")}</span><span class="place">CBTIS 26</span><p>{t("Robomatrix Minisumo — 3rd regional, 4th continental.", "Minisumo Robomatrix — 3.º regional, 4.º continental.")}</p></li>
<li class="stop"><span class="node" aria-hidden="true"></span><span class="lbl accent">{t("In progress", "En curso")}</span><span class="place">UNAM</span><p>{t("Electrical &amp; Electronics Engineering, GPA 9.4 / 10.", "Ingeniería Eléctrica Electrónica, promedio 9.4 / 10.")}</p></li>
<li class="stop"><span class="node" aria-hidden="true"></span><span class="lbl accent">2026</span><span class="place">Roboduca</span><p>{t("3rd place, Minisumo, with the CROFI Robotics Club.", "3.er lugar en Minisumo, con el Club de Robótica CROFI.")}</p></li>
<li class="stop next"><span class="node" aria-hidden="true"></span><span class="lbl faint">{t("Next", "Siguiente")}</span><span class="place">{t("Graduate research", "Posgrado de investigación")}</span><p>{t("Physics, mathematics, or robotics at a research program.", "Física, matemáticas o robótica en un programa de investigación.")}</p></li>
</ol>
</div>
</section>

<section class="section">
<div class="wrap">
{section_head(t("§ 04 — Recognition", "§ 04 — Reconocimientos"),
              t("Results, <em>on the record.</em>", "Resultados, <em>documentados.</em>"),
              f'<a class="lbl text-link" href="certificates.html">{t("All recognition →", "Todos los reconocimientos →")}</a>')}
<div class="split">
<div class="records">
{records(certs_competition())}
{records(certs_coursework())}
</div>
{languages_panel()}
</div>
</div>
</section>'''
    return page("index.html", "Alejandro Favero",
                t("Electrical & Electronics Engineering student at UNAM, competition robot builder, and founder of Travel in Oaxaca.",
                  "Estudiante de Ingeniería Eléctrica Electrónica en la UNAM, constructor de robots de competencia y fundador de Travel in Oaxaca."),
                main)


def about():
    entries = [
        (t("Founder — Travel in Oaxaca", "Fundador — Travel in Oaxaca"),
         t("Oaxaca, México · Oct. 2020 – present", "Oaxaca, México · Oct. 2020 – actual"),
         t("Started in October 2020 as a travel blog; after the pandemic, readers began requesting tours, and it has recently become a DMC and bilingual (English / Spanish) luxury travel concierge. Designed and built the business’s website, including a multi-step inquiry form.",
           "Comenzó en octubre de 2020 como blog de viajes; después de la pandemia empezaron a llegar solicitudes de tours, y recientemente se convirtió en una DMC y concierge de viajes de lujo bilingüe (inglés / español). Diseñé y construí el sitio web del negocio, incluido un formulario de consulta de varios pasos."),
         ("travel.html", t("Travel in Oaxaca →", "Travel in Oaxaca →"))),
        (t("Minisumo team — CROFI, UNAM", "Equipo Minisumo — CROFI, UNAM"),
         t("Faculty of Engineering, UNAM · In progress", "Facultad de Ingeniería, UNAM · En curso"),
         t("Designing and fabricating a competition robot from scratch — custom PCB, 3D-printed chassis, embedded firmware. 3rd place, Roboduca 2026.",
           "Diseño y fabricación de un robot de competencia desde cero — PCB propia, chasis impreso en 3D, firmware embebido. 3.er lugar, Roboduca 2026."),
         ("projects.html", t("Selected work →", "Proyectos →"))),
        (t("Video editor — freelance", "Editor de video — independiente"),
         t("Oaxaca, México · ~2 years, during high school", "Oaxaca, México · ~2 años, durante el bachillerato"),
         t("Edited and delivered video for weddings, quinceañeras, baptisms, and other social events.",
           "Edición y entrega de video para bodas, XV años, bautizos y otros eventos sociales."),
         None),
        (t("Robotics Club — CBTIS 26", "Club de Robótica — CBTIS 26"),
         t("High school", "Bachillerato"),
         t("Built the Minisumo and RoboFut robots later entered at Robomatrix — 3rd place regional and 4th place continental in Minisumo, competing against university-level teams.",
           "Construí los robots Minisumo y RoboFut que después compitieron en Robomatrix — 3.er lugar regional y 4.º continental en Minisumo, contra equipos universitarios."),
         ("projects.html", t("Selected work →", "Proyectos →"))),
    ]
    entry_html = []
    for title, meta, text, link in entries:
        link_html = f'<a class="lbl text-link" href="{link[0]}">{link[1]}</a>' if link else ""
        entry_html.append(f'''<article class="entry">
<div><h3>{title}</h3><p class="lbl meta">{meta}</p></div>
<div class="body"><p>{text}</p>{link_html}</div>
</article>''')

    skills = [
        (t("Hardware design &amp; fabrication", "Diseño y fabricación de hardware"),
         t("PCB design, 3D printing, soldering, and electronic assembly.", "Diseño de PCB, impresión 3D, soldadura y ensamble electrónico."),
         t("Intermediate", "Intermedio")),
        (t("Embedded programming", "Programación embebida"), "Arduino / ESP32, C / C++.", t("Intermediate", "Intermedio")),
        (t("Data structures in C", "Estructuras de datos en C"),
         t("Linked lists, stacks, queues, dynamic arrays.", "Listas ligadas, pilas, colas, arreglos dinámicos."),
         t("Basic–Intermediate", "Básico–Intermedio")),
        (t("Web development", "Desarrollo web"), "WordPress, CSS.", t("Basic", "Básico")),
        (t("Workflow tools", "Herramientas de trabajo"), "Notion, Google Calendar.", ""),
    ]
    skill_html = "\n".join(
        f'<div class="skill"><div><h3>{n}</h3><p>{d}</p></div>' + (f'<span class="tag lbl">{lvl}</span>' if lvl else "") + '</div>'
        for n, d, lvl in skills)

    main = f'''<div class="wrap">
<section class="page-hero">
<span class="eyebrow lbl">{t("Profile", "Perfil")}</span>
<h1 class="page-title">{t("About", "Sobre")} <em>{t("me.", "mí.")}</em></h1>
<p class="lede">{t("Third-semester Electrical &amp; Electronics Engineering student at UNAM (GPA 9.4 / 10), with hands-on experience designing and building competition robots from scratch — PCB, mechanical fabrication, and embedded firmware — and founder of Travel in Oaxaca, a DMC and luxury travel concierge. Working toward a rigorous quantitative foundation in engineering, with an eye on graduate study in physics, mathematics, or robotics at top research programs.",
                   "Estudiante de tercer semestre de Ingeniería Eléctrica Electrónica en la UNAM (promedio 9.4 / 10), con experiencia práctica diseñando y construyendo robots de competencia desde cero — PCB, fabricación mecánica y firmware embebido — y fundador de Travel in Oaxaca, una DMC y concierge de viajes de lujo. Construyendo una base cuantitativa rigurosa en ingeniería, con la mira en un posgrado en física, matemáticas o robótica en programas de investigación de primer nivel.")}</p>
</section>
</div>

<section class="section">
<div class="wrap">
{section_head(t("§ 01 — Education", "§ 01 — Formación"), t("UNAM, <em>Faculty of Engineering.</em>", "UNAM, <em>Facultad de Ingeniería.</em>"))}
<div class="split">
{spec([(t("Program", "Carrera"), t("Electrical &amp; Electronics Engineering", "Ingeniería Eléctrica Electrónica")),
       (t("Length", "Duración"), t("10 semesters · Mexico City", "10 semestres · Ciudad de México")),
       (t("Standing", "Estado"), t("Third semester, in progress", "Tercer semestre, en curso")),
       (t("GPA", "Promedio"), "9.4 / 10", True),
       (t("Current course", "Asignatura en curso"), t("<em>Developing Management Skills</em>, Faculty of Engineering (term 2027-1)",
                                                  "<em>Desarrollo de Habilidades Directivas</em>, Facultad de Ingeniería (semestre 2027-1)"))])}
<div class="stats" style="grid-template-columns: repeat(2, minmax(0, 1fr));">
<div class="stat"><span class="n">9.4<small> / 10</small></span><span class="lbl">{t("GPA", "Promedio")}</span></div>
<div class="stat"><span class="n">3<sup>{t("rd", "er")}</sup></span><span class="lbl">{t("Semester of 10", "Semestre de 10")}</span></div>
</div>
</div>
</div>
</section>

<section class="section">
<div class="wrap">
{section_head(t("§ 02 — Experience", "§ 02 — Experiencia"), t("What I’ve <em>built and run.</em>", "Lo que he <em>construido y dirigido.</em>"))}
<div class="entries">
{chr(10).join(entry_html)}
</div>
</div>
</section>

<section class="section">
<div class="wrap">
{section_head(t("§ 03 — Skills", "§ 03 — Habilidades"), t("Hardware, firmware, <em>and code.</em>", "Hardware, firmware <em>y código.</em>"))}
<div class="split">
<div class="stack">
{skill_html}
</div>
{languages_panel()}
</div>
</div>
</section>

<section class="section">
<div class="wrap">
{section_head(t("§ 04 — Ways of working", "§ 04 — Forma de trabajo"), t("How the work <em>gets done.</em>", "Cómo se <em>hace el trabajo.</em>"))}
<ul class="marks" style="max-width: 44em;">
<li>{t("Bilingual client communication, English / Spanish.", "Comunicación bilingüe con clientes, inglés / español.")}</li>
<li>{t("End-to-end project execution — design, fabrication, and programming — carried out independently from start to finish.", "Ejecución de proyectos de principio a fin — diseño, fabricación y programación — de forma independiente.")}</li>
<li>{t("Teamwork within technical collaboration dynamics.", "Trabajo en equipo en dinámicas de colaboración técnica.")}</li>
<li>{t("Analytical rigor and a preference for solving problems from first principles.", "Rigor analítico y preferencia por resolver problemas desde primeros principios.")}</li>
</ul>
</div>
</section>'''
    return page("about.html", t("About — Alejandro Favero", "Perfil — Alejandro Favero"),
                t("Education, experience, languages, and skills of Alejandro Favero, Electrical & Electronics Engineering student at UNAM.",
                  "Formación, experiencia, idiomas y habilidades de Alejandro Favero, estudiante de Ingeniería Eléctrica Electrónica en la UNAM."),
                main)


def projects():
    main = f'''<div class="wrap">
<section class="page-hero">
<span class="eyebrow lbl">{t("Selected work", "Proyectos")}</span>
<h1 class="page-title">{t("Built from<br><em>first principles.</em>", "Construido desde<br><em>primeros principios.</em>")}</h1>
<p class="lede">{t("Robots designed and built from bare components — no kits — covering PCB layout, mechanical fabrication, and embedded firmware end to end.",
                   "Robots diseñados y construidos desde componentes — sin kits — cubriendo diseño de PCB, fabricación mecánica y firmware embebido de principio a fin.")}</p>
</section>
</div>

<section class="section" style="padding-top: 0;">
<div class="wrap">
{feature_minisumo()}
{feature_robomatrix()}
</div>
</section>

<section class="section raised">
<div class="wrap cta">
<span class="lbl accent">{t("In progress", "En curso")}</span>
<h2 class="section-title">{t("More builds, <em>being written up.</em>", "Más proyectos, <em>en documentación.</em>")}</h2>
<p class="body">{t("The Minisumo’s PCB and firmware are being prepared for an open-source release on GitHub.",
                   "La PCB y el firmware del Minisumo se están preparando para publicarse como open source en GitHub.")}</p>
<div class="btn-row">
<a class="btn btn-primary" href="https://github.com/AlejandroFavero" target="_blank" rel="noopener">GitHub <span aria-hidden="true">↗</span></a>
<a class="btn btn-secondary" href="certificates.html">{t("Recognition", "Reconocimientos")}</a>
</div>
</div>
</section>'''
    return page("projects.html", t("Projects — Alejandro Favero", "Proyectos — Alejandro Favero"),
                t("Competition robots built from bare PCBs — chassis, firmware, and results.",
                  "Robots de competencia construidos desde la PCB — chasis, firmware y resultados."),
                main)


def certificates():
    main = f'''<div class="wrap">
<section class="page-hero">
<span class="eyebrow lbl">{t("Recognition", "Reconocimientos")}</span>
<h1 class="page-title">{t("Results,<br><em>on the record.</em>", "Resultados,<br><em>documentados.</em>")}</h1>
<p class="lede">{t("Competition results and completed coursework. New certificates are added as they are earned.",
                   "Resultados de competencia y cursos completados. Los nuevos certificados se agregan conforme se obtienen.")}</p>
</section>
</div>

<section class="section" style="padding-top: 0;">
<div class="wrap">
{section_head(t("§ 01 — Competition", "§ 01 — Competencias"), t("On the <em>dohyo.</em>", "En el <em>dohyo.</em>"))}
<div class="certs">
{chr(10).join(cert_card(c) for c in certs_competition())}
</div>
</div>
</section>

<section class="section">
<div class="wrap">
{section_head(t("§ 02 — Coursework", "§ 02 — Cursos"), t("Always <em>learning.</em>", "Siempre <em>aprendiendo.</em>"))}
<div class="certs">
{chr(10).join(cert_card(c) for c in certs_coursework())}
</div>
</div>
</section>'''
    return page("certificates.html", t("Recognition — Alejandro Favero", "Reconocimientos — Alejandro Favero"),
                t("Competition results and coursework certificates.", "Resultados de competencia y certificados de cursos."),
                main)


def travel():
    def g(path, label, note, h, cls=""):
        return photo(path, label, note, h=h, cls=cls)
    main = f'''<section class="oax-hero">
{photo("assets/img/travel/oaxaca-landscape.jpg", t("Photo — full-bleed Oaxaca landscape · 16 : 9", "Foto — paisaje de Oaxaca a sangre · 16 : 9"),
       alt=t("Stone fretwork of the Palace of Mitla, Oaxaca", "Grecas de piedra del Palacio de Mitla, Oaxaca"), pos="50% 45%")}
<div class="oax-hero-copy">
<div class="wrap">
<div>
<span class="eyebrow lbl">{t("II. Hospitality — since October 2020", "II. Hospitalidad — desde octubre de 2020")}</span>
<h1 class="page-title" style="font-size: clamp(64px, 9.7vw, 140px);">Travel in<br><em>Oaxaca</em></h1>
</div>
<div class="oax-hero-aside">
<p class="tagline">{t("A DMC and luxury travel concierge — grown from a travel blog, run while studying engineering full time.",
                      "Una DMC y concierge de viajes de lujo — nacida de un blog de viajes, dirigida mientras estudio ingeniería de tiempo completo.")}</p>
<p class="lbl hero-credit">Mitla, Oaxaca · {credit()}</p>
</div>
</div>
</div>
</section>

<section class="section">
<div class="wrap intro">
{spec([(t("Role", "Rol"), t("Founder", "Fundador")),
       (t("Founded", "Fundación"), t("October 2020, as a blog", "Octubre 2020, como blog")),
       (t("Today", "Hoy"), t("DMC · Luxury concierge", "DMC · Concierge de lujo"), True),
       (t("Languages", "Idiomas"), t("English · Spanish", "Inglés · Español")),
       (t("Base", "Sede"), "Oaxaca, México")])}
<div class="stack" style="gap: 32px;">
<span class="lbl accent">{t("§ 01 — The house", "§ 01 — La casa")}</span>
<p class="statement">{t("For travelers who want Oaxaca handled with care — in their own language, <em>from first inquiry to the last evening.</em>",
                        "Para viajeros que quieren vivir Oaxaca con todo cuidado — en su propio idioma, <em>de la primera consulta a la última noche.</em>")}</p>
<a class="lbl text-link" href="https://travelinoaxaca.com" target="_blank" rel="noopener">travelinoaxaca.com ↗</a>
</div>
</div>
</section>

<section class="section">
<div class="wrap">
{section_head(t("§ 02 — How it grew", "§ 02 — Cómo creció"), t("From a blog <em>to a DMC.</em>", "De un blog <em>a una DMC.</em>"))}
<ol class="services">
<li class="service"><span class="lbl accent">2020</span><h3>Blog</h3><p class="body">{t("Travel in Oaxaca began in October 2020 as a travel blog about Oaxaca.", "Travel in Oaxaca comenzó en octubre de 2020 como un blog de viajes sobre Oaxaca.")}</p></li>
<li class="service"><span class="lbl accent">{t("After the pandemic", "Después de la pandemia")}</span><h3>Tours</h3><p class="body">{t("As travel reopened, readers started sending tour requests — and the blog began organizing trips.", "Con la reapertura de los viajes, los lectores empezaron a solicitar tours — y el blog comenzó a organizar viajes.")}</p></li>
<li class="service"><span class="lbl accent">{t("Today", "Hoy")}</span><h3>{t("DMC &amp; concierge", "DMC y concierge")}</h3><p class="body">{t("A destination management company (DMC) and luxury travel concierge, handling Oaxaca end to end.", "Una empresa de gestión de destinos (DMC) y concierge de viajes de lujo que se encarga de Oaxaca de principio a fin.")}</p></li>
</ol>
</div>
</section>

<section class="section">
<div class="wrap">
{section_head(t("§ 03 — The work", "§ 03 — El trabajo"), t("Run end to end, <em>by one person.</em>", "De principio a fin, <em>por una sola persona.</em>"))}
<div class="services">
<div class="service"><span class="num">01</span><h3>Concierge</h3><p class="body">{t("Bilingual, direct client service for guests visiting Oaxaca, in English or Spanish.", "Atención directa y bilingüe para quienes visitan Oaxaca, en inglés o español.")}</p></div>
<div class="service"><span class="num">02</span><h3>{t("Digital", "Digital")}</h3><p class="body">{t("Designed and built the business’s website, including a multi-step inquiry form.", "Diseñé y construí el sitio web del negocio, incluido un formulario de consulta de varios pasos.")}</p></div>
<div class="service"><span class="num">03</span><h3>{t("Brand", "Marca")}</h3><p class="body">{t("Brand positioning and content writing for a luxury audience.", "Posicionamiento de marca y redacción de contenido para un público de lujo.")}</p></div>
</div>
</div>
</section>

<section class="section">
<div class="wrap">
{section_head(t("§ 04 — Field notes", "§ 04 — Notas de campo"), t("From <em>Oaxaca.</em>", "Desde <em>Oaxaca.</em>"), '<span class="lbl faint">Fig. 02 — 06</span>')}
<div class="gallery">
{g("assets/img/travel/field-landscape.jpg", t("Fig. 02 — Landscape", "Fig. 02 — Paisaje"), t("Wide, golden hour", "Plano abierto, hora dorada"), 580, "g-7")}
<div class="g-col">
{g("assets/img/travel/field-architecture.jpg", t("Fig. 03 — Architecture", "Fig. 03 — Arquitectura"), t("Colonial detail, stone and color", "Detalle colonial, cantera y color"), 278)}
{g("assets/img/travel/field-table.jpg", t("Fig. 04 — Table", "Fig. 04 — Mesa"), t("Mezcal, mole, market", "Mezcal, mole, mercado"), 278)}
</div>
{g("assets/img/travel/field-craft.jpg", t("Fig. 05 — Craft", "Fig. 05 — Artesanía"), t("Textiles or alebrijes, close-up", "Textiles o alebrijes, en detalle"), 340, "g-5")}
{g("assets/img/travel/field-guests.jpg", t("Fig. 06 — Guests", "Fig. 06 — Huéspedes"), t("A client moment, with permission", "Un momento con clientes, con permiso"), 340, "g-7")}
</div>
</div>
</section>

<section class="section raised">
<div class="wrap cta">
<span class="lbl accent">{t("§ 05 — Plan a journey", "§ 05 — Planea tu viaje")}</span>
<h2 class="section-title">Oaxaca, <em>{t("well planned.", "bien planeado.")}</em></h2>
<p class="body">{t("Inquiries are handled personally, in English or Spanish, through the Travel in Oaxaca website.",
                   "Las consultas se atienden personalmente, en inglés o español, a través del sitio de Travel in Oaxaca.")}</p>
<div class="btn-row">
<a class="btn btn-primary" href="https://travelinoaxaca.com" target="_blank" rel="noopener">{t("Visit travelinoaxaca.com", "Visita travelinoaxaca.com")} <span aria-hidden="true">↗</span></a>
<a class="btn btn-secondary" href="index.html">{t("Back to engineering", "Volver a ingeniería")}</a>
</div>
</div>
</section>'''
    return page("travel.html", "Travel in Oaxaca — Alejandro Favero",
                t("Travel in Oaxaca — a travel blog started in 2020 that grew into a DMC and luxury travel concierge, run by Alejandro Favero.",
                  "Travel in Oaxaca — un blog de viajes nacido en 2020 que se convirtió en una DMC y concierge de viajes de lujo, dirigida por Alejandro Favero."),
                main, body_cls="sheet-oaxaca", coords="17.07° N · 96.73° W", footer=footer_slim)


PAGES = {"index.html": index, "about.html": about, "projects.html": projects,
         "certificates.html": certificates, "travel.html": travel}


def main():
    global L
    for L in ("en", "es"):
        out_dir = ROOT if L == "en" else os.path.join(ROOT, "es")
        os.makedirs(out_dir, exist_ok=True)
        for name, build in PAGES.items():
            with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
                f.write(build())
            print(f"wrote {'' if L == 'en' else 'es/'}{name}")


if __name__ == "__main__":
    main()
