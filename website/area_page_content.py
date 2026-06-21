"""SEO / AEO / GEO content generators for city and county service area pages."""

from __future__ import annotations

from city_area_profiles import city_profile
from service_areas_data import (
    COUNTIES,
    COUNTY_BY_NAME,
    HOME_CITY,
    HOME_ZIP,
    SERVICE_RADIUS_MILES,
    cities_in_county,
)
from services_data import (
    NOT_OFFERED,
    NOT_OFFERED_NOTE,
    SERVICE_CATEGORIES,
    SERVICES,
    SITE_EMAIL,
    SITE_POSITIONING,
    services_for_category,
)

BRAND = "Faith Works Outdoor Services"
OWNER = "Tyler R. Edwards"

COUNTY_PROFILES: dict[str, dict] = {
    "Polk County": {
        "region": "Central Florida's lake country",
        "terrain": "flat to gently rolling land with lakes, ponds, citrus groves, pasture, and mixed residential acreage",
        "property_types": [
            "Residential lots with overgrown back acreage",
            "Lakefront and pond-adjacent homes",
            "Rural homesteads and small farms",
            "Vacant land and build-ready parcels",
            "Commercial and church property with unmanaged edges",
        ],
        "common_jobs": [
            "Overgrown lot and acreage clearing before fencing or building",
            "Pond bank brush removal and visibility cleanup",
            "Ditch and swale vegetation clearing after rainy seasons",
            "Trail and access path reopening across larger properties",
            "Storm debris and yard cleanup after wind events",
            "Pool dig-out dirt removal support under licensed pool builders",
        ],
        "local_note": (
            "Polk County properties often combine open pasture, wooded edges, and water features — "
            "which means brush, pond banks, and ditch lines need ongoing outdoor maintenance, not just one-time mowing."
        ),
        "nearby_counties": ["Osceola County", "Hillsborough County", "Lake County", "Hardee County", "Highlands County"],
        "meta_lead": (
            "Faith Works Outdoor Services clears land, pond banks, ditches, and overgrown acreage across Polk County "
            "from its Auburndale home base — serving Auburndale, Lakeland, Winter Haven, Bartow, and 14 Polk communities."
        ),
        "coverage_snapshot": (
            "From Chain of Lakes pond banks in Winter Haven to ridge scrub near Lake Wales and phosphate-country acreage "
            "around Mulberry, Polk jobs vary widely — each estimate is scoped from property photos, not a flat county rate."
        ),
        "unique_faqs": [
            (
                "Why is Polk County the core service area for Faith Works?",
                "Faith Works is headquartered in Auburndale (33823) in Polk County. Most equipment mobilization, scheduling, and estimate review starts here — making Polk the fastest-response county we serve.",
            ),
            (
                "Does Faith Works handle both suburban Polk lots and large rural acreage?",
                "Yes. Polk County includes Winter Haven lakefront lots, Lakeland rear acreage, and south Polk ranch parcels toward Fort Meade — scope and equipment are matched to each property after photo review.",
            ),
        ],
    },
    "Osceola County": {
        "region": "south Central Florida",
        "terrain": "a mix of suburban growth corridors, ranch land, and rural acreage south of Polk County",
        "property_types": [
            "Subdivision lots with rear conservation or wet areas",
            "Ranch and equestrian properties with fence lines to maintain",
            "Retention pond edges near newer development",
            "Acreage parcels between Kissimmee and Poinciana",
            "Vacant land being prepared for future use",
        ],
        "common_jobs": [
            "Brush clearing along fence lines and property boundaries",
            "Retention and pond edge cleanup where growth has taken over",
            "Access road and trail clearing on multi-acre parcels",
            "Forestry mulching for overgrown sections of acreage",
            "Debris haul-off after clearing or storm cleanup",
            "Ongoing ditch and drainage path vegetation removal",
        ],
        "local_note": (
            "Osceola County includes fast-growing communities and large rural parcels — "
            "property owners often need equipment that can work around ponds, tree lines, and long fence runs."
        ),
        "nearby_counties": ["Polk County", "Orange County", "Lake County", "Highlands County"],
        "meta_lead": (
            "Land clearing and pond bank work across Osceola County — Kissimmee, St Cloud, Poinciana, and rural acreage "
            "south of Polk. Faith Works travels from Auburndale within a 70-mile radius."
        ),
        "coverage_snapshot": (
            "Osceola blends fast-growing Poinciana subdivisions with ranch land south of Kissimmee — retention pond edges, "
            "fence lines, and multi-acre access trails are common reasons owners call from this county."
        ),
        "unique_faqs": [
            (
                "Does Faith Works serve both Kissimmee and Poinciana?",
                "Yes. Kissimmee, St Cloud, and Poinciana are listed Osceola communities — each has a dedicated city page with localized service details and estimate forms.",
            ),
            (
                "Are Osceola retention pond edges a common Faith Works job?",
                "Retention and pond edge cleanup around newer Osceola development is a frequent request — we handle private outdoor edges, not engineered stormwater system installation.",
            ),
        ],
    },
    "Orange County": {
        "region": "Greater Orlando",
        "terrain": "suburban residential neighborhoods, larger lot subdivisions, and rural edges toward Apopka and west Orange",
        "property_types": [
            "Oversized residential lots with unmanaged rear acreage",
            "Properties backing to woods, ponds, or conservation",
            "Small-acreage homes needing brush and trail work",
            "Land being opened for outbuildings, fencing, or access",
            "Post-storm yard and property debris cleanup",
        ],
        "common_jobs": [
            "Back-lot and rear acreage brush clearing",
            "Pond and wet-area edge cleanup where allowed on private property",
            "Fence line and boundary clearing",
            "Forestry mulching for dense undergrowth",
            "Property and lot cleanup before listing or building",
            "Trail clearing for access to barns, sheds, or rear fields",
        ],
        "local_note": (
            "Orange County homeowners often call when rear acreage, pond edges, or conservation borders "
            "have grown beyond what a lawn service can handle — that is where outdoor property equipment makes the difference."
        ),
        "nearby_counties": ["Osceola County", "Lake County", "Polk County", "Seminole County"],
        "meta_lead": (
            "Outdoor property clearing in Orange County — Orlando, Ocoee, Winter Garden, and Apopka. "
            "Rear acreage, pond edges, and brush removal from Faith Works in Auburndale."
        ),
        "coverage_snapshot": (
            "Greater Orlando includes oversized suburban lots backing to woods and conservation — jobs often focus on "
            "rear-acreage mulching and fence lines rather than small front-yard mowing."
        ),
        "unique_faqs": [
            (
                "Does Faith Works serve Orlando and western Orange County?",
                "Yes. Orlando, Ocoee, Winter Garden, and Apopka are within our service radius — each city page covers localized property types and common outdoor projects.",
            ),
            (
                "Can Faith Works clear rear acreage behind Orange County subdivisions?",
                "Rear wooded sections and conservation borders on private property are common Orange County requests — send photos showing property lines and access gates.",
            ),
        ],
    },
    "Lake County": {
        "region": "Florida's lake and hill country",
        "terrain": "rolling terrain with lakes, horse properties, rural acreage, and lake-country residential lots",
        "property_types": [
            "Lakefront homes with steep or overgrown banks",
            "Horse and equestrian properties with paddock edges",
            "Rural acreage with woods and pasture mix",
            "Residential lots with pond or retention features",
            "Vacant land needing selective clearing",
        ],
        "common_jobs": [
            "Pond bank and lake edge brush removal",
            "Trail and driveway access clearing on acreage",
            "Forestry mulching in wooded sections",
            "Fence line and pasture edge maintenance",
            "Property cleanup after years of deferred maintenance",
            "Ditch and runoff path vegetation clearing",
        ],
        "local_note": (
            "Lake County's mix of hills, lakes, and larger lots creates unique access challenges — "
            "compact equipment and experienced operators matter when banks, slopes, and tree lines are involved."
        ),
        "nearby_counties": ["Orange County", "Polk County", "Sumter County", "Marion County"],
        "meta_lead": (
            "Lake County land clearing and pond bank work — Clermont, Leesburg, Mount Dora, Tavares, and Groveland. "
            "Hill-country acreage and lakefront cleanup from Faith Works."
        ),
        "coverage_snapshot": (
            "Lake County's rolling terrain and horse properties create slope and bank access challenges — compact equipment "
            "and photo-based scope review matter before scheduling Clermont or Mount Dora jobs."
        ),
        "unique_faqs": [
            (
                "Does Faith Works handle sloped pond banks in Lake County?",
                "Yes. Lake County lakefront and pond edges on rolling terrain are common — send slope and access photos so we confirm the right equipment approach.",
            ),
            (
                "Can Faith Works clear horse property fence lines in Lake County?",
                "Fence line and paddock edge clearing around equestrian properties in Clermont, Leesburg, and Mount Dora are regular Lake County requests.",
            ),
        ],
    },
    "Hillsborough County": {
        "region": "Tampa Bay's eastern corridor",
        "terrain": "suburban Brandon and Valrico neighborhoods, agricultural land around Plant City, and rural edges toward Pasco",
        "property_types": [
            "Suburban homes with large back lots or wooded rear acreage",
            "Plant City and eastern Hillsborough rural parcels",
            "Properties with ditches, ponds, or retention areas",
            "Acreage being cleared for fencing, barns, or access",
            "Post-storm debris and brush cleanup",
        ],
        "common_jobs": [
            "Land and lot clearing on residential acreage",
            "Brush cutting and forestry mulching along overgrown edges",
            "Ditch clearing where vegetation blocks runoff paths",
            "Pond bank cleanup on private water features",
            "Access road and trail reopening",
            "Pool dig-out support under licensed pool contractors",
        ],
        "local_note": (
            "From Plant City strawberry country to Brandon subdivisions with oversized lots, Hillsborough properties "
            "often need the same core outdoor services: clear growth, open access, and haul debris — without utility excavation work."
        ),
        "nearby_counties": ["Polk County", "Pasco County", "Manatee County"],
        "meta_lead": (
            "Hillsborough County outdoor property services — Plant City, Brandon, Valrico, and Tampa. "
            "Land clearing, brush cutting, and pond work from Faith Works near Polk County."
        ),
        "coverage_snapshot": (
            "Eastern Hillsborough spans strawberry-country acreage around Plant City and oversized Brandon lots with wooded "
            "rear sections — two different property profiles that both need equipment-based clearing."
        ),
        "unique_faqs": [
            (
                "Does Faith Works serve both Plant City and Brandon?",
                "Yes. Plant City, Brandon, Valrico, and Tampa each have dedicated service area pages with city-specific property notes and estimate forms.",
            ),
            (
                "Can Faith Works clear agricultural acreage near Plant City?",
                "Plant City and eastern Hillsborough agricultural parcels are within our travel range — fence lines, ditches, and land clearing scope is confirmed from photos.",
            ),
        ],
    },
    "Pasco County": {
        "region": "north of Tampa Bay",
        "terrain": "rolling rural Pasco, Zephyrhills highlands, and growing Wesley Chapel subdivisions with larger lots",
        "property_types": [
            "Rural acreage and homestead parcels",
            "Equestrian and hobby farm properties",
            "Large-lot subdivisions with rear wooded areas",
            "Vacant land and future build sites",
            "Properties with pond or ditch maintenance needs",
        ],
        "common_jobs": [
            "Acreage and overgrown lot clearing",
            "Trail and access path cutting through wooded sections",
            "Fence line and boundary brush removal",
            "Forestry mulching for dense undergrowth",
            "Pond bank and ditch edge cleanup",
            "Storm and yard debris removal",
        ],
        "local_note": (
            "Pasco County still has substantial rural land alongside fast-growing suburbs — "
            "property owners often need one contractor who can handle brush, trails, ponds, and debris on the same visit."
        ),
        "nearby_counties": ["Hillsborough County", "Polk County", "Sumter County", "Hernando County"],
        "meta_lead": (
            "Pasco County land clearing — Zephyrhills, Wesley Chapel, and Dade City acreage cleanup. "
            "Rural Pasco and large-lot suburb brush removal from Faith Works."
        ),
        "coverage_snapshot": (
            "Pasco still holds substantial ranch and equestrian land alongside Wesley Chapel growth — one county where "
            "the same contractor may clear a five-acre homestead and a subdivision rear wooded buffer in the same week."
        ),
        "unique_faqs": [
            (
                "Does Faith Works serve Zephyrhills and Wesley Chapel?",
                "Yes. Zephyrhills, Wesley Chapel, and Dade City are listed Pasco communities with unique city pages and localized outdoor service details.",
            ),
            (
                "Can Faith Works handle Pasco equestrian property cleanup?",
                "Pasture edges, paddock fence lines, and trail access on Pasco horse properties are common — send photos of boundaries and gate access.",
            ),
        ],
    },
    "Hardee County": {
        "region": "south Central Florida ranch country",
        "terrain": "agricultural acreage, cattle ranch land, and rural homesteads",
        "property_types": [
            "Cattle ranch and pasture properties",
            "Large rural acreage parcels",
            "Homesteads with overgrown fence lines",
            "Vacant agricultural land",
            "Properties with pond or ditch edges needing cleanup",
        ],
        "common_jobs": [
            "Fence line and pasture edge clearing",
            "Access road and trail maintenance across acreage",
            "Overgrowth removal in unused sections of ranch land",
            "Forestry mulching for thick brush and saplings",
            "Pond bank brush removal",
            "Debris haul-off after clearing projects",
        ],
        "local_note": (
            "Hardee County work is often about reopening access — fence lines, ranch roads, and pond edges "
            "that have grown shut after a season or two without equipment maintenance."
        ),
        "nearby_counties": ["Polk County", "DeSoto County", "Highlands County", "Manatee County"],
        "meta_lead": (
            "Hardee County ranch and acreage clearing — Wauchula and rural south Central Florida land. "
            "Fence lines, pond banks, and pasture cleanup from Faith Works."
        ),
        "coverage_snapshot": (
            "Hardee County jobs are often about reopening ranch infrastructure — overgrown roads, gate areas, and long fence "
            "runs that cattle operations depend on for daily access."
        ),
        "unique_faqs": [
            (
                "Does Faith Works travel to Wauchula and Hardee County?",
                "Yes. Wauchula and rural Hardee County acreage are within our approximately 70-mile service radius from Auburndale — larger ranch jobs are reviewed by scope.",
            ),
            (
                "Can Faith Works work around active Hardee County cattle operations?",
                "Ranch road and fence line clearing near working pasture is common — note livestock locations and gate access when submitting photos for Wauchula-area jobs.",
            ),
        ],
    },
    "Highlands County": {
        "region": "south Central Florida lake plateau",
        "terrain": "lakes, rural residential lots, and agricultural acreage around Sebring and Avon Park",
        "property_types": [
            "Lakefront and pond-adjacent homes",
            "Rural residential acreage",
            "Vacant land and small farms",
            "Properties with unmanaged ditch or swale lines",
            "Lots needing cleanup before sale or development",
        ],
        "common_jobs": [
            "Land and lot clearing for usable space",
            "Pond bank and lake edge brush removal",
            "Property cleanup after deferred maintenance",
            "Trail and access clearing on multi-acre parcels",
            "Storm debris and yard cleanup",
            "Forestry mulching in wooded sections",
        ],
        "local_note": (
            "Highlands County properties frequently combine water features with unmanaged edges — "
            "pond banks, ditches, and back-acreage brush are common reasons owners reach out."
        ),
        "nearby_counties": ["Polk County", "Hardee County", "Osceola County", "Okeechobee County"],
        "meta_lead": (
            "Highlands County property cleanup — Sebring, Avon Park, and lake-plateau acreage. "
            "Land clearing, pond banks, and brush removal from Faith Works."
        ),
        "coverage_snapshot": (
            "Highlands County's lake plateau mixes scattered lakefront homes with rural residential acreage — pond edges "
            "and unmanaged ditch lines drive many Sebring and Avon Park estimate requests."
        ),
        "unique_faqs": [
            (
                "Does Faith Works serve both Sebring and Avon Park?",
                "Yes. Sebring and Avon Park each have dedicated city pages covering localized Highlands County property types and common outdoor projects.",
            ),
            (
                "Are Highlands County lakefront banks a common clearing request?",
                "Private lake and pond bank trimming around Sebring and Avon Park is a core outdoor service — bank slope and access are reviewed from photos first.",
            ),
        ],
    },
    "DeSoto County": {
        "region": "southwest Central Florida ranch land",
        "terrain": "wide-open pasture, cattle ranch acreage, and rural homesteads centered on Arcadia",
        "property_types": [
            "Large ranch and agricultural parcels",
            "Rural homestead acreage",
            "Vacant land needing selective clearing",
            "Properties with pond or drainage ditch edges",
            "Fence line and boundary maintenance projects",
        ],
        "common_jobs": [
            "Acreage cleanup and overgrowth removal",
            "Fence line and ranch road clearing",
            "Forestry mulching on overgrown sections",
            "Pond bank brush cutting",
            "Access trail reopening",
            "Debris removal after clearing or storms",
        ],
        "local_note": (
            "DeSoto County jobs often cover larger acreage with long fence runs and pond edges — "
            "equipment mobility and clear scope planning matter before work begins."
        ),
        "nearby_counties": ["Hardee County", "Manatee County", "Sarasota County", "Charlotte County"],
        "meta_lead": (
            "DeSoto County ranch land clearing — Arcadia acreage, fence lines, and pond banks. "
            "Large-parcel outdoor property work from Faith Works within travel range."
        ),
        "coverage_snapshot": (
            "DeSoto County parcels tend to be wide-open ranch land with long boundaries — scope planning for fence runs, "
            "pond edges, and equipment turnaround space starts with aerial or wide-angle property photos."
        ),
        "unique_faqs": [
            (
                "Does Faith Works serve Arcadia and rural DeSoto County?",
                "Yes. Arcadia and rural DeSoto acreage are within our service radius — large ranch parcels are reviewed individually for travel, access, and equipment needs.",
            ),
            (
                "Can Faith Works clear long fence lines on DeSoto County ranch land?",
                "Long fence run clearing is one of the most common DeSoto requests — send photos showing total length, gate locations, and pasture access.",
            ),
        ],
    },
    "Sumter County": {
        "region": "Central Florida's growing retirement and acreage corridor",
        "terrain": "The Villages area growth, Bushnell rural land, and rolling acreage between Orlando and Ocala",
        "property_types": [
            "Acreage homes with pond or retention features",
            "Rural parcels with overgrown edges",
            "Properties needing trail or access clearing",
            "Lots being prepared for fencing or outbuildings",
            "Homes with ditch or swale vegetation buildup",
        ],
        "common_jobs": [
            "Brush and overgrowth removal on acreage lots",
            "Pond bank and water-edge cleanup",
            "Property cleanup before move-in or sale",
            "Trail and access path clearing",
            "Forestry mulching in wooded sections",
            "Ditch line vegetation removal",
        ],
        "local_note": (
            "Sumter County includes both active retirement communities and rural acreage — "
            "owners often want outdoor property work handled carefully around homes, ponds, and established landscaping."
        ),
        "nearby_counties": ["Lake County", "Marion County", "Pasco County", "Polk County"],
        "meta_lead": (
            "Sumter County acreage cleanup — The Villages, Bushnell, and rural land between Orlando and Ocala. "
            "Pond banks, brush removal, and trail clearing from Faith Works."
        ),
        "coverage_snapshot": (
            "Sumter County mixes active retirement-community acreage with rural Bushnell land — owners often want careful "
            "clearing around established homes, ponds, and landscaping rather than aggressive whole-lot stripping."
        ),
        "unique_faqs": [
            (
                "Does Faith Works serve The Villages and Bushnell?",
                "Yes. The Villages and Bushnell have dedicated city pages with Sumter County-specific property notes and outdoor service details.",
            ),
            (
                "Can Faith Works work carefully around Sumter County homes and ponds?",
                "Many Sumter jobs require selective clearing around homes and water features — detailed photos help us plan equipment paths and avoid unnecessary disturbance.",
            ),
        ],
    },
    "Manatee County": {
        "region": "Tampa Bay's southern reach",
        "terrain": "Bradenton suburban neighborhoods, Parrish growth areas, and rural edges within travel range from Auburndale",
        "property_types": [
            "Suburban homes with larger back lots",
            "Rural Parrish and eastern Manatee acreage",
            "Properties with pond or ditch maintenance needs",
            "Vacant land being opened for use",
            "Post-storm property cleanup projects",
        ],
        "common_jobs": [
            "Land and lot clearing on residential acreage",
            "Brush cutting and forestry mulching",
            "Pond bank edge cleanup",
            "Fence line and boundary clearing",
            "Debris removal after clearing or weather events",
            "Pool dig-out support under licensed pool contractors",
        ],
        "local_note": (
            "Northern Manatee County properties within our travel range often mirror Polk and Hillsborough jobs — "
            "overgrown edges, pond banks, and acreage cleanup rather than utility or site-development excavation."
        ),
        "nearby_counties": ["Hillsborough County", "Polk County", "Sarasota County", "DeSoto County"],
        "meta_lead": (
            "Manatee County outdoor property services — Bradenton and Parrish land clearing within Faith Works travel range. "
            "Brush cutting, pond edges, and acreage cleanup from Auburndale."
        ),
        "coverage_snapshot": (
            "Northern Manatee within our radius often mirrors Hillsborough jobs — oversized suburban rear lots in Bradenton "
            "and rural Parrish acreage both need mulching, pond edges, and debris haul-off rather than utility excavation."
        ),
        "unique_faqs": [
            (
                "Does Faith Works serve Bradenton and Parrish in Manatee County?",
                "Yes. Bradenton and Parrish are listed Manatee communities — each has a city page with localized service details within our travel range.",
            ),
            (
                "Is northern Manatee County within the 70-mile Faith Works radius?",
                "Northern Manatee communities like Parrish and Bradenton fall within our approximately 70-mile service radius from Auburndale — confirm with your address and photos.",
            ),
        ],
    },
}


