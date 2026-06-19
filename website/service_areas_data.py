"""Service area cities and counties — ~70 miles from Auburndale, FL (33823)."""

from __future__ import annotations

HOME_ZIP = "33823"
HOME_CITY = "Auburndale"
SERVICE_RADIUS_MILES = 70

COUNTIES = [
    {
        "name": "Polk County",
        "slug": "polk-county-fl",
        "description": "Primary service area — Auburndale, Lakeland, Winter Haven, Bartow, Haines City, Lake Wales, and surrounding Polk County communities.",
    },
    {
        "name": "Osceola County",
        "slug": "osceola-county-fl",
        "description": "Kissimmee, St Cloud, Poinciana, and rural acreage south of Polk County.",
    },
    {
        "name": "Orange County",
        "slug": "orange-county-fl",
        "description": "Orlando, Ocoee, Winter Garden, Apopka, and western Orange County property.",
    },
    {
        "name": "Lake County",
        "slug": "lake-county-fl",
        "description": "Clermont, Leesburg, Mount Dora, Tavares, and lake-country acreage.",
    },
    {
        "name": "Hillsborough County",
        "slug": "hillsborough-county-fl",
        "description": "Plant City, Brandon, Valrico, Tampa, and eastern Hillsborough outdoor property work.",
    },
    {
        "name": "Pasco County",
        "slug": "pasco-county-fl",
        "description": "Zephyrhills, Dade City, Wesley Chapel, and rural Pasco land.",
    },
    {
        "name": "Hardee County",
        "slug": "hardee-county-fl",
        "description": "Wauchula, Bowling Green, and rural Hardee County acreage.",
    },
    {
        "name": "Highlands County",
        "slug": "highlands-county-fl",
        "description": "Sebring, Avon Park, and Highlands County property cleanup.",
    },
    {
        "name": "DeSoto County",
        "slug": "desoto-county-fl",
        "description": "Arcadia and rural DeSoto County land clearing.",
    },
    {
        "name": "Sumter County",
        "slug": "sumter-county-fl",
        "description": "The Villages, Bushnell, Wildwood, and Sumter County acreage.",
    },
    {
        "name": "Manatee County",
        "slug": "manatee-county-fl",
        "description": "Parrish, Bradenton, and northern Manatee outdoor property services within our travel range.",
    },
]

# slug, name, county — cities reasonably within ~70 miles of Auburndale (33823)
CITIES = [
    {"slug": "auburndale-fl", "name": "Auburndale", "county": "Polk County", "featured": True},
    {"slug": "winter-haven-fl", "name": "Winter Haven", "county": "Polk County", "featured": True},
    {"slug": "lakeland-fl", "name": "Lakeland", "county": "Polk County", "featured": True},
    {"slug": "lake-alfred-fl", "name": "Lake Alfred", "county": "Polk County", "featured": True},
    {"slug": "bartow-fl", "name": "Bartow", "county": "Polk County", "featured": True},
    {"slug": "haines-city-fl", "name": "Haines City", "county": "Polk County", "featured": True},
    {"slug": "davenport-fl", "name": "Davenport", "county": "Polk County", "featured": True},
    {"slug": "lake-wales-fl", "name": "Lake Wales", "county": "Polk County", "featured": True},
    {"slug": "polk-city-fl", "name": "Polk City", "county": "Polk County", "featured": True},
    {"slug": "mulberry-fl", "name": "Mulberry", "county": "Polk County"},
    {"slug": "fort-meade-fl", "name": "Fort Meade", "county": "Polk County"},
    {"slug": "frostproof-fl", "name": "Frostproof", "county": "Polk County"},
    {"slug": "dundee-fl", "name": "Dundee", "county": "Polk County"},
    {"slug": "eagle-lake-fl", "name": "Eagle Lake", "county": "Polk County"},
    {"slug": "plant-city-fl", "name": "Plant City", "county": "Hillsborough County", "featured": True},
    {"slug": "kissimmee-fl", "name": "Kissimmee", "county": "Osceola County", "featured": True},
    {"slug": "st-cloud-fl", "name": "St Cloud", "county": "Osceola County"},
    {"slug": "poinciana-fl", "name": "Poinciana", "county": "Osceola County"},
    {"slug": "orlando-fl", "name": "Orlando", "county": "Orange County", "featured": True},
    {"slug": "ocoee-fl", "name": "Ocoee", "county": "Orange County"},
    {"slug": "winter-garden-fl", "name": "Winter Garden", "county": "Orange County"},
    {"slug": "apopka-fl", "name": "Apopka", "county": "Orange County"},
    {"slug": "clermont-fl", "name": "Clermont", "county": "Lake County", "featured": True},
    {"slug": "leesburg-fl", "name": "Leesburg", "county": "Lake County"},
    {"slug": "mount-dora-fl", "name": "Mount Dora", "county": "Lake County"},
    {"slug": "tavares-fl", "name": "Tavares", "county": "Lake County"},
    {"slug": "groveland-fl", "name": "Groveland", "county": "Lake County"},
    {"slug": "brandon-fl", "name": "Brandon", "county": "Hillsborough County"},
    {"slug": "tampa-fl", "name": "Tampa", "county": "Hillsborough County"},
    {"slug": "valrico-fl", "name": "Valrico", "county": "Hillsborough County"},
    {"slug": "zephyrhills-fl", "name": "Zephyrhills", "county": "Pasco County"},
    {"slug": "wesley-chapel-fl", "name": "Wesley Chapel", "county": "Pasco County"},
    {"slug": "dade-city-fl", "name": "Dade City", "county": "Pasco County"},
    {"slug": "wauchula-fl", "name": "Wauchula", "county": "Hardee County"},
    {"slug": "sebring-fl", "name": "Sebring", "county": "Highlands County"},
    {"slug": "avon-park-fl", "name": "Avon Park", "county": "Highlands County"},
    {"slug": "arcadia-fl", "name": "Arcadia", "county": "DeSoto County"},
    {"slug": "the-villages-fl", "name": "The Villages", "county": "Sumter County"},
    {"slug": "bushnell-fl", "name": "Bushnell", "county": "Sumter County"},
    {"slug": "bradenton-fl", "name": "Bradenton", "county": "Manatee County"},
    {"slug": "parrish-fl", "name": "Parrish", "county": "Manatee County"},
]

COUNTY_BY_NAME = {c["name"]: c for c in COUNTIES}
COUNTY_BY_SLUG = {c["slug"]: c for c in COUNTIES}
CITY_BY_SLUG = {c["slug"]: c for c in CITIES}
CITY_NAMES = [c["name"] for c in CITIES]
FEATURED_CITIES = [c for c in CITIES if c.get("featured")]


def cities_in_county(county_name: str) -> list[dict]:
    return [c for c in CITIES if c["county"] == county_name]


def city_href(slug: str) -> str:
    return f"areas/{slug}.html"
