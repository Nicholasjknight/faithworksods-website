#!/usr/bin/env python3
"""Generate Faith Works Outdoor Services static website."""

from __future__ import annotations

import json
import os
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import quote

from service_areas_data import (
    CITIES as AREA_CITIES,
    CITY_BY_SLUG,
    CITY_NAMES,
    COUNTIES,
    COUNTY_BY_NAME,
    FEATURED_CITIES,
    HOME_CITY,
    HOME_ZIP,
    SERVICE_RADIUS_MILES,
    cities_in_county,
    city_href,
)
from services_data import (
    NOT_OFFERED,
    NOT_OFFERED_NOTE,
    PHASE1_COUNT,
    PHASE1_SERVICES,
    SERVICE_BY_SLUG,
    SERVICE_CATEGORIES,
    SERVICE_COUNT,
    SERVICES,
    SITE_POSITIONING,
    services_for_category,
)

ROOT = Path(__file__).resolve().parent.parent  # E:\All Client Websites\Faith Works
LOGO = "Images/fw-logo3.png"


def sync_logo() -> None:
    src = ROOT / "Images" / "fw-logo3.png"
    dst = ROOT / "Images" / "Logo.png"
    if src.exists():
        shutil.copy2(src, dst)


def logo_coin(modifier: str = "fw-logo-coin--header", size: int = 68, alt: str = "", logo_src: str | None = None) -> str:
    src = logo_src or LOGO
    alt_attr = f' alt="{alt}"' if alt else ' alt=""'
    hidden = ' aria-hidden="true"' if not alt else ""
    return f"""<div class="fw-logo-coin {modifier}"{hidden}>
            <div class="fw-logo-coin__scene">
              <div class="fw-logo-coin__spinner">
                <div class="fw-logo-coin__face fw-logo-coin__face--front">
                  <img src="{src}"{alt_attr} width="{size}" height="{size}" loading="eager" decoding="async">
                </div>
                <div class="fw-logo-coin__face fw-logo-coin__face--back">
                  <img src="{src}" alt="" width="{size}" height="{size}" loading="eager" decoding="async">
                </div>
              </div>
            </div>
          </div>"""


def configured_formspree_id() -> str:
    env_id = os.environ.get("FORMSPREE_FORM_ID", "").strip()
    id_file = ROOT / "formspree-id.txt"
    form_id = env_id or (id_file.read_text(encoding="utf-8").strip() if id_file.exists() else "")
    return "" if form_id == "PLACEHOLDER" else form_id


def formspree_endpoint() -> str:
    form_id = configured_formspree_id()
    return f"https://formspree.io/f/{form_id}" if form_id else ""


def form_action_attrs(subject: str) -> tuple[str, str, str, str]:
    endpoint = formspree_endpoint()
    if endpoint:
        return endpoint, "POST", "multipart/form-data", ""
    mail_subject = quote(subject)
    return f"mailto:{SITE['email']}?subject={mail_subject}", "POST", "text/plain", ' data-form-mode="email"'


SITE = {
    "url": "https://faithworksods.com",
    "legal_name": "Faith Works Outdoor Services LLC",
    "brand": "Faith Works Outdoor Services",
    "short": "Faith Works ODS",
    "owner": "Tyler R. Edwards",
    "email": "contact@faithworksods.com",
    "phone_display": "(863) 272-1596",
    "phone_tel": "8632721596",
    "city": "Auburndale",
    "region": "FL",
    "area": f"Central Florida within {SERVICE_RADIUS_MILES} miles of {HOME_CITY}",
    "geo_lat": "28.0653",
    "geo_lng": "-81.7887",
    "facebook": "https://www.facebook.com/profile.php?id=PLACEHOLDER",
    "youtube": "https://www.youtube.com/@PLACEHOLDER",
    "formspree": "https://formspree.io/f/PLACEHOLDER",
    "ga4": "G-PLACEHOLDER",
    "clarity": "PLACEHOLDER",
}

GALLERY = [
    ("excavator-and-truck-photo.webp", "Kubota excavator and dump trailer on a residential pool dig-out support site in Polk County Florida", "Pool Dig-Out Support"),
    ("excavator-photo.webp", "Kubota mini excavator on a land clearing job site in Polk County", "Land Clearing"),
    ("photo-of-all-equipment.webp", "Faith Works Outdoor Services fleet — Kubota excavator, tractor with loader, pickup, dump trailer, and flatbed trailer", "Equipment"),
    ("stump-before-ground-leveled.webp", "Property cleanup and light grading after brush clearing in a residential yard", "Property Cleanup"),
    ("stump-during-removal-1.webp", "Kubota equipment during overgrowth removal and land clearing in Polk County", "Overgrowth Removal"),
    ("stump-during-removal-2.webp", "Equipment removing brush and root material during acreage cleanup", "Acreage Cleanup"),
    ("stump-during-removal.webp", "Compact equipment working through overgrown yard cleanup", "Overgrowth Removal"),
    ("stump-post-removal-1.webp", "Property after brush clearing with soil ready for leveling and cleanup", "Land Clearing"),
    ("stump-post-removal.webp", "Completed overgrowth removal with cleared ground and debris ready for haul-off", "Property Cleanup"),
    ("stump-prior-to-removal.webp", "Overgrown yard area before Faith Works brush clearing and cleanup begins", "Brush Clearing"),
    ("tractor.webp", "Kubota compact tractor with loader attachment on a Central Florida job site", "Equipment"),
    ("tractor-moving-item-with-grapple.webp", "Kubota tractor using a grapple attachment to move brush and debris during property cleanup", "Property Cleanup"),
    ("tractor-with-box-blade-leveling-ground.webp", "Kubota tractor with box blade leveling ground after brush clearing and cleanup", "Ditch Clearing"),
]

HERO_DESKTOP = "photo-of-all-equipment.webp"
HERO_MOBILE = "excavator-and-truck-photo.webp"

INTENT_ROUTES = [
    {
        "label": "Overgrown lots and acreage",
        "slug": "land-clearing",
        "text": "Clear brush, saplings, and unmanaged growth so the property is usable again.",
    },
    {
        "label": "Pond banks and retention areas",
        "slug": "pond-bank-clearing",
        "text": "Open up access, improve visibility, and clean up heavy growth near water edges.",
    },
    {
        "label": "Ditches and drainage paths",
        "slug": "ditch-clearing",
        "text": "Remove vegetation and debris from outdoor ditch areas without claiming engineered drainage work.",
    },
    {
        "label": "Storm and yard debris",
        "slug": "debris-removal",
        "text": "Haul away piles, limbs, brush, and cleanup debris after clearing or weather events.",
    },
    {
        "label": "Trails, fence lines, and access",
        "slug": "trail-clearing",
        "text": "Reopen routes around ponds, barns, fence lines, hunting areas, and private acreage.",
    },
    {
        "label": "Pool dig-out cleanup support",
        "slug": "pool-dig-out-support",
        "text": "Dirt removal and site cleanup support under a licensed pool contractor.",
    },
]

HOME_FAQS = [
    (
        "Do you offer free estimates?",
        f"Yes. Send photos through the contact form or email {SITE['email']}. Photo-based estimates help us review access, vegetation, debris, and project scope before scheduling.",
    ),
    (
        "What areas do you serve?",
        f"{SITE['brand']} is based in {SITE['city']} and serves {SITE['area']}, including Winter Haven, Lakeland, Bartow, Haines City, Lake Wales, and nearby communities.",
    ),
    (
        "Do I need to call 811 before digging?",
        "For digging or soil-moving work, contact Sunshine 811 at least two full business days before work begins so underground utilities can be marked.",
    ),
    (
        "Do you install pools or do utility trenching?",
        f"No. Faith Works does not install pools, hold pool contractor licensing, or perform utility trenching, stormwater system installation, sewer work, water mains, site development, or engineered drainage. The focus is {SITE_POSITIONING.lower()}.",
    ),
    (
        "What jobs do people usually call you for?",
        "Most calls are for pond banks, trails, brush, overgrowth, debris, and acreage cleanup. Pool dig-out support is available under licensed pool builders.",
    ),
    (
        "Can you help with pool dig-out dirt removal?",
        "Yes, as support under a licensed pool contractor. Faith Works can help with dirt removal and site cleanup, but does not contract directly as a pool installer.",
    ),
]

FACEBOOK_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>'
YOUTUBE_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>'


def live_url(url: str) -> bool:
    return bool(url and "PLACEHOLDER" not in url)


def same_as_links() -> list[str]:
    return [url for url in (SITE["facebook"], SITE["youtube"]) if live_url(url)]


def social_icon_links() -> str:
    links: list[str] = []
    if live_url(SITE["facebook"]):
        links.append(
            f'<a href="{SITE["facebook"]}" class="social-icon" target="_blank" rel="noopener noreferrer" aria-label="Facebook">{FACEBOOK_SVG}</a>'
        )
    if live_url(SITE["youtube"]):
        links.append(
            f'<a href="{SITE["youtube"]}" class="social-icon" target="_blank" rel="noopener noreferrer" aria-label="YouTube">{YOUTUBE_SVG}</a>'
        )
    return "\n              ".join(links)


def social_block(kind: str, attrs: str = "") -> str:
    links = social_icon_links()
    if not links:
        return ""
    attr = f" {attrs}" if attrs else ""
    if kind == "hero":
        return f"""
          <div class="hero-social"{attr}>
            <span class="hero-social-label">Follow us</span>
            <div class="social-icons">
              {links}
            </div>
          </div>"""
    if kind == "mobile":
        return f"""
    <div class="mobile-nav-social">
      <p class="mobile-nav-social-label">Follow Us</p>
      <div class="social-icons">
              {links}
      </div>
    </div>"""
    return f"""
        <div class="footer-social">
          <div class="social-icons">
              {links}
          </div>
        </div>"""