def city_intent_routes(city: dict) -> list[dict]:
    return city_profile(city["slug"])["intent_routes"]


def city_strip_note(city: dict) -> str:
    return city_profile(city["slug"])["strip_note"]


def city_intro_html(city: dict) -> str:
    name = city["name"]
    county = city["county"]
    profile = city_profile(city["slug"])
    return f"""
          <h2>Land Clearing &amp; Outdoor Property Services in {name}, {county}</h2>
          <p>{profile["hook"]}</p>
          <p>{profile["context"]}</p>
          <p>{profile["local_detail"]}</p>
          <p>
            {OWNER} reviews photos from {name} property owners before confirming scope, equipment, and scheduling.
            Faith Works focuses on outdoor property work — clearing, mulching, cleanup, and maintenance — not utility
            trenching, engineered drainage, or pool installation. Pool dig-out support is available under licensed pool
            contractors when your builder needs dirt removal and site cleanup.
          </p>"""


def county_profile(county_name: str) -> dict:
    return COUNTY_PROFILES.get(county_name, {
        "region": "Central Florida",
        "terrain": "residential, rural, and acreage properties",
        "property_types": ["Residential lots", "Rural acreage", "Vacant land", "Properties with ponds or ditches"],
        "common_jobs": ["Land clearing", "Brush cutting", "Pond bank cleanup", "Debris removal", "Trail clearing"],
        "local_note": f"Property owners across {county_name} often need outdoor clearing, mulching, and cleanup — not utility excavation.",
        "nearby_counties": [],
        "meta_lead": f"{BRAND} serves {county_name}, FL with outdoor property clearing and cleanup.",
        "coverage_snapshot": f"Faith Works travels to {county_name} from {HOME_CITY} within approximately {SERVICE_RADIUS_MILES} miles.",
        "unique_faqs": [],
    })


