"""Unique per-city content for Faith Works service area pages."""

from __future__ import annotations

from city_profiles_remaining import REMAINING_CITY_PROFILES

# Hand-authored home-base and flagship Polk cities
_BASE_CITY_PROFILES: dict[str, dict] = {
    "auburndale-fl": {
        "meta_description": (
            "Auburndale land clearing, brush clearing, pond bank work, and ditch maintenance from Faith Works. "
            "Owner-operated outdoor services from 33823. Call or text Tyler."
        ),
        "hook": (
            "Auburndale is where Faith Works Outdoor Services is headquartered — Tyler Edwards runs estimates, "
            "scheduling, and field work from this Polk County lake-country community."
        ),
        "context": (
            "Between Lake Ariana, Lake Juliana, and the I-4 corridor, Auburndale mixes in-town neighborhoods "
            "with citrus acreage and small-lake frontage. Properties here often have rear pond edges, drainage "
            "ditches along road frontage, and fence lines that creep shut between mowing seasons."
        ),
        "local_detail": (
            "Because we are based here, Auburndale jobs typically get the fastest response for site visits "
            "and equipment mobilization across eastern Polk County."
        ),
        "property_types": [
            "In-town lots with overgrown rear acreage toward Lake Ariana",
            "Citrus grove edges and abandoned grove cleanup parcels",
            "Lakefront homes with unmanaged pond or canal banks",
            "Commercial pads and church grounds with brush-choked perimeters",
            "Vacant parcels being opened for new construction near Berkley Road",
        ],
        "common_jobs": [
            "Clearing overgrown residential lots before listing or building",
            "Brush removal around homes, sheds, and fence lines",
            "Pond bank brush removal along small Auburndale lakes",
            "Ditch and swale cleanup along county roads after summer growth",
            "Fence line reopening on acreage between Auburndale and Winter Haven",
            "Storm debris haul-off after wind events in Polk County",
        ],
        "intent_routes": [
            {"label": "Lake-country lot clearing", "slug": "land-clearing", "text": "Open overgrown Auburndale lots backed by woods, groves, or water edges."},
            {"label": "Pond and canal banks", "slug": "pond-bank-clearing", "text": "Cut back brush on private pond, canal, and retention edges common around Auburndale lakes."},
            {"label": "Road and ditch lines", "slug": "ditch-clearing", "text": "Clear vegetation from drainage paths along property frontage and swales."},
            {"label": "Citrus acreage edges", "slug": "forestry-mulching", "text": "Mulch saplings and thick undergrowth on former grove and pasture parcels."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works offer same-day estimates in Auburndale?",
                "Auburndale is our home base, so photo-based estimates and scheduling often move faster here than for distant travel jobs. Send property photos and your Auburndale address for the quickest review.",
            ),
            (
                "Can Faith Works clear land near Lake Ariana or Lake Juliana?",
                "Yes. Lake-adjacent lots and pond banks around Auburndale's small lakes are common requests — we match compact equipment to bank access and vegetation density after reviewing your photos.",
            ),
        ],
        "strip_note": "Home-base response for Auburndale pond banks, ditch lines, and overgrown acreage.",
    },
    "winter-haven-fl": {
        "meta_description": (
            "Winter Haven pond bank clearing, brush removal, land clearing, and storm debris cleanup. "
            "Faith Works serves Chain of Lakes properties from nearby Auburndale."
        ),
        "hook": (
            "Winter Haven's Chain of Lakes geography puts pond edges, canal banks, and lake-adjacent lots "
            "at the center of many outdoor property projects Faith Works handles in Polk County."
        ),
        "context": (
            "From downtown lakefront neighborhoods to Cypress Gardens Boulevard acreage, Winter Haven properties "
            "often combine managed front yards with unmanaged rear banks, conservation borders, and ditch lines "
            "that standard lawn crews will not touch with forestry or mulching equipment."
        ),
        "local_detail": (
            "Canal-side homes and larger lots toward Dundee and Eagle Lake frequently need brush cut back "
            "without disturbing seawalls or neighbor sight lines — scope is confirmed from photos before work."
        ),
        "property_types": [
            "Chain of Lakes homes with overgrown pond or canal banks",
            "Residential lots with rear conservation or wetland buffers",
            "Acreage parcels between Winter Haven and Haines City",
            "Vacant land near Cypress Gardens area being prepared for build",
            "Properties with drainage ditches feeding lake systems",
        ],
        "common_jobs": [
            "Pond and canal bank brush removal for visibility and access",
            "Brush removal around lake-country rear lots and fence lines",
            "Clearing overgrown rear lots before fencing or pool projects",
            "Ditch line vegetation removal after rainy-season growth",
            "Trail reopening across multi-acre Winter Haven parcels",
            "Storm debris cleanup along lakefront and tree-canopy neighborhoods",
        ],
        "intent_routes": [
            {"label": "Chain of Lakes pond banks", "slug": "pond-bank-clearing", "text": "Clean back brush on Winter Haven lake, canal, and retention edges."},
            {"label": "Rear lot and acreage clearing", "slug": "land-clearing", "text": "Reclaim usable space on overgrown lots across Winter Haven neighborhoods."},
            {"label": "Drainage path cleanup", "slug": "ditch-clearing", "text": "Open outdoor ditch and swale lines that feed Winter Haven lake systems."},
            {"label": "Storm and yard debris", "slug": "storm-debris-cleanup", "text": "Haul limbs and brush piles after storms across lake-country properties."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works work on Winter Haven canal and lake banks?",
                "Yes. Chain of Lakes properties often need pond bank and canal edge clearing — we review bank slope, access, and vegetation type from photos before confirming Winter Haven jobs.",
            ),
            (
                "Can you clear conservation buffers behind Winter Haven homes?",
                "We clear private outdoor property areas you own or maintain — not protected public conservation. Send photos showing property lines and access so scope stays accurate.",
            ),
        ],
        "strip_note": "Chain of Lakes pond banks, canal edges, and overgrown rear lots in Winter Haven.",
    },
    "lakeland-fl": {
        "meta_description": (
            "Lakeland brush clearing, land clearing, pond bank cleanup, and acreage cleanup from Faith Works. "
            "Photo-based estimates for lakefront, rear-lot, and south Polk properties."
        ),
        "hook": (
            "Lakeland spans from historic lakefront neighborhoods around Lake Morton and Lake Hollingsworth "
            "to rural land toward Mulberry and south Polk — each with different clearing and cleanup needs."
        ),
        "context": (
            "Faith Works handles Lakeland jobs where rear acreage, wooded buffers, pond edges, and ditch lines "
            "have outgrown routine maintenance. Compact equipment fits many in-town access constraints when "
            "photos show gate width, slopes, and obstacles clearly."
        ),
        "local_detail": (
            "South and southwest Lakeland toward the Polk Parkway often mix suburban lots with larger parcels "
            "needing forestry mulching, fence line work, and debris haul-off in one project."
        ),
        "property_types": [
            "Historic district homes with large rear wooded sections",
            "Lake Morton and Lake Hollingsworth adjacent properties",
            "South Lakeland acreage toward Mulberry and Bartow",
            "Commercial and industrial pads with unmanaged perimeters",
            "Build-ready vacant parcels needing selective clearing",
        ],
        "common_jobs": [
            "Rear acreage brush clearing on oversized Lakeland lots",
            "Brush removal where wooded buffers meet homes and outbuildings",
            "Pond and lake edge cleanup on private water features",
            "Land clearing before fencing, barns, or outbuildings",
            "Forestry mulching on sapling-choked sections",
            "Ditch and swale maintenance on drainage easements",
        ],
        "intent_routes": [
            {"label": "Oversized lot clearing", "slug": "land-clearing", "text": "Clear dense growth on Lakeland lots too large for standard lawn service."},
            {"label": "Lakefront edge work", "slug": "pond-bank-clearing", "text": "Trim brush on private lake and pond banks across Lakeland neighborhoods."},
            {"label": "South Polk acreage", "slug": "acreage-cleanup", "text": "Cleanup and mulching on larger parcels toward Mulberry and Bartow."},
            {"label": "Pre-build lot prep", "slug": "lot-cleanup", "text": "Open vacant Lakeland parcels before construction or sale."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve north and south Lakeland equally?",
                "Yes. We travel throughout Lakeland within our service radius — from lakefront neighborhoods to south Polk acreage. Photos and address help confirm access and scheduling.",
            ),
            (
                "Can you work on Lakeland properties near Florida Southern or downtown lakes?",
                "Many downtown-adjacent lots have tight access. Send gate measurements and photos of the work area so we can confirm equipment fit before scheduling Lakeland jobs.",
            ),
        ],
        "strip_note": "Lakeland lakefront edges, rear acreage, and south Polk cleanup projects.",
    },
}

CITY_PROFILES: dict[str, dict] = {**_BASE_CITY_PROFILES, **REMAINING_CITY_PROFILES}


def city_profile(slug: str) -> dict:
    if slug not in CITY_PROFILES:
        raise KeyError(f"Missing city profile for {slug}")
    return CITY_PROFILES[slug]
