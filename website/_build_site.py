#!/usr/bin/env python3
"""Generate Faith Works Outdoor Services static website."""

from __future__ import annotations

import json
import os
import re
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import quote

from area_page_content import (
    area_intent_cards,
    area_services_by_category,
    city_area_faqs,
    city_common_jobs_section,
    city_intro_html,
    city_meta_description,
    city_page_title,
    city_process_section,
    city_property_section,
    city_scope_section,
    county_area_faqs,
    county_intro_html,
    county_meta_description,
    county_property_section,
    nearby_cities_html,
    nearby_counties_html,
)
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
LOGO = "Images/fw-logo3-144.webp"
LOGO_LARGE = "Images/fw-logo3.webp"


def sync_logo() -> None:
    src = ROOT / "Images" / "fw-logo3-192.png"
    dst = ROOT / "Images" / "Logo.png"
    if src.exists():
        shutil.copy2(src, dst)
    elif (ROOT / "Images" / "fw-logo3.png").exists():
        shutil.copy2(ROOT / "Images" / "fw-logo3.png", dst)


def logo_path(display_size: int) -> str:
    return LOGO_LARGE if display_size >= 160 else LOGO


def mosaic_image_src(filename: str) -> str:
    card = f"Gallery/cards/{filename}"
    if (ROOT / card).exists():
        return card
    return f"Gallery/{filename}"


def logo_coin(modifier: str = "fw-logo-coin--header", size: int = 68, alt: str = "", logo_src: str | None = None) -> str:
    src = logo_src or logo_path(size)
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


def public_asset_url(relative_path: str) -> str:
    base = os.environ.get(
        "PUBLIC_ASSET_BASE",
        "https://nicholasjknight.github.io/faithworksods-website",
    ).strip().rstrip("/")
    return f"{base}/{relative_path.lstrip('/')}"


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
    "area": "Polk County and nearby Central Florida communities",
    "area_detail": "Based in Auburndale, FL, Faith Works primarily serves Polk County and nearby Central Florida communities. Larger acreage, land clearing, and equipment-assisted cleanup projects may be considered outside the immediate area.",
    "geo_lat": "28.0653",
    "geo_lng": "-81.7887",
    "facebook": "https://www.facebook.com/profile.php?id=PLACEHOLDER",
    "youtube": "https://www.youtube.com/@PLACEHOLDER",
    "google_business": "PLACEHOLDER",
    "formspree": "https://formspree.io/f/PLACEHOLDER",
    "ga4": "G-PLACEHOLDER",
    "clarity": "PLACEHOLDER",
}


def formspree_endpoint() -> str:
    form_id = configured_formspree_id()
    if not form_id:
        formspree_url = SITE.get("formspree", "")
        if formspree_url and "PLACEHOLDER" not in formspree_url:
            form_id = formspree_url.rstrip("/").rsplit("/", 1)[-1]
    return f"https://formspree.io/f/{form_id}" if form_id else ""


def formsubmit_endpoint() -> str:
    return f"https://formsubmit.co/ajax/{SITE['email']}"


def form_action_attrs(subject: str) -> tuple[str, str, str, str, str]:
    endpoint = formspree_endpoint()
    if endpoint:
        return endpoint, "POST", "multipart/form-data", "", "formspree"
    return formsubmit_endpoint(), "POST", "multipart/form-data", ' data-form-mode="formsubmit"', "formsubmit"


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

ASSET_VERSION = "20260627"
HERO_DESKTOP = "photo-of-all-equipment.webp"
HERO_MOBILE = "excavator-and-truck-photo.webp"
HERO_MOBILE_LCP = f"heroes/{HERO_MOBILE}"
CONTACT_BANNER = "Gallery/equipment-photos5.webp"
CONTACT_CUTOUT = "Images/fw-banner-cutout.webp"
PROCESS_BG = "Gallery/tractor-with-box-blade-leveling-ground.webp"

GOOGLE_G_LOGO = """<svg class="fw-google-g-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" aria-hidden="true" focusable="false">
                                <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                                <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                                <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
                                <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
                            </svg>"""

REVIEW_PLACEHOLDERS: list[dict] = []

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


HOME_BUYER_CATEGORIES = [
    {
        "title": "Land Clearing & Forestry Mulching",
        "text": "Open up overgrown lots, small acreage, wooded edges, and brush-heavy areas with owner-operated equipment.",
        "image": "excavator-photo.webp",
        "links": ["land-clearing", "forestry-mulching", "brush-clearing", "overgrowth-removal"],
    },
    {
        "title": "Pond Bank & Ditch Clearing",
        "text": "Clear vegetation, debris, and access problems around private pond banks, swales, and outdoor ditch lines.",
        "image": "tractor-with-box-blade-leveling-ground.webp",
        "links": ["pond-bank-clearing", "pond-cleanup", "ditch-clearing", "ditch-maintenance"],
    },
    {
        "title": "Trail, Fence Line & Access Clearing",
        "text": "Reopen paths, fence rows, access routes, and hard-to-reach property edges across residential and rural land.",
        "image": "tractor.webp",
        "links": ["trail-clearing", "fence-line-clearing", "access-road-clearing", "tractor-services"],
    },
    {
        "title": "Storm, Yard & Property Cleanup",
        "text": "Clean up limbs, brush piles, yard debris, overgrown lots, and deferred-maintenance areas after weather or clearing.",
        "image": "tractor-moving-item-with-grapple.webp",
        "links": ["debris-removal", "storm-debris-cleanup", "yard-debris-removal", "property-cleanup"],
    },
    {
        "title": "Tractor & Equipment Services",
        "text": "Kubota tractor, excavator, trailers, and brush equipment for practical outdoor property jobs with direct owner communication.",
        "image": "photo-of-all-equipment.webp",
        "links": ["equipment-services", "tractor-services", "acreage-cleanup", "lot-cleanup"],
    },
]

HOME_FAQS = [
    (
        "Do you offer free estimates?",
        f"Yes. Text photos to {SITE['phone_display']} or use the estimate form. Photo-based estimates help us review access, vegetation, debris, and project scope before scheduling.",
    ),
    (
        "What areas do you serve near Auburndale, FL?",
        f"{SITE['brand']} is based in {SITE['city']} (33823) and primarily serves Polk County communities including Auburndale, Winter Haven, Lakeland, Lake Alfred, Bartow, Haines City, Davenport, Lake Wales, and Polk City. Plant City and larger Central Florida projects may be reviewed by scope.",
    ),
    (
        "How far from Auburndale will Faith Works travel for a job?",
        "Most launch work is focused in Polk County and nearby communities so scheduling, estimates, and Google Business Profile relevance stay accurate. Larger acreage, land clearing, and equipment-assisted cleanup projects outside the immediate area can be reviewed case by case.",
    ),
    (
        "What outdoor property services do you offer in Polk County?",
        f"Faith Works provides {SITE_POSITIONING.lower()} - including land clearing, trail clearing, brush cutting, forestry mulching, pond bank clearing, pond cleanup, ditch clearing, debris removal, acreage cleanup, pool dig-out support, and tractor services.",
    ),
    (
        "Do you clear overgrown pond banks and ditches?",
        "Yes. Pond bank clearing and ditch clearing are core services. We use compact equipment, brush cutters, and tractors to open access, remove overgrowth, and clean vegetation from outdoor ditch and pond-edge areas.",
    ),
    (
        "Do I need to call 811 before digging?",
        "For digging or soil-moving work, contact Sunshine 811 at least two full business days before work begins so underground utilities can be marked.",
    ),
    (
        "What work is outside Faith Works' scope?",
        f"Faith Works does not install pools, hold pool contractor licensing, or perform utility trenching, stormwater system installation, sewer work, water mains, site development, or engineered drainage. The focus is {SITE_POSITIONING.lower()}.",
    ),
    (
        "What jobs do people usually call you for?",
        "Most calls are for pond banks, trails, brush, overgrowth, debris, acreage cleanup, and owner-operated tractor or equipment help. Pool dig-out support is available under licensed pool builders.",
    ),
    (
        "Can you help with pool dig-out dirt removal?",
        "Yes, as support under a licensed pool contractor. Faith Works can help with dirt removal and site cleanup, but does not contract directly as a pool installer.",
    ),
    (
        "Do you handle storm debris cleanup in Central Florida?",
        "Yes. Storm debris cleanup, yard debris removal, and property cleanup are available after wind and storm events when access and scope allow. Send photos of limbs, brush piles, and blocked areas for a faster estimate.",
    ),
]

FACEBOOK_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>'
YOUTUBE_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>'


def live_url(url: str) -> bool:
    return bool(url and "PLACEHOLDER" not in url)


def same_as_links() -> list[str]:
    return [url for url in (SITE["facebook"], SITE["youtube"], SITE["google_business"]) if live_url(url)]


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


def minify_css(css: str) -> str:
    css = re.sub(r"/\*[\s\S]*?\*/", "", css)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", css)
    return css.strip()


def fonts_head() -> str:
    return """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap"></noscript>"""


def favicon_head(root_prefix: str = "") -> str:
    icon = f"{root_prefix}Images/fw-logo3-192.png"
    return f"""  <link rel="icon" type="image/png" href="{icon}">
  <link rel="apple-touch-icon" href="{icon}">"""


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
            <img class="fw-service-card__bg" src="{mosaic_image_src(s['mosaic_image'])}" alt="{img_alt}" loading="lazy" decoding="async" width="800" height="800">
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
          <h2>Outdoor Property Services - Clear Project Fit</h2>
          <p>Faith Works keeps estimates practical by matching each job to the right outdoor property service, equipment access, and cleanup outcome before work begins.</p>
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
            <h3>Work outside our scope</h3>
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


def reviews_section() -> str:
    return f"""
    <section id="reviews" class="reviews-section section-shell reviews-section--soon">
      <div class="container">
        <div class="reviews-coming-soon" data-fw-enter="bottom">
          <p class="eyebrow">Reviews coming soon</p>
          <h2>Faith Works Outdoor Services Is Newly Launched</h2>
          <p>Google reviews will appear here once the Google Business Profile is verified and real customer reviews are available. Until then, this site will not publish unverified testimonials, review schema, or aggregate rating markup.</p>
          <a class="btn btn-ghost" href="contact.html">Request an Estimate</a>
        </div>
      </div>
    </section>"""


def process_section() -> str:
    return f"""
    <section id="process" class="process-section process-section--parallax section-shell" data-parallax-overscan="0.38" data-parallax-rate="0.78" aria-label="How it works">
      <div class="process-bg fw-parallax-bg" aria-hidden="true">
        <img src="{PROCESS_BG}" alt="" width="1920" height="1080" loading="lazy" decoding="async" class="process-bg__img" role="presentation">
      </div>
      <div class="process-overlay" aria-hidden="true"></div>
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">How it works</p>
          <h2>How to Get Land Clearing or Property Cleanup in {SITE['city']}</h2>
          <p>A simple four-step process from photos to scheduled outdoor property work across {SITE['area']}.</p>
        </div>
        <div class="process-grid">
          <div class="process-step" data-fw-enter="bottom" style="--fw-enter-delay: 0ms;"><span>1</span><h3>Text photos or use the form</h3><p>Share your property city, contact details, and photos of overgrowth, pond banks, ditches, brush, or debris.</p></div>
          <div class="process-step" data-fw-enter="bottom" style="--fw-enter-delay: 70ms;"><span>2</span><h3>Confirm scope</h3><p>Tyler reviews access, vegetation volume, equipment room, haul-off needs, and the outdoor service that fits the job.</p></div>
          <div class="process-step" data-fw-enter="bottom" style="--fw-enter-delay: 140ms;"><span>3</span><h3>Receive estimate</h3><p>Get a clear estimate before work begins, with scope matched to the property and equipment access.</p></div>
          <div class="process-step" data-fw-enter="bottom" style="--fw-enter-delay: 210ms;"><span>4</span><h3>Schedule service</h3><p>Faith Works shows up with the right equipment for clearing, cleanup, or tractor work on your property.</p></div>
        </div>
      </div>
    </section>"""