def clean_output(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"


def write_site_file(path: Path, text: str) -> None:
    path.write_text(clean_output(text), encoding="utf-8")


def fonts_head() -> str:
    return """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap"></noscript>"""


def favicon_head(root_prefix: str = "") -> str:
    return f"""  <link rel="icon" type="image/png" href="{root_prefix}Images/fw-logo3.png">
  <link rel="apple-touch-icon" href="{root_prefix}Images/fw-logo3.png">"""


def analytics_head() -> str:
    ga4 = SITE["ga4"]
    clarity = SITE["clarity"]
    if ga4 == "G-PLACEHOLDER":
        ga = ""
    else:
        ga = f"""  <script async src="https://www.googletagmanager.com/gtag/js?id={ga4}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{ga4}');
  </script>"""
    if clarity == "PLACEHOLDER":
        clarity_script = ""
    else:
        clarity_script = f"""  <script>window.addEventListener('load',function(){{setTimeout(function(){{(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(window,document,"clarity","script","{clarity}");}},4000);}},{{once:true}});</script>"""
    return ga + "\n" + clarity_script


def _option_selected(label: str, selected: str | None, service: dict | None = None) -> str:
    if not selected:
        return ""
    if selected == label or selected == "Other / Not sure":
        return " selected"
    if service and selected in (service["name"], service["form_label"], service["nav"]):
        return " selected"
    return ""


def service_options(selected: str | None = None) -> str:
    opts = ['<option value="" disabled selected>Select a service...</option>']
    for cat in SERVICE_CATEGORIES:
        group = services_for_category(cat["id"])
        if not group:
            continue
        opts.append(f'<optgroup label="{cat["label"]}">')
        for s in group:
            label = s["form_label"]
            sel = _option_selected(label, selected, s)
            opts.append(f'<option{sel}>{label}</option>')
        opts.append("</optgroup>")
    sel_other = ' selected' if selected == "Other / Not sure" else ""
    opts.append(f'<option{sel_other}>Other / Not sure</option>')
    return "\n                ".join(opts)


def nav_service_links(root_prefix: str = "") -> str:
    branches: list[str] = []
    for cat in SERVICE_CATEGORIES:
        group = services_for_category(cat["id"])
        if not group:
            continue
        sub_id = f"fw-mega-{cat['id']}"
        flyout_items = "\n".join(
            f'              <li class="fw-services-mega__flyout-item"><a href="{root_prefix}{s["slug"]}.html" role="menuitem">{s["nav"]}</a></li>'
            for s in group
        )
        branches.append(
            f"""
        <li class="fw-services-mega__item fw-services-mega__item--branch">
          <button type="button" class="fw-services-mega__trigger subnav-toggle" aria-expanded="false" aria-haspopup="true" aria-controls="{sub_id}">
            <span class="fw-services-mega__label">{cat['label']}</span>
            <span class="fw-services-mega__chevron" aria-hidden="true"></span>
          </button>
          <ul class="fw-services-mega__flyout" id="{sub_id}" role="menu">
{flyout_items}
          </ul>
        </li>"""
        )
    return f"""<ul class="fw-services-mega__list">
{"".join(branches)}
        </ul>"""


def mobile_service_links(root_prefix: str = "") -> str:
    lines = ['      <ul class="fw-mm-nav">']
    for cat in SERVICE_CATEGORIES:
        group = services_for_category(cat["id"])
        if not group:
            continue
        sub_id = f"fw-mobile-{cat['id']}"
        items = "\n".join(
            f'          <li class="fw-mm-item"><a class="fw-mm-sublink" href="{root_prefix}{s["slug"]}.html">{s["nav"]}</a></li>'
            for s in group
        )
        lines.append(
            f"""      <li class="fw-mm-item fw-mm-item--branch">
        <button type="button" class="fw-mm-trigger" aria-expanded="false" aria-controls="{sub_id}">
          <span class="fw-mm-label">{cat['label']}</span>
          <span class="fw-mm-chevron" aria-hidden="true"></span>
        </button>
        <ul class="fw-mm-submenu" id="{sub_id}" hidden>
{items}
        </ul>
      </li>"""
        )
    lines.append("      </ul>")
    return "\n".join(lines)


def area_page_href(slug: str, root_prefix: str = "") -> str:
    return f"{root_prefix}areas/{slug}.html"


def nav_area_links(root_prefix: str = "") -> str:
    branches: list[str] = []
    for county in COUNTIES:
        cities = cities_in_county(county["name"])
        if not cities:
            continue
        sub_id = f"fw-area-{county['slug']}"
        county_overview = (
            f'              <li class="fw-services-mega__flyout-item fw-services-mega__flyout-item--overview">'
            f'<a href="{area_page_href(county["slug"], root_prefix)}" role="menuitem">All {county["name"]}</a></li>'
        )
        flyout_items = county_overview + "\n" + "\n".join(
            f'              <li class="fw-services-mega__flyout-item"><a href="{area_page_href(c["slug"], root_prefix)}" role="menuitem">{c["name"]}, FL</a></li>'
            for c in cities
        )
        label = county["name"].replace(" County", "")
        branches.append(
            f"""
        <li class="fw-services-mega__item fw-services-mega__item--branch">
          <button type="button" class="fw-services-mega__trigger subnav-toggle" aria-expanded="false" aria-haspopup="true" aria-controls="{sub_id}">
            <span class="fw-services-mega__label">{label}</span>
            <span class="fw-services-mega__chevron" aria-hidden="true"></span>
          </button>
          <ul class="fw-services-mega__flyout" id="{sub_id}" role="menu">
{flyout_items}
          </ul>
        </li>"""
        )
    return f"""<ul class="fw-services-mega__list">
{"".join(branches)}
        </ul>"""


def mobile_area_links(root_prefix: str = "") -> str:
    lines = ['      <ul class="fw-mm-nav">']
    for county in COUNTIES:
        cities = cities_in_county(county["name"])
        if not cities:
            continue
        sub_id = f"fw-mobile-area-{county['slug']}"
        county_link = (
            f'          <li class="fw-mm-item"><a class="fw-mm-sublink fw-mm-sublink--overview" '
            f'href="{area_page_href(county["slug"], root_prefix)}">All {county["name"]}</a></li>'
        )
        items = county_link + "\n" + "\n".join(
            f'          <li class="fw-mm-item"><a class="fw-mm-sublink" href="{area_page_href(c["slug"], root_prefix)}">{c["name"]}, FL</a></li>'
            for c in cities
        )
        label = county["name"].replace(" County", "")
        lines.append(
            f"""      <li class="fw-mm-item fw-mm-item--branch">
        <button type="button" class="fw-mm-trigger" aria-expanded="false" aria-controls="{sub_id}">
          <span class="fw-mm-label">{label}</span>
          <span class="fw-mm-chevron" aria-hidden="true"></span>
        </button>
        <ul class="fw-mm-submenu" id="{sub_id}" hidden>
{items}
        </ul>
      </li>"""
        )
    lines.append("      </ul>")
    return "\n".join(lines)


def nav_areas_dropdown(current: str, root_prefix: str = "") -> str:
    is_current = current == "service-areas.html" or current.startswith("areas/")
    btn_cur = ' aria-current="page"' if is_current else ""
    return f"""        <div class="nav-dropdown-wrap">
          <button class="nav-dropdown-btn" aria-expanded="false" aria-haspopup="true"{btn_cur}>
            Service Areas
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
          </button>
          <div class="nav-dropdown-menu fw-services-mega fw-areas-mega" role="menu">
            <a href="{root_prefix}service-areas.html" class="fw-services-mega__overview" role="menuitem">All Service Areas</a>
            {nav_area_links(root_prefix)}
          </div>
        </div>"""


def service_mosaic_card(s: dict, delay_ms: int, featured: bool = False) -> str:
    img_alt = next((alt for f, alt, _lbl in GALLERY if f == s["mosaic_image"]), s["name"])
    badge = '<span class="fw-service-card__badge">Core Service</span>' if featured else ""
    return f"""
          <a class="fw-service-card{" fw-service-card--featured" if featured else ""}" href="{s['slug']}.html" data-fw-enter="bottom" style="--fw-enter-delay: {delay_ms}ms;">
            {badge}
            <img class="fw-service-card__bg" src="Images/gallery/{s['mosaic_image']}" alt="{img_alt}" loading="lazy" decoding="async" width="800" height="800">
            <span class="fw-service-card__overlay" aria-hidden="true"></span>
            <span class="fw-service-card__panel fw-service-card__panel--front">
              <strong class="fw-service-card__headline">{s['mosaic_headline']}</strong>
            </span>
            <span class="fw-service-card__panel fw-service-card__panel--hover">
              <strong class="fw-service-card__title">{s['name']}</strong>
              <span class="fw-service-card__detail">{s['desc']}</span>
              <span class="fw-service-card__cta">View More</span>
            </span>
          </a>"""


def service_directory_group(cat: dict) -> str:
    items = ""
    for s in services_for_category(cat["id"]):
        items += f"""
            <a class="service-directory-item" href="{s['slug']}.html">
              <strong>{s['name']}</strong>
              <span>{s['desc']}</span>
            </a>"""
    return f"""
        <div class="service-directory-group" data-fw-enter="bottom">
          <h3>{cat['label']}</h3>
          <p>{cat['description']}</p>
          <div class="service-directory-items">{items}
          </div>
        </div>"""


def scope_section() -> str:
    not_list = "\n".join(f"            <li>{item}</li>" for item in NOT_OFFERED)
    return f"""
    <section id="scope" class="scope-section section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Clear scope</p>
          <h2>Outdoor Property Services — Not Utility Excavation</h2>
          <p>Faith Works is positioned as <strong>{SITE_POSITIONING}</strong> — not an excavation contractor.</p>
        </div>
        <div class="scope-grid">
          <div class="scope-card scope-card--do" data-fw-enter="left">
            <h3>What we do</h3>
            <p>Land clearing, trail clearing, brush cutting, forestry mulching, pond bank clearing, pond cleanup, ditch clearing, debris removal, property cleanup, acreage cleanup, and owner-operated equipment services across {SITE['area']}.</p>
            <ul>
              <li>Pond banks, trails, brush, and overgrowth</li>
              <li>Acreage cleanup and property maintenance</li>
              <li>Pool dig-out support under licensed pool builders</li>
              <li>Tractor and equipment work for outdoor property jobs</li>
            </ul>
            <a class="btn btn-ghost" href="services.html">See all {SERVICE_COUNT} services</a>
          </div>
          <div class="scope-card scope-card--dont" data-fw-enter="right">
            <h3>What we do not do</h3>
            <p>{NOT_OFFERED_NOTE}</p>
            <ul>{not_list}
            </ul>
          </div>
        </div>
      </div>
    </section>"""


def related_services_block(slugs: list[str]) -> str:
    links = ""
    for slug in slugs:
        s = SERVICE_BY_SLUG.get(slug)
        if not s:
            continue
        links += f'            <a href="{slug}.html">{s["name"]}</a>\n'
    if not links:
        return ""
    return f"""
          <h2>Related Services</h2>
          <div class="related-services">{links}          </div>"""


def category_label(category_id: str) -> str:
    return next((cat["label"] for cat in SERVICE_CATEGORIES if cat["id"] == category_id), "Outdoor Property Services")


def intent_router_section(context: str = "home") -> str:
    intro = (
        "Start with the property problem, then choose the service that matches the scope. "
        "These routes help searchers and customers get from broad outdoor-service intent to the exact page they need."
    )
    if context == "services":
        intro = (
            "Not every outdoor project uses the same equipment or scope. Pick the closest need below, then send photos "
            "if you want Tyler to confirm the best service."
        )
    cards = ""
    for i, item in enumerate(INTENT_ROUTES):
        service = SERVICE_BY_SLUG[item["slug"]]
        cards += f"""
          <a class="intent-card" href="{service['slug']}.html" data-fw-enter="bottom" style="--fw-enter-delay: {(i % 3) * 70}ms;">
            <span class="intent-card__label">{item['label']}</span>
            <h3>{service['name']}</h3>
            <p>{item['text']}</p>
            <span class="intent-card__cta">View {service['nav']}</span>
          </a>"""
    return f"""
    <section class="intent-router section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Find the right fit</p>
          <h2>What Outdoor Problem Are You Trying to Solve?</h2>
          <p>{intro}</p>
        </div>
        <div class="intent-grid">{cards}
        </div>
      </div>
    </section>"""


def service_scope_details(s: dict) -> str:
    details = "\n".join(f"              <li>{b}</li>" for b in s["bullets"][:4])
    fits = "\n".join(f"              <li>{item}</li>" for item in s["ideal_for"][:4])
    city_links = "".join(
        f'<a href="{city_href(c["slug"])}">{c["name"]}</a>' for c in FEATURED_CITIES[:8]
    )
    return f"""
          <h2>How We Scope {s['name']}</h2>
          <p>Every {s['keyword']} request is scoped around access, vegetation or debris volume, equipment room, haul-off needs, and the condition you want the property left in. Clear scope keeps the estimate practical and prevents the job from being confused with utility excavation or engineered site work.</p>
          <div class="service-detail-grid">
            <article>
              <h3>Project details we review</h3>
              <ul>{details}
              </ul>
            </article>
            <article>
              <h3>Good-fit properties</h3>
              <ul>{fits}
              </ul>
            </article>
            <article>
              <h3>Fast estimate checklist</h3>
              <ul>
                <li>Photos or short video of the work area</li>
                <li>City, gate width, and equipment access notes</li>
                <li>Whether debris should be mulched, piled, or hauled off</li>
                <li>Known utilities, wet areas, slopes, or obstacles</li>
              </ul>
            </article>
          </div>
          <div class="service-area-links" aria-label="{s['name']} service areas">
            <span>{s['name']} service areas:</span>
            {city_links}
          </div>"""


def service_faqs(s: dict) -> list[tuple[str, str]]:
    return [
        (
            f"How do I get a {s['name'].lower()} estimate?",
            f"Send photos, the city or job address, access notes, and a short description of the area. Tyler reviews the scope and follows up with the next step for {s['name'].lower()} in {SITE['area']}.",
        ),
        (
            f"Is {s['name'].lower()} priced before work starts?",
            "Yes. The goal is to confirm the visible scope, equipment access, debris handling, and any limits before scheduling so the estimate is clear.",
        ),
        (
            f"Can this be combined with another service?",
            f"Often, yes. {s['name']} is commonly paired with related outdoor services such as {', '.join(SERVICE_BY_SLUG[slug]['name'] for slug in s['related_slugs'][:3] if slug in SERVICE_BY_SLUG)}.",
        ),
        (
            "What work is outside the scope?",
            "Faith Works does not install underground utilities, sewer systems, stormwater systems, water mains, engineered drainage, or pools. Digging work should be cleared through Sunshine 811 before it begins.",
        ),
    ]


def faq_accordion(faqs: list[tuple[str, str]], prefix: str) -> str:
    items = ""
    for i, (question, answer) in enumerate(faqs, start=1):
        item_id = f"{prefix}-faq-{i}"
        items += f"""
            <div class="faq-item"><button class="faq-question" aria-expanded="false" aria-controls="{item_id}">{question}<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></button><div class="faq-answer" id="{item_id}" aria-hidden="true" inert><div class="faq-answer-inner"><p>{answer}</p></div></div></div>"""
    return f"""
          <div class="faq-list service-faq-list">{items}
          </div>"""


def faq_page_schema(faqs: list[tuple[str, str]]) -> str:
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
            for question, answer in faqs
        ],
    }, indent=2)


def breadcrumb_schema(items: list[tuple[str, str]]) -> str:
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "name": name,
                "item": SITE["url"] if path == "index.html" else f"{SITE['url']}/{path}",
            }
            for i, (name, path) in enumerate(items, start=1)
        ],
    }, indent=2)


def service_schema(s: dict) -> str:
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": f"{SITE['url']}/{s['slug']}.html#service",
        "name": s["name"],
        "serviceType": s["keyword"],
        "category": category_label(s["category"]),
        "description": s["desc"],
        "url": f"{SITE['url']}/{s['slug']}.html",
        "mainEntityOfPage": f"{SITE['url']}/{s['slug']}.html",
        "image": f"{SITE['url']}/Images/gallery/{s['mosaic_image']}",
        "provider": {"@id": f"{SITE['url']}/#business"},
        "areaServed": [{"@type": "City", "name": f"{city}, FL"} for city in CITY_NAMES],
    }, indent=2)