def city_page_title(city_name: str) -> str:
    return f"{SITE_POSITIONING} in {city_name}, FL"


def city_meta_description(city: dict) -> str:
    profile = city_profile(city["slug"])
    return profile["meta_description"]


def county_meta_description(county: dict, city_count: int) -> str:
    profile = county_profile(county["name"])
    lead = profile.get("meta_lead") or (
        f"{BRAND} serves {county['name']}, FL with land clearing, pond bank clearing, ditch clearing, "
        f"brush cutting, forestry mulching, and outdoor property cleanup."
    )
    return f"{lead} {city_count} cities listed. Based in {HOME_CITY} ({HOME_ZIP}). Free photo estimates."


def _list_html(items: list[str]) -> str:
    return "<ul>\n" + "\n".join(f"            <li>{item}</li>" for item in items) + "\n          </ul>"


def area_services_by_category(root_prefix: str, place_name: str) -> str:
    blocks = ""
    for cat in SERVICE_CATEGORIES:
        group = services_for_category(cat["id"])
        if not group:
            continue
        links = "\n".join(
            f'              <li><a href="{root_prefix}{s["slug"]}.html">{s["nav"]} in {place_name}</a> — {s["desc"].split(".")[0]}.</li>'
            for s in group
        )
        blocks += f"""
          <div class="area-service-group">
            <h3>{cat["label"]}</h3>
            <p>{cat["description"]}</p>
            <ul class="area-service-list">
{links}
            </ul>
          </div>"""
    return blocks


