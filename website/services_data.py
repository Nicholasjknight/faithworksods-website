"""Faith Works Outdoor Services — service definitions for site generator."""

from __future__ import annotations

AREA = "Polk County & Central Florida"
CITY = "Auburndale"

# Exact positioning from communication1.txt
SITE_POSITIONING = "Land Clearing, Pond Bank Clearing, Ditch Clearing & Outdoor Property Services"

NOT_OFFERED = [
    "Installing underground utilities",
    "Stormwater systems",
    "Sewer systems",
    "Water mains",
    "Utility trenching",
    "Site development",
    "Engineered drainage systems",
    "Pool installation or licensed pool contracting (we support dig-out cleanup under your pool builder)",
    "Excavation contractor / utility infrastructure work",
]

NOT_OFFERED_NOTE = (
    "Florida's Underground Utility & Excavation contractor license covers sanitary sewer, water distribution, "
    "storm sewer systems, utility line work, directional drilling, and similar infrastructure — not the outdoor "
    "property clearing, mulching, and cleanup services Faith Works focuses on."
)

IMAGES = [
    "excavator-photo.webp",
    "tractor.webp",
    "stump-during-removal-1.webp",
    "tractor-with-box-blade-leveling-ground.webp",
    "tractor-moving-item-with-grapple.webp",
    "stump-before-ground-leveled.webp",
    "stump-prior-to-removal.webp",
    "photo-of-all-equipment.webp",
    "excavator-and-truck-photo.webp",
    "stump-during-removal.webp",
    "stump-post-removal.webp",
    "stump-during-removal-2.webp",
    "stump-post-removal-1.webp",
]

SERVICE_CATEGORIES = [
    {
        "id": "phase1",
        "label": "Core Outdoor Services",
        "description": "Land clearing, trail clearing, pond bank clearing, ditch clearing, brush cutting, debris removal, pool dig-out support, and tractor services.",
    },
    {
        "id": "clearing",
        "label": "Clearing & Mulching",
        "description": "Trail, brush, forestry mulching, overgrowth, fence line, and access work.",
    },
    {
        "id": "pond_ditch",
        "label": "Pond & Ditch Work",
        "description": "Pond bank clearing, pond cleanup, ditch clearing, and ongoing maintenance.",
    },
    {
        "id": "cleanup",
        "label": "Cleanup & Debris Removal",
        "description": "Yard debris, storm cleanup, property and lot cleanup, and acreage restoration.",
    },
    {
        "id": "maintenance",
        "label": "Property Maintenance",
        "description": "Ongoing outdoor property, pond, and ditch maintenance for long-term land care.",
    },
    {
        "id": "equipment",
        "label": "Equipment & Tractor Services",
        "description": "Owner-operated Kubota equipment and tractor work for outdoor property jobs.",
    },
]


def _svc(
    slug: str,
    name: str,
    *,
    category: str,
    nav: str | None = None,
    form_label: str | None = None,
    phase1: bool = False,
    title: str,
    h1: str,
    desc: str,
    keyword: str,
    intro: str,
    bullets: list[str],
    benefits: list[str],
    ideal_for: list[str],
    related_slugs: list[str],
    mosaic_headline: str,
    mosaic_image: str | None = None,
    index: int = 0,
) -> dict:
    return {
        "slug": slug,
        "name": name,
        "nav": nav or name,
        "form_label": form_label or name,
        "category": category,
        "phase1": phase1,
        "title": title,
        "h1": h1,
        "desc": desc,
        "keyword": keyword,
        "intro": intro,
        "bullets": bullets,
        "benefits": benefits,
        "ideal_for": ideal_for,
        "related_slugs": related_slugs,
        "mosaic_image": mosaic_image or IMAGES[index % len(IMAGES)],
        "mosaic_headline": mosaic_headline,
    }