def estimate_form(
    form_id: str = "hero-contact-form",
    selected: str | None = None,
    subject: str | None = None,
    page: str = "",
    compact: bool = False,
) -> str:
    subj = subject or f"New estimate request - {SITE['brand']}"
    page_field = f'<input type="hidden" name="page" value="{page}">' if page else ""
    form_class = "contact-form contact-form-hero" if compact else "contact-form"
    phone = SITE["phone_display"]
    action, method, enctype, mode_attr = form_action_attrs(subj)

    if compact:
        fields = f"""
              <div class="form-group">
                <label for="{form_id}-name">Your Name</label>
                <input type="text" id="{form_id}-name" name="name" placeholder="First and last name" required autocomplete="name">
              </div>
              <div class="form-group">
                <label for="{form_id}-phone">Phone Number</label>
                <input type="tel" id="{form_id}-phone" name="phone" placeholder="{phone}" required autocomplete="tel">
              </div>
              <div class="form-group">
                <label for="{form_id}-service">Service Needed</label>
                <select id="{form_id}-service" name="service" required>
                {service_options(selected)}
                </select>
              </div>
              <div class="form-group">
                <label for="{form_id}-message">Project Details</label>
                <textarea id="{form_id}-message" name="message" placeholder="City, property size, and what you need done..." rows="3"></textarea>
              </div>"""
        replyto_field = ""
    else:
        fields = f"""
              <div class="form-group">
                <label for="{form_id}-name">Your Name</label>
                <input type="text" id="{form_id}-name" name="name" placeholder="First and last name" required autocomplete="name">
              </div>
              <div class="form-group">
                <label for="{form_id}-phone">Phone Number</label>
                <input type="tel" id="{form_id}-phone" name="phone" placeholder="{phone}" required autocomplete="tel">
              </div>
              <div class="form-group">
                <label for="{form_id}-email">Email</label>
                <input type="email" id="{form_id}-email" name="email" placeholder="you@email.com" autocomplete="email">
              </div>
              <div class="form-group">
                <label for="{form_id}-location">Job Address / City</label>
                <input type="text" id="{form_id}-location" name="job_location" placeholder="Street or city in Polk County" required>
              </div>
              <div class="form-group">
                <label for="{form_id}-service">Service Needed</label>
                <select id="{form_id}-service" name="service" required>
                {service_options(selected)}
                </select>
              </div>
              <div class="form-group">
                <label for="{form_id}-photos">Upload Project Photos</label>
                <input type="file" id="{form_id}-photos" name="photos" accept="image/*" multiple>
              </div>
              <div class="form-group">
                <label for="{form_id}-access">Equipment Access Notes</label>
                <input type="text" id="{form_id}-access" name="access_notes" placeholder="Gate width, obstacles, utilities known">
              </div>
              <div class="form-group">
                <label for="{form_id}-message">Project Details</label>
                <textarea id="{form_id}-message" name="message" placeholder="Describe the property, size, timeline, and what you need cleared or removed..." rows="4"></textarea>
              </div>"""
        replyto_field = '<input type="hidden" name="_replyto" value="email">'

    return f"""
            <form class="{form_class}" action="{action}" method="{method}" id="{form_id}" enctype="{enctype}"{mode_attr}>
              {page_field}
              {fields}
              <input type="hidden" name="_subject" value="{subj}">
              {replyto_field}
              <input type="hidden" name="_format" value="plain">
              <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
              <div class="form-footer">
                <button type="submit" class="btn btn-primary btn-full">Send Estimate Request</button>
                <p class="form-note">Or call/text <a href="tel:{SITE['phone_tel']}">{phone}</a></p>
              </div>
            </form>
            <div class="form-success" id="{form_id}-success" aria-live="polite" hidden>
              <p class="form-success-msg">Thanks! Tyler will review your project and contact you shortly.</p>
            </div>"""


PHONE_ICON = (
    '<svg viewBox="0 0 24 24" width="18" height="18" focusable="false">'
    '<path fill="currentColor" d="M6.6 10.8c1.5 2.9 3.7 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 '
    "1.1.4 2.3.6 3.5.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.3 21 3 13.7 3 4c0-.6.4-1 1-1h3.5c.6 0 "
    "1 .4 1 1 0 1.2.2 2.4.6 3.5.1.3 0 .7-.2 1L6.6 10.8z\"/></svg>"
)


def call_cta_link(extra_class: str = "") -> str:
    classes = f"fw-header-call {extra_class}".strip()
    phone = SITE["phone_display"]
    return f"""<a href="tel:{SITE['phone_tel']}" class="{classes}" title="Call or text {phone}" aria-label="Call or text {phone}">
        <span class="fw-header-call__icon" aria-hidden="true">{PHONE_ICON}</span>
        <span class="fw-header-call__text">
          <span class="fw-header-call__label">Call or Text</span>
          <span class="fw-header-call__number">{phone}</span>
        </span>
      </a>"""


def header(current: str = "", root_prefix: str = "") -> str:
    logo_src = f"{root_prefix}{LOGO}"

    def nav_link(href: str, label: str) -> str:
        cur = ' aria-current="page"' if current == href else ""
        return f'<a href="{root_prefix}{href}"{cur}>{label}</a>'

    service_links = nav_service_links(root_prefix)
    call_link = call_cta_link()
    menu_call_link = call_cta_link("fw-header-call--menu")
    return f"""  <header class="site-header" id="top">
    <div class="container header-inner">
      <button class="hamburger-btn" id="hamburger-btn" aria-label="Open navigation menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
      <div class="brand-wrap">
        <a class="brand" href="{root_prefix}index.html" aria-label="{SITE['brand']} home">
          {logo_coin("fw-logo-coin--header", 68, SITE['brand'], logo_src)}
        </a>
        <div class="brand-text-wrap">
          <a href="{root_prefix}index.html" class="brand-title-link"><span class="brand-title">{SITE['brand']}</span></a>
          <span class="brand-tagline">{SITE_POSITIONING} · {SITE['city']}, FL</span>
          <div class="header-brand-ctas" aria-label="Quick actions">
            <a href="{root_prefix}contact.html" class="btn-mobile-estimate">Free Estimate</a>
          </div>
        </div>
      </div>
      <nav class="site-nav" aria-label="Primary navigation">
        {nav_link('index.html', 'Home')}
        {nav_link('about.html', 'About')}
        <div class="nav-dropdown-wrap">
          <button class="nav-dropdown-btn" aria-expanded="false" aria-haspopup="true">
            Service Menu
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
          </button>
          <div class="nav-dropdown-menu fw-services-mega" role="menu">
            {service_links}
          </div>
        </div>
        {nav_areas_dropdown(current, root_prefix)}
        {nav_link('gallery.html', 'Gallery')}
        {nav_link('contact.html', 'Contact')}
      </nav>
      <div class="header-actions">
        <a href="{root_prefix}contact.html" class="btn btn-primary btn-header-estimate">Request Estimate</a>
      </div>
      {call_link}
    </div>
  </header>"""


def footer(root_prefix: str = "") -> str:
    logo_src = f"{root_prefix}{LOGO}"
    cities = " &nbsp;&middot;&nbsp; ".join(CITY_NAMES[:6])
    return f"""  <footer class="site-footer">
    <div class="container footer-inner">
      {logo_coin("fw-logo-coin--footer", 80, SITE['brand'], logo_src)}
      <div class="footer-info">
        <p><strong>{SITE['legal_name']}</strong></p>
        <p>{SITE['owner']} &nbsp;-&nbsp; <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></p>
        <p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
        <p>Based in {SITE['city']}, {SITE['region']} &nbsp;&middot;&nbsp; Serving within {SERVICE_RADIUS_MILES} miles of {HOME_CITY}</p>
        <p class="footer-cities">{cities}</p>
        {social_block("footer")}
      </div>
    </div>
    <div class="footer-copy-bar">
      <nav class="footer-links" aria-label="Footer links">
        <a href="{root_prefix}gallery.html">Gallery</a>
        <a href="{root_prefix}service-areas.html">Service Areas</a>
        <a href="{root_prefix}contact.html">Contact</a>
        <a href="{root_prefix}privacy-policy.html">Privacy Policy</a>
      </nav>
      <p class="footer-copy">&copy; <span id="current-year"></span> {SITE['legal_name']}. All rights reserved. &nbsp;&middot;&nbsp; <a href="https://knightlogics.com" rel="noopener noreferrer" style="color:inherit;text-decoration:none;opacity:.7;">Site by Knight Logics</a></p>
      <p class="footer-disclaimer">Outdoor property services — not utility trenching or engineered stormwater installation. For digging projects, contact Sunshine 811 at least two full business days before work begins so underground utilities can be marked.</p>
    </div>
  </footer>

  <div class="nav-overlay" id="nav-overlay" aria-hidden="true"></div>
  <nav class="mobile-nav" id="mobile-nav" aria-label="Mobile navigation" aria-hidden="true" inert>
    <div class="mobile-nav-header">
      <a href="{root_prefix}index.html" class="mobile-menu-brand" aria-label="{SITE['brand']} home">
        {logo_coin("fw-logo-coin--menu", 36, SITE['brand'], logo_src)}
        <span class="mobile-menu-brand-name">{SITE['short']}</span>
      </a>
      <button class="mobile-nav-close" id="mobile-nav-close" aria-label="Close navigation menu">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <div class="mobile-nav-links">
      <a href="{root_prefix}index.html">Home</a>
      <a href="{root_prefix}about.html">About</a>
      <button class="mobile-services-toggle" id="mobile-services-toggle" aria-expanded="false" aria-controls="mobile-services-sub">
        Service Menu
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
      </button>
      <div class="mobile-services-sub" id="mobile-services-sub">
        {mobile_service_links(root_prefix)}
      </div>
      <button class="mobile-services-toggle" id="mobile-areas-toggle" aria-expanded="false" aria-controls="mobile-areas-sub">
        Service Areas
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
      </button>
      <div class="mobile-services-sub" id="mobile-areas-sub">
        <a href="{root_prefix}service-areas.html" class="fw-mm-link--overview">All Service Areas</a>
        {mobile_area_links(root_prefix)}
      </div>
      <a href="{root_prefix}gallery.html">Gallery</a>
      <a href="{root_prefix}contact.html">Contact</a>
    </div>
    <div class="mobile-cta-row">
      <a href="{root_prefix}contact.html" class="btn btn-primary btn-full">Request Free Estimate</a>
      {call_cta_link("fw-header-call--menu")}
    </div>
    {social_block("mobile")}
    <div class="mobile-menu-footer">
      <p>{SITE['legal_name']}</p>
    </div>
  </nav>"""


def page_shell(
    title: str,
    description: str,
    canonical: str,
    body: str,
    extra_head: str = "",
    current: str = "",
    preload_hero: bool = False,
    root_prefix: str = "",
) -> str:
    canonical_url = f"{SITE['url']}/" if canonical == "index.html" else f"{SITE['url']}/{canonical}"
    hero_preloads = ""
    if preload_hero:
        hero_preloads = f"""  <link rel="preload" as="image" href="{root_prefix}Images/gallery/{HERO_MOBILE}" fetchpriority="high" media="(max-width: 768px)">
  <link rel="preload" as="image" href="{root_prefix}Images/gallery/{HERO_DESKTOP}" fetchpriority="high" media="(min-width: 769px)">"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical_url}">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="author" content="{SITE['legal_name']}">
  <meta name="geo.region" content="US-FL">
  <meta name="geo.placename" content="{SITE['city']}, Florida">
  <meta name="geo.position" content="{SITE['geo_lat']};{SITE['geo_lng']}">
  <meta name="ICBM" content="{SITE['geo_lat']}, {SITE['geo_lng']}">
  <meta name="theme-color" content="#0a0a0a">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{SITE['url']}/Images/gallery/{HERO_DESKTOP}">
  <meta property="og:site_name" content="{SITE['brand']}">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{SITE['url']}/Images/gallery/{HERO_DESKTOP}">
{extra_head}
{favicon_head(root_prefix)}
{fonts_head()}
{hero_preloads}
  <link rel="stylesheet" href="{root_prefix}styles.css">
{analytics_head()}
</head>
<body>
{header(current, root_prefix)}
<main>
{body}
</main>
{footer(root_prefix)}
  <script src="{root_prefix}script.js"></script>
</body>
</html>"""


def business_schema() -> str:
    services = [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"]}} for s in SERVICES]
    areas = [f"{c}, FL" for c in CITY_NAMES]
    schema = {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "@id": f"{SITE['url']}/#business",
        "name": SITE["brand"],
        "legalName": SITE["legal_name"],
        "description": f"{SITE['brand']} — {SITE_POSITIONING} in {SITE['area']}.",
        "url": SITE["url"],
        "telephone": f"+1-{SITE['phone_tel'][:3]}-{SITE['phone_tel'][3:6]}-{SITE['phone_tel'][6:]}",
        "email": SITE["email"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": SITE["city"],
            "addressRegion": SITE["region"],
            "addressCountry": "US",
        },
        "image": f"{SITE['url']}/Images/gallery/{HERO_DESKTOP}",
        "logo": f"{SITE['url']}/{LOGO}",
        "priceRange": "$$",
        "openingHours": "Mo-Sa 07:00-18:00",
        "areaServed": areas,
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Outdoor Services",
            "itemListElement": services,
        },
    }
    links = same_as_links()
    if links:
        schema["sameAs"] = links
    return json.dumps(schema, indent=2)