def area_intent_cards(root_prefix: str, place_name: str, intent_routes: list[dict]) -> str:
    cards = ""
    for i, item in enumerate(intent_routes):
        label = SERVICE_BY_SLUG_LABEL(item["slug"])
        cards += f"""
          <article class="intent-card" data-fw-enter="bottom" style="--fw-enter-delay: {(i % 6) * 60}ms;">
            <h3><a href="{root_prefix}{item['slug']}.html">{item['label']} in {place_name}</a></h3>
            <p>{item['text']}</p>
            <a class="intent-card__cta" href="{root_prefix}{item['slug']}.html">Learn about {label} &rarr;</a>
          </article>"""
    return f'<div class="intent-grid area-intent-grid">{cards}\n        </div>'


def SERVICE_BY_SLUG_LABEL(slug: str) -> str:
    for s in SERVICES:
        if s["slug"] == slug:
            return s["nav"]
    return slug.replace("-", " ").title()


def city_property_section(city: dict) -> str:
    name = city["name"]
    profile = city_profile(city["slug"])
    return f"""
          <h2>Property Types We Serve in {name}, FL</h2>
          <p>
            {name} property owners call Faith Works for outdoor projects tied to local land use and terrain. Common {name} property types include:
          </p>
          {_list_html(profile["property_types"])}
          <p>
            If your {name} property has unmanaged growth, blocked access, pond or ditch edges that need attention, or debris
            piled after clearing or weather events, send photos through our estimate form — that is the fastest way to get an
            accurate scope review for {name}, FL.
          </p>"""