def home_geo_section() -> str:
    city_sample = ", ".join(c["name"] for c in FEATURED_CITIES[:6])
    county_names = " and ".join(c["name"] for c in COUNTIES)
    return f"""
    <section id="service-areas" class="home-geo-strip" aria-label="Service areas">
      <div class="container home-geo-strip__inner">
        <div class="home-geo-strip__copy" data-fw-enter="left">
          <p class="home-geo-strip__eyebrow">Service areas</p>
          <p class="home-geo-strip__text">Based in {SITE['city']}, FL — {SITE['brand']} serves {county_names} with land clearing, pond bank work, ditch clearing, and outdoor property cleanup. Common launch cities include {city_sample}, and nearby communities.</p>
        </div>
        <div class="home-geo-strip__actions" data-fw-enter="right">
          <a class="btn btn-ghost home-geo-strip__cta" href="service-areas.html">View all service areas</a>
          <a class="btn btn-primary home-geo-strip__cta" href="contact.html">Request estimate</a>
        </div>
      </div>
    </section>"""


def gallery_teaser_section() -> str:
    thumbs = ""
    for i, (img, alt, label) in enumerate(GALLERY[:6]):
        thumbs += f"""
          <a class="work-thumb" href="gallery.html" aria-label="View {label} gallery" data-fw-enter="bottom" style="--fw-enter-delay: {(i % 3) * 70}ms;">
            <img src="{mosaic_image_src(img)}" alt="{alt}" loading="lazy" width="600" height="450">
            <span class="work-thumb-label">{label}</span>
          </a>"""
    return f"""
    <section id="gallery" class="work-teaser section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Proof of work</p>
          <h2>Real Land Clearing &amp; Property Cleanup Jobs in Central Florida</h2>
          <p>Photos from actual outdoor property work — land clearing, brush cutting, pond bank clearing, ditch work, and debris removal across Polk County and nearby areas.</p>
        </div>
        <div class="work-teaser-grid work-teaser-grid--6">{thumbs}
        </div>
        <div style="text-align:center;margin-top:2rem">
          <a class="btn btn-ghost" href="gallery.html">See Full Project Gallery &rarr;</a>
        </div>
      </div>
    </section>"""


def equipment_trust_section() -> str:
    cards = [
        ("Kubota Excavator", "excavator-photo.webp", "Compact excavator support for digging, dirt removal, bank cleanup, and property access work."),
        ("Kubota Tractor", "tractor.webp", "Tractor and loader work for brush, soil, leveling, cleanup, and outdoor property maintenance."),
        ("Trailers & Haul-Off", "excavator-and-truck-photo.webp", "Dump and flatbed trailer support for debris, equipment transport, and job-site cleanup."),
        ("Brush & Grapple Work", "tractor-moving-item-with-grapple.webp", "Brush handling, piles, limbs, and cleanup support for overgrown property projects."),
    ]
    items = ""
    for i, (title, img, desc) in enumerate(cards):
        alt = next((alt for f, alt, _lbl in GALLERY if f == img), title)
        items += f"""
          <article class="equipment-card" data-fw-enter="bottom" style="--fw-enter-delay: {(i % 4) * 70}ms;">
            <img src="{mosaic_image_src(img)}" alt="{alt}" loading="lazy" width="640" height="480">
            <div>
              <h3>{title}</h3>
              <p>{desc}</p>
            </div>
          </article>"""
    return f"""
    <section class="equipment-trust section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Equipment-ready outdoor services</p>
          <h2>Owner-Operated Equipment for Polk County Property Work</h2>
          <p>Faith Works uses Kubota equipment, trailers, and brush-handling tools for land clearing, pond bank access, ditch cleanup, trails, fence lines, storm debris, and acreage projects. Exact scope is confirmed before scheduling.</p>
        </div>
        <div class="equipment-grid">{items}
        </div>
      </div>
    </section>"""


def home_services_hub_section() -> str:
    cards = ""
    for i, cat in enumerate(HOME_BUYER_CATEGORIES):
        links = "".join(
            f'<a href="{SERVICE_BY_SLUG[slug]["slug"]}.html">{SERVICE_BY_SLUG[slug]["nav"]}</a>'
            for slug in cat["links"]
            if slug in SERVICE_BY_SLUG
        )
        img_alt = next((alt for f, alt, _lbl in GALLERY if f == cat["image"]), cat["title"])
        cards += f"""
          <article class="home-services-hub-card home-services-hub-card--buyer" data-fw-enter="bottom" style="--fw-enter-delay: {(i % 3) * 60}ms;">
            <img class="home-services-hub-card__image" src="{mosaic_image_src(cat['image'])}" alt="{img_alt}" loading="lazy" width="640" height="420">
            <div class="home-services-hub-card__body">
              <h3>{cat['title']}</h3>
              <p>{cat['text']}</p>
              <div class="home-services-hub-links">{links}</div>
            </div>
          </article>"""
    return f"""
    <section id="all-services" class="home-services-hub section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Service categories</p>
          <h2>Choose the Outdoor Property Problem You Need Solved</h2>
          <p>The homepage focuses on the main buyer categories. The full services hub still covers every detailed service page for search, estimates, and scope clarity.</p>
        </div>
        <div class="home-services-hub-grid home-services-hub-grid--buyer">{cards}
        </div>
        <div style="text-align:center;margin-top:2.5rem">
          <a class="btn btn-ghost" href="services.html">Open full services hub &rarr;</a>
        </div>
      </div>
    </section>"""