def write_index() -> None:
    phase1_cards = ""
    for i, s in enumerate(PHASE1_SERVICES):
        phase1_cards += service_mosaic_card(s, i * 70, featured=True)

    directory = ""
    for cat in SERVICE_CATEGORIES:
        directory += service_directory_group(cat)

    thumbs = ""
    for i, (img, alt, label) in enumerate(GALLERY[:4]):
        thumbs += f"""
          <a class="work-thumb" href="gallery.html" aria-label="View {label} gallery" data-fw-enter="bottom" style="--fw-enter-delay: {i * 70}ms;">
            <img src="Images/gallery/{img}" alt="{alt}" loading="lazy" width="600" height="450">
            <span class="work-thumb-label">{label}</span>
          </a>"""

    schema = f"""  <script type="application/ld+json">{business_schema()}</script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","@id":"{SITE['url']}/#website","url":"{SITE['url']}/","name":"{SITE['brand']}","publisher":{{"@id":"{SITE['url']}/#business"}}}}</script>
  <script type="application/ld+json">{faq_page_schema(HOME_FAQS)}</script>"""

    body = f"""
    <section class="hero">
      <div class="hero-bg" aria-hidden="true"></div>
      <div class="hero-overlay" aria-hidden="true"></div>
      <div class="container hero-inner">
        <div class="hero-copy">
          <p class="eyebrow" data-fw-enter="left" data-fw-enter-immediate="true">{SITE_POSITIONING}</p>
          <h1 data-fw-enter="left" data-fw-enter-immediate="true" style="--fw-enter-delay: 80ms;">{SITE['city']} <span class="h1-accent">{SITE_POSITIONING}</span></h1>
          <p class="hero-sub" data-fw-enter="left" data-fw-enter-immediate="true" style="--fw-enter-delay: 160ms;">
            {SITE['brand']} helps homeowners and property owners with land clearing, trail clearing, brush cutting, forestry mulching, pond bank clearing, pond cleanup, ditch clearing, debris removal, acreage cleanup, and tractor services across {SITE['area']} — outdoor property work, not utility trenching or engineered drainage.
          </p>
          <div class="hero-actions" data-fw-enter="left" data-fw-enter-immediate="true" style="--fw-enter-delay: 240ms;">
            <a class="btn btn-primary" href="contact.html">Request a Free Estimate</a>
            <a class="btn btn-ghost" href="services.html">All Services</a>
          </div>
          <div class="trust-row" data-fw-enter="left" data-fw-enter-immediate="true" style="--fw-enter-delay: 320ms;">
            <div class="trust-item"><strong>{PHASE1_COUNT}</strong><span>Core services</span></div>
            <div class="trust-divider" aria-hidden="true"></div>
            <div class="trust-item"><strong>{SERVICE_COUNT}</strong><span>Total services</span></div>
            <div class="trust-divider" aria-hidden="true"></div>
            <div class="trust-item"><strong>Local</strong><span>{SITE['city']}, FL</span></div>
          </div>
          {social_block("hero", 'data-fw-enter="left" data-fw-enter-immediate="true" style="--fw-enter-delay: 400ms;"')}
        </div>
        <aside class="hero-card" aria-label="Get a free estimate" data-fw-enter="right" data-fw-enter-immediate="true" style="--fw-enter-delay: 120ms;">
          <p class="card-eyebrow">Free photo-based estimate</p>
          <h2 class="card-name">Talk to Tyler Today</h2>
          <p class="card-note">Tell us what you need and Tyler will follow up. Text photos to <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a> for a faster quote.</p>
          {estimate_form(page="index.html", compact=True)}
        </aside>
      </div>
    </section>

    {intent_router_section()}

    <section id="services" class="services-section section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Primary outdoor services</p>
          <h2>Core Outdoor Services in Polk County</h2>
          <p>Land clearing, trail clearing, pond bank clearing, ditch clearing, brush cutting, debris removal, pool dig-out support, and tractor services — the most common jobs homeowners and property owners call for.</p>
        </div>
      </div>
      <div class="services-mosaic-wrap">
        <div class="services-mosaic services-mosaic--phase1">{phase1_cards}
        </div>
      </div>
      <div class="container" style="margin-top:2.5rem;text-align:center">
        <a class="btn btn-ghost" href="services.html">View all {SERVICE_COUNT} services by category &rarr;</a>
      </div>
    </section>

    {scope_section()}

    <section class="service-directory-section section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Full service list</p>
          <h2>Every Outdoor Property Service We Offer</h2>
          <p>From core clearing and cleanup to pond management, ditch maintenance, and equipment services.</p>
        </div>
        <div class="service-directory">{directory}
        </div>
      </div>
    </section>

    <section class="work-teaser section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Proof of work</p>
          <h2>Real Jobs, Real Equipment</h2>
          <p>Every photo is from actual outdoor work — land clearing, brush cutting, pond bank work, and property cleanup across Central Florida.</p>
        </div>
        <div class="work-teaser-grid">{thumbs}
        </div>
        <div style="text-align:center;margin-top:2rem">
          <a class="btn btn-ghost" href="gallery.html">See Full Gallery &rarr;</a>
        </div>
      </div>
    </section>

    <section id="about" class="about-section section-shell">
      <div class="container about-grid">
        <div class="about-copy" data-fw-enter="left">
          <p class="eyebrow">Why choose us</p>
          <h2>Owner-operated.<br>Equipment-ready.<br>Clear communication.</h2>
          <p>{SITE['owner']} runs {SITE['brand']} as a local Auburndale business built on hard work, honest estimates, and faith-based service. When you reach out, you're talking directly to the person doing the work.</p>
          <p>From land clearing and pond bank work to ditch cleanup and debris haul-off, we focus on outdoor property services that help homeowners and property owners reclaim usable land — not utility trenching or engineered drainage systems.</p>
        </div>
        <div class="about-card" data-fw-enter="right">
          <h3>What to expect</h3>
          <ul class="about-list">
            <li>Direct contact with Tyler — no call center</li>
            <li>Photo-based estimates for outdoor projects</li>
            <li>Equipment-ready for clearing and cleanup jobs</li>
            <li>Local {SITE['city']} business serving Polk County</li>
            <li>Residential and property-owner friendly service</li>
            <li>Colossians 3:23 work ethic on every job</li>
          </ul>
          <a class="btn btn-primary" href="contact.html">Request an Estimate</a>
        </div>
      </div>
    </section>

    <section class="process-section section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">How it works</p>
          <h2>Simple Project Process</h2>
        </div>
        <div class="process-grid">
          <div class="process-step" data-fw-enter="bottom" style="--fw-enter-delay: 0ms;"><span>1</span><h3>Send photos or call</h3><p>Share your property location and upload photos of the area that needs work.</p></div>
          <div class="process-step" data-fw-enter="bottom" style="--fw-enter-delay: 70ms;"><span>2</span><h3>Confirm scope</h3><p>We review access, vegetation, dirt volume, and the type of service needed.</p></div>
          <div class="process-step" data-fw-enter="bottom" style="--fw-enter-delay: 140ms;"><span>3</span><h3>Receive estimate</h3><p>Get a clear estimate before work begins — no vague pricing.</p></div>
          <div class="process-step" data-fw-enter="bottom" style="--fw-enter-delay: 210ms;"><span>4</span><h3>Schedule service</h3><p>We show up with the right equipment and get your property cleared or cleaned up.</p></div>
        </div>
      </div>
    </section>

    <section id="faq" class="faq-section section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Common questions</p>
          <h2>Frequently Asked Questions</h2>
        </div>
        <div class="faq-list">
          <div class="faq-item"><button class="faq-question" aria-expanded="false" aria-controls="faq-a1">Do you offer free estimates?<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></button><div class="faq-answer" id="faq-a1" aria-hidden="true" inert><div class="faq-answer-inner"><p>Yes. Send photos through our contact form or email {SITE['email']}. Photo-based estimates help us understand access, vegetation, and project scope before we schedule a visit.</p></div></div></div>
          <div class="faq-item"><button class="faq-question" aria-expanded="false" aria-controls="faq-a2">What areas do you serve?<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></button><div class="faq-answer" id="faq-a2" aria-hidden="true" inert><div class="faq-answer-inner"><p>We are based in {SITE['city']} and serve {SITE['area']}, including Winter Haven, Lakeland, Bartow, Haines City, Lake Wales, and nearby communities.</p></div></div></div>
          <div class="faq-item"><button class="faq-question" aria-expanded="false" aria-controls="faq-a3">Do I need to call 811 before digging?<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></button><div class="faq-answer" id="faq-a3" aria-hidden="true" inert><div class="faq-answer-inner"><p>For any digging or soil-moving work, Florida law requires contacting Sunshine 811 at least two full business days before work begins so underground utilities can be marked.</p></div></div></div>
          <div class="faq-item"><button class="faq-question" aria-expanded="false" aria-controls="faq-a4">Do you install pools or do utility trenching?<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></button><div class="faq-answer" id="faq-a4" aria-hidden="true" inert><div class="faq-answer-inner"><p>No. We do not install pools, hold pool contractor licensing, or perform utility trenching, stormwater system installation, sewer work, water mains, site development, or engineered drainage. We provide {SITE_POSITIONING.lower()} — including pool dig-out support under licensed pool contractors when needed.</p></div></div></div>
          <div class="faq-item"><button class="faq-question" aria-expanded="false" aria-controls="faq-a5">What jobs do people usually call you for?<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></button><div class="faq-answer" id="faq-a5" aria-hidden="true" inert><div class="faq-answer-inner"><p>Most inquiries are pond banks, trails, brush, overgrowth, and acreage cleanup — exactly the outdoor property work we built this site around. Pool dig-out support is available under licensed pool builders. Utility trenching and engineered drainage are not services we offer.</p></div></div></div>
          <div class="faq-item"><button class="faq-question" aria-expanded="false" aria-controls="faq-a6">Can you help with pool dig-out dirt removal?<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></button><div class="faq-answer" id="faq-a6" aria-hidden="true" inert><div class="faq-answer-inner"><p>Yes — as pool dig-out support under a licensed pool contractor. We handle dirt removal and site cleanup; we do not contract directly as a pool installer.</p></div></div></div>
        </div>
      </div>
    </section>

    <section id="contact" class="contact-section section-shell">
      <div class="container contact-inner" data-fw-enter="top">
        <p class="eyebrow">Ready to get started?</p>
        <h2>Need land cleared, a ditch cleaned, or property debris removed?</h2>
        <p>Request an estimate from {SITE['brand']} today. Send photos for the fastest quote.</p>
        <a class="btn btn-primary btn-lg" href="contact.html">Request a Free Estimate</a>
      </div>
    </section>"""

    html = page_shell(
        f"{SITE['city']} Land Clearing & Outdoor Services | Faith Works",
        f"{SITE_POSITIONING} in {SITE['city']} and Polk County, FL — land clearing, brush cutting, forestry mulching, pond cleanup, debris removal, and tractor services. Free photo-based estimates.",
        "index.html",
        body,
        schema,
        "index.html",
        preload_hero=True,
    )
    html = page_shell(
        f"{SITE['city']} Land Clearing & Outdoor Services | Faith Works",
        f"{SITE['brand']} provides land clearing, pond bank clearing, ditch clearing, brush cutting, debris removal, and tractor work in Polk County, FL.",
        "index.html",
        body,
        schema,
        "index.html",
        preload_hero=True,
    )
    write_site_file(ROOT / "index.html", html)


def write_service_page(s: dict) -> None:
    bullets = "\n".join(f"            <li>{b}</li>" for b in s["bullets"])
    benefits = "\n".join(f"            <li>{b}</li>" for b in s["benefits"])
    ideal_for = "\n".join(f"            <li>{item}</li>" for item in s["ideal_for"])
    related = related_services_block(s["related_slugs"])
    faqs = service_faqs(s)
    service_faq_block = faq_accordion(faqs, s["slug"])
    phase_badge = '<p class="phase-badge">Core Service</p>' if s.get("phase1") else ""
    schema = f"""  <script type="application/ld+json">{business_schema()}</script>
  <script type="application/ld+json">{service_schema(s)}</script>
  <script type="application/ld+json">{breadcrumb_schema([('Home', 'index.html'), ('Services', 'services.html'), (s['name'], s['slug'] + '.html')])}</script>
  <script type="application/ld+json">{faq_page_schema(faqs)}</script>"""

    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; <a href="services.html">Services</a> &rsaquo; {s['name']}</p>
        {phase_badge}
        <h1>{s['h1']}</h1>
        <p>{s['desc']}</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container sp-layout">
        <div class="sp-content" data-fw-enter="left">
          <h2>{s['name']} in {SITE['area']}</h2>
          <p>{s['intro']}</p>
          <h2>What We Handle</h2>
          <ul>{bullets}</ul>
          <h2>Ideal For</h2>
          <ul>{ideal_for}</ul>
          <h2>Benefits</h2>
          <ul>{benefits}</ul>
          {service_scope_details(s)}
          {related}
          <h2>Owner-Operated Service</h2>
          <p>When Tyler handles your project, you get direct communication from estimate through completion — not a subcontractor chain. Serving residential and property-owner clients throughout {SITE['city']}, Polk County, and nearby Central Florida areas.</p>
          <p class="utility-note"><strong>Scope note:</strong> Faith Works provides outdoor property services — land clearing, mulching, brush cutting, and cleanup. We do not install utility lines, stormwater systems, sewer systems, water mains, or engineered drainage. For any digging work, Sunshine 811 should be contacted at least two full business days before work begins.</p>
          <h2>{s['name']} FAQs</h2>
          {service_faq_block}
        </div>
        <aside class="sp-sidebar" data-fw-enter="right">
          <div class="hero-card" aria-label="Get a free estimate">
            <p class="card-eyebrow">Free photo-based estimate</p>
            <h2 class="card-name">Request {s['name']}</h2>
            <p class="card-note">Upload photos and describe your property for a faster quote.</p>
            {estimate_form(selected=s['form_label'], subject=f"{s['name']} estimate - {SITE['brand']}", page=f"{s['slug']}.html", compact=True)}
          </div>
        </aside>
      </div>
    </section>
    <section class="areas-strip">
      <div class="container">
        <p class="eyebrow">Where we work</p>
        <p>Serving <strong>{'</strong>, <strong>'.join(c["name"] for c in FEATURED_CITIES[:8])}</strong>, and communities within {SERVICE_RADIUS_MILES} miles of {HOME_CITY}. <a href="service-areas.html">See all service areas &rarr;</a></p>
      </div>
    </section>"""

    html = page_shell(s["title"], s["desc"], f"{s['slug']}.html", body, schema, f"{s['slug']}.html")
    write_site_file(ROOT / f"{s['slug']}.html", html)


def write_services() -> None:
    phase1_cards = ""
    for i, s in enumerate(PHASE1_SERVICES):
        phase1_cards += service_mosaic_card(s, i * 60, featured=True)

    directory = ""
    for cat in SERVICE_CATEGORIES:
        directory += service_directory_group(cat)
    service_list_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{SITE['brand']} services",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "name": item["name"],
                "url": f"{SITE['url']}/{item['slug']}.html",
            }
            for i, item in enumerate(SERVICES, start=1)
        ],
    }, indent=2)
    schema = f"""  <script type="application/ld+json">{business_schema()}</script>
  <script type="application/ld+json">{breadcrumb_schema([('Home', 'index.html'), ('Services', 'services.html')])}</script>
  <script type="application/ld+json">{service_list_schema}</script>"""

    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; Services</p>
        <h1>{SITE_POSITIONING}</h1>
        <p>Faith Works Outdoor Services in {SITE['city']} and {SITE['area']} — outdoor property clearing, mulching, cleanup, and maintenance. Not an excavation contractor.</p>
      </div>
    </section>

    {intent_router_section("services")}

    <section class="section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Primary outdoor services</p>
          <h2>Core Outdoor Services</h2>
          <p>Land clearing, trail clearing, pond bank clearing, ditch clearing, brush cutting, debris removal, pool dig-out support, and tractor services.</p>
        </div>
        <div class="services-mosaic services-mosaic--phase1">{phase1_cards}
        </div>
      </div>
    </section>

    {scope_section()}

    <section class="service-directory-section section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">All services by category</p>
          <h2>{SERVICE_COUNT} Outdoor Property Services</h2>
          <p>Every service page includes scope details, ideal projects, and a photo-based estimate form.</p>
        </div>
        <div class="service-directory">{directory}
        </div>
      </div>
    </section>

    <section class="section-shell">
      <div class="container contact-inner" data-fw-enter="top">
        <p class="eyebrow">Not sure which service fits?</p>
        <h2>Send photos — Tyler will confirm scope</h2>
        <p>Most calls start with pond banks, trails, brush, overgrowth, or acreage cleanup. Tell us what you need and we will match the right service.</p>
        <a class="btn btn-primary btn-lg" href="contact.html">Request a Free Estimate</a>
      </div>
    </section>"""

    html = page_shell(
        f"Outdoor Property Services in Polk County FL | Faith Works",
        f"Full service list for {SITE['brand']} — {SITE_POSITIONING} in Polk County, FL.",
        "services.html",
        body,
        schema,
        "services.html",
    )
    write_site_file(ROOT / "services.html", html)