def city_common_jobs_section(city: dict) -> str:
    name = city["name"]
    county = city["county"]
    profile = city_profile(city["slug"])
    return f"""
          <h2>Common Outdoor Projects in {name}, {county}</h2>
          <p>These are the outdoor property jobs {name} owners request most often from Faith Works:</p>
          {_list_html(profile["common_jobs"])}
          <p>
            Every {name} property is different. Access, vegetation density, water edges, and debris volume all affect equipment choice
            and scheduling — photo-based estimates confirm scope before {name} work is scheduled.
          </p>"""


def city_services_teaser(city: dict, root_prefix: str) -> str:
    """Compact, city-specific service links — avoids duplicating the full 22-service catalog on every city page."""
    profile = city_profile(city["slug"])
    seen: set[str] = set()
    links: list[str] = []
    for item in profile["intent_routes"]:
        slug = item["slug"]
        if slug in seen:
            continue
        seen.add(slug)
        label = SERVICE_BY_SLUG_LABEL(slug)
        links.append(
            f'<a href="{root_prefix}{slug}.html">{label} in {city["name"]}</a>'
        )
    extra = ["land-clearing", "debris-removal", "tractor-services"]
    for slug in extra:
        if slug not in seen:
            seen.add(slug)
            label = SERVICE_BY_SLUG_LABEL(slug)
            links.append(f'<a href="{root_prefix}{slug}.html">{label}</a>')
    link_html = "\n            ".join(links)
    return f"""
          <h2>Popular Services in {city['name']}, FL</h2>
          <p>Start with the outdoor property services {city['name']} owners request most — each links to a full service page with scope details.</p>
          <div class="area-card-links area-card-links--wrap">
            {link_html}
          </div>
          <p>Browse all <a href="{root_prefix}services.html">{len(SERVICES)} outdoor property services</a> or view the <a href="{root_prefix}service-areas.html">full service area map</a>.</p>"""