def home_faq_section() -> str:
    return f"""
    <section id="faq" class="faq-section section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Common questions</p>
          <h2>Land Clearing &amp; Outdoor Property FAQs</h2>
          <p>Answers property owners in {SITE['city']}, Polk County, and Central Florida often ask before requesting an estimate.</p>
        </div>
        {faq_accordion(HOME_FAQS, "home")}
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


def page_url(path: str) -> str:
    path = path.removeprefix("/")
    if path in ("", "index.html"):
        return f"{SITE['url']}/"
    return f"{SITE['url']}/{path}"


def schema_asset_url(relative_path: str) -> str:
    return f"{SITE['url'].rstrip('/')}/{relative_path.lstrip('/')}"


def schema_dict(value: str | dict) -> dict:
    if isinstance(value, dict):
        data = value
    else:
        data = json.loads(value)
    return {k: v for k, v in data.items() if k != "@context"}


def schema_graph_block(*parts: str | dict) -> str:
    graph: list[dict] = []
    for part in parts:
        node = schema_dict(part)
        if "@graph" in node:
            graph.extend(node["@graph"])
        else:
            graph.append(node)
    payload = {"@context": "https://schema.org", "@graph": graph}
    return f'  <script type="application/ld+json">{json.dumps(payload, indent=2)}</script>'


def breadcrumb_node(items: list[tuple[str, str]], path: str) -> dict:
    return {
        "@type": "BreadcrumbList",
        "@id": f"{page_url(path)}#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "name": name,
                "item": page_url(item_path),
            }
            for i, (name, item_path) in enumerate(items, start=1)
        ],
    }


def faq_node(faqs: list[tuple[str, str]], path: str) -> dict:
    return {
        "@type": "FAQPage",
        "@id": f"{page_url(path)}#faq",
        "url": page_url(path),
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
            for question, answer in faqs
        ],
    }


def webpage_node(
    name: str,
    description: str,
    path: str,
    page_type: str | list[str] = "WebPage",
    about: dict | None = None,
    main_entity: dict | str | None = None,
    primary_image_id: str | None = None,
    include_breadcrumb: bool = True,
) -> dict:
    types = page_type if isinstance(page_type, list) else [page_type]
    node: dict = {
        "@type": types if len(types) > 1 else types[0],
        "@id": f"{page_url(path)}#webpage",
        "url": page_url(path),
        "name": name,
        "description": description,
        "isPartOf": {"@id": f"{SITE['url']}/#website"},
        "publisher": {"@id": f"{SITE['url']}/#business"},
        "inLanguage": "en-US",
    }
    if include_breadcrumb:
        node["breadcrumb"] = {"@id": f"{page_url(path)}#breadcrumb"}
    if about:
        node["about"] = about
    if main_entity:
        node["mainEntity"] = main_entity
    if primary_image_id:
        node["primaryImageOfPage"] = {"@id": primary_image_id}
    return node


def item_list_node(name: str, path: str, items: list[tuple[str, str]], list_id: str = "list") -> dict:
    return {
        "@type": "ItemList",
        "@id": f"{page_url(path)}#{list_id}",
        "name": name,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "name": label,
                "url": page_url(item_path),
            }
            for i, (label, item_path) in enumerate(items, start=1)
        ],
    }


def city_place_node(city: dict) -> dict:
    path = f"areas/{city['slug']}.html"
    return {
        "@type": "City",
        "@id": f"{page_url(path)}#place",
        "name": f"{city['name']}, FL",
        "containedInPlace": {
            "@type": "AdministrativeArea",
            "name": city["county"],
        },
    }


def county_place_node(county: dict) -> dict:
    path = f"areas/{county['slug']}.html"
    return {
        "@type": "AdministrativeArea",
        "@id": f"{page_url(path)}#place",
        "name": county["name"],
    }


def faq_page_schema(faqs: list[tuple[str, str]], path: str = "index.html") -> str:
    return json.dumps(faq_node(faqs, path), indent=2)


def breadcrumb_schema(items: list[tuple[str, str]], path: str = "index.html") -> str:
    return json.dumps(breadcrumb_node(items, path), indent=2)


def service_schema(s: dict) -> str:
    path = f"{s['slug']}.html"
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": f"{page_url(path)}#service",
        "name": s["name"],
        "serviceType": s["keyword"],
        "category": category_label(s["category"]),
        "description": s["desc"],
        "url": page_url(path),
        "mainEntityOfPage": {"@id": f"{page_url(path)}#webpage"},
        "image": schema_asset_url(f"Gallery/{s['mosaic_image']}"),
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
    action, method, enctype, mode_attr, provider = form_action_attrs(subj)
    upload_enabled = bool(formspree_endpoint())

    photo_upload = ""
    if upload_enabled:
        photo_upload = f"""
              <div class="form-group">
                <label for="{form_id}-photos">Upload Project Photos</label>
                <input type="file" id="{form_id}-photos" name="photos" accept="image/*" multiple>
                <p class="form-help">Wide photos, closeups, and access photos help Tyler quote faster.</p>
              </div>"""

    text_photos_select = f"""
              <div class="form-group">
                <label for="{form_id}-can-text">Can you text photos?</label>
                <select id="{form_id}-can-text" name="can_text_photos" required>
                  <option value="" disabled selected>Select one...</option>
                  <option>Yes - I can text photos</option>
                  <option>No - please call me first</option>
                  <option>I already included photos</option>
                </select>
              </div>"""

    common_fields = f"""
              <div class="form-group">
                <label for="{form_id}-location">City / Job Location</label>
                <input type="text" id="{form_id}-location" name="job_location" placeholder="Auburndale, Winter Haven, Lakeland..." required>
              </div>
              <div class="form-group">
                <label for="{form_id}-service">Service Needed</label>
                <select id="{form_id}-service" name="service" required>
                {service_options(selected)}
                </select>
              </div>
              {text_photos_select}
              <div class="form-group">
                <label for="{form_id}-best-time">Best Time to Contact</label>
                <input type="text" id="{form_id}-best-time" name="best_time" placeholder="Morning, afternoon, evening, or specific time">
              </div>
              <div class="form-group">
                <label for="{form_id}-access">Property Access Notes</label>
                <input type="text" id="{form_id}-access" name="access_notes" placeholder="Gate width, slopes, wet areas, utilities, pets, locks">
              </div>"""

    if compact:
        service_hidden = (
            f'<input type="hidden" name="service" value="{selected}">' if selected else ""
        )
        fields = f"""
              <div class="form-group">
                <label for="{form_id}-name">Your Name</label>
                <input type="text" id="{form_id}-name" name="name" placeholder="Your name" required autocomplete="name">
              </div>
              <div class="form-group">
                <label for="{form_id}-phone">Phone Number</label>
                <input type="tel" id="{form_id}-phone" name="phone" placeholder="{phone}" required autocomplete="tel">
              </div>
              {service_hidden}
              <div class="form-group">
                <label for="{form_id}-message">What do you need?</label>
                <textarea id="{form_id}-message" name="message" placeholder="City + quick description — e.g. brush clearing in Auburndale" rows="2"></textarea>
              </div>"""
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
              {common_fields}
              {photo_upload}
              <div class="form-group">
                <label for="{form_id}-message">Project Details</label>
                <textarea id="{form_id}-message" name="message" placeholder="Describe the property, size, timeline, equipment access, and what you need cleared or removed..." rows="4"></textarea>
              </div>"""

    photo_note = (
        "Upload photos here or text photos"
        if upload_enabled
        else "Text photos"
    )
    submit_label = "Get Free Estimate" if compact else "Send Estimate Request"
    footer_note = (
        f'Text photos to <a href="tel:{SITE["phone_tel"]}">{phone}</a> for the fastest quote.'
        if compact
        else f'{photo_note} to <a href="tel:{SITE["phone_tel"]}">{phone}</a> for the fastest estimate.'
    )
    provider_fields = (
        '<input type="hidden" name="_format" value="plain">'
        if provider == "formspree"
        else """
              <input type="hidden" name="_captcha" value="false">
              <input type="hidden" name="_template" value="table">"""
    )
    return f"""
            <form class="{form_class}" action="{action}" method="{method}" id="{form_id}" enctype="{enctype}"{mode_attr}>
              {page_field}
              {fields}
              <input type="hidden" name="_subject" value="{subj}">
              {provider_fields}
              <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
              <div class="form-footer">
                <button type="submit" class="btn btn-primary btn-full">{submit_label}</button>
                <p class="form-note">{footer_note}</p>
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


def footer_service_links(root_prefix: str) -> str:
    return "\n          ".join(
        f'<a href="{root_prefix}{s["slug"]}.html">{s["nav"]}</a>' for s in SERVICES
    )


def footer_service_area_summary(root_prefix: str) -> str:
    city_links = " &nbsp;&middot;&nbsp; ".join(
        f'<a href="{root_prefix}{city_href(c["slug"])}">{c["name"]}</a>'
        for c in FEATURED_CITIES
    )
    return f"""<p class="footer-area-intro">Based in <strong>{HOME_CITY}, FL</strong>, primarily serving Polk County and nearby Central Florida communities.</p>
            <p class="footer-area-counties">{city_links}</p>
            <p class="footer-area-hub"><a href="{root_prefix}service-areas.html">View launch service areas &rarr;</a></p>"""


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
    service_links = footer_service_links(root_prefix)
    area_summary = footer_service_area_summary(root_prefix)
    call_link = call_cta_link("fw-footer-call")
    return f"""  <footer class="site-footer fw-site-footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-left">
          <div class="footer-company">
            <div class="footer-logo">
              {logo_coin("fw-logo-coin--footer", 72, SITE['brand'], logo_src)}
              <div class="footer-brand-lockup">
                <h3>Faith Works</h3>
                <p>Outdoor Services LLC</p>
              </div>
            </div>
            <p>{SITE['city']}, FL &nbsp;&middot;&nbsp; Polk County &amp; nearby Central Florida</p>
            <p class="company-description">{SITE_POSITIONING}</p>
            <div class="footer-service-area">
              {area_summary}
            </div>
          </div>
        </div>

        <div class="footer-center">
          <h4>Our Services</h4>
          <div class="footer-quick-links">
            {service_links}
          </div>
        </div>

        <div class="footer-right">
          <h4>Connect With Us</h4>
          <div class="footer-contact">
            <div class="footer-contact__phone">
              {call_link}
            </div>
            <p>
              <span class="contact-icon">Email</span>
              <a href="mailto:{SITE['email']}" class="footer-email-link">{SITE['email']}</a>
            </p>
            <p class="footer-owner">{SITE['owner']}, Owner</p>
          </div>
          {social_block("footer")}
        </div>
      </div>
    </div>

    <div class="footer-legal">
      <nav aria-label="Legal and policy pages">
        <a href="{root_prefix}gallery.html">Gallery</a>
        <span aria-hidden="true">&middot;</span>
        <a href="{root_prefix}service-areas.html">Service Areas</a>
        <span aria-hidden="true">&middot;</span>
        <a href="{root_prefix}contact.html">Contact</a>
        <span aria-hidden="true">&middot;</span>
        <a href="{root_prefix}privacy-policy.html">Privacy Policy</a>
      </nav>
    </div>

    <div class="footer-bottom">
      <p>&copy; <span id="current-year"></span> {SITE['legal_name']}. All rights reserved. &nbsp;&middot;&nbsp; <a href="https://knightlogics.com" rel="noopener noreferrer">Site by Knight Logics</a></p>
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
    robots: str = "index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1",
) -> str:
    canonical_url = f"{SITE['url']}/" if canonical == "index.html" else f"{SITE['url']}/{canonical}"
    hero_preloads = ""
    if preload_hero:
        hero_preloads = f"""  <link rel="preload" as="image" href="{root_prefix}Gallery/{HERO_MOBILE_LCP}" fetchpriority="high" media="(max-width: 768px)">
  <link rel="preload" as="image" href="{root_prefix}Gallery/{HERO_DESKTOP}" fetchpriority="high" media="(min-width: 769px)">"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical_url}">
  <meta name="robots" content="{robots}">
  <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
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
  <meta property="og:image" content="{public_asset_url(f'Gallery/{HERO_DESKTOP}')}">
  <meta property="og:site_name" content="{SITE['brand']}">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{public_asset_url(f'Gallery/{HERO_DESKTOP}')}">
{extra_head}
{favicon_head(root_prefix)}
{fonts_head()}
{hero_preloads}
  <link rel="preload" href="{root_prefix}styles.css?v={ASSET_VERSION}" as="style">
  <link rel="preload" href="{root_prefix}script.js" as="script">
  <link rel="stylesheet" href="{root_prefix}styles.css?v={ASSET_VERSION}">
{analytics_head()}
  <script defer src="{root_prefix}script.js"></script>
</head>
<body>
{header(current, root_prefix)}
<main>
{body}
</main>
{footer(root_prefix)}
  <script>
    if ("serviceWorker" in navigator) {{
      window.addEventListener("load", function () {{
        navigator.serviceWorker.register("{root_prefix}sw.js").catch(function () {{}});
      }});
    }}
  </script>
</body>
</html>"""


def business_schema() -> str:
    services = [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"]}} for s in SERVICES]
    areas = [{"@type": "City", "name": f"{c['name']}, FL"} for c in AREA_CITIES]
    county_areas = [{"@type": "AdministrativeArea", "name": c["name"]} for c in COUNTIES]
    schema = {
        "@context": "https://schema.org",
        "@type": ["Organization", "HomeAndConstructionBusiness"],
        "@id": f"{SITE['url']}/#business",
        "name": SITE["brand"],
        "legalName": SITE["legal_name"],
        "alternateName": SITE["short"],
        "description": f"{SITE['brand']} - {SITE_POSITIONING} in {SITE['area']}.",
        "url": SITE["url"],
        "telephone": f"+1-{SITE['phone_tel'][:3]}-{SITE['phone_tel'][3:6]}-{SITE['phone_tel'][6:]}",
        "email": SITE["email"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": SITE["city"],
            "addressRegion": SITE["region"],
            "postalCode": HOME_ZIP,
            "addressCountry": "US",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": SITE["geo_lat"],
            "longitude": SITE["geo_lng"],
        },
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "telephone": f"+1-{SITE['phone_tel'][:3]}-{SITE['phone_tel'][3:6]}-{SITE['phone_tel'][6:]}",
                "contactType": "customer service",
                "email": SITE["email"],
                "areaServed": "US-FL",
                "availableLanguage": ["English"],
            }
        ],
        "founder": {
            "@type": "Person",
            "name": SITE["owner"],
        },
        "image": schema_asset_url(f"Gallery/{HERO_DESKTOP}"),
        "logo": schema_asset_url(LOGO),
        "priceRange": "$$",
        "openingHours": "Mo-Sa 07:00-18:00",
        "areaServed": county_areas + areas,
        "slogan": "Land clearing, pond bank clearing, ditch clearing, and outdoor property services in Polk County, FL.",
        "knowsAbout": [
            "land clearing",
            "forestry mulching",
            "pond bank clearing",
            "ditch clearing",
            "brush clearing",
            "tractor services",
            "storm debris cleanup",
        ],
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


def website_schema() -> str:
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{SITE['url']}/#website",
        "url": f"{SITE['url']}/",
        "name": SITE["brand"],
        "description": f"{SITE['brand']} - {SITE_POSITIONING} in {SITE['area']}.",
        "publisher": {"@id": f"{SITE['url']}/#business"},
        "inLanguage": "en-US",
    }, indent=2)


def image_object_schema(image: str, caption: str, page: str) -> str:
    image_url = schema_asset_url(f"Gallery/{image}")
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "ImageObject",
        "@id": f"{image_url}#image",
        "contentUrl": image_url,
        "url": image_url,
        "caption": caption,
        "representativeOfPage": page == "index.html",
        "mainEntityOfPage": {"@id": f"{page_url(page)}#webpage"},
        "creator": {"@id": f"{SITE['url']}/#business"},
    }, indent=2)


def gallery_image_graph_schema() -> str:
    return json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ImageObject",
                "@id": f"{schema_asset_url(f'Gallery/{img}')}#image",
                "contentUrl": schema_asset_url(f"Gallery/{img}"),
                "url": schema_asset_url(f"Gallery/{img}"),
                "caption": alt,
                "name": label,
                "creator": {"@id": f"{SITE['url']}/#business"},
            }
            for img, alt, label in GALLERY
        ],
    }, indent=2)


def hero_background_html(root_prefix: str = "") -> str:
    desktop = f"{root_prefix}Gallery/{HERO_DESKTOP}"
    mobile = f"{root_prefix}Gallery/{HERO_MOBILE_LCP}"
    return f"""      <div class="hero-bg" aria-hidden="true">
        <picture>
          <source media="(max-width: 768px)" srcset="{mobile}" type="image/webp">
          <img src="{desktop}" alt="" width="1920" height="1080" fetchpriority="high" decoding="async" class="hero-bg__img">
        </picture>
      </div>"""


def contact_background_html(root_prefix: str = "") -> str:
    banner = f"{root_prefix}{CONTACT_BANNER}"
    cutout = f"{root_prefix}{CONTACT_CUTOUT}"
    return f"""      <div class="contact-bg" aria-hidden="true">
        <img src="{banner}" alt="" width="1920" height="1080" loading="lazy" decoding="async" class="contact-bg__img">
      </div>
      <div class="contact-overlay" aria-hidden="true"></div>
      <div class="contact-cutout-wrap" aria-hidden="true">
        <img class="contact-cutout" src="{cutout}" alt="" width="693" height="791" loading="lazy" decoding="async" role="presentation">
      </div>"""