def write_gallery() -> None:
    items = ""
    for i, (img, alt, label) in enumerate(GALLERY):
        items += f"""
          <figure class="gallery-item" data-fw-enter="bottom" style="--fw-enter-delay: {(i % 6) * 60}ms;">
            <img src="Images/gallery/{img}" alt="{alt}" loading="lazy" width="800" height="600">
            <figcaption>{label}</figcaption>
          </figure>"""
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; Gallery</p>
        <h1>Project Gallery</h1>
        <p>Real outdoor work from {SITE['brand']} — land clearing, brush cutting, pond bank work, and property cleanup across Central Florida.</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container">
        <div class="gallery-grid">{items}
        </div>
      </div>
    </section>"""
    html = page_shell(
        f"Outdoor Services Project Gallery | {SITE['brand']}",
        f"View land clearing, brush cutting, and outdoor property cleanup projects by {SITE['brand']} in Polk County, FL.",
        "gallery.html",
        body,
        "",
        "gallery.html",
    )
    write_site_file(ROOT / "gallery.html", html)


def write_about() -> None:
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; About</p>
        <h1>About {SITE['brand']}</h1>
        <p>Local Auburndale outdoor services built on faith, hard work, and equipment-ready property cleanup.</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container about-grid">
        <div class="about-copy" data-fw-enter="left">
          <h2>Meet {SITE['owner']}</h2>
          <p>{SITE['owner']} founded {SITE['legal_name']} in {SITE['city']}, Florida to serve homeowners and property owners who need reliable outdoor property work — {SITE_POSITIONING.lower()}.</p>
          <p>{SITE['brand']} focuses on the work people actually call for: pond banks, trails, brush, overgrowth, acreage cleanup, ditch clearing, and debris haul-off. We are not a utility excavation contractor — we do not install underground utilities, stormwater systems, sewer systems, water mains, or engineered drainage.</p>
          <p>Our work is guided by Colossians 3:23 — whatever we do, we work at it with all our heart. That means showing up prepared, communicating clearly, and leaving properties cleaner than we found them.</p>
        </div>
        <div class="about-card" data-fw-enter="right">
          {logo_coin("fw-logo-coin--about", 220, SITE['brand'])}
          <h3>Business Details</h3>
          <ul class="about-list">
            <li>Legal name: {SITE['legal_name']}</li>
            <li>Based in {SITE['city']}, {SITE['region']}</li>
            <li>Service-area business — we come to you</li>
            <li>Email: {SITE['email']}</li>
            <li>Active Florida LLC</li>
          </ul>
        </div>
      </div>
    </section>"""
    html = page_shell(
        f"About {SITE['owner']} | {SITE['brand']}",
        f"Meet {SITE['owner']}, owner of {SITE['brand']} — {SITE_POSITIONING} in Polk County, FL.",
        "about.html",
        body,
        "",
        "about.html",
    )
    write_site_file(ROOT / "about.html", html)


def write_contact() -> None:
    schema = f"""  <script type="application/ld+json">{business_schema()}</script>
  <script type="application/ld+json">{breadcrumb_schema([('Home', 'index.html'), ('Contact', 'contact.html')])}</script>"""
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; Contact</p>
        <h1>Request an Outdoor Property Services Estimate</h1>
        <p>Send photos of your property and tell us what you need cleared, mulched, or cleaned up. We'll review the details and follow up with you.</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container">
        <div class="contact-page-form hero-card" data-fw-enter="right">
          <p class="card-eyebrow">Free photo-based estimate</p>
          <h2 class="card-name">Project Estimate Form</h2>
          {estimate_form('contact-form', subject=f'Contact form - {SITE["brand"]}', page='contact.html')}
        </div>
        <div class="contact-direct">
          <div class="contact-direct-card"><p class="eyebrow">Phone</p><p><a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></p></div>
          <div class="contact-direct-card"><p class="eyebrow">Email</p><p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p></div>
          <div class="contact-direct-card"><p class="eyebrow">Service Area</p><p>{SITE['city']}, FL<br>Serving {SITE['area']}</p></div>
        </div>
      </div>
    </section>
    <section class="section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Faster estimates</p>
          <h2>What To Send With Your Request</h2>
          <p>The best estimate requests include enough detail to understand access, debris volume, and the condition you want the property left in.</p>
        </div>
        <div class="service-detail-grid">
          <article data-fw-enter="bottom">
            <h3>Photos or video</h3>
            <ul>
              <li>Wide photos of the full work area</li>
              <li>Close photos of heavy brush, banks, or debris piles</li>
              <li>Any wet areas, slopes, fences, gates, or obstacles</li>
            </ul>
          </article>
          <article data-fw-enter="bottom" style="--fw-enter-delay: 70ms;">
            <h3>Access details</h3>
            <ul>
              <li>City or job address</li>
              <li>Gate width and driveway access</li>
              <li>Where equipment can park or unload</li>
            </ul>
          </article>
          <article data-fw-enter="bottom" style="--fw-enter-delay: 140ms;">
            <h3>Desired outcome</h3>
            <ul>
              <li>Clear, mulch, pile, or haul off debris</li>
              <li>Any deadline or scheduling needs</li>
              <li>Whether this connects to another outdoor project</li>
            </ul>
          </article>
        </div>
      </div>
    </section>"""
    html = page_shell(
        f"Contact {SITE['brand']} | Free Outdoor Services Estimate",
        f"Request a free photo-based estimate for {SITE_POSITIONING.lower()} in Polk County, FL.",
        "contact.html",
        body,
        schema,
        "contact.html",
    )
    write_site_file(ROOT / "contact.html", html)


def area_service_links(root_prefix: str = "") -> str:
    core = [SERVICE_BY_SLUG[item["slug"]] for item in INTENT_ROUTES[:5]]
    return "".join(f'<a href="{root_prefix}{s["slug"]}.html">{s["nav"]}</a>' for s in core)


def write_city_area_page(city: dict, areas_dir: Path) -> None:
    root_prefix = "../"
    canonical = f"areas/{city['slug']}.html"
    county = COUNTY_BY_NAME[city["county"]]
    county_href = f"{county['slug']}.html"
    nearby = [c for c in cities_in_county(city["county"]) if c["slug"] != city["slug"]][:6]
    nearby_html = "".join(
        f'<a href="{c["slug"]}.html">{c["name"]}, FL</a>' for c in nearby
    )
    core_links = area_service_links(root_prefix)
    title = f"{SITE_POSITIONING} in {city['name']}, FL"
    desc = (
        f"{SITE['brand']} serves {city['name']}, {city['county']} with land clearing, pond bank clearing, "
        f"ditch clearing, brush cutting, debris removal, and outdoor property services. Based in {HOME_CITY} — "
        f"within {SERVICE_RADIUS_MILES} miles of {HOME_ZIP}."
    )
    schema = f"""  <script type="application/ld+json">{business_schema()}</script>
  <script type="application/ld+json">{breadcrumb_schema([('Home', 'index.html'), ('Service Areas', 'service-areas.html'), (f"{city['name']}, FL", canonical)])}</script>"""
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="{root_prefix}index.html">Home</a> &rsaquo; <a href="{root_prefix}service-areas.html">Service Areas</a> &rsaquo; <a href="{county_href}">{city['county']}</a> &rsaquo; {city['name']}</p>
        <h1>{SITE_POSITIONING} in {city['name']}, FL</h1>
        <p>{desc}</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container sp-layout">
        <div class="sp-content" data-fw-enter="left">
          <h2>Outdoor Property Services in {city['name']}</h2>
          <p>{SITE['brand']} is based in {HOME_CITY}, Florida ({HOME_ZIP}) and serves {city['name']} property owners across {city['county']}. Typical jobs include overgrown lots, pond banks, ditches, brush, trails, storm debris, acreage cleanup, and outdoor property maintenance.</p>
          <p>We focus on outdoor property work — not utility trenching, engineered drainage, or pool installation. Pool dig-out support is available under licensed pool contractors when needed.</p>
          <h2>Popular Services Near {city['name']}</h2>
          <div class="area-card-links">{core_links}</div>
          <h2>Also Serving Nearby in {city['county']}</h2>
          <div class="area-card-links">{nearby_html}</div>
          <p class="utility-note"><strong>Coverage note:</strong> {city['name']} is within our approximately {SERVICE_RADIUS_MILES}-mile service radius from {HOME_CITY}. Send photos through the form and Tyler will confirm scope and scheduling.</p>
        </div>
        <aside class="sp-sidebar" data-fw-enter="right">
          <div class="hero-card" aria-label="Get a free estimate">
            <p class="card-eyebrow">Free photo-based estimate</p>
            <h2 class="card-name">Request Service in {city['name']}</h2>
            <p class="card-note">Upload photos of your property in {city['name']}, FL for a faster quote.</p>
            {estimate_form(selected=None, subject=f"{city['name']} estimate - {SITE['brand']}", page=canonical, compact=True)}
          </div>
        </aside>
      </div>
    </section>"""
    html = page_shell(
        f"{city['name']}, FL Outdoor Property Services | {SITE['brand']}",
        desc,
        canonical,
        body,
        schema,
        canonical,
        root_prefix=root_prefix,
    )
    write_site_file(areas_dir / f"{city['slug']}.html", html)


def write_county_area_page(county: dict, areas_dir: Path) -> None:
    root_prefix = "../"
    canonical = f"areas/{county['slug']}.html"
    cities = cities_in_county(county["name"])
    city_cards = ""
    for i, city in enumerate(cities):
        city_cards += f"""
          <article class="area-card" data-fw-enter="bottom" style="--fw-enter-delay: {(i % 6) * 60}ms;">
            <h3><a href="{city['slug']}.html">{city['name']}, FL</a></h3>
            <p>{SITE_POSITIONING} for {city['name']} property owners in {county['name']}.</p>
            <a class="area-card-cta" href="{city['slug']}.html">View {city['name']} services &rarr;</a>
          </article>"""
    core_links = area_service_links(root_prefix)
    desc = f"{SITE['brand']} serves {county['name']} with land clearing, pond bank clearing, ditch clearing, brush cutting, and outdoor property cleanup. Based in {HOME_CITY} within {SERVICE_RADIUS_MILES} miles."
    schema = f"""  <script type="application/ld+json">{business_schema()}</script>
  <script type="application/ld+json">{breadcrumb_schema([('Home', 'index.html'), ('Service Areas', 'service-areas.html'), (county['name'], canonical)])}</script>"""
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="{root_prefix}index.html">Home</a> &rsaquo; <a href="{root_prefix}service-areas.html">Service Areas</a> &rsaquo; {county['name']}</p>
        <h1>Outdoor Property Services in {county['name']}</h1>
        <p>{county['description']}</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Cities we serve</p>
          <h2>{county['name']} Service Areas</h2>
          <p>Faith Works travels from {HOME_CITY} to serve property owners across {county['name']} within approximately {SERVICE_RADIUS_MILES} miles.</p>
        </div>
        <div class="areas-grid">{city_cards}
        </div>
        <div class="section-heading" style="margin-top:2.5rem" data-fw-enter="left">
          <p class="eyebrow">Core services</p>
          <h2>Popular Services in {county['name']}</h2>
        </div>
        <div class="area-card-links">{core_links}</div>
        <p class="areas-note" style="margin-top:2rem"><a href="{root_prefix}service-areas.html">&larr; All service areas</a> &nbsp;&middot;&nbsp; <a href="{root_prefix}contact.html">Request an estimate</a></p>
      </div>
    </section>"""
    html = page_shell(
        f"{county['name']} Outdoor Property Services | {SITE['brand']}",
        desc,
        canonical,
        body,
        schema,
        canonical,
        root_prefix=root_prefix,
    )
    write_site_file(areas_dir / f"{county['slug']}.html", html)


def write_area_pages() -> None:
    areas_dir = ROOT / "areas"
    areas_dir.mkdir(exist_ok=True)
    for county in COUNTIES:
        write_county_area_page(county, areas_dir)
    for city in AREA_CITIES:
        write_city_area_page(city, areas_dir)


def write_service_areas() -> None:
    county_cards = ""
    for i, county in enumerate(COUNTIES):
        city_count = len(cities_in_county(county["name"]))
        county_cards += f"""
          <article class="area-card area-card--county" data-fw-enter="bottom" style="--fw-enter-delay: {(i % 6) * 60}ms;">
            <h3><a href="areas/{county['slug']}.html">{county['name']}</a></h3>
            <p>{county['description']}</p>
            <p class="area-card-meta">{city_count} cities listed</p>
            <a class="area-card-cta" href="areas/{county['slug']}.html">View {county['name']} &rarr;</a>
          </article>"""

    city_cards = ""
    core_links = area_service_links()
    for i, city in enumerate(AREA_CITIES):
        city_cards += f"""
          <article class="area-card" data-fw-enter="bottom" style="--fw-enter-delay: {(i % 6) * 60}ms;">
            <h3><a href="{city_href(city['slug'])}">{city['name']}, FL</a></h3>
            <p class="area-card-county">{city['county']}</p>
            <p>{SITE_POSITIONING} for {city['name']} property owners, including overgrown lots, pond banks, ditches, brush, trails, storm debris, and acreage cleanup.</p>
            <div class="area-card-links" aria-label="Core services near {city['name']}">{core_links}</div>
            <a class="area-card-cta" href="{city_href(city['slug'])}">View {city['name']} services &rarr;</a>
          </article>"""

    schema = f"""  <script type="application/ld+json">{business_schema()}</script>
  <script type="application/ld+json">{breadcrumb_schema([('Home', 'index.html'), ('Service Areas', 'service-areas.html')])}</script>"""
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; Service Areas</p>
        <h1>Service Areas Within {SERVICE_RADIUS_MILES} Miles of {HOME_CITY}</h1>
        <p>Based in {HOME_CITY}, FL ({HOME_ZIP}), {SITE['brand']} serves property owners across Polk County and nearby Central Florida counties.</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Counties we serve</p>
          <h2>Central Florida Counties</h2>
          <p>Outdoor property services across {len(COUNTIES)} counties within approximately {SERVICE_RADIUS_MILES} miles of {HOME_CITY}.</p>
        </div>
        <div class="areas-grid areas-grid--counties">{county_cards}
        </div>
      </div>
    </section>
    <section class="section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">City coverage</p>
          <h2>Cities &amp; Communities We Serve</h2>
          <p>Select your city for local service details, common job types, and a photo-based estimate form.</p>
        </div>
        <div class="areas-grid">{city_cards}
        </div>
        <p class="areas-note" data-fw-enter="top">Not sure if we serve your area? Send your city and project photos through our <a href="contact.html">contact form</a> and we'll confirm coverage.</p>
      </div>
    </section>"""
    html = page_shell(
        f"Service Areas Within {SERVICE_RADIUS_MILES} Miles of {HOME_CITY} | {SITE['brand']}",
        f"{SITE['brand']} serves Polk, Osceola, Orange, Lake, Hillsborough, Pasco, and nearby Central Florida counties within {SERVICE_RADIUS_MILES} miles of Auburndale, FL.",
        "service-areas.html",
        body,
        schema,
        "service-areas.html",
    )
    write_site_file(ROOT / "service-areas.html", html)