SERVICES = [
    _svc(
        "land-clearing",
        "Land Clearing",
        category="phase1",
        phase1=True,
        title=f"Land Clearing Services in {AREA}, FL",
        h1=f"Land Clearing Services — {AREA}",
        desc=f"Land clearing for overgrown lots, brush, and acreage in {CITY}, Lakeland, Winter Haven, and surrounding Polk County areas.",
        keyword="land clearing Polk County FL",
        intro=(
            f"Overgrown lots, thick brush, and unmanaged vegetation make property harder to use and harder to maintain. "
            f"Faith Works Outdoor Services clears land for homeowners and property owners across {AREA} using forestry mulching, "
            "brush cutting, and equipment-ready cleanup — outdoor property services, not utility excavation or site development."
        ),
        bullets=[
            "Overgrown lot and acreage clearing",
            "Brush and vegetation removal",
            "Selective clearing around structures and fences",
            "Small-acreage and residential land clearing",
            "Cleanup and debris haul-off after clearing",
        ],
        benefits=[
            "Opens up usable property space",
            "Improves visibility and access across the property",
            "Prepares land for trails, fencing, or future outdoor projects",
            "Equipment-ready for tough Central Florida growth",
        ],
        ideal_for=[
            "Overgrown lots and acreage",
            "Property you want to fence or build on later",
            "Land that has not been maintained in years",
            "Homeowners reclaiming usable yard space",
        ],
        related_slugs=["forestry-mulching", "brush-clearing", "overgrowth-removal", "debris-removal"],
        mosaic_headline="Overgrown lot holding up your plans?",
        mosaic_image="excavator-photo.webp",
        index=0,
    ),
    _svc(
        "trail-clearing",
        "Trail Clearing",
        category="phase1",
        phase1=True,
        title=f"Trail Clearing & Trail Maintenance in Central Florida",
        h1="Trail Clearing & Trail Maintenance — Central Florida",
        desc=f"Cut new trails or restore overgrown trails on private property in {CITY}, Polk County, and surrounding areas.",
        keyword="trail clearing Florida",
        intro=(
            "Whether you need a new access path cut in or an existing trail reopened after years of overgrowth, "
            "Faith Works Outdoor Services helps property owners reclaim usable trails with brush cutters, "
            "mulching equipment, and careful clearing along the path."
        ),
        bullets=[
            "New trail cutting and path opening",
            "Overgrown trail restoration",
            "Brush and low-hanging vegetation removal along paths",
            "Trail edge cleanup and widening where needed",
            "Debris removal from trail work",
        ],
        benefits=[
            "Restores access across large or wooded properties",
            "Improves safety by removing obstructive growth",
            "Helps maintain trails season after season",
            "Ideal for private land, acreage, and rural properties",
        ],
        ideal_for=[
            "Private trails that have grown shut",
            "New paths across acreage or wooded land",
            "Farm and ranch access routes",
            "Properties where you need to reach ponds, barns, or back fields",
        ],
        related_slugs=["access-road-clearing", "brush-clearing", "forestry-mulching", "tractor-services"],
        mosaic_headline="Trails overgrown and hard to use?",
        mosaic_image="tractor.webp",
        index=1,
    ),
    _svc(
        "brush-clearing",
        "Brush Clearing & Brush Cutting",
        category="phase1",
        phase1=True,
        nav="Brush Clearing",
        form_label="Brush Clearing / Brush Cutting",
        title=f"Brush Clearing & Brush Cutting in {AREA}, FL",
        h1=f"Brush Clearing & Brush Cutting — {AREA}",
        desc=f"Brush clearing and brush cutting for overgrown property edges, fields, and wooded areas in {CITY} and Polk County.",
        keyword="brush clearing Polk County FL",
        intro=(
            "Thick brush takes over fast in Central Florida — along fence lines, pond banks, ditches, and unused acreage. "
            "Faith Works Outdoor Services cuts and clears brush using compact tractors, brush cutters, and mulching "
            "equipment sized for residential and rural properties."
        ),
        bullets=[
            "Heavy brush and sapling removal",
            "Brush cutting along property lines and fence rows",
            "Clearing around ponds, ditches, and structures",
            "Selective brush removal where you want to keep trees",
            "Debris cleanup and haul-off after brush work",
        ],
        benefits=[
            "Reclaims usable space from overgrown brush",
            "Improves visibility and property maintenance access",
            "Reduces fire fuel and pest habitat near structures",
            "Pairs well with trail, ditch, and pond bank clearing",
        ],
        ideal_for=[
            "Fence lines swallowed by vegetation",
            "Field edges and property boundaries",
            "Areas too thick to mow with a lawn tractor",
            "Pond banks and ditch lines with heavy brush",
        ],
        related_slugs=["forestry-mulching", "fence-line-clearing", "overgrowth-removal", "tractor-services"],
        mosaic_headline="Brush taking over your property edges?",
        mosaic_image="stump-during-removal-1.webp",
        index=2,
    ),
    _svc(
        "forestry-mulching",
        "Forestry Mulching",
        category="clearing",
        title=f"Forestry Mulching Services in {AREA}, FL",
        h1=f"Forestry Mulching — {AREA}",
        desc=f"Forestry mulching for land clearing, overgrowth removal, and vegetation management in {CITY} and Polk County.",
        keyword="forestry mulching Polk County FL",
        intro=(
            "Forestry mulching grinds vegetation in place — reducing haul-off, opening up land faster, and leaving "
            "a cleaner finish on many clearing jobs. Faith Works Outdoor Services uses mulching equipment for "
            "overgrown acreage, pond banks, fence lines, and property cleanup across Central Florida."
        ),
        bullets=[
            "Forestry mulching for overgrown lots and acreage",
            "Mulching along pond banks and drainage areas",
            "Vegetation reduction for fence lines and access paths",
            "Selective mulching around trees and structures",
            "Follow-up debris cleanup where needed",
        ],
        benefits=[
            "Clears dense vegetation efficiently on large areas",
            "Reduces brush piles compared to cut-and-haul methods",
            "Improves access for ongoing property maintenance",
            "Well suited to Florida undergrowth and saplings",
        ],
        ideal_for=[
            "Dense acreage and wooded undergrowth",
            "Large areas where haul-off is expensive",
            "Pond banks and fence rows with thick vegetation",
            "Properties needing fast vegetation reduction",
        ],
        related_slugs=["land-clearing", "brush-clearing", "overgrowth-removal", "pond-bank-clearing"],
        mosaic_headline="Dense vegetation too thick to cut by hand?",
        mosaic_image="stump-during-removal.webp",
        index=3,
    ),
    _svc(
        "pond-bank-clearing",
        "Pond Bank Clearing",
        category="phase1",
        phase1=True,
        title=f"Pond Bank Clearing & Brush Removal in Polk County",
        h1="Pond Bank Clearing & Brush Removal — Polk County",
        desc=f"Clean overgrown pond banks with mulching equipment and brush cutters in {CITY} and Polk County.",
        keyword="pond bank clearing Polk County",
        intro=(
            "Overgrown pond banks reduce access, block views, and make maintenance harder. Faith Works Outdoor Services "
            "clears pond banks using mulching equipment and brush cutters built for tough vegetation along water edges "
            "and retention areas — pond bank work and mulching, not engineered stormwater installation."
        ),
        bullets=[
            "Overgrown pond bank clearing",
            "Brush cutting along pond edges",
            "Mulching of thick vegetation on banks",
            "Access improvement around ponds and retention areas",
            "Debris cleanup after bank work",
        ],
        benefits=[
            "Improves pond appearance and visibility",
            "Makes bank maintenance easier over time",
            "Reduces overgrowth encroaching into the water edge",
            "Professional equipment for dense Florida vegetation",
        ],
        ideal_for=[
            "Pond banks you cannot reach or maintain",
            "Retention ponds on residential or rural property",
            "Shorelines blocked by brush and saplings",
            "Property owners who want a cleaner water edge",
        ],
        related_slugs=["pond-cleanup", "pond-management", "brush-clearing", "forestry-mulching"],
        mosaic_headline="Pond banks overgrown and blocking access?",
        mosaic_image="stump-during-removal-1.webp",
        index=4,
    ),
    _svc(
        "pond-cleanup",
        "Pond Cleanup",
        category="pond_ditch",
        title=f"Pond Cleanup Services in {AREA}, FL",
        h1=f"Pond Cleanup — {AREA}",
        desc=f"Pond cleanup for overgrown edges, floating debris, and shoreline maintenance in {CITY} and Polk County.",
        keyword="pond cleanup Polk County FL",
        intro=(
            "Ponds collect debris, overgrowth, and shoreline clutter that makes the water harder to enjoy and maintain. "
            "Faith Works Outdoor Services provides pond cleanup — clearing banks, removing reachable debris, and "
            "helping property owners restore a cleaner shoreline. This is outdoor pond cleanup and mulching work, "
            "not utility or engineered drainage system installation."
        ),
        bullets=[
            "Shoreline and pond edge cleanup",
            "Removal of reachable floating and bank debris",
            "Overgrowth clearing along pond perimeters",
            "Access improvement for ongoing pond maintenance",
            "Coordination with property owners on scope and access",
        ],
        benefits=[
            "Improves pond appearance and usability",
            "Makes seasonal pond maintenance easier",
            "Clears visual clutter from banks and edges",
            "Owner-operated communication from estimate to completion",
        ],
        ideal_for=[
            "Ponds with accumulated shoreline debris",
            "Retention areas that look neglected",
            "Property owners preparing land for sale or use",
            "Ponds paired with bank clearing or maintenance plans",
        ],
        related_slugs=["pond-bank-clearing", "pond-management", "property-cleanup", "debris-removal"],
        mosaic_headline="Pond looking neglected and overgrown?",
        mosaic_image="tractor-with-box-blade-leveling-ground.webp",
        index=5,
    ),
    _svc(
        "ditch-clearing",
        "Ditch Clearing",
        category="phase1",
        phase1=True,
        title=f"Ditch Clearing & Runoff Cleanup in {CITY}, FL",
        h1=f"Ditch Clearing & Runoff Cleanup — {CITY} & Polk County",
        desc=f"Clean overgrown ditches and runoff paths in {CITY}, Lakeland, and Polk County using mulching equipment and brush cutters.",
        keyword="ditch clearing Auburndale",
        intro=(
            "Florida rain season puts real pressure on ditches and runoff paths. When ditches become overgrown, "
            "water movement and property drainage suffer. Faith Works Outdoor Services clears overgrown ditches "
            "and runoff areas — vegetation and debris removal, not engineered stormwater or sewer system work."
        ),
        bullets=[
            "Overgrown ditch clearing",
            "Runoff path and swale cleanup",
            "Brush cutting in drainage easements",
            "Vegetation removal from ditch lines",
            "Basic ditch-line reshaping where appropriate",
        ],
        benefits=[
            "Helps water move more freely during heavy rain",
            "Reduces blocked or overgrown drainage paths",
            "Improves property maintenance access",
            "Equipment suited for dense ditch-line growth",
        ],
        ideal_for=[
            "Ditches clogged with brush before rain season",
            "Swales and runoff paths on acreage",
            "Drainage easements that have not been maintained",
            "Properties with recurring standing water from overgrowth",
        ],
        related_slugs=["ditch-maintenance", "brush-clearing", "forestry-mulching", "tractor-services"],
        mosaic_headline="Ditches clogged before rain season?",
        mosaic_image="tractor-with-box-blade-leveling-ground.webp",
        index=6,
    ),
    _svc(
        "debris-removal",
        "Debris Removal",
        category="phase1",
        phase1=True,
        title=f"Debris Removal Services in {AREA}, FL",
        h1=f"Debris Removal — {AREA}",
        desc=f"Debris removal for yard cleanup, storm cleanup, property cleanup, and lot cleanup in {CITY} and Polk County.",
        keyword="debris removal Polk County FL",
        intro=(
            "Land clearing, storms, and property projects all leave debris behind. Faith Works Outdoor Services "
            "removes yard debris, brush piles, storm mess, and outdoor cleanup material so your property looks "
            "finished when the job is done. One call can cover multiple cleanup areas on the same property."
        ),
        bullets=[
            "Yard debris and brush pile removal",
            "Storm debris cleanup and haul-off",
            "Property and lot cleanup after clearing",
            "Leftover material from land and brush projects",
            "Non-hazardous outdoor debris only",
        ],
        benefits=[
            "Finishes clearing jobs the right way",
            "Saves time after storms or major cleanup",
            "Combines multiple cleanup types in one visit",
            "Leaves the property cleaner and more usable",
        ],
        ideal_for=[
            "Brush piles left after clearing work",
            "Post-storm yard and acreage cleanup",
            "Vacant lots with accumulated outdoor debris",
            "Property owners who want haul-off handled in one trip",
        ],
        related_slugs=["yard-debris-removal", "storm-debris-cleanup", "property-cleanup", "lot-cleanup"],
        mosaic_headline="Brush piles and debris still on site?",
        mosaic_image="tractor-moving-item-with-grapple.webp",
        index=7,
    ),
    _svc(
        "yard-debris-removal",
        "Yard Debris Removal",
        category="cleanup",
        form_label="Yard Debris Removal",
        title=f"Yard Debris Removal in Polk County, FL",
        h1="Yard Debris & Brush Pile Removal — Polk County",
        desc=f"Remove yard debris, brush piles, and outdoor cleanup material in {CITY} and surrounding Polk County communities.",
        keyword="yard debris removal Polk County",
        intro=(
            "Yard projects, tree work, and clearing jobs leave debris behind. Faith Works Outdoor Services removes "
            "yard debris, brush piles, and non-hazardous outdoor cleanup material from residential and rural properties."
        ),
        bullets=[
            "Yard debris and brush pile removal",
            "Outdoor cleanup haul-off support",
            "Leftover material from land and brush projects",
            "Property cleanup after clearing work",
            "Non-hazardous outdoor debris only",
        ],
        benefits=[
            "Leaves the yard cleaner and more usable",
            "Saves time after major cleanup projects",
            "Works well combined with clearing services",
            "Photo-based estimates for faster scheduling",
        ],
        ideal_for=[
            "Residential yards with brush piles",
            "Homeowners after DIY or contractor cleanup",
            "Properties with scattered yard debris",
            "Follow-up haul-off after land clearing",
        ],
        related_slugs=["debris-removal", "storm-debris-cleanup", "property-cleanup", "land-clearing"],
        mosaic_headline="Yard debris piling up after a project?",
        mosaic_image="tractor-moving-item-with-grapple.webp",
        index=8,
    ),
    _svc(
        "storm-debris-cleanup",
        "Storm Debris Cleanup",
        category="cleanup",
        title=f"Storm Debris Cleanup in {AREA}, FL",
        h1=f"Storm Debris Cleanup — {AREA}",
        desc=f"Storm debris cleanup for fallen branches, yard mess, and outdoor property damage in {CITY} and Polk County.",
        keyword="storm debris cleanup Polk County FL",
        intro=(
            "Storms leave behind branches, scattered debris, and blocked access across Florida properties. "
            "Faith Works Outdoor Services helps homeowners and property owners clean up storm debris — "
            "clearing paths, hauling brush, and restoring usable outdoor space after weather events."
        ),
        bullets=[
            "Fallen branch and limb cleanup",
            "Storm-scattered yard debris removal",
            "Access path and driveway clearing after storms",
            "Brush pile consolidation and haul-off",
            "Follow-up property cleanup as needed",
        ],
        benefits=[
            "Restores safe access after storm damage",
            "Clears debris before it attracts pests or mold",
            "Reduces trip hazards across the property",
            "Fast photo-based estimates for storm cleanup",
        ],
        ideal_for=[
            "Properties hit by Florida storm season",
            "Fallen limbs blocking driveways or trails",
            "Yards with scattered storm debris",
            "Acreage needing post-storm access restored",
        ],
        related_slugs=["debris-removal", "yard-debris-removal", "property-cleanup", "access-road-clearing"],
        mosaic_headline="Storm left your property a mess?",
        mosaic_image="tractor-moving-item-with-grapple.webp",
        index=9,
    ),
    _svc(
        "property-cleanup",
        "Property Cleanup",
        category="cleanup",
        title=f"Property Cleanup Services in {AREA}, FL",
        h1=f"Outdoor Property Cleanup — {AREA}",
        desc=f"Full outdoor property cleanup for overgrown yards, acreage, and unused land in {CITY} and Polk County.",
        keyword="property cleanup Polk County FL",
        intro=(
            "Unused acreage, rental properties, and long-neglected yards need more than a quick mow. "
            "Faith Works Outdoor Services provides outdoor property cleanup — combining brush clearing, debris removal, "
            "and equipment-ready land work to help properties look maintained again."
        ),
        bullets=[
            "Full outdoor property cleanup projects",
            "Overgrown yard and acreage restoration",
            "Brush, debris, and clutter removal",
            "Clearing around structures and driveways",
            "One-call cleanup for multiple problem areas",
        ],
        benefits=[
            "Brings neglected properties back under control",
            "Improves curb appeal and usability",
            "Combines multiple services in one project",
            "Direct communication with Tyler from start to finish",
        ],
        ideal_for=[
            "Rental or inherited properties needing cleanup",
            "Homes with multiple overgrown areas",
            "Property owners preparing to sell or lease",
            "Acreage that has not been touched in seasons",
        ],
        related_slugs=["lot-cleanup", "acreage-cleanup", "debris-removal", "land-clearing"],
        mosaic_headline="Property looking neglected and overgrown?",
        mosaic_image="stump-before-ground-leveled.webp",
        index=10,
    ),
    _svc(
        "lot-cleanup",
        "Lot Cleanup",
        category="cleanup",
        title=f"Lot Cleanup Services in {AREA}, FL",
        h1=f"Lot Cleanup — {AREA}",
        desc=f"Lot cleanup for vacant land, build-ready sites, and overgrown parcels in {CITY} and Polk County.",
        keyword="lot cleanup Polk County FL",
        intro=(
            "Vacant lots and unused parcels collect brush, trash, and overgrowth fast in Central Florida. "
            "Faith Works Outdoor Services clears and cleans lots for property owners, investors, and families "
            "preparing land for sale, fencing, or future use."
        ),
        bullets=[
            "Vacant lot clearing and cleanup",
            "Overgrown parcel brush removal",
            "Trash and debris removal from outdoor lots",
            "Access improvement for future projects",
            "Photo-based estimates for lot size and scope",
        ],
        benefits=[
            "Makes vacant lots easier to show and sell",
            "Reduces code and neighbor concerns on neglected parcels",
            "Prepares land for fencing, trails, or future plans",
            "Equipment-ready for larger lot cleanup jobs",
        ],
        ideal_for=[
            "Vacant parcels in Polk County",
            "Lots overgrown before a sale or build",
            "Investment properties needing a clean appearance",
            "Land you plan to fence or clear for family use",
        ],
        related_slugs=["land-clearing", "acreage-cleanup", "property-cleanup", "debris-removal"],
        mosaic_headline="Vacant lot overgrown and unusable?",
        mosaic_image="stump-prior-to-removal.webp",
        index=11,
    ),
    _svc(
        "acreage-cleanup",
        "Acreage Cleanup",
        category="cleanup",
        title=f"Acreage Cleanup Services in {AREA}, FL",
        h1=f"Acreage Cleanup — {AREA}",
        desc=f"Acreage cleanup for overgrown fields, rural land, and large properties in {CITY} and Polk County.",
        keyword="acreage cleanup Polk County FL",
        intro=(
            "Large properties and rural acreage collect brush, overgrowth, and debris across fields, edges, and access paths. "
            "Faith Works Outdoor Services provides acreage cleanup — one of the most common reasons property owners call — "
            "combining land clearing, trail work, brush cutting, and debris haul-off for usable land again."
        ),
        bullets=[
            "Large-acreage brush and overgrowth clearing",
            "Field edge and open-area cleanup",
            "Access path and trail reopening on acreage",
            "Debris and brush pile haul-off",
            "Multi-area scoping for large rural properties",
        ],
        benefits=[
            "Restores usable land across large properties",
            "Improves access to ponds, barns, and back fields",
            "Combines clearing, trails, and cleanup in one plan",
            "Equipment suited to rural Polk County acreage",
        ],
        ideal_for=[
            "Rural acreage that has grown up unchecked",
            "Properties where trails and access are blocked",
            "Landowners managing fields and wooded edges",
            "One of the most common inquiry types we see",
        ],
        related_slugs=["land-clearing", "trail-clearing", "access-road-clearing", "overgrowth-removal"],
        mosaic_headline="Acreage overgrown and hard to use?",
        mosaic_image="excavator-photo.webp",
        index=12,
    ),
    _svc(
        "access-road-clearing",
        "Access Road Clearing",
        category="clearing",
        title=f"Access Road Clearing in {AREA}, FL",
        h1=f"Access Road Clearing — {AREA}",
        desc=f"Clear overgrown access roads, drive paths, and private lanes in {CITY} and rural Polk County properties.",
        keyword="access road clearing Florida",
        intro=(
            "Private access roads, farm lanes, and long drive paths disappear under Florida growth within a season. "
            "Faith Works Outdoor Services clears access roads so you can reach barns, ponds, fields, and back acreage "
            "safely again — using tractors, brush cutters, and clearing equipment."
        ),
        bullets=[
            "Overgrown access road and lane clearing",
            "Private drive path reopening",
            "Brush cutting along road edges",
            "Debris removal from cleared access paths",
            "Width and clearance planning with property owners",
        ],
        benefits=[
            "Restores vehicle access to back acreage",
            "Improves safety on overgrown private roads",
            "Reduces damage from branches and hidden obstacles",
            "Ideal for rural and acreage properties",
        ],
        ideal_for=[
            "Farm lanes and private drive paths",
            "Roads to ponds, barns, or hunting areas",
            "Properties where you cannot reach the back acreage",
            "Rural land with seasonal overgrowth on access routes",
        ],
        related_slugs=["trail-clearing", "acreage-cleanup", "brush-clearing", "tractor-services"],
        mosaic_headline="Can't reach the back of your property?",
        mosaic_image="tractor.webp",
        index=13,
    ),
    _svc(
        "fence-line-clearing",
        "Fence Line Clearing",
        category="clearing",
        title=f"Fence Line Clearing in {AREA}, FL",
        h1=f"Fence Line Clearing — {AREA}",
        desc=f"Clear overgrown fence lines and property boundaries in {CITY} and Polk County with brush cutters and mulching equipment.",
        keyword="fence line clearing Polk County FL",
        intro=(
            "Fence lines are where Florida vegetation grows fastest — wrapping posts, pushing on wire, and blocking "
            "maintenance access. Faith Works Outdoor Services clears fence lines and property boundaries so fences "
            "stay visible, accessible, and easier to maintain."
        ),
        bullets=[
            "Overgrown fence line brush removal",
            "Boundary and property line clearing",
            "Mulching along fence rows where appropriate",
            "Selective clearing to protect fence integrity",
            "Debris cleanup after fence line work",
        ],
        benefits=[
            "Extends fence life by reducing vegetation pressure",
            "Makes fence repairs and inspections easier",
            "Clears sight lines along property boundaries",
            "Pairs well with land and lot clearing projects",
        ],
        ideal_for=[
            "Fence lines you cannot see or maintain",
            "Property boundaries overgrown with saplings",
            "Pasture and acreage fence maintenance",
            "Homes with privacy fences buried in brush",
        ],
        related_slugs=["brush-clearing", "overgrowth-removal", "land-clearing", "forestry-mulching"],
        mosaic_headline="Fence line disappeared into the brush?",
        mosaic_image="stump-during-removal-2.webp",
        index=14,
    ),
    _svc(
        "overgrowth-removal",
        "Overgrowth Removal",
        category="clearing",
        title=f"Overgrowth Removal in {AREA}, FL",
        h1=f"Overgrowth Removal — {AREA}",
        desc=f"Overgrowth removal for yards, acreage, pond banks, and unused outdoor areas in {CITY} and Polk County.",
        keyword="overgrowth removal Polk County FL",
        intro=(
            "Central Florida overgrowth spreads quickly — saplings, vines, and thick brush that swallow yards and "
            "acreage whole. Faith Works Outdoor Services removes overgrowth with brush cutters, forestry mulching, "
            "and equipment-ready clearing tailored to your property."
        ),
        bullets=[
            "Heavy overgrowth cutting and clearing",
            "Sapling and vine removal",
            "Overgrowth along structures, fences, and ponds",
            "Acreage and yard overgrowth restoration",
            "Debris haul-off after overgrowth removal",
        ],
        benefits=[
            "Reclaims usable outdoor space quickly",
            "Reduces pest and snake habitat near structures",
            "Improves property appearance and maintenance access",
            "Custom scope based on photos and property walkthrough",
        ],
        ideal_for=[
            "Yards and acreage swallowed by saplings",
            "Overgrowth along ponds, trails, and structures",
            "Properties where mowing is no longer enough",
            "One of the most common types of cleanup calls",
        ],
        related_slugs=["brush-clearing", "forestry-mulching", "acreage-cleanup", "land-clearing"],
        mosaic_headline="Overgrowth swallowing your yard or acreage?",
        mosaic_image="stump-post-removal.webp",
        index=15,
    ),
    _svc(
        "pool-dig-out-support",
        "Pool Dig-Out Support",
        category="phase1",
        phase1=True,
        title=f"Pool Dig-Out Support & Dirt Removal in {CITY}, FL",
        h1="Pool Dig-Out Support & Dirt Removal — Polk County",
        desc=f"Pool dig-out support and dirt removal for pool installation projects in {CITY}, Lakeland, Winter Haven, and Polk County.",
        keyword="pool dig out support Polk County FL",
        intro=(
            "Installing a pool often means moving a serious amount of dirt. Faith Works Outdoor Services provides "
            "pool dig-out support and dirt removal so your licensed pool contractor can focus on the install while "
            "your property gets cleaned up properly. We do not install pools or hold pool contractor licensing — "
            "we support dig-out cleanup and haul-off under the pool builder's project."
        ),
        bullets=[
            "Pool dig-out dirt removal and haul-off support",
            "Site cleanup after pool dig-out",
            "Fill and spoil pile management support",
            "Coordination with licensed pool installers",
            "Property access planning for equipment",
        ],
        benefits=[
            "Keeps the job site cleaner during pool work",
            "Reduces delays caused by piled-up fill and debris",
            "Helps restore usable yard space after digging",
            "Support role under licensed pool contractors — not direct pool contracting",
        ],
        ideal_for=[
            "Homeowners with a licensed pool builder handling the install",
            "Pool digs with dirt piled on site",
            "Projects needing haul-off and yard cleanup support",
            "Contractors needing a local dig-out cleanup partner",
        ],
        related_slugs=["debris-removal", "equipment-services", "land-clearing", "property-cleanup"],
        mosaic_headline="Pool dig leaving dirt piled up on site?",
        mosaic_image="excavator-and-truck-photo.webp",
        index=16,
    ),
    _svc(
        "property-maintenance",
        "Property Maintenance",
        category="maintenance",
        title=f"Outdoor Property Maintenance in {AREA}, FL",
        h1=f"Outdoor Property Maintenance — {AREA}",
        desc=f"Ongoing outdoor property maintenance for acreage, trails, fence lines, and cleared land in {CITY} and Polk County.",
        keyword="outdoor property maintenance Polk County FL",
        intro=(
            "Cleared land does not stay cleared on its own in Central Florida. Faith Works Outdoor Services provides "
            "ongoing outdoor property maintenance — keeping trails open, fence lines cut back, and acreage manageable "
            "season after season without chasing utility or excavation licensing you may not need yet."
        ),
        bullets=[
            "Seasonal trail and access path maintenance",
            "Fence line and boundary touch-up cutting",
            "Acreage edge and field maintenance",
            "Follow-up clearing after initial cleanup projects",
            "Scheduled maintenance plans for rural properties",
        ],
        benefits=[
            "Keeps property usable year-round",
            "Costs less than full re-clearing every few years",
            "Builds a long-term land care relationship",
            "Ideal Phase 2 growth path for outdoor services",
        ],
        ideal_for=[
            "Property owners who already had a major cleanup",
            "Acreage and rural land needing seasonal touch-ups",
            "Landlords and families managing multiple areas",
            "Owners building toward a maintenance-focused business model",
        ],
        related_slugs=["trail-clearing", "fence-line-clearing", "overgrowth-removal", "ditch-maintenance"],
        mosaic_headline="Property growing back faster than you can maintain it?",
        mosaic_image="tractor.webp",
        index=17,
    ),
    _svc(
        "pond-management",
        "Pond Management",
        category="maintenance",
        title=f"Pond Management Services in {AREA}, FL",
        h1=f"Pond Management — {AREA}",
        desc=f"Pond management for shoreline maintenance, bank clearing, and ongoing pond cleanup in {CITY} and Polk County.",
        keyword="pond management Polk County FL",
        intro=(
            "Ponds need ongoing attention — not just a one-time cleanup. Faith Works Outdoor Services provides pond "
            "management through bank clearing, shoreline cleanup, and seasonal maintenance so your pond stays accessible "
            "and presentable. This is outdoor pond care and mulching — not engineered stormwater or utility work."
        ),
        bullets=[
            "Seasonal pond bank and shoreline maintenance",
            "Recurring overgrowth control along water edges",
            "Reachable debris and shoreline cleanup",
            "Mulching and brush cutting on pond perimeters",
            "Maintenance plans paired with initial pond cleanup",
        ],
        benefits=[
            "Keeps ponds looking maintained year-round",
            "Reduces the cost of full bank re-clearing",
            "Pairs naturally with pond bank clearing services",
            "Aligns with long-term outdoor services growth",
        ],
        ideal_for=[
            "Property owners with ponds that regrow every season",
            "Homes and acreage with retention ponds",
            "Clients who want recurring outdoor property care",
            "Landowners focused on pond banks and trails",
        ],
        related_slugs=["pond-bank-clearing", "pond-cleanup", "brush-clearing", "property-maintenance"],
        mosaic_headline="Pond needs more than a one-time cleanup?",
        mosaic_image="stump-during-removal-1.webp",
        index=18,
    ),
    _svc(
        "ditch-maintenance",
        "Ditch Maintenance",
        category="maintenance",
        title=f"Ditch Maintenance Services in {AREA}, FL",
        h1=f"Ditch Maintenance — {AREA}",
        desc=f"Ditch maintenance for runoff paths, swales, and drainage easements in {CITY} and Polk County.",
        keyword="ditch maintenance Polk County FL",
        intro=(
            "Ditches and runoff paths clog back up quickly in Florida. Faith Works Outdoor Services provides ditch "
            "maintenance — keeping vegetation cut back and paths open so water can move during rain season. "
            "This is ditch-line clearing and maintenance, not engineered stormwater system installation."
        ),
        bullets=[
            "Seasonal ditch and swale maintenance",
            "Vegetation cutback along runoff paths",
            "Recurring clearing in drainage easements",
            "Follow-up work after initial ditch clearing",
            "Maintenance visits before heavy rain season",
        ],
        benefits=[
            "Reduces repeat flooding from overgrown ditches",
            "Costs less than full ditch re-clearing each year",
            "Keeps property drainage paths accessible",
            "Natural fit after an initial ditch clearing project",
        ],
        ideal_for=[
            "Properties with ditches that clog every season",
            "Acreage with swales and runoff paths",
            "Owners who want preventive maintenance before storms",
            "Land cleared once and needing ongoing care",
        ],
        related_slugs=["ditch-clearing", "brush-clearing", "property-maintenance", "tractor-services"],
        mosaic_headline="Ditches clogging back up every season?",
        mosaic_image="tractor-with-box-blade-leveling-ground.webp",
        index=19,
    ),
    _svc(
        "equipment-services",
        "Equipment Services",
        category="equipment",
        title=f"Outdoor Equipment Services in {AREA}, FL",
        h1=f"Equipment Services — {AREA}",
        desc=f"Kubota equipment services for land clearing and outdoor property work in {CITY} and Polk County.",
        keyword="equipment services land clearing Florida",
        intro=(
            "Faith Works Outdoor Services runs Kubota compact equipment, dump trailers, and support machinery for "
            "outdoor property work across Central Florida. Equipment services cover operator time and machinery for "
            "clearing, cleanup, and property maintenance — not utility trenching or engineered infrastructure installation."
        ),
        bullets=[
            "Kubota compact equipment for clearing and cleanup support",
            "Compact tractor with loader, grapple, and box blade",
            "Dump trailer and haul-off support",
            "Equipment matched to property access and scope",
            "Owner-operated — Tyler runs the equipment on your job",
        ],
        benefits=[
            "Right-sized equipment for residential and rural properties",
            "No subcontractor chain — direct operator communication",
            "Versatile fleet for clearing, debris, and cleanup",
            "Photo-based scoping before equipment mobilization",
        ],
        ideal_for=[
            "Jobs needing the right machine, not just labor",
            "Properties with tight access considerations",
            "Clearing and cleanup projects combined",
            "Contractors needing local equipment support",
        ],
        related_slugs=["tractor-services", "land-clearing", "debris-removal", "pool-dig-out-support"],
        mosaic_headline="Need the right equipment on your property?",
        mosaic_image="photo-of-all-equipment.webp",
        index=20,
    ),
    _svc(
        "tractor-services",
        "Tractor Services",
        category="phase1",
        phase1=True,
        title=f"Tractor Services in {AREA}, FL",
        h1=f"Tractor Services — {AREA}",
        desc=f"Tractor services for brush cutting, land clearing, ditch work, and property cleanup in {CITY} and Polk County.",
        keyword="tractor services land clearing Florida",
        intro=(
            "Compact tractors with brush cutters, loaders, grapples, and box blades handle a wide range of outdoor "
            "property work in Central Florida. Faith Works Outdoor Services provides tractor services for brush "
            "cutting, trail maintenance, ditch clearing, debris handling, and general land cleanup."
        ),
        bullets=[
            "Brush cutting and mowing with tractor attachments",
            "Loader and grapple work for debris and material",
            "Box blade leveling and light ground work",
            "Trail, ditch, and fence line maintenance",
            "Property cleanup with tractor-supported haul-off",
        ],
        benefits=[
            "Efficient clearing on paths, ditches, and open acreage",
            "Versatile attachments for multiple job types",
            "Less ground disturbance than heavy equipment on many jobs",
            "Ideal complement to forestry mulching and land clearing",
        ],
        ideal_for=[
            "Trail, ditch, and fence line work",
            "Acreage needing brush cutting and light grading",
            "Debris handling and property cleanup",
            "Properties where a tractor is the right tool for the job",
        ],
        related_slugs=["brush-clearing", "ditch-clearing", "access-road-clearing", "equipment-services"],
        mosaic_headline="Need tractor work on your acreage or lot?",
        mosaic_image="tractor.webp",
        index=21,
    ),
]

SERVICE_COUNT = len(SERVICES)
PHASE1_SERVICES = [s for s in SERVICES if s["phase1"]]
PHASE1_COUNT = len(PHASE1_SERVICES)

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}


def services_for_category(category_id: str) -> list[dict]:
    return [s for s in SERVICES if s["category"] == category_id]