def write_index() -> None:
    phase1_cards = ""
    for i, s in enumerate(PHASE1_SERVICES):
        phase1_cards += service_mosaic_card(s, i * 70, featured=True)

    schema = schema_graph_block(
        business_schema(),
        website_schema(),
        image_object_schema(HERO_DESKTOP, "Faith Works Outdoor Services equipment in Polk County, Florida", "index.html"),
        webpage_node(
            f"{SITE['city']} Land Clearing & Outdoor Services | Faith Works",
            f"{SITE['brand']} provides land clearing, pond bank clearing, ditch clearing, brush cutting, debris removal, and tractor work in Polk County, FL.",
            "index.html",
            main_entity={"@id": f"{page_url('index.html')}#faq"},
            primary_image_id=f"{schema_asset_url(f'Gallery/{HERO_DESKTOP}')}#image",
        ),
        breadcrumb_node([("Home", "index.html")], "index.html"),
        faq_node(HOME_FAQS, "index.html"),
    )

    body = f"""
    <section class="hero">
      {hero_background_html()}
      <div class="hero-overlay" aria-hidden="true"></div>
      <div class="container hero-inner">
        <div class="hero-copy">
          <p class="eyebrow" data-fw-enter="left" data-fw-enter-immediate="true">{SITE_POSITIONING}</p>
          <h1 data-fw-enter="left" data-fw-enter-immediate="true" style="--fw-enter-delay: 80ms;">Land Clearing &amp; Outdoor Property Services in <span class="h1-accent">{SITE['city']}, FL</span></h1>
          <p class="hero-sub" data-fw-enter="left" data-fw-enter-immediate="true" style="--fw-enter-delay: 160ms;">
            {SITE['brand']} helps homeowners, landowners, and property managers with land clearing, forestry mulching, pond bank clearing, ditch clearing, trails, fence lines, debris removal, acreage cleanup, and tractor services across Polk County and nearby Central Florida communities.
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

    <section id="about" class="about-section section-shell">
      <div class="container about-grid">
        <div class="about-copy" data-fw-enter="left">
          <p class="eyebrow">About Faith Works</p>
          <h2>Owner-operated.<br>Equipment-ready.<br>Clear communication.</h2>
          <p>{SITE['owner']} runs {SITE['brand']} as a local {SITE['city']} business built on hard work, honest estimates, and faith-based service. When you reach out, you're talking directly to the person doing the work.</p>
          <p>From land clearing and pond bank work to ditch cleanup and debris haul-off, we focus on outdoor property services that help homeowners and property owners reclaim usable land with clear communication and practical equipment access.</p>
          <a class="btn btn-ghost" href="about.html">Learn more about us &rarr;</a>
        </div>
        <div class="about-card" data-fw-enter="right">
          <h3>What to expect</h3>
          <ul class="about-list">
            <li>Direct contact with Tyler — no call center</li>
            <li>Photo-based estimates for outdoor projects</li>
            <li>Equipment-ready for clearing and cleanup jobs</li>
            <li>Local {SITE['city']} business focused on Polk County and nearby communities</li>
            <li>Residential and property-owner friendly service</li>
            <li>Colossians 3:23 work ethic on every job</li>
          </ul>
          <a class="btn btn-primary" href="contact.html">Request an Estimate</a>
        </div>
      </div>
    </section>

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

    {reviews_section()}

    {equipment_trust_section()}

    {process_section()}

    {home_geo_section()}

    {gallery_teaser_section()}

    {scope_section()}

    {home_services_hub_section()}

    {home_faq_section()}

    <section id="contact" class="contact-section section-shell">
      {contact_background_html()}
      <div class="container contact-inner" data-fw-enter="top">
        <p class="eyebrow">Ready to get started?</p>
        <h2>Need land cleared, a ditch cleaned, or property debris removed?</h2>
        <p>Request an estimate from {SITE['brand']} today. Send photos for the fastest quote.</p>
        <a class="btn btn-primary btn-lg" href="contact.html">Request a Free Estimate</a>
      </div>
    </section>"""

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
    path = f"{s['slug']}.html"
    schema = schema_graph_block(
        business_schema(),
        service_schema(s),
        webpage_node(
            s["title"],
            s["desc"],
            path,
            main_entity={"@id": f"{page_url(path)}#service"},
        ),
        breadcrumb_node([("Home", "index.html"), ("Services", "services.html"), (s["name"], path)], path),
        faq_node(faqs, path),
    )

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
            <p class="card-note">Text photos to <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a> and describe your property for a faster quote.</p>
            {estimate_form(selected=s['form_label'], subject=f"{s['name']} estimate - {SITE['brand']}", page=f"{s['slug']}.html", compact=True)}
          </div>
        </aside>
      </div>
    </section>
    <section class="areas-strip">
      <div class="container">
        <p class="eyebrow">Where we work</p>
        <p>Serving <strong>{'</strong>, <strong>'.join(c["name"] for c in FEATURED_CITIES[:8])}</strong>, plus nearby communities when the scope fits. <a href="service-areas.html">See all service areas &rarr;</a></p>
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
    services_path = "services.html"
    services_title = "Outdoor Property Services in Polk County FL | Faith Works"
    services_desc = f"Full service list for {SITE['brand']} — {SITE_POSITIONING} in Polk County, FL."
    service_items = [(item["name"], f"{item['slug']}.html") for item in SERVICES]
    schema = schema_graph_block(
        business_schema(),
        website_schema(),
        webpage_node(
            services_title,
            services_desc,
            services_path,
            page_type=["WebPage", "CollectionPage"],
            main_entity={"@id": f"{page_url(services_path)}#services"},
        ),
        breadcrumb_node([("Home", "index.html"), ("Services", services_path)], services_path),
        item_list_node(f"{SITE['brand']} services", services_path, service_items, "services"),
    )

    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; Services</p>
        <h1>{SITE_POSITIONING}</h1>
        <p>Faith Works Outdoor Services in {SITE['city']} and {SITE['area']} - outdoor property clearing, mulching, cleanup, and maintenance with owner-operated equipment.</p>
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
            <img src="Gallery/{img}" alt="{alt}" loading="lazy" width="800" height="600">
            <figcaption>{label}</figcaption>
          </figure>"""
    gallery_path = "gallery.html"
    gallery_title = f"Outdoor Services Project Gallery | {SITE['brand']}"
    gallery_desc = f"View land clearing, brush cutting, tractor work, and outdoor property cleanup projects by {SITE['brand']} in Polk County, FL."
    schema = schema_graph_block(
        business_schema(),
        gallery_image_graph_schema(),
        webpage_node(
            gallery_title,
            gallery_desc,
            gallery_path,
            page_type=["WebPage", "CollectionPage"],
        ),
        breadcrumb_node([("Home", "index.html"), ("Gallery", gallery_path)], gallery_path),
    )
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; Gallery</p>
        <h1>Project Gallery</h1>
        <p>Real outdoor work from {SITE['brand']} - land clearing, brush cutting, pond bank work, tractor support, and property cleanup across Polk County and nearby Central Florida.</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Equipment and job photos</p>
          <h2>Real Faith Works Equipment on Real Outdoor Property Jobs</h2>
          <p>These images support service pages, local SEO, image search, and customer trust by showing the actual equipment used for clearing, cleanup, and tractor work.</p>
        </div>
        <div class="gallery-grid">{items}
        </div>
      </div>
    </section>"""
    html = page_shell(
        f"Outdoor Services Project Gallery | {SITE['brand']}",
        f"View land clearing, brush cutting, tractor work, and outdoor property cleanup projects by {SITE['brand']} in Polk County, FL.",
        "gallery.html",
        body,
        schema,
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
          <p>{SITE['brand']} focuses on the work people actually call for: pond banks, trails, brush, overgrowth, acreage cleanup, ditch clearing, and debris haul-off. We keep project scope clear, confirm equipment access early, and explain what cleanup outcome makes sense before scheduling.</p>
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
    about_path = "about.html"
    about_title = f"About {SITE['owner']} | {SITE['brand']}"
    about_desc = f"Meet {SITE['owner']}, owner of {SITE['brand']} — {SITE_POSITIONING} in Polk County, FL."
    schema = schema_graph_block(
        business_schema(),
        webpage_node(
            about_title,
            about_desc,
            about_path,
            page_type=["WebPage", "AboutPage"],
            about={"@id": f"{SITE['url']}/#business"},
        ),
        breadcrumb_node([("Home", "index.html"), ("About", about_path)], about_path),
    )
    html = page_shell(
        about_title,
        about_desc,
        about_path,
        body,
        schema,
        "about.html",
    )
    write_site_file(ROOT / "about.html", html)


def write_contact() -> None:
    contact_path = "contact.html"
    contact_title = f"Contact {SITE['brand']} | Free Outdoor Services Estimate"
    contact_desc = f"Request a free photo-based estimate for {SITE_POSITIONING.lower()} in Polk County, FL."
    schema = schema_graph_block(
        business_schema(),
        webpage_node(
            contact_title,
            contact_desc,
            contact_path,
            page_type=["WebPage", "ContactPage"],
        ),
        breadcrumb_node([("Home", "index.html"), ("Contact", contact_path)], contact_path),
    )
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; Contact</p>
        <h1>Request an Outdoor Property Services Estimate</h1>
        <p>Tell us the city or job location, whether you can text photos, your best contact time, and what you need cleared, mulched, or cleaned up. Tyler reviews the details and follows up directly.</p>
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
          <div class="contact-direct-card"><p class="eyebrow">Service Area</p><p>{SITE['city']}, FL<br>{SITE['area_detail']}</p></div>
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
    return "".join(f'<a href="{root_prefix}{s["slug"]}.html">{s["nav"]}</a>' for s in SERVICES)


def write_city_area_page(city: dict, areas_dir: Path) -> None:
    root_prefix = "../"
    canonical = f"areas/{city['slug']}.html"
    county = COUNTY_BY_NAME[city["county"]]
    county_href = f"{county['slug']}.html"
    name = city["name"]
    faqs = city_area_faqs(name, city["county"])
    faq_block = faq_accordion(faqs, city["slug"])
    desc = city_meta_description(name, city["county"])
    title = city_page_title(name)
    nearby_html = nearby_cities_html(city)
    service_groups = area_services_by_category(root_prefix, name)
    intent_cards = area_intent_cards(root_prefix, name, INTENT_ROUTES)
    all_service_links = area_service_links(root_prefix)
    schema = schema_graph_block(
        business_schema(),
        city_place_node(city),
        webpage_node(
            f"{name}, FL Outdoor Property Services | {SITE['brand']}",
            desc,
            canonical,
            about={"@id": f"{page_url(canonical)}#place"},
            main_entity={"@id": f"{page_url(canonical)}#faq"},
        ),
        breadcrumb_node(
            [
                ("Home", "index.html"),
                ("Service Areas", "service-areas.html"),
                (city["county"], f"areas/{county['slug']}.html"),
                (f"{name}, FL", canonical),
            ],
            canonical,
        ),
        faq_node(faqs, canonical),
    )
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="{root_prefix}index.html">Home</a> &rsaquo; <a href="{root_prefix}service-areas.html">Service Areas</a> &rsaquo; <a href="{county_href}">{city['county']}</a> &rsaquo; {name}</p>
        <h1>{title}</h1>
        <p>{desc}</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container sp-layout">
        <div class="sp-content area-rich-content" data-fw-enter="left">
          {city_intro_html(city)}
          {city_property_section(city)}
          {city_common_jobs_section(city)}
          <h2>Start With Your Project Type in {name}</h2>
          <p>Select the outdoor property problem that best matches your {name} site — each links to a full service page with scope details and estimate options.</p>
          {intent_cards}
          <h2>All Outdoor Services in {name}, FL</h2>
          <p>Faith Works offers {len(SERVICES)} outdoor property services in {name}. Browse by category or view the full <a href="{root_prefix}services.html">services overview</a>.</p>
          <div class="area-service-catalog">
            {service_groups}
          </div>
          <div class="area-card-links area-card-links--wrap">{all_service_links}</div>
          {city_process_section(name)}
          {city_scope_section()}
          <h2>Also Serving Nearby in {city['county']}</h2>
          <p>Faith Works serves {name} and neighboring {city['county']} communities within our {SERVICE_RADIUS_MILES}-mile radius from {HOME_CITY}:</p>
          <div class="area-card-links">{nearby_html}</div>
          <p>View the full <a href="{county_href}">{city['county']} service area page</a> or browse <a href="{root_prefix}service-areas.html">all {len(COUNTIES)} counties and {len(AREA_CITIES)} cities</a> we serve.</p>
          <h2>{name}, FL Outdoor Property FAQs</h2>
          <p>Common questions from {name} and {city['county']} property owners about land clearing, pond banks, ditches, and outdoor cleanup.</p>
          {faq_block}
        </div>
        <aside class="sp-sidebar" data-fw-enter="right">
          <div class="hero-card" aria-label="Get a free estimate">
            <p class="card-eyebrow">Free photo-based estimate</p>
            <h2 class="card-name">Request Service in {name}</h2>
            <p class="card-note">Upload photos of your property in {name}, FL for a faster quote. {SITE['owner']} reviews every request personally.</p>
            {estimate_form(selected=None, subject=f"{name} estimate - {SITE['brand']}", page=canonical, compact=True)}
          </div>
          <div class="area-sidebar-note">
            <p><strong>Based in {HOME_CITY}</strong> &nbsp;&middot;&nbsp; {SERVICE_RADIUS_MILES}-mile radius</p>
            <p><a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></p>
            <p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
          </div>
        </aside>
      </div>
    </section>
    <section class="areas-strip">
      <div class="container">
        <p class="eyebrow">Ready for a {name} estimate?</p>
        <p>Send photos of your overgrown lot, pond bank, ditch line, trails, or debris piles in <strong>{name}, FL</strong>. {SITE['owner']} will review scope and follow up with next steps. <a href="{root_prefix}contact.html">Contact Faith Works &rarr;</a></p>
      </div>
    </section>"""
    html = page_shell(
        f"{name}, FL Outdoor Property Services | {SITE['brand']}",
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
        city_desc = city_meta_description(city["name"], county["name"]).split(".")[0] + "."
        city_cards += f"""
          <article class="area-card area-card--rich" data-fw-enter="bottom" style="--fw-enter-delay: {(i % 6) * 60}ms;">
            <h3><a href="{city['slug']}.html">{city['name']}, FL</a></h3>
            <p>{city_desc}</p>
            <a class="area-card-cta" href="{city['slug']}.html">{city['name']} land clearing &amp; outdoor services &rarr;</a>
          </article>"""
    faqs = county_area_faqs(county["name"], cities)
    faq_block = faq_accordion(faqs, county["slug"])
    desc = county_meta_description(county["name"], len(cities))
    service_groups = area_services_by_category(root_prefix, county["name"])
    intent_cards = area_intent_cards(root_prefix, county["name"], INTENT_ROUTES)
    all_service_links = area_service_links(root_prefix)
    nearby_counties = nearby_counties_html(county["name"], root_prefix)
    city_items = [(f"{c['name']}, FL", f"areas/{c['slug']}.html") for c in cities]
    schema = schema_graph_block(
        business_schema(),
        county_place_node(county),
        webpage_node(
            f"{county['name']} Outdoor Property Services | {SITE['brand']}",
            desc,
            canonical,
            about={"@id": f"{page_url(canonical)}#place"},
            main_entity={"@id": f"{page_url(canonical)}#faq"},
        ),
        breadcrumb_node(
            [("Home", "index.html"), ("Service Areas", "service-areas.html"), (county["name"], canonical)],
            canonical,
        ),
        faq_node(faqs, canonical),
        item_list_node(f"Cities in {county['name']}", canonical, city_items, "cities"),
    )
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="{root_prefix}index.html">Home</a> &rsaquo; <a href="{root_prefix}service-areas.html">Service Areas</a> &rsaquo; {county['name']}</p>
        <h1>Outdoor Property Services in {county['name']}</h1>
        <p>{desc}</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container">
        <div class="sp-content area-rich-content" data-fw-enter="left">
          {county_intro_html(county, cities)}
          {county_property_section(county["name"])}
          <h2>Project Types Across {county['name']}</h2>
          <p>Property owners in {county['name']} often start with one of these outdoor property needs:</p>
          {intent_cards}
          <h2>All Services Available in {county['name']}</h2>
          <p>Every service below is available throughout {county['name']} within our {SERVICE_RADIUS_MILES}-mile radius from {HOME_CITY}.</p>
          <div class="area-service-catalog">
            {service_groups}
          </div>
          <div class="area-card-links area-card-links--wrap">{all_service_links}</div>
          <h2>{county['name']} Outdoor Property FAQs</h2>
          {faq_block}
        </div>
        <div class="section-heading" style="margin-top:2.5rem" data-fw-enter="left">
          <p class="eyebrow">{len(cities)} cities in {county['name']}</p>
          <h2>{county['name']} City Service Pages</h2>
          <p>Each city page includes localized FAQs, full service listings, and a photo-based estimate form for {county['name']} property owners.</p>
        </div>
        <div class="areas-grid">{city_cards}
        </div>
        <div class="area-county-footer" data-fw-enter="left">
          <h2>Nearby Counties</h2>
          <p>Faith Works also serves property owners in {nearby_counties}.</p>
          <p class="areas-note"><a href="{root_prefix}service-areas.html">&larr; All service areas</a> &nbsp;&middot;&nbsp; <a href="{root_prefix}contact.html">Request an estimate</a> &nbsp;&middot;&nbsp; <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></p>
        </div>
      </div>
    </section>
    <section class="areas-strip">
      <div class="container">
        <p class="eyebrow">{county['name']} estimates</p>
        <p>Land clearing, pond bank clearing, ditch clearing, brush cutting, and outdoor property cleanup across <strong>{county['name']}</strong>. Based in {HOME_CITY} — serving {len(cities)} communities. <a href="{root_prefix}contact.html">Get a free estimate &rarr;</a></p>
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

    areas_path = "service-areas.html"
    areas_title = f"Polk County Service Areas | {SITE['brand']}"
    areas_desc = f"{SITE['brand']} serves Auburndale, Winter Haven, Lakeland, Lake Alfred, Bartow, Haines City, Davenport, Lake Wales, Polk City, and Plant City, FL."
    area_items = [(county["name"], f"areas/{county['slug']}.html") for county in COUNTIES]
    area_items.extend((f"{city['name']}, FL", f"areas/{city['slug']}.html") for city in AREA_CITIES)
    schema = schema_graph_block(
        business_schema(),
        webpage_node(
            areas_title,
            areas_desc,
            areas_path,
            page_type=["WebPage", "CollectionPage"],
            main_entity={"@id": f"{page_url(areas_path)}#areas"},
        ),
        breadcrumb_node([("Home", "index.html"), ("Service Areas", areas_path)], areas_path),
        item_list_node("Faith Works service areas", areas_path, area_items, "areas"),
    )
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; Service Areas</p>
        <h1>Polk County &amp; Nearby Central Florida Service Areas</h1>
        <p>{SITE['area_detail']}</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container">
        <div class="section-heading" data-fw-enter="left">
          <p class="eyebrow">Counties we serve</p>
          <h2>Launch County Focus</h2>
          <p>For launch, the site focuses on realistic service areas tied to Auburndale, Polk County, and nearby Plant City work.</p>
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
        f"Polk County Service Areas | {SITE['brand']}",
        f"{SITE['brand']} serves Auburndale, Winter Haven, Lakeland, Lake Alfred, Bartow, Haines City, Davenport, Lake Wales, Polk City, and Plant City, FL.",
        "service-areas.html",
        body,
        schema,
        "service-areas.html",
    )
    write_site_file(ROOT / "service-areas.html", html)


def write_404() -> None:
    body = f"""
    <section class="sp-hero"><div class="container"><h1>Page Not Found</h1><p>The page may have moved as Faith Works narrowed the launch service-area strategy. Start with the main services hub or request an estimate.</p></div></section>
    <section class="section-shell"><div class="container contact-inner">
      <p class="eyebrow">Need outdoor property help?</p>
      <h2>Land clearing, pond bank clearing, ditch clearing, and property cleanup in Polk County</h2>
      <p>Use the services page to find the right fit or contact Tyler directly with your city, photos, and access notes.</p>
      <div class="hero-actions" style="justify-content:center">
        <a class="btn btn-primary" href="services.html">View Services</a>
        <a class="btn btn-ghost" href="contact.html">Request Estimate</a>
      </div>
    </div></section>"""
    write_site_file(
        ROOT / "404.html",
        page_shell("Page Not Found | Faith Works Outdoor Services", "Find Faith Works Outdoor Services pages for Polk County land clearing and outdoor property cleanup.", "404.html", body, robots="noindex, follow"),
    )


def write_privacy() -> None:
    body = f"""
    <section class="sp-hero"><div class="container"><h1>Privacy Policy</h1></div></section>
    <section class="section-shell"><div class="container sp-content">
      <p>{SITE['legal_name']} ("we") respects your privacy. Information submitted through our contact forms is processed by <strong>Formspree</strong> (formspree.io) and delivered to us by email. We use that information only to respond to your estimate request and provide our services.</p>
      <p>We do not sell personal information. Analytics tools may collect anonymous usage data to improve the website.</p>
      <p>Questions? Contact <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
    </div></section>"""
    privacy_path = "privacy-policy.html"
    privacy_title = "Privacy Policy"
    privacy_desc = f"Privacy policy for {SITE['brand']}."
    schema = schema_graph_block(
        business_schema(),
        webpage_node(privacy_title, privacy_desc, privacy_path),
        breadcrumb_node([("Home", "index.html"), ("Privacy Policy", privacy_path)], privacy_path),
    )
    write_site_file(
        ROOT / "privacy-policy.html",
        page_shell(privacy_title, privacy_desc, privacy_path, body, schema),
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
    write_site_file(ROOT / "robots.txt", f"User-agent: *\nAllow: /\nDisallow: /faithworksods-website/\nSitemap: {SITE['url']}/sitemap.xml\n")


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
    src = src.replace('url("Images/ScreenTeamBanner.webp")', f'url("Gallery/{HERO_DESKTOP}")')
    src = src.replace('url("Images/ScreenTeamBanner-mobile.webp")', f'url("Gallery/{HERO_MOBILE_LCP}")')
    src = src.replace('url("Images/service-hero-bg.jpg")', f'url("Gallery/{HERO_DESKTOP}")')
    src = src.replace(
        ".contact-section {\n  background: linear-gradient(135deg, #08152a 0%, #060f1c 100%);",
        ".contact-section {\n  position: relative;\n  overflow: hidden;\n  background: #0a0a0a;",
    )
    src = src.replace(
        ".hero {\n  position: relative;\n  min-height: 92vh;\n  display: flex;\n  align-items: center;\n  background:",
        ".hero {\n  position: relative;\n  min-height: 92vh;\n  display: block;\n  width: 100%;\n  max-width: none;\n  background:",
    )
    src = src.replace(
        ".hero-overlay {\n  position: absolute;\n  inset: -2px 0 0 0;",
        ".hero-overlay {\n  position: absolute;\n  inset: 0;",
    )
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
.process-section {
  border-top: 1px solid var(--border);
}
.process-section--parallax {
  position: relative;
  overflow: hidden;
  isolation: isolate;
  background: #0a0a0a;
}
.process-bg {
  position: absolute;
  left: 0;
  right: 0;
  top: -32%;
  height: 164%;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}
.process-bg__img {
  display: block;
  width: 100%;
  height: 100%;
  max-width: none;
  object-fit: cover;
  object-position: center 58%;
  transform: translate3d(0, var(--fw-band-shift, 0px), 0);
  will-change: transform;
}
.process-overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
  background: linear-gradient(
    135deg,
    rgba(10, 10, 10, 0.84) 0%,
    rgba(12, 18, 12, 0.76) 42%,
    rgba(16, 22, 16, 0.62) 100%
  );
}
.process-section--parallax .container {
  position: relative;
  z-index: 2;
}
.process-section--parallax .process-step {
  background: rgba(12, 14, 12, 0.78);
  border-color: rgba(201, 162, 39, 0.18);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
@media (prefers-reduced-motion: reduce) {
  .process-bg__img {
    transform: none !important;
  }
}
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
.scope-section {
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
  position: relative;
  overflow: hidden;
  isolation: isolate;
}
.header-actions .btn-header-estimate::after {
  content: "";
  position: absolute;
  inset: -50% -80%;
  z-index: 1;
  pointer-events: none;
  background: linear-gradient(
    105deg,
    transparent 38%,
    rgba(255, 232, 160, 0.2) 44%,
    rgba(255, 255, 255, 0.55) 50%,
    rgba(255, 232, 160, 0.2) 56%,
    transparent 62%
  );
  transform: translateX(-130%) skewX(-14deg);
  animation: fwGoldGlimmer 10s ease-in-out infinite;
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
  animation: fwPhoneGlow 10s ease-in-out infinite;
  will-change: color, text-shadow;
}
@keyframes fwPhoneGlow {
  0%, 72%, 100% {
    color: #fff;
    text-shadow: none;
  }
  76% {
    color: #f5e6a8;
    text-shadow:
      0 0 8px rgba(201, 162, 39, 0.85),
      0 0 16px rgba(201, 162, 39, 0.55);
  }
  80%, 84% {
    color: var(--accent);
    text-shadow:
      0 0 10px rgba(201, 162, 39, 1),
      0 0 22px rgba(201, 162, 39, 0.9),
      0 0 38px rgba(201, 162, 39, 0.6);
  }
  88% {
    color: #f5e6a8;
    text-shadow:
      0 0 6px rgba(201, 162, 39, 0.65),
      0 0 14px rgba(201, 162, 39, 0.35);
  }
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
  display: block;
  width: 100%;
  max-width: none;
  overflow: hidden;
  isolation: isolate;
  background: #0a0a0a;
  background-image: none;
  min-height: 92vh;
}
.hero-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  min-height: 100%;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}
.hero-bg picture {
  display: block;
  width: 100%;
  height: 100%;
  min-height: 100%;
}
.hero-bg__img {
  display: block;
  width: 100%;
  height: 100%;
  min-height: 100%;
  max-width: none;
  object-fit: cover;
  object-position: 65% center;
  transform: translate3d(0, var(--hero-shift, 0px), 0);
  will-change: transform;
}
.hero-overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
}
.hero-inner {
  position: relative;
  z-index: 2;
  align-items: center;
  gap: clamp(32px, 4vw, 56px);
  max-width: none;
  margin: 0 auto;
  padding-top: clamp(64px, 10vh, 100px);
  padding-bottom: clamp(72px, 10vh, 100px);
}
.hero .hero-card {
  background: rgba(10, 14, 12, 0.46);
  border: 1px solid rgba(255, 255, 255, 0.16);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 0 24px 54px rgba(0, 0, 0, 0.32);
}
.hero .hero-card .contact-form-hero .form-group input,
.hero .hero-card .contact-form-hero .form-group textarea {
  background: rgba(0, 0, 0, 0.34);
  border-color: rgba(255, 255, 255, 0.14);
}
.hero .hero-card .contact-form-hero .form-group input:focus,
.hero .hero-card .contact-form-hero .form-group textarea:focus {
  background: rgba(0, 0, 0, 0.46);
  border-color: rgba(201, 162, 39, 0.45);
}

@media (max-width: 1060px) {
  .hero-overlay {
    background: linear-gradient(
      180deg,
      rgba(4, 9, 20, 0.93) 0%,
      rgba(4, 9, 20, 0.84) 40%,
      rgba(4, 9, 20, 0.58) 100%
    ) !important;
  }
}

@media (min-width: 1061px) {
  .hero-inner {
    grid-template-columns: minmax(0, 1fr) minmax(360px, 440px);
    align-items: center;
  }
}

@media (max-width: 1060px) {
  .hero-inner {
    grid-template-columns: 1fr;
    max-width: min(960px, 100%);
    padding: clamp(48px, 8vw, 64px) 0 clamp(56px, 10vw, 80px);
  }
  .hero-copy {
    width: 100%;
    min-width: 0;
  }
  .hero-card {
    width: 100%;
    max-width: 100%;
  }
  .hero-sub {
    max-width: none;
    font-size: clamp(0.98rem, 2.8vw, 1.08rem);
    line-height: 1.65;
  }
  .hero-copy .eyebrow {
    display: inline-flex;
    white-space: normal;
    text-wrap: balance;
  }
}

@media (max-width: 720px) {
  .hero {
    min-height: auto;
    align-items: flex-start;
  }
  .hero-bg__img {
    object-position: top center;
  }
  .hero-inner {
    padding: 36px 0 48px;
    gap: 28px;
  }
  .hero-copy h1 {
    font-size: clamp(1.55rem, 6.8vw, 2.1rem);
    line-height: 1.12;
    text-wrap: balance;
  }
  .hero-copy .eyebrow {
    font-size: 0.58rem;
    letter-spacing: 0.07em;
    padding: 7px 12px;
    line-height: 1.4;
  }
  .hero-sub {
    margin-bottom: 24px;
  }
  .hero-actions {
    margin-bottom: 28px;
  }
  .trust-row {
    flex-wrap: wrap;
    gap: 14px 20px;
  }
  .trust-divider {
    display: none;
  }
  .trust-item {
    min-width: calc(50% - 10px);
  }
  .hero-card {
    padding: 24px 20px;
  }
}

@media (max-width: 460px) {
  .hero-inner {
    padding: 28px 0 40px;
  }
  .hero-copy h1 {
    font-size: clamp(1.42rem, 7.2vw, 1.85rem);
  }
  .trust-item {
    min-width: 100%;
  }
}

@media (min-width: 1061px) {
  .hero-copy {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .hero-card {
    display: flex;
    flex-direction: column;
    padding: 28px 24px;
    align-self: center;
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
    display: flex;
    flex-direction: column;
    gap: 10px;
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
}

/* Homepage contact CTA — fw-banner background */
.contact-section {
  position: relative;
  overflow: hidden;
  isolation: isolate;
  width: 100%;
  max-width: none;
}
.contact-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}
.contact-bg__img {
  display: block;
  width: 100%;
  height: 100%;
  min-height: 100%;
  max-width: none;
  object-fit: cover;
  object-position: center;
}
.contact-overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
  background: linear-gradient(
    90deg,
    rgba(10, 10, 10, 0.92) 0%,
    rgba(10, 10, 10, 0.78) 42%,
    rgba(10, 10, 10, 0.38) 68%,
    rgba(10, 10, 10, 0.12) 100%
  );
}
.contact-cutout-wrap {
  position: absolute;
  right: clamp(0px, 2vw, 28px);
  bottom: 0;
  z-index: 2;
  height: min(94%, 900px);
  width: min(40vw, 440px);
  pointer-events: none;
}
.contact-cutout {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: right bottom;
  opacity: 0;
  transform: translate3d(16%, 0, 0);
}
.contact-section.contact-ready .contact-cutout {
  animation: contactCutoutEnter 0.95s ease-out 0.35s forwards;
}
@keyframes contactCutoutEnter {
  from {
    opacity: 0;
    transform: translate3d(16%, 0, 0);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}
.contact-inner {
  position: relative;
  z-index: 3;
}
@media (max-width: 900px) {
  .contact-cutout-wrap {
    width: min(46vw, 320px);
    height: min(78%, 560px);
    right: clamp(0px, 1vw, 12px);
  }
}
@media (max-width: 640px) {
  .contact-cutout-wrap {
    width: min(52vw, 260px);
    height: min(70%, 420px);
    opacity: 0.92;
  }
  .contact-overlay {
    background: linear-gradient(
      90deg,
      rgba(10, 10, 10, 0.94) 0%,
      rgba(10, 10, 10, 0.82) 55%,
      rgba(10, 10, 10, 0.45) 100%
    );
  }
}
@media (prefers-reduced-motion: reduce) {
  .contact-cutout {
    opacity: 1 !important;
    transform: none !important;
    animation: none !important;
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
  position: relative;
  overflow: hidden;
  border-radius: 50%;
}
.fw-logo-coin--header .fw-logo-coin__scene::after {
  content: "";
  position: absolute;
  inset: -25%;
  z-index: 6;
  pointer-events: none;
  background: linear-gradient(
    105deg,
    transparent 38%,
    rgba(255, 232, 160, 0.12) 44%,
    rgba(201, 162, 39, 0.78) 50%,
    rgba(255, 232, 160, 0.12) 56%,
    transparent 62%
  );
  transform: translateX(-130%) skewX(-14deg);
  animation: fwGoldGlimmer 10s ease-in-out infinite;
}
@keyframes fwGoldGlimmer {
  0%, 72%, 100% {
    transform: translateX(-130%) skewX(-14deg);
    opacity: 0;
  }
  76% { opacity: 0.55; }
  80% {
    transform: translateX(0%) skewX(-14deg);
    opacity: 1;
  }
  84% {
    transform: translateX(130%) skewX(-14deg);
    opacity: 1;
  }
  88% { opacity: 0; }
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
  .fw-logo-coin--header .fw-logo-coin__scene::after,
  .header-actions .btn-header-estimate::after,
  .fw-header-call__number {
    animation: none;
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
  width: 95vw;
  max-width: 95vw;
  margin: 2rem auto 0;
}
.services-mosaic {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0;
  width: 100%;
  margin: 0 auto;
}
@media (min-width: 540px) {
  .services-mosaic--phase1 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
@media (min-width: 1024px) {
  .services-mosaic--phase1 {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}
@media (min-width: 900px) {
  .services-mosaic:not(.services-mosaic--phase1) {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
@media (max-width: 539px) {
  .services-mosaic--phase1 .fw-service-card {
    min-height: 220px;
    aspect-ratio: 16 / 11;
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

/* ---- Reviews showcase (Knight Logics-style carousel) ---- */
.reviews-section {
  background: linear-gradient(180deg, #101510 0%, #0a0a0a 100%);
  border-top: 1px solid var(--border);
}
.fw-reviews-showcase {
  background: var(--bg-card);
  border: 1px solid rgba(201, 162, 39, 0.22);
  border-radius: var(--radius-lg);
  padding: clamp(22px, 3vw, 32px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
}
.fw-reviews-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px 14px;
  margin-bottom: 22px;
  padding-bottom: 18px;
  border-bottom: 1px solid rgba(201, 162, 39, 0.18);
}
.fw-google-g-logo {
  width: 28px;
  height: 28px;
  flex-shrink: 0;
}
.fw-reviews-header__label {
  font-weight: 700;
  color: #fff;
  font-size: 0.95rem;
}
.fw-review-stars {
  color: var(--accent);
  letter-spacing: 0.08em;
  font-size: 0.95rem;
}
.fw-review-stars--header {
  font-size: 1rem;
}
.fw-reviews-summary {
  width: 100%;
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--muted);
}
.fw-review-carousel {
  display: flex;
  align-items: center;
  gap: 12px;
}
.fw-review-viewport {
  overflow: hidden;
  flex: 1;
  min-width: 0;
}
.fw-review-track {
  display: flex;
  gap: 18px;
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
.fw-review-card {
  position: relative;
  min-width: calc(33.333% - 12px);
  max-width: calc(33.333% - 12px);
  background: rgba(8, 18, 34, 0.72);
  border: 1px solid rgba(201, 162, 39, 0.16);
  border-radius: var(--radius-md);
  padding: 22px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.28);
}
.fw-review-placeholder-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 8px;
  border-radius: 999px;
  background: rgba(201, 162, 39, 0.14);
  border: 1px solid rgba(201, 162, 39, 0.28);
  color: var(--accent);
  font-size: 0.62rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.fw-review-header {
  display: flex;
  gap: 12px;
  align-items: center;
  padding-right: 72px;
}
.fw-review-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 800;
  flex-shrink: 0;
}
.fw-review-name {
  margin: 0;
  font-family: var(--font-head);
  font-size: 1rem;
  color: #fff;
}
.fw-review-sub {
  color: var(--muted);
  font-size: 0.84rem;
}
.fw-review-text {
  color: rgba(245, 240, 232, 0.88);
  line-height: 1.72;
  font-size: 0.94rem;
  flex: 1;
  margin: 0;
}
.fw-review-date {
  color: var(--muted);
  font-size: 0.82rem;
  font-weight: 700;
}
.fw-review-btn {
  width: 44px;
  height: 44px;
  border: 0;
  border-radius: 50%;
  background: var(--accent);
  color: #0a0a0a;
  font-size: 1.45rem;
  line-height: 1;
  cursor: pointer;
  flex-shrink: 0;
  transition: transform 0.2s ease, filter 0.2s ease;
}
.fw-review-btn:hover:not(:disabled) {
  filter: brightness(1.08);
  transform: translateY(-1px);
}
.fw-review-btn:disabled {
  opacity: 0.38;
  cursor: not-allowed;
}
.fw-review-dots {
  display: flex;
  justify-content: center;
  gap: 0;
  margin-top: 14px;
}
.fw-review-dot {
  width: 44px;
  height: 44px;
  border: 0;
  border-radius: 50%;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.fw-review-dot::after {
  content: "";
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(201, 162, 39, 0.24);
  transition: transform 0.2s ease, background 0.2s ease;
}
.fw-review-dot.is-active::after {
  background: var(--accent);
  transform: scale(1.12);
}
.fw-reviews-footnote {
  margin: 18px 0 0;
  text-align: center;
  color: var(--muted);
  font-size: 0.84rem;
  line-height: 1.6;
}
@media (max-width: 1060px) {
  .fw-review-card {
    min-width: calc(50% - 9px);
    max-width: calc(50% - 9px);
  }
}
@media (max-width: 720px) {
  .fw-review-carousel {
    gap: 8px;
  }
  .fw-review-card {
    min-width: 100%;
    max-width: 100%;
  }
  .fw-review-btn {
    width: 38px;
    height: 38px;
    font-size: 1.25rem;
  }
  .fw-review-header {
    padding-right: 0;
  }
}

/* ---- Homepage GEO strip + services hub (SEO/AEO) ---- */
.home-geo-strip {
  padding: 44px 0;
  background: linear-gradient(90deg, #0a0a0a 0%, #101510 50%, #0a0a0a 100%);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}
.home-geo-strip__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: clamp(20px, 4vw, 40px);
}
.home-geo-strip__copy {
  flex: 1 1 520px;
  min-width: 0;
}
.home-geo-strip__eyebrow {
  margin: 0 0 8px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent);
}
.home-geo-strip__text {
  margin: 0;
  color: var(--muted);
  font-size: 0.96rem;
  line-height: 1.65;
  max-width: 62ch;
}
.home-geo-strip__actions {
  display: flex;
  flex-shrink: 0;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: flex-end;
}
.home-geo-strip__cta {
  white-space: nowrap;
}
@media (max-width: 860px) {
  .home-geo-strip {
    padding: 36px 0;
  }
  .home-geo-strip__inner {
    flex-direction: column;
    align-items: flex-start;
  }
  .home-geo-strip__actions {
    width: 100%;
    justify-content: flex-start;
  }
}
.home-services-hub {
  border-top: 1px solid var(--border);
}
.home-services-hub-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}
.home-services-hub-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 22px 20px;
}
.home-services-hub-card h3 {
  font-family: var(--font-head);
  color: #fff;
  font-size: 1.05rem;
  margin-bottom: 8px;
}
.home-services-hub-card p {
  color: var(--muted);
  font-size: 0.9rem;
  line-height: 1.6;
  margin-bottom: 14px;
}
.home-services-hub-links {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.home-services-hub-links a {
  color: var(--accent);
  font-size: 0.86rem;
  font-weight: 650;
  text-decoration: none;
}
.home-services-hub-links a:hover {
  text-decoration: underline;
}
.work-teaser-grid--6 {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}
@media (max-width: 900px) {
  .home-services-hub-grid,
  .work-teaser-grid--6 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
@media (max-width: 560px) {
  .home-services-hub-grid,
  .work-teaser-grid--6 {
    grid-template-columns: 1fr;
  }
}

/* ---- Knight Logics-style footer ---- */
footer.fw-site-footer {
  --fw-footer-link: var(--accent);
  --fw-footer-link-hover: #fff;
  background:
    radial-gradient(circle at 12% 0, rgba(201, 162, 39, 0.14), transparent 28%),
    radial-gradient(circle at 88% 12%, rgba(138, 109, 18, 0.1), transparent 24%),
    linear-gradient(180deg, #101510 0%, #0a0a0a 100%);
  color: #fff;
  padding: clamp(56px, 7vw, 80px) 0 0;
  margin-top: 0;
  position: relative;
  border-top: 1px solid rgba(201, 162, 39, 0.16);
  box-shadow: 0 -12px 40px rgba(0, 0, 0, 0.18);
}
footer.fw-site-footer::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(201, 162, 39, 0.32), transparent);
}
footer.fw-site-footer .footer-content {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr) minmax(0, 1.1fr);
  gap: clamp(32px, 5vw, 56px);
  margin-bottom: clamp(32px, 4vw, 48px);
}
footer.fw-site-footer .footer-company {
  text-align: left;
}
footer.fw-site-footer .footer-logo {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 20px;
}
footer.fw-site-footer .footer-logo .fw-logo-coin--footer {
  flex-shrink: 0;
  opacity: 0.95;
}
footer.fw-site-footer .footer-brand-lockup h3 {
  color: #fff;
  font-size: 1.55rem;
  font-family: var(--font-head);
  font-weight: 700;
  margin: 0;
  line-height: 1.1;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
footer.fw-site-footer .footer-brand-lockup p {
  margin: 4px 0 0;
  color: rgba(245, 240, 232, 0.82);
  font-size: 0.92rem;
  font-weight: 600;
  line-height: 1.3;
}
footer.fw-site-footer .footer-company > p {
  color: rgba(255, 255, 255, 0.78);
  font-size: 0.95rem;
  line-height: 1.65;
  margin: 8px 0;
}
footer.fw-site-footer .company-description {
  font-style: italic;
  margin-top: 14px;
  padding-left: 16px;
  border-left: 2px solid rgba(201, 162, 39, 0.55);
  color: rgba(255, 255, 255, 0.72);
}
footer.fw-site-footer .footer-service-area {
  margin-top: 14px;
}
footer.fw-site-footer .footer-area-intro {
  font-size: 0.9rem;
  line-height: 1.65;
  color: rgba(255, 255, 255, 0.78);
  margin: 0 0 10px;
}
footer.fw-site-footer .footer-area-intro strong {
  color: rgba(245, 240, 232, 0.95);
  font-weight: 700;
}
footer.fw-site-footer .footer-area-counties {
  font-size: 0.8rem;
  line-height: 1.75;
  margin: 0 0 10px;
  color: rgba(255, 255, 255, 0.62);
}
footer.fw-site-footer .footer-area-counties a {
  color: var(--fw-footer-link);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}
footer.fw-site-footer .footer-area-counties a:hover,
footer.fw-site-footer .footer-area-counties a:focus-visible {
  color: var(--fw-footer-link-hover);
  outline: none;
}
footer.fw-site-footer .footer-area-hub {
  margin: 0;
  font-size: 0.86rem;
}
footer.fw-site-footer .footer-area-hub a {
  color: var(--fw-footer-link);
  font-weight: 700;
  text-decoration: none;
  transition: color 0.2s ease;
}
footer.fw-site-footer .footer-area-hub a:hover,
footer.fw-site-footer .footer-area-hub a:focus-visible {
  color: var(--fw-footer-link-hover);
  text-decoration: underline;
  outline: none;
}
footer.fw-site-footer .footer-center h4,
footer.fw-site-footer .footer-right h4 {
  color: #fff;
  font-size: 1.15rem;
  margin: 0 0 18px;
  font-family: var(--font-head);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  position: relative;
}
footer.fw-site-footer .footer-center h4::after,
footer.fw-site-footer .footer-right h4::after {
  content: "";
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 36px;
  height: 2px;
  background: rgba(201, 162, 39, 0.75);
}
footer.fw-site-footer .footer-quick-links {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px 14px;
  margin-top: 8px;
}
footer.fw-site-footer .footer-quick-links a {
  color: var(--fw-footer-link);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.94rem;
  padding: 8px 0;
  min-height: 40px;
  display: flex;
  align-items: center;
  transition: color 0.2s ease, transform 0.2s ease;
}
footer.fw-site-footer .footer-quick-links a:hover,
footer.fw-site-footer .footer-quick-links a:focus-visible {
  color: var(--fw-footer-link-hover);
  transform: translateX(4px);
  outline: none;
}
footer.fw-site-footer .footer-contact {
  margin-bottom: 22px;
}
footer.fw-site-footer .footer-contact__phone {
  margin: 8px 0 16px;
}
footer.fw-site-footer .footer-contact p {
  color: rgba(255, 255, 255, 0.86);
  margin: 0 0 10px;
  font-size: 0.95rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
footer.fw-site-footer .footer-contact .contact-icon {
  flex: 0 0 auto;
  min-width: 48px;
  font-size: 0.875rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--fw-footer-link);
}
footer.fw-site-footer .footer-email-link {
  color: var(--fw-footer-link);
  font-weight: 700;
  text-decoration: none;
  word-break: break-word;
  transition: color 0.2s ease;
}
footer.fw-site-footer .footer-email-link:hover,
footer.fw-site-footer .footer-email-link:focus-visible {
  color: var(--fw-footer-link-hover);
  text-decoration: underline;
  outline: none;
}
footer.fw-site-footer .footer-owner {
  font-size: 0.86rem !important;
  color: rgba(255, 255, 255, 0.62) !important;
}
footer.fw-site-footer .footer-social {
  margin-top: 4px;
}
footer.fw-site-footer .footer-social .social-icons {
  gap: 10px;
}
footer.fw-site-footer .footer-social .social-icon {
  width: 46px;
  height: 46px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(201, 162, 39, 0.16);
}
footer.fw-site-footer .footer-social .social-icon:hover {
  background: rgba(201, 162, 39, 0.22);
  border-color: rgba(201, 162, 39, 0.32);
}
footer.fw-site-footer .footer-legal {
  width: 100%;
  padding: 16px 20px;
  border-top: 1px solid rgba(201, 162, 39, 0.12);
  background: rgba(0, 0, 0, 0.14);
}
footer.fw-site-footer .footer-legal nav {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 8px 10px;
  max-width: var(--container);
  margin: 0 auto;
}
footer.fw-site-footer .footer-legal a {
  color: var(--fw-footer-link);
  text-decoration: none;
  font-size: 0.9375rem;
  font-weight: 600;
  padding: 6px 4px;
  white-space: nowrap;
  transition: color 0.2s ease;
}
footer.fw-site-footer .footer-legal a:hover,
footer.fw-site-footer .footer-legal a:focus-visible {
  color: var(--fw-footer-link-hover);
  outline: none;
}
footer.fw-site-footer .footer-legal span[aria-hidden="true"] {
  color: rgba(255, 255, 255, 0.28);
  font-size: 0.875rem;
  user-select: none;
}
footer.fw-site-footer .footer-bottom {
  width: 100%;
  text-align: center;
  padding: 18px 20px 22px;
  border-top: 1px solid rgba(201, 162, 39, 0.1);
  color: rgba(255, 255, 255, 0.68);
  font-size: 0.9rem;
  background: rgba(0, 0, 0, 0.2);
}
footer.fw-site-footer .footer-bottom p {
  margin: 0;
}
footer.fw-site-footer .footer-bottom a {
  color: inherit;
  text-decoration: none;
  opacity: 0.85;
}
footer.fw-site-footer .footer-bottom a:hover,
footer.fw-site-footer .footer-bottom a:focus-visible {
  opacity: 1;
  text-decoration: underline;
}
footer.fw-site-footer .footer-disclaimer {
  max-width: 820px;
  margin: 12px auto 0 !important;
  font-size: 0.72rem !important;
  line-height: 1.55;
  color: rgba(255, 255, 255, 0.48) !important;
  opacity: 1 !important;
}
@media (min-width: 767px) and (max-width: 997px) {
  footer.fw-site-footer .footer-content {
    grid-template-columns: 1fr 1fr;
    text-align: center;
  }
  footer.fw-site-footer .footer-left {
    grid-column: 1 / -1;
  }
  footer.fw-site-footer .footer-logo,
  footer.fw-site-footer .footer-company {
    text-align: center;
    justify-content: center;
  }
  footer.fw-site-footer .footer-logo {
    justify-content: center;
  }
  footer.fw-site-footer .footer-center h4::after,
  footer.fw-site-footer .footer-right h4::after {
    left: 50%;
    transform: translateX(-50%);
  }
  footer.fw-site-footer .footer-contact p {
    justify-content: center;
  }
  footer.fw-site-footer .footer-contact__phone {
    display: flex;
    justify-content: center;
  }
  footer.fw-site-footer .footer-social .social-icons {
    justify-content: center;
  }
}
@media (max-width: 768px) {
  footer.fw-site-footer {
    padding-top: 52px;
  }
  footer.fw-site-footer .footer-content {
    grid-template-columns: 1fr;
    gap: 36px;
    text-align: center;
  }
  footer.fw-site-footer .footer-company,
  footer.fw-site-footer .footer-logo {
    text-align: center;
    justify-content: center;
  }
  footer.fw-site-footer .company-description {
    border-left: none;
    border-top: 2px solid rgba(201, 162, 39, 0.45);
    padding-left: 0;
    padding-top: 14px;
  }
  footer.fw-site-footer .footer-quick-links {
    grid-template-columns: 1fr;
    max-width: 280px;
    margin-left: auto;
    margin-right: auto;
  }
  footer.fw-site-footer .footer-quick-links a {
    justify-content: center;
  }
  footer.fw-site-footer .footer-center h4::after,
  footer.fw-site-footer .footer-right h4::after {
    left: 50%;
    transform: translateX(-50%);
  }
  footer.fw-site-footer .footer-contact p {
    justify-content: center;
  }
  footer.fw-site-footer .footer-contact__phone {
    display: flex;
    justify-content: center;
  }
  footer.fw-site-footer .footer-social .social-icons {
    justify-content: center;
  }
}

/* ---- Rich service area pages (SEO / AEO / GEO) ---- */
.area-rich-content h2 {
  margin-top: 2.25rem;
  margin-bottom: 0.85rem;
}
.area-rich-content h2:first-child {
  margin-top: 0;
}
.area-rich-content h3 {
  font-family: var(--font-head);
  font-size: 1rem;
  color: #fff;
  margin: 1.5rem 0 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.area-rich-content p,
.area-rich-content li {
  color: var(--muted);
  font-size: 0.96rem;
  line-height: 1.72;
}
.area-rich-content ul {
  margin: 0.75rem 0 1rem;
  padding-left: 1.2rem;
}
.area-rich-content a {
  color: var(--accent);
}
.area-service-catalog {
  display: grid;
  gap: 1.25rem;
  margin: 1.25rem 0 1.5rem;
}
.area-service-group {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1.1rem 1.15rem 1rem;
}
.area-service-group p {
  margin-bottom: 0.65rem;
  font-size: 0.9rem;
}
.area-service-list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.area-service-list li {
  padding: 0.45rem 0;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  font-size: 0.88rem;
  line-height: 1.55;
}
.area-service-list li:first-child {
  border-top: none;
}
.area-service-list a {
  font-weight: 700;
  text-decoration: none;
}
.area-service-list a:hover {
  text-decoration: underline;
}
.area-intent-grid {
  margin: 1rem 0 1.5rem;
}
.area-process-grid {
  margin: 1rem 0 1.5rem;
}
.area-card-links--wrap {
  margin: 0.5rem 0 1.5rem;
}
.area-sidebar-note {
  margin-top: 1rem;
  padding: 1rem 1.1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  background: rgba(201, 162, 39, 0.05);
}
.area-sidebar-note p {
  margin: 0 0 0.45rem;
  font-size: 0.86rem;
  color: var(--muted);
}
.area-sidebar-note p:last-child {
  margin-bottom: 0;
}
.area-sidebar-note a {
  color: var(--accent);
  font-weight: 700;
  text-decoration: none;
}
.area-card--rich p {
  font-size: 0.88rem;
  line-height: 1.6;
  min-height: 3.2em;
}
.area-county-footer {
  margin-top: 2.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
}
.area-county-footer h2 {
  font-family: var(--font-head);
  font-size: 1.15rem;
  color: #fff;
  margin-bottom: 0.65rem;
}
.area-county-footer p {
  color: var(--muted);
  line-height: 1.65;
}
@media (max-width: 900px) {
  .area-process-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 560px) {
  .area-process-grid {
    grid-template-columns: 1fr;
  }
}


.reviews-section--soon {
  background: linear-gradient(180deg, #101510 0%, #0a0a0a 100%);
}
.reviews-coming-soon {
  max-width: 820px;
  margin: 0 auto;
  padding: clamp(28px, 5vw, 48px);
  border: 1px solid rgba(201, 162, 39, 0.22);
  border-radius: var(--radius-md);
  background: rgba(201, 162, 39, 0.06);
  text-align: center;
}
.reviews-coming-soon h2 {
  font-family: var(--font-head);
  color: #fff;
  font-size: clamp(1.45rem, 3vw, 2.3rem);
  margin-bottom: 12px;
}
.reviews-coming-soon p {
  max-width: 64ch;
  margin: 0 auto 22px;
  color: var(--muted);
  line-height: 1.7;
}
.equipment-trust {
  background: linear-gradient(180deg, #0a0a0a 0%, #101510 100%);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}
.equipment-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}
.equipment-card {
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  background: var(--bg-card);
}
.equipment-card img,
.home-services-hub-card__image {
  display: block;
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
}
.equipment-card div,
.home-services-hub-card__body {
  padding: 18px 16px;
}
.equipment-card h3 {
  margin-bottom: 8px;
  color: #fff;
  font-family: var(--font-head);
  font-size: 1rem;
}
.equipment-card p {
  color: var(--muted);
  font-size: 0.9rem;
  line-height: 1.6;
}
.home-services-hub-grid--buyer {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 16px;
}
.home-services-hub-card--buyer {
  overflow: hidden;
  padding: 0;
}
.form-help {
  margin-top: 6px;
  font-size: 0.76rem;
  color: var(--muted);
  line-height: 1.35;
}
@media (max-width: 1180px) {
  .home-services-hub-grid--buyer,
  .equipment-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
@media (max-width: 640px) {
  .home-services-hub-grid--buyer,
  .equipment-grid {
    grid-template-columns: 1fr;
  }
}

"""
    write_site_file(ROOT / "styles.css", minify_css(src + extra))


def write_sw() -> None:
    sw = f"""/* Faith Works static asset cache v{ASSET_VERSION} */
"use strict";
const CACHE = "fw-static-{ASSET_VERSION}";

self.addEventListener("install", (event) => {{
  self.skipWaiting();
}});

self.addEventListener("activate", (event) => {{
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))
    ).then(() => self.clients.claim())
  );
}});

self.addEventListener("fetch", (event) => {{
  const {{ request }} = event;
  if (request.method !== "GET") return;
  let url;
  try {{
    url = new URL(request.url);
  }} catch {{
    return;
  }}
  if (url.origin !== self.location.origin) return;
  if (!/\\.(webp|png|jpe?g|css|js|woff2?)$/i.test(url.pathname)) return;

  event.respondWith(
    caches.open(CACHE).then(async (cache) => {{
      const cached = await cache.match(request);
      const network = fetch(request).then((response) => {{
        if (response && response.ok) {{
          cache.put(request, response.clone());
        }}
        return response;
      }});
      return cached || network;
    }})
  );
}});
"""
    write_site_file(ROOT / "sw.js", sw)


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
  const bg = hero && hero.querySelector(".hero-bg__img, .hero-bg img");
  if (!hero || !bg) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  let restTop = 0;
  let headerHeight = 0;
  let ticking = false;
  const rate = 0.45;

  function measureHeader() {
    const header = document.querySelector(".site-header");
    headerHeight = header ? header.offsetHeight : 0;
  }

  function update() {
    ticking = false;
    const rect = hero.getBoundingClientRect();
    if (window.scrollY < 2) {
      restTop = headerHeight || rect.top;
    }
    const shift = -(rect.top - restTop) * rate;
    bg.style.setProperty("--hero-shift", Math.round(shift) + "px");
  }

  function queue() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  function init() {
    measureHeader();
    requestAnimationFrame(queue);
  }

  window.addEventListener("load", init, { once: true });
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", () => {
    measureHeader();
    queue();
  }, { passive: true });
})();