def write_privacy() -> None:
    body = f"""
    <section class="sp-hero"><div class="container"><h1>Privacy Policy</h1></div></section>
    <section class="section-shell"><div class="container sp-content">
      <p>{SITE['legal_name']} ("we") respects your privacy. Information submitted through our contact forms is processed by <strong>Formspree</strong> (formspree.io) and delivered to us by email. We use that information only to respond to your estimate request and provide our services.</p>
      <p>We do not sell personal information. Analytics tools may collect anonymous usage data to improve the website.</p>
      <p>Questions? Contact <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
    </div></section>"""
    write_site_file(
        ROOT / "privacy-policy.html",
        page_shell("Privacy Policy", f"Privacy policy for {SITE['brand']}.", "privacy-policy.html", body),
    )


def write_sitemap() -> None:
    pages = ["index.html", "services.html", "about.html", "contact.html", "gallery.html", "service-areas.html", "privacy-policy.html"]
    pages += [f"{s['slug']}.html" for s in SERVICES]
    pages += [f"areas/{c['slug']}.html" for c in AREA_CITIES]
    pages += [f"areas/{c['slug']}.html" for c in COUNTIES]
    today = date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        loc = f"{SITE['url']}/" if p == "index.html" else f"{SITE['url']}/{p}"
        priority = "1.0" if p == "index.html" else ("0.9" if p in {"services.html", "contact.html"} else "0.8")
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{priority}</priority></url>")
    lines.append("</urlset>")
    write_site_file(ROOT / "sitemap.xml", "\n".join(lines))