def city_process_section(city: dict) -> str:
    city_name = city["name"]
    note = city_profile(city["slug"])["local_detail"]
    return f"""
          <h2>How to Get Service in {city_name}, FL</h2>
          <p>{note}</p>
          <div class="process-grid area-process-grid">
            <article class="process-step">
              <span>1</span>
              <h3>Send Photos</h3>
              <p>Text or send property photos, your {city_name} address or cross streets, and a short description of what you need cleared or cleaned up.</p>
            </article>
            <article class="process-step">
              <span>2</span>
              <h3>Scope Review</h3>
              <p>{OWNER} reviews access, vegetation, pond or ditch edges, debris, and equipment needs for your {city_name} property — then follows up with next steps.</p>
            </article>
            <article class="process-step">
              <span>3</span>
              <h3>Estimate &amp; Schedule</h3>
              <p>Once scope is clear, you receive pricing and scheduling options for your {city_name} property before work begins.</p>
            </article>
            <article class="process-step">
              <span>4</span>
              <h3>Outdoor Property Work</h3>
              <p>Faith Works completes clearing, mulching, brush cutting, cleanup, or debris removal in {city_name} — outdoor property services only, not utility excavation.</p>
            </article>
          </div>"""


def city_scope_section() -> str:
    not_offered = "\n".join(f"            <li>{item}</li>" for item in NOT_OFFERED)
    return f"""
          <h2>What Faith Works Does &amp; Does Not Do</h2>
          <h3>Outdoor property services we provide</h3>
          <p>{SITE_POSITIONING} — including all {len(SERVICES)} service pages listed on this site, from land clearing and forestry mulching to pond bank work, ditch clearing, debris removal, and tractor services.</p>
          <h3>Work we do not perform</h3>
          <p>{NOT_OFFERED_NOTE}</p>
          <ul>
{not_offered}
          </ul>
          <p class="utility-note"><strong>Sunshine 811:</strong> For any digging or soil-moving work, contact Sunshine 811 at least two full business days before work begins so underground utilities can be marked.</p>"""