(function initProcessParallax() {
  const section = document.querySelector(".process-section--parallax");
  const bgImg = section && section.querySelector(".process-bg__img");
  if (!section || !bgImg) return;
  if (prefersReducedMotion()) return;

  let ticking = false;
  let maxShift = 0;
  const rate = Number(section.dataset.parallaxRate) || 0.78;
  const overscanRatio = Number(section.dataset.parallaxOverscan) || 0.38;

  function measureSection() {
    maxShift = section.offsetHeight * overscanRatio;
  }

  function clampShift(shift, limit) {
    return Math.round(Math.max(-limit, Math.min(limit, shift)));
  }

  function update() {
    ticking = false;
    const rect = section.getBoundingClientRect();
    const anchor = window.innerHeight * 0.5;
    const shift = -(rect.top - anchor) * rate;
    bgImg.style.setProperty("--fw-band-shift", clampShift(shift, maxShift) + "px");
  }

  function queue() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  function init() {
    measureSection();
    requestAnimationFrame(queue);
  }

  window.addEventListener("load", init, { once: true });
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", () => {
    measureSection();
    queue();
  }, { passive: true });
})();
"""
    if "initHeroParallax" in text:
        text = re.sub(
            r"// ---- Hero parallax ----[\s\S]*?\}\)\(\);\s*(?=\(function initProcessParallax|\Z)",
            parallax_block.strip() + "\n",
            text,
            count=1,
        )
    else:
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
            "404.html",
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
    from optimize_images import main as optimize_images

    optimize_images()
    sync_logo()
    write_styles()
    write_sw()
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
    write_404()
    write_sitemap()
    write_robots()
    write_cname()
    cleanup_obsolete_pages()
    from verify_schema import main as verify_schema

    if verify_schema() != 0:
        raise SystemExit("Schema verification failed after build.")
    print(f"Built Faith Works website in {ROOT} ({SERVICE_COUNT} services)")


if __name__ == "__main__":
    main()