def write_robots() -> None:
    write_site_file(ROOT / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")


def write_cname() -> None:
    write_site_file(ROOT / "CNAME", "faithworksods.com\n")


def write_styles() -> None:
    src = Path(r"E:\ScreenTeamLLC\styles.css").read_text(encoding="utf-8")
    src = src.replace("THE SCREEN TEAM LLC", "FAITH WORKS OUTDOOR SERVICES")
    src = src.replace("Dark navy professional theme", "Black & gold outdoor services theme")
    src = src.replace('"Oswald", sans-serif', '"Cinzel", serif')
    src = src.replace("rgba(7, 13, 24, 0.9)", "rgba(10, 10, 10, 0.94)")
    src = src.replace("#070d18", "#0a0a0a")
    src = src.replace("#0d1c2e", "#141414")
    src = src.replace("#152b40", "#1f2a1f")
    src = src.replace("#deeaf5", "#f5f0e8")
    src = src.replace("#7499b8", "#a89878")
    src = src.replace("#3da8d8", "#c9a227")
    src = src.replace("#1b5f82", "#8a6d12")
    src = src.replace("rgba(61, 168, 216,", "rgba(201, 162, 39,")
    src = src.replace("#7499b8", "#a89878")
    src = src.replace("#aac8df", "#d4c4a0")
    src = src.replace("--container:     1200px;", "--container:     1400px;")
    src = src.replace('url("Images/ScreenTeamBanner.webp")', f'url("Images/gallery/{HERO_DESKTOP}")')
    src = src.replace('url("Images/ScreenTeamBanner-mobile.webp")', f'url("Images/gallery/{HERO_MOBILE}")')
    src = src.replace('url("Images/service-hero-bg.jpg")', f'url("Images/gallery/{HERO_DESKTOP}")')
    src = src.replace("filter: brightness(0) invert(1);\n  mix-blend-mode: screen;", "filter: none;")
    src = src.replace(
        "font-size: clamp(3.8rem, 8.5vw, 7rem);",
        "font-size: clamp(2.2rem, 4.8vw, 4.25rem);",
    )
    src = src.replace(
        "  .hero-inner {\n    grid-template-columns: 1fr;\n    max-width: 680px;\n",
        "  .hero-inner {\n    grid-template-columns: 1fr;\n    max-width: min(960px, 100%);\n",
    )
    src = src.replace(
        "  .hero-copy h1 {\n    font-size: clamp(3.2rem, 10vw, 5rem);\n  }",
        "  .hero-copy h1 {\n    font-size: clamp(1.75rem, 7vw, 2.75rem);\n  }",
    )
    src = src.replace(".footer-logo {\n  height: 108px;\n  width: auto;\n  filter: brightness(0) invert(1);\n  opacity: 0.35;\n}", ".footer-logo {\n  height: 100px;\n  width: auto;\n  opacity: 0.85;\n}")
    extra = """

/* Faith Works extras */
.process-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}
.process-step {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 24px 20px;
}
.process-step span {
  display: inline-flex;
  width: 36px;
  height: 36px;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(201, 162, 39, 0.15);
  color: var(--accent);
  font-family: var(--font-head);
  font-weight: 700;
  margin-bottom: 12px;
}
.process-step h3 {
  font-family: var(--font-head);
  font-size: 1rem;
  color: #fff;
  margin-bottom: 8px;
  text-transform: uppercase;
}
.process-step p { font-size: 0.92rem; color: var(--muted); line-height: 1.6; }
.process-section { background: linear-gradient(180deg, #0a0a0a 0%, #121812 100%); border-top: 1px solid var(--border); }
.gallery-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.gallery-item { margin: 0; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-md); overflow: hidden; }
.gallery-item img { width: 100%; aspect-ratio: 4/3; object-fit: cover; }
.gallery-item figcaption { padding: 12px 14px; font-size: 0.85rem; color: var(--muted); }
.areas-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.area-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 22px 20px; }
.area-card h3 { font-family: var(--font-head); color: #fff; margin-bottom: 8px; font-size: 1.05rem; }
.area-card p { color: var(--muted); font-size: 0.92rem; line-height: 1.6; }
.areas-note { margin-top: 32px; text-align: center; color: var(--muted); }
.areas-note a { color: var(--accent); }
.intent-router {
  background: linear-gradient(180deg, #101510 0%, #0a0a0a 100%);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}
.intent-grid,
.service-detail-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}
.intent-card,
.service-detail-grid article {
  display: block;
  min-width: 0;
  text-decoration: none;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 22px 20px;
  color: inherit;
  transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}
.intent-card:hover,
.intent-card:focus-visible {
  transform: translateY(-2px);
  border-color: rgba(201, 162, 39, 0.48);
  background: rgba(201, 162, 39, 0.08);
}
.intent-card__label,
.service-area-links span {
  display: block;
  color: var(--accent);
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.intent-card h3,
.service-detail-grid h3 {
  color: #fff;
  font-family: var(--font-head);
  font-size: 1.02rem;
  line-height: 1.25;
  margin-bottom: 10px;
}
.intent-card p,
.service-detail-grid li {
  color: var(--muted);
  font-size: 0.92rem;
  line-height: 1.6;
}
.service-detail-grid ul {
  padding-left: 1.05rem;
}
.intent-card__cta {
  display: inline-flex;
  margin-top: 14px;
  color: var(--accent);
  font-weight: 800;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.service-area-links {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin: 24px 0;
  padding: 16px;
  background: rgba(201, 162, 39, 0.08);
  border: 1px solid rgba(201, 162, 39, 0.18);
  border-radius: var(--radius-sm);
}
.service-area-links span {
  flex-basis: 100%;
  margin-bottom: 0;
}
.service-area-links a,
.area-card-links a {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 7px 10px;
  border: 1px solid rgba(201, 162, 39, 0.24);
  border-radius: 999px;
  color: #f5f0e8;
  text-decoration: none;
  font-size: 0.78rem;
  line-height: 1.2;
  overflow-wrap: anywhere;
}
.service-area-links a:hover,
.area-card-links a:hover {
  border-color: rgba(201, 162, 39, 0.55);
  color: var(--accent);
}
.service-faq-list {
  margin-top: 12px;
}
.area-card-links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}
.about-logo { margin: 0 auto 20px; border-radius: 50%; max-width: 220px; }
.utility-note { margin-top: 24px; padding: 16px; border-left: 3px solid var(--accent); background: rgba(201,162,39,0.08); border-radius: 0 8px 8px 0; }
.footer-disclaimer { font-size: 0.72rem; color: var(--muted); margin-top: 8px; opacity: 0.8; }
.form-group input[type="file"] { padding: 8px; }

/* Services mega menu — category column + right flyout panels */
.site-header,
.nav-dropdown-wrap {
  overflow: visible;
}
.nav-dropdown-menu.fw-services-mega {
  left: 50%;
  min-width: 17rem;
  max-width: 19rem;
  max-height: none;
  overflow: visible;
  padding: 8px 0 10px;
  transform: translateX(-58%) translateY(-8px);
}
.nav-dropdown-wrap:hover .nav-dropdown-menu.fw-services-mega,
.nav-dropdown-btn[aria-expanded="true"] + .nav-dropdown-menu.fw-services-mega {
  transform: translateX(-58%) translateY(0);
}
.fw-services-mega__overview {
  display: block;
  margin: 2px 10px 8px;
  padding: 10px 12px 12px;
  border-bottom: 1px solid rgba(201, 162, 39, 0.22);
  font-size: 0.84rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--accent);
  text-decoration: none;
}
.fw-services-mega__overview::before {
  display: none;
}
.fw-services-mega__overview:hover {
  color: #fff;
  background: rgba(201, 162, 39, 0.1);
  border-radius: 8px;
  padding-left: 12px;
}
.fw-services-mega__list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.fw-services-mega__item {
  margin: 0;
  padding: 0;
}
.fw-services-mega__item--branch {
  position: relative;
}
.fw-services-mega__trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.65rem;
  width: 100%;
  padding: 10px 16px 10px 17px;
  border: 0;
  border-left: 3px solid transparent;
  background: transparent;
  color: var(--muted);
  font-family: var(--font-body);
  font-size: 0.84rem;
  font-weight: 650;
  line-height: 1.25;
  text-align: left;
  cursor: pointer;
  transition: color 0.2s ease, background 0.2s ease, border-color 0.2s ease;
}
.fw-services-mega__trigger::before {
  display: none;
}
.fw-services-mega__label {
  flex: 1 1 auto;
  min-width: 0;
}
.fw-services-mega__chevron {
  flex: 0 0 auto;
  width: 7px;
  height: 7px;
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
  transform: rotate(-45deg) translateY(-1px);
  opacity: 0.75;
}
.fw-services-mega__item--branch.subnav-open > .fw-services-mega__trigger,
.fw-services-mega__item--branch:hover > .fw-services-mega__trigger,
.fw-services-mega__item--branch:focus-within > .fw-services-mega__trigger {
  color: var(--ink);
  background: rgba(201, 162, 39, 0.1);
  border-left-color: var(--accent);
}
.fw-services-mega__flyout {
  position: absolute;
  top: -0.25rem;
  left: calc(100% - 4px);
  min-width: 15.75rem;
  max-width: 18rem;
  max-height: min(70vh, 28rem);
  overflow-x: hidden;
  overflow-y: auto;
  overscroll-behavior: contain;
  list-style: none;
  margin: 0;
  padding: 6px;
  background: rgba(7, 16, 30, 0.98);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(201, 162, 39, 0.28);
  border-radius: var(--radius-md);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transform: translateX(10px);
  transition: opacity 0.18s ease, transform 0.2s ease, visibility 0.18s ease;
  z-index: 220;
}
.fw-services-mega__item--branch.subnav-open > .fw-services-mega__flyout,
.fw-services-mega__item--branch:hover > .fw-services-mega__flyout,
.fw-services-mega__item--branch:focus-within > .fw-services-mega__flyout {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
  transform: translateX(0);
}
.fw-services-mega__flyout-item {
  margin: 0;
}
.fw-services-mega__flyout a {
  display: block;
  padding: 9px 12px;
  font-size: 0.84rem;
  font-weight: 600;
  line-height: 1.3;
  color: var(--muted);
  text-decoration: none;
  border-radius: 6px;
  border-left: 0;
  white-space: normal;
}
.fw-services-mega__flyout a::before {
  display: none;
}
.fw-services-mega__flyout a:hover {
  color: var(--ink);
  background: rgba(201, 162, 39, 0.12);
  padding-left: 12px;
}
.fw-areas-mega {
  min-width: 15.5rem;
  max-width: 17.5rem;
}
.fw-areas-mega .fw-services-mega__flyout {
  min-width: 16.75rem;
  max-width: 19rem;
}
.fw-services-mega__flyout-item--overview a {
  font-weight: 700;
  color: var(--accent);
  border-bottom: 1px solid rgba(201, 162, 39, 0.18);
  margin-bottom: 2px;
  padding-bottom: 10px;
}
.fw-services-mega__flyout-item--overview a:hover {
  color: #fff;
}
.fw-mm-sublink--overview {
  font-weight: 700;
  color: var(--accent) !important;
}

/* Mobile service menu accordion */
.mobile-services-sub {
  max-height: none;
  overflow: visible;
  padding: 0 0 8px;
}
.mobile-services-sub.is-open {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding-left: 0;
}
.fw-mm-nav,
.fw-mm-submenu {
  list-style: none;
  margin: 0;
  padding: 0;
}
.fw-mm-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.fw-mm-link--overview {
  display: block;
  margin: 0 0 8px;
  padding: 12px 14px;
  border-radius: 8px;
  font-weight: 700;
  color: var(--accent);
  text-decoration: none;
}
.fw-mm-link--overview:hover {
  background: rgba(201, 162, 39, 0.1);
}
.fw-mm-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.65rem;
  width: 100%;
  min-height: 44px;
  padding: 10px 14px;
  border: 0;
  border-radius: 8px;
  background: transparent;
  color: #fff;
  font-family: inherit;
  font-size: 0.88rem;
  font-weight: 700;
  text-align: left;
  cursor: pointer;
}
.fw-mm-item--branch.fw-mm-item--open > .fw-mm-trigger {
  background: rgba(201, 162, 39, 0.14);
  color: var(--accent);
}
.fw-mm-label {
  flex: 1 1 auto;
  min-width: 0;
  line-height: 1.25;
}
.fw-mm-chevron {
  flex: 0 0 auto;
  width: 8px;
  height: 8px;
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
  transform: rotate(45deg) translateY(-1px);
  transition: transform 0.22s ease;
}
.fw-mm-item--open > .fw-mm-trigger .fw-mm-chevron {
  transform: rotate(-135deg) translateY(1px);
}
.fw-mm-submenu {
  display: flex;
  flex-direction: column;
  gap: 1px;
  padding: 4px 0 8px 10px;
}
.fw-mm-submenu[hidden] {
  display: none !important;
}
.fw-mm-sublink {
  display: block;
  padding: 9px 12px;
  border-radius: 6px;
  color: rgba(255, 255, 255, 0.78);
  font-size: 0.86rem;
  font-weight: 600;
  text-decoration: none;
}
.fw-mm-sublink:hover {
  background: rgba(201, 162, 39, 0.1);
  color: #fff;
}
.area-card h3 a {
  color: #fff;
  text-decoration: none;
}
.area-card h3 a:hover {
  color: var(--accent);
}
.area-card-county {
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--accent);
  margin: -4px 0 10px;
}
.area-card-meta {
  font-size: 0.82rem;
  color: var(--muted);
  margin: 0 0 12px;
}
.area-card-cta {
  display: inline-flex;
  margin-top: 14px;
  font-size: 0.86rem;
  font-weight: 700;
  color: var(--accent);
  text-decoration: none;
}
.area-card-cta:hover {
  text-decoration: underline;
}
.area-card--county {
  border-color: rgba(201, 162, 39, 0.22);
}
.areas-grid--counties {
  margin-bottom: 0;
}
  background: linear-gradient(180deg, #0a0a0a 0%, #101510 100%);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}
.scope-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}
.scope-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 28px 24px;
}
.scope-card h3 {
  font-family: var(--font-head);
  color: #fff;
  margin-bottom: 12px;
  font-size: 1.15rem;
}
.scope-card p,
.scope-card li {
  color: var(--muted);
  font-size: 0.94rem;
  line-height: 1.65;
}
.scope-card ul {
  margin: 14px 0 0;
  padding-left: 1.1rem;
}
.scope-card--dont {
  border-color: rgba(180, 80, 80, 0.25);
}
.service-directory {
  display: grid;
  gap: 28px;
}
.service-directory-group h3 {
  font-family: var(--font-head);
  color: #fff;
  margin-bottom: 8px;
}
.service-directory-group > p {
  color: var(--muted);
  margin-bottom: 16px;
  max-width: 70ch;
}
.service-directory-items {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}
.service-directory-item {
  display: block;
  text-decoration: none;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 18px 16px;
  transition: border-color 0.2s ease, transform 0.2s ease;
}
.service-directory-item:hover {
  border-color: rgba(201, 162, 39, 0.45);
  transform: translateY(-2px);
}
.service-directory-item strong {
  display: block;
  color: #fff;
  font-size: 0.98rem;
  margin-bottom: 8px;
}
.service-directory-item span {
  display: block;
  color: var(--muted);
  font-size: 0.86rem;
  line-height: 1.55;
}
.fw-service-card--featured {
  outline: 1px solid rgba(201, 162, 39, 0.35);
}
.fw-service-card__badge {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 3;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(201, 162, 39, 0.92);
  color: #0a0a0a;
  font-size: 0.62rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.phase-badge {
  display: inline-block;
  margin-bottom: 10px;
  padding: 5px 12px;
  border-radius: 999px;
  background: rgba(201, 162, 39, 0.15);
  border: 1px solid rgba(201, 162, 39, 0.35);
  color: var(--accent);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.related-services {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 24px;
}
.related-services a {
  display: inline-flex;
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid rgba(201, 162, 39, 0.25);
  color: var(--accent);
  text-decoration: none;
  font-size: 0.86rem;
}
.related-services a:hover {
  background: rgba(201, 162, 39, 0.1);
}
@media (max-width: 900px) {
  .scope-grid,
  .service-directory-items {
    grid-template-columns: 1fr;
  }
}

/* ---- Knight-style mobile header & drawer ---- */
.site-header .header-inner {
  min-height: 84px;
  gap: clamp(10px, 1.5vw, 18px);
  flex-wrap: nowrap;
}
.brand-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 0 0 auto;
  min-width: 0;
}
.site-header .brand-logo {
  height: 68px;
  width: auto;
}
.site-nav {
  flex: 1 1 auto;
  justify-content: center;
  gap: clamp(10px, 1.4vw, 22px);
  min-width: 0;
}
.site-nav a,
.nav-dropdown-btn {
  font-size: clamp(0.68rem, 0.45vw + 0.6rem, 0.78rem);
  letter-spacing: 0.08em;
  white-space: nowrap;
}
.btn-header-estimate {
  min-height: 40px;
  padding: 0 14px;
  font-size: 0.74rem;
  letter-spacing: 0.06em;
  white-space: nowrap;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}
.hamburger-btn {
  display: none;
  flex-shrink: 0;
}

/* Knight Group-style call CTA (gold theme) */
.fw-header-call {
  display: inline-flex;
  flex-direction: row;
  align-items: center;
  gap: 0.55rem;
  flex-shrink: 0;
  text-decoration: none;
  color: #fff;
  transition: transform 0.18s ease;
}
.fw-header-call:hover,
.fw-header-call:focus-visible {
  transform: translateY(-1px);
  outline: none;
}
.fw-header-call__icon {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 2px solid var(--accent);
  color: var(--accent);
  background: rgba(201, 162, 39, 0.12);
  box-shadow: 0 0 14px rgba(201, 162, 39, 0.22);
}
.fw-header-call__icon svg {
  display: block;
}
.fw-header-call__text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: 0.05rem;
  line-height: 1.1;
  min-width: 0;
}
.fw-header-call__label {
  font-size: clamp(0.52rem, 0.15vw + 0.46rem, 0.62rem);
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(245, 240, 232, 0.88);
}
.fw-header-call__number {
  font-family: var(--font-head);
  font-size: clamp(0.78rem, 0.35vw + 0.62rem, 0.92rem);
  font-weight: 700;
  letter-spacing: 0.02em;
  color: #fff;
  white-space: nowrap;
}
.fw-header-call:hover .fw-header-call__icon,
.fw-header-call:focus-visible .fw-header-call__icon {
  border-color: #e0c04a;
  color: #f0e0a8;
  background: rgba(201, 162, 39, 0.22);
}
.fw-header-call:focus-visible .fw-header-call__icon {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.fw-header-call--menu {
  width: 100%;
  justify-content: center;
  padding: 12px 16px;
  border: 1px solid rgba(201, 162, 39, 0.28);
  border-radius: var(--radius-md);
  background: rgba(201, 162, 39, 0.06);
}

.hero-copy h1 {
  font-size: clamp(2.2rem, 4.8vw, 4.25rem);
  line-height: 0.98;
  margin-bottom: 20px;
}

/* Hero parallax */
.hero {
  position: relative;
  overflow: hidden;
  isolation: isolate;
  background: #0a0a0a;
  background-image: none;
}
.hero-bg {
  position: absolute;
  inset: -22% 0;
  z-index: 0;
  background: url("Images/gallery/photo-of-all-equipment.webp") center / cover no-repeat;
  transform: translate3d(0, var(--hero-shift, 0px), 0);
  will-change: transform;
}
.hero-overlay {
  z-index: 1;
}
.hero-inner {
  position: relative;
  z-index: 2;
  grid-template-columns: minmax(0, 1fr) minmax(360px, 440px);
  gap: clamp(32px, 4vw, 56px);
  max-width: none;
}

@media (min-width: 1061px) {
  .hero-inner {
    align-items: stretch;
  }
  .hero-copy {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .hero-card {
    display: flex;
    flex-direction: column;
    padding: 28px 24px;
  }
  .hero-card .card-eyebrow {
    margin-bottom: 8px;
  }
  .hero-card .card-name {
    font-size: 1.45rem;
    margin-bottom: 8px;
  }
  .hero-card .card-note {
    margin-bottom: 14px;
    font-size: 0.84rem;
  }
  .hero-card .contact-form-hero {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-height: 0;
  }
  .hero-card .contact-form-hero .form-group {
    gap: 4px;
  }
  .hero-card .contact-form-hero .form-group label {
    font-size: 0.72rem;
  }
  .hero-card .contact-form-hero .form-group input,
  .hero-card .contact-form-hero .form-group select,
  .hero-card .contact-form-hero .form-group textarea {
    padding: 10px 12px;
    font-size: 0.92rem;
  }
  .hero-card .contact-form-hero .form-group textarea {
    min-height: 72px;
    resize: vertical;
  }
  .hero-card .form-footer {
    margin-top: auto;
    padding-top: 4px;
  }
  .hero-card .form-footer .form-note {
    margin-top: 8px;
    margin-bottom: 0;
    font-size: 0.78rem;
  }
}

@media (max-width: 720px) {
  .hero {
    background-image: none;
  }
  .hero-bg {
    background-image: url("Images/gallery/excavator-and-truck-photo.webp");
    background-position: top center;
  }
}

.brand-text-wrap {
  display: none;
  flex-direction: column;
  min-width: 0;
  line-height: 1.25;
}
.brand-title-link {
  text-decoration: none;
  color: inherit;
}
.brand-title {
  font-family: var(--font-head);
  font-size: 1.05rem;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.04em;
}
.brand-tagline {
  font-size: 0.72rem;
  color: var(--muted);
  margin-top: 2px;
}
.header-brand-ctas {
  display: none;
  align-items: center;
  gap: 8px;
  margin-top: 6px;
  flex-wrap: wrap;
}
.btn-mobile-estimate {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  text-decoration: none;
  color: #0a0a0a;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%);
  white-space: nowrap;
}
.mobile-menu-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: inherit;
}
.mobile-menu-brand-name {
  font-family: var(--font-head);
  font-size: 1.05rem;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.04em;
}
.mobile-cta-row {
  display: none;
  flex-direction: column;
  gap: 10px;
  padding: 16px 16px 8px;
  border-top: 1px solid rgba(201, 162, 39, 0.15);
}
.mobile-menu-footer {
  display: none;
  padding: 16px 20px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  margin-top: auto;
  text-align: center;
}
.mobile-menu-footer p {
  margin: 0;
  font-size: 0.72rem;
  color: var(--muted);
}

@media (max-width: 1320px) and (min-width: 1201px) {
  .site-nav {
    gap: 12px;
  }
}

@media (max-width: 1200px) {
  .site-nav {
    display: none !important;
  }
  .site-header .header-inner {
    min-height: 78px;
    padding: 10px 0;
    gap: 10px;
    justify-content: flex-start;
  }
  .site-header .brand-logo {
    height: 50px;
  }
  .header-actions {
    display: flex !important;
    margin-left: auto;
    flex-shrink: 0;
  }
  .btn-header-estimate {
    min-height: 38px;
    padding: 0 12px;
    font-size: 0.68rem;
  }
  .fw-header-call {
    margin-left: 8px;
    flex-shrink: 0;
  }
  .fw-header-call__text {
    display: flex;
  }
  .fw-header-call__icon {
    width: 36px;
    height: 36px;
  }
  .fw-header-call__label {
    font-size: 0.48rem;
    letter-spacing: 0.08em;
  }
  .fw-header-call__number {
    font-size: clamp(0.66rem, 2.8vw, 0.78rem);
    white-space: nowrap;
  }
  .hamburger-btn {
    display: flex !important;
    flex-shrink: 0;
    order: -1;
    background: rgba(20, 20, 20, 0.95);
    border: 1px solid rgba(201, 162, 39, 0.28);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 12px;
  }
  .hamburger-btn span {
    background: var(--accent);
    box-shadow: 0 0 8px rgba(201, 162, 39, 0.2);
  }
  .hamburger-btn:hover {
    background: rgba(30, 30, 30, 1);
    border-color: rgba(201, 162, 39, 0.5);
  }
  .brand-wrap {
    flex: 0 0 auto;
  }
  .brand-text-wrap {
    display: none;
  }
  .mobile-cta-row,
  .mobile-menu-footer {
    display: flex;
  }
  .mobile-nav {
    left: -100%;
    right: auto;
    border-right: 1px solid rgba(201, 162, 39, 0.28);
    border-left: none;
    box-shadow: 10px 0 50px rgba(0, 0, 0, 0.6);
    background: linear-gradient(135deg, #111111 0%, #1a1a1a 50%, #111111 100%);
    transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .mobile-nav.is-open {
    left: 0;
    right: auto;
  }
  .mobile-nav-logo {
    height: 36px;
    width: 36px;
    filter: none;
    border-radius: 8px;
    object-fit: contain;
  }
  .mobile-nav-close:hover {
    background: rgba(201, 162, 39, 0.12);
    border-color: var(--accent);
  }
  .mobile-nav-links a:hover,
  .mobile-services-toggle:hover {
    background: rgba(201, 162, 39, 0.1);
    border-color: var(--accent);
  }
}

@media (min-width: 1201px) {
  .hamburger-btn {
    display: none !important;
  }
}

@media (max-width: 640px) {
  .brand-text-wrap,
  .header-brand-ctas,
  .header-actions {
    display: none !important;
  }
  .site-header .header-inner {
    min-height: 64px;
    padding: 8px 0;
    gap: 8px;
  }
  .site-header .brand-logo {
    height: 44px;
  }
  .fw-header-call {
    margin-left: auto;
    gap: 0.4rem;
  }
  .fw-header-call__icon {
    width: 32px;
    height: 32px;
  }
  .fw-header-call__label {
    font-size: 0.46rem;
  }
  .fw-header-call__number {
    font-size: clamp(0.62rem, 2.6vw, 0.74rem);
  }
  .hero-copy .eyebrow {
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    line-height: 1.45;
    margin-bottom: 12px;
  }
  .hero-copy h1 {
    font-size: clamp(1.65rem, 7.5vw, 2.35rem);
    line-height: 1.06;
    margin-bottom: 16px;
  }
}

@media (max-width: 480px) {
  .site-header .brand-logo {
    height: 40px;
  }
}

@media (max-width: 720px) {
  .site-header .header-inner {
    flex-wrap: nowrap;
  }
}

html, body {
  overflow-x: clip;
}

/* ---- 3D logo coin (Knight Group style) ---- */
.fw-logo-coin {
  display: inline-flex;
  flex-shrink: 0;
}
.fw-logo-coin__scene {
  width: 100%;
  height: 100%;
  perspective: 1000px;
}
.fw-logo-coin__spinner {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  animation: fwLogoCoinFlip 7s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite;
}
.fw-logo-coin__face {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  overflow: hidden;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  background: #0a0a0a;
  box-shadow:
    inset 0 0 0 3px rgba(201, 162, 39, 0.32),
    0 14px 32px rgba(0, 0, 0, 0.38);
}
.fw-logo-coin__face img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.fw-logo-coin__face--back {
  transform: rotateY(180deg);
}
.fw-logo-coin--header .fw-logo-coin__scene {
  width: 68px;
  height: 68px;
}
.fw-logo-coin--menu .fw-logo-coin__scene {
  width: 36px;
  height: 36px;
}
.fw-logo-coin--footer .fw-logo-coin__scene {
  width: 80px;
  height: 80px;
}
.fw-logo-coin--about .fw-logo-coin__scene {
  width: clamp(160px, 18vw, 220px);
  height: clamp(160px, 18vw, 220px);
  margin: 0 auto 20px;
}
@keyframes fwLogoCoinFlip {
  0%, 18%   { transform: rotateY(0deg); }
  32%, 68%  { transform: rotateY(180deg); }
  82%, 100% { transform: rotateY(360deg); }
}
@media (prefers-reduced-motion: reduce) {
  .fw-logo-coin__spinner {
    animation: none;
    transform: rotateY(0deg);
  }
}

/* ---- Knight-style slide-in enters ---- */
:root {
  --fw-ease-out: cubic-bezier(0.22, 1, 0.36, 1);
}
html.fw-js [data-fw-enter] {
  opacity: 0;
  will-change: transform, opacity;
}
html.fw-js [data-fw-enter="left"] {
  transform: translate3d(calc(-1 * min(34vw, 128px)), 0, 0);
}
html.fw-js main h1[data-fw-enter="left"],
html.fw-js .hero-copy h1[data-fw-enter="left"] {
  transform: translate3d(calc(-1 * min(48vw, 180px)), 0, 0);
}
html.fw-js [data-fw-enter="right"] {
  transform: translate3d(min(34vw, 128px), 0, 0);
}
html.fw-js [data-fw-enter="top"] {
  transform: translate3d(0, calc(-1 * min(18vh, 88px)), 0);
}
html.fw-js [data-fw-enter="bottom"] {
  transform: translate3d(0, min(18vh, 88px), 0);
}
html.fw-js [data-fw-enter].is-visible {
  animation: fwEnterIn 0.86s var(--fw-ease-out) var(--fw-enter-delay, 0ms) forwards;
}
@keyframes fwEnterIn {
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}
@media (prefers-reduced-motion: reduce) {
  html.fw-js [data-fw-enter] {
    opacity: 1;
    transform: none;
    animation: none !important;
  }
}

/* Pill eyebrows */
.eyebrow,
.card-eyebrow {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  max-width: 100%;
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(201, 162, 39, 0.1);
  border: 1px solid rgba(201, 162, 39, 0.28);
  line-height: 1.35;
}
.section-heading .eyebrow {
  margin-bottom: 14px;
}
.sp-hero .eyebrow {
  margin-bottom: 12px;
}
.footer-inner .fw-logo-coin--footer {
  opacity: 0.92;
}
@media (max-width: 1200px) {
  .fw-logo-coin--header .fw-logo-coin__scene {
    width: 50px;
    height: 50px;
  }
}
@media (max-width: 640px) {
  .fw-logo-coin--header .fw-logo-coin__scene {
    width: 44px;
    height: 44px;
  }
}
@media (max-width: 480px) {
  .fw-logo-coin--header .fw-logo-coin__scene {
    width: 40px;
    height: 40px;
  }
}

@media (max-width: 900px) { .process-grid, .areas-grid, .intent-grid, .service-detail-grid { grid-template-columns: repeat(2, 1fr); } .gallery-grid { grid-template-columns: repeat(2, 1fr); } }

/* ---- Service mosaic (Knight Group / Clearwater Dentist v2 pattern) ---- */
.services-section .container .section-heading {
  margin-bottom: 0;
}
.services-mosaic-wrap {
  width: min(95vw, var(--container));
  margin: 2rem auto 0;
}
.services-mosaic {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr));
  gap: 0;
}
@media (min-width: 900px) {
  .services-mosaic {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
.fw-service-card {
  position: relative;
  display: block;
  min-height: 236px;
  aspect-ratio: 1 / 1;
  padding: 0;
  overflow: hidden;
  border: 0;
  border-radius: 0;
  box-shadow: none;
  text-decoration: none;
  color: #fff;
  background: #0a0a0a;
}
.fw-service-card__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center center;
  z-index: 0;
  transition: transform 0.45s cubic-bezier(0.22, 1, 0.36, 1);
}
.fw-service-card__overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background: linear-gradient(
    180deg,
    rgba(0, 0, 0, 0.22) 0%,
    rgba(0, 0, 0, 0.42) 55%,
    rgba(0, 0, 0, 0.62) 100%
  );
  transition: background 0.3s ease;
}
.fw-service-card__panel {
  position: absolute;
  inset: 0;
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: flex-start;
  padding: 1.35rem 1.2rem 1.25rem;
  transition: opacity 0.38s ease, transform 0.38s ease;
}
.fw-service-card__panel--hover {
  opacity: 0;
  transform: translateY(10px);
  pointer-events: none;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 0.45rem;
  padding: 0.85rem 1rem 1rem;
  box-sizing: border-box;
}
.fw-service-card__icon {
  display: block;
  width: 28px;
  height: 28px;
  margin-bottom: 0.7rem;
  flex: 0 0 auto;
  color: var(--accent);
  filter: drop-shadow(0 1px 8px rgba(0, 0, 0, 0.5));
}
.fw-service-card__headline {
  display: block;
  font-family: var(--font-head);
  font-size: clamp(0.95rem, 0.45vw + 0.78rem, 1.1rem);
  line-height: 1.28;
  font-weight: 700;
  margin: 0;
  color: #fff;
  max-width: 18ch;
  text-shadow: 0 1px 12px rgba(0, 0, 0, 0.55);
}
.fw-service-card__title {
  display: block;
  font-family: var(--font-head);
  font-size: clamp(1.08rem, 0.5vw + 0.92rem, 1.32rem);
  line-height: 1.22;
  font-weight: 700;
  margin: 0;
  color: #fff;
  max-width: 92%;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  text-shadow: 0 1px 10px rgba(0, 0, 0, 0.5);
}
.fw-service-card__detail {
  display: -webkit-box;
  overflow: hidden;
  font-size: clamp(0.84rem, 0.35vw + 0.74rem, 0.96rem);
  line-height: 1.45;
  color: rgba(245, 240, 232, 0.92);
  margin: 0;
  max-width: 92%;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 4;
  line-clamp: 4;
}
.fw-service-card__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 9.5rem;
  max-width: 13.5rem;
  min-height: 36px;
  padding: 0.45rem 0.75rem;
  border: 2px solid var(--accent);
  background: rgba(0, 0, 0, 0.55);
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #f5f0e8;
  box-sizing: border-box;
  margin-top: 0.2rem;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.78);
}
@media (hover: hover) {
  .fw-service-card:hover .fw-service-card__bg,
  .fw-service-card:focus-visible .fw-service-card__bg {
    transform: scale(1.03);
  }
  .fw-service-card:hover .fw-service-card__overlay,
  .fw-service-card:focus-visible .fw-service-card__overlay {
    background: linear-gradient(
      180deg,
      rgba(0, 0, 0, 0.45) 0%,
      rgba(0, 0, 0, 0.62) 50%,
      rgba(0, 0, 0, 0.76) 100%
    );
  }
  .fw-service-card:hover .fw-service-card__panel--front,
  .fw-service-card:focus-visible .fw-service-card__panel--front {
    opacity: 0;
    transform: translateY(-10px);
  }
  .fw-service-card:hover .fw-service-card__panel--hover,
  .fw-service-card:focus-visible .fw-service-card__panel--hover {
    opacity: 1;
    transform: translateY(0);
    pointer-events: auto;
    z-index: 3;
  }
}
@media (max-width: 560px) { .process-grid, .areas-grid, .gallery-grid, .intent-grid, .service-detail-grid { grid-template-columns: 1fr; } }
"""
    write_site_file(ROOT / "styles.css", src + extra)


def patch_script() -> None:
    text = (ROOT / "script.js").read_text(encoding="utf-8")
    text = text.replace("(727) 386-6562", SITE["phone_display"])
    text = text.replace("7273866562", SITE["phone_tel"])
    text = text.replace("Chris will be in touch shortly", "Tyler will review your project and contact you shortly")
    text = text.replace("hero-contact-form", "hero-contact-form")
    # Handle contact page form too
    if "contact-form" not in text:
        contact_handler = """
const contactForm = document.getElementById("contact-form");
const contactSuccess = document.getElementById("form-success");

if (contactForm && contactSuccess && !heroForm) {
  contactForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const submitBtn = contactForm.querySelector("[type='submit']");
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = "Sending...";
    try {
      const res = await fetch(contactForm.action, {
        method: "POST",
        body: new FormData(contactForm),
        headers: { Accept: "application/json" },
      });
      if (res.ok) {
        submitBtn.textContent = "Sent! ✓";
        setTimeout(() => {
          contactForm.hidden = true;
          contactSuccess.hidden = false;
        }, 1800);
      } else {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
        alert("Something went wrong. Please email contact@faithworksods.com directly.");
      }
    } catch {
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
      alert("Could not send. Please email contact@faithworksods.com directly.");
    }
  });
}
"""
        text += contact_handler

    parallax_block = """
// ---- Hero parallax ----
(function initHeroParallax() {
  const hero = document.querySelector(".hero");
  const bg = hero && hero.querySelector(".hero-bg");
  if (!hero || !bg) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  let restTop = 0;
  let ticking = false;
  const rate = 0.45;

  function update() {
    ticking = false;
    const rect = hero.getBoundingClientRect();
    if (window.scrollY < 2) {
      const header = document.querySelector(".site-header");
      restTop = header ? header.getBoundingClientRect().height : rect.top;
    }
    const shift = -(rect.top - restTop) * rate;
    bg.style.setProperty("--hero-shift", Math.round(shift) + "px");
  }

  function queue() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  update();
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", queue, { passive: true });
})();
"""
    if "initHeroParallax" not in text:
        text += parallax_block

    write_site_file(ROOT / "script.js", text)


def cleanup_obsolete_pages() -> None:
    keep = {f"{s['slug']}.html" for s in SERVICES}
    keep.update(
        {
            "index.html",
            "services.html",
            "about.html",
            "contact.html",
            "gallery.html",
            "service-areas.html",
            "privacy-policy.html",
        }
    )
    area_keep = {c["slug"] for c in AREA_CITIES} | {c["slug"] for c in COUNTIES}
    areas_dir = ROOT / "areas"
    areas_dir.mkdir(exist_ok=True)
    for path in areas_dir.glob("*.html"):
        if path.stem not in area_keep:
            path.unlink(missing_ok=True)
    for path in ROOT.glob("*.html"):
        if path.name not in keep:
            path.unlink(missing_ok=True)


def main() -> None:
    sync_logo()
    write_styles()
    patch_script()
    write_index()
    write_services()
    for s in SERVICES:
        write_service_page(s)
    write_gallery()
    write_about()
    write_contact()
    write_service_areas()
    write_area_pages()
    write_privacy()
    write_sitemap()
    write_robots()
    write_cname()
    cleanup_obsolete_pages()
    print(f"Built Faith Works website in {ROOT} ({SERVICE_COUNT} services)")


if __name__ == "__main__":
    main()