def city_area_faqs(city: dict) -> list[tuple[str, str]]:
    city_name = city["name"]
    county_name = city["county"]
    profile = city_profile(city["slug"])
    core = [
        (
            f"Does Faith Works Outdoor Services serve {city_name}, FL?",
            f"Yes. {BRAND} serves {city_name} in {county_name} from our base in {HOME_CITY}, Florida ({HOME_ZIP}). Send photos and project details for a free estimate.",
        ),
        (
            f"How do I get a free estimate for outdoor property work in {city_name}?",
            f"Use the contact form on this page. Send photos of the area you need cleared in {city_name}, include your phone number, and describe access notes or deadlines. {OWNER} reviews scope and follows up directly.",
        ),
        (
            f"Is Faith Works an excavation contractor in {city_name}?",
            f"No. Faith Works is not a utility excavation contractor. We focus on {SITE_POSITIONING.lower()} — outdoor clearing, mulching, cleanup, and maintenance in {city_name}.",
        ),
        (
            f"What should I include when requesting service in {city_name}?",
            f"Include your {city_name} address or nearest cross streets, photos of the work area, vegetation or debris type, access notes (gates, slopes, water edges), and any deadline.",
        ),
        (
            f"Who owns Faith Works Outdoor Services?",
            f"{OWNER} owns and operates {BRAND}. {city_name} clients work directly with the owner from estimate through completion.",
        ),
    ]
    return list(profile["unique_faqs"]) + core


def county_intro_html(county: dict, cities: list[dict]) -> str:
    profile = county_profile(county["name"])
    city_names = ", ".join(c["name"] for c in cities[:8])
    extra = f", and more" if len(cities) > 8 else ""
    return f"""
          <h2>{SITE_POSITIONING} Across {county['name']}</h2>
          <p>
            {BRAND} serves property owners throughout <strong>{county['name']}, Florida</strong> from our home base in
            {HOME_CITY} ({HOME_ZIP}). We travel within approximately {SERVICE_RADIUS_MILES} miles for land clearing,
            pond bank clearing, ditch clearing, brush cutting, forestry mulching, debris removal, and outdoor property cleanup.
          </p>
          <p>
            {county['name']} is part of {profile['region']}, where {profile['terrain']}. {profile['local_note']}
          </p>
          <p>{profile.get('coverage_snapshot', '')}</p>
          <p>
            Cities and communities we serve in {county['name']} include <strong>{city_names}</strong>{extra}.
            Each city page includes localized service details, property types, common jobs, and a photo-based estimate form.
          </p>
          <p>
            Faith Works is owner-operated by {OWNER}. You get direct communication from estimate through job completion —
            not a call-center handoff. We focus on outdoor property work, not utility trenching, engineered drainage, or pool installation.
          </p>"""


def county_property_section(county_name: str) -> str:
    profile = county_profile(county_name)
    return f"""
          <h2>Property Types in {county_name}</h2>
          <p>{county_name} property owners across {profile['region']} commonly need help with:</p>
          {_list_html(profile["property_types"])}
          <h2>Common Projects in {county_name}</h2>
          {_list_html(profile["common_jobs"])}"""


def county_area_faqs(county_name: str, cities: list[dict]) -> list[tuple[str, str]]:
    profile = county_profile(county_name)
    city_sample = ", ".join(c["name"] for c in cities[:5])
    extra = " and surrounding communities" if len(cities) > 5 else ""
    core = [
        (
            f"What cities does Faith Works serve in {county_name}?",
            f"Faith Works serves {len(cities)} communities in {county_name}, including {city_sample}{extra}. Each city has a dedicated page with localized outdoor property details.",
        ),
        (
            f"How do I request an outdoor property estimate in {county_name}?",
            f"Choose your city on this page or use our contact form. Upload property photos, describe the clearing or cleanup needed, and include access notes. {OWNER} reviews scope and follows up directly.",
        ),
        (
            f"Is Faith Works licensed for utility excavation in {county_name}?",
            f"No. Faith Works does not perform utility trenching, storm sewer installation, water main work, site development excavation, or pool contracting in {county_name}.",
        ),
        (
            f"Who should I contact for Faith Works service in {county_name}?",
            f"Contact {OWNER} through the estimate form, email {SITE_EMAIL}, or call (863) 272-1596. Include your {county_name} city and property photos.",
        ),
    ]
    return list(profile.get("unique_faqs", [])) + core


def nearby_cities_html(city: dict, limit: int = 8) -> str:
    siblings = [c for c in cities_in_county(city["county"]) if c["slug"] != city["slug"]]
    return "".join(f'<a href="{c["slug"]}.html">{c["name"]}, FL</a>' for c in siblings[:limit])


def nearby_counties_html(county_name: str, root_prefix: str) -> str:
    profile = county_profile(county_name)
    links = []
    for name in profile.get("nearby_counties", []):
        county = COUNTY_BY_NAME.get(name)
        if county:
            links.append(f'<a href="{root_prefix}areas/{county["slug"]}.html">{name}</a>')
    for c in COUNTIES:
        if c["name"] != county_name and c["name"] not in profile.get("nearby_counties", []):
            if len(links) >= 11:
                break
            if f'<a href="{root_prefix}areas/{c["slug"]}.html">{c["name"]}</a>' not in links:
                links.append(f'<a href="{root_prefix}areas/{c["slug"]}.html">{c["name"]}</a>')
    return " &nbsp;&middot;&nbsp; ".join(links[:11])


def area_webpage_schema(name: str, description: str, canonical_path: str) -> str:
    import json

    return json.dumps({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": f"https://faithworksclearing.com/{canonical_path}#webpage",
        "name": name,
        "description": description,
        "url": f"https://faithworksclearing.com/{canonical_path}",
        "isPartOf": {"@id": "https://faithworksclearing.com/#website"},
        "about": {"@type": "Place", "name": name},
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [".sp-content h2", ".sp-content p", ".faq-question"],
        },
    }, indent=2)
