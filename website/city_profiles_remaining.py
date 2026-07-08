"""Remaining unique city profiles for Faith Works service area pages."""
from __future__ import annotations

REMAINING_CITY_PROFILES: dict[str, dict] = {
    "lake-alfred-fl": {
        "meta_description": (
            "Land clearing and pond bank work in Lake Alfred, FL — citrus country and lake-adjacent lots. "
            "Faith Works from Auburndale. Free photo estimates. Call (863) 272-1596."
        ),
        "hook": (
            "Lake Alfred sits between Auburndale and Winter Haven with citrus heritage, small-lake frontage, "
            "and residential lots that often hide overgrown rear acreage."
        ),
        "context": (
            "Florida Southern College's nearby presence and Polk State activity mean Lake Alfred has a mix of "
            "student rentals, family homes, and grove-adjacent land where fence lines and pond banks need "
            "equipment-based clearing."
        ),
        "local_detail": (
            "Properties along Lake Haines and toward the US-92 corridor frequently combine ditch maintenance "
            "with rear-lot brush removal in one visit."
        ),
        "property_types": [
            "Citrus grove transition parcels near US-92",
            "Lake Haines adjacent homes with brush-choked banks",
            "Student-area rental yards with rear overgrowth",
            "Small-acreage homesteads toward Winter Haven",
            "Vacant lots near downtown Lake Alfred redevelopment",
        ],
        "common_jobs": [
            "Grove-edge and fence line clearing on former citrus parcels",
            "Pond bank brush cutback on Lake Haines properties",
            "Overgrown rental lot cleanup before turnover",
            "Ditch vegetation removal along US-92 frontage",
            "Forestry mulching on sapling-choked acreage",
            "Trail access reopening on multi-lot parcels",
        ],
        "intent_routes": [
            {"label": "Grove-edge clearing", "slug": "fence-line-clearing", "text": "Reopen fence lines on Lake Alfred grove and acreage parcels."},
            {"label": "Lake Haines pond banks", "slug": "pond-bank-clearing", "text": "Trim brush on private banks along Lake Haines."},
            {"label": "Rental lot cleanup", "slug": "lot-cleanup", "text": "Clear overgrown yards on Lake Alfred rental properties."},
            {"label": "Acreage mulching", "slug": "forestry-mulching", "text": "Mulch thick undergrowth on small Lake Alfred acreage."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works clear small Lake Alfred citrus parcels?",
                "Yes. Former grove edges and small citrus parcels around Lake Alfred are common — send photos of tree lines, fence runs, and access gates for scope review.",
            ),
            (
                "How close is Lake Alfred to Faith Works headquarters?",
                "Lake Alfred is minutes from our Auburndale base, which helps with quick estimate review and scheduling across eastern Polk County.",
            ),
        ],
        "strip_note": "Lake Alfred grove edges, Lake Haines banks, and rental lot cleanup.",
    },
    "bartow-fl": {
        "meta_description": (
            "Land clearing and outdoor property cleanup in Bartow, FL — Polk County seat acreage and pond work. "
            "Faith Works owner-operated from Auburndale. Free photo estimates."
        ),
        "hook": (
            "As the Polk County seat, Bartow combines historic neighborhoods, courthouse-area commercial parcels, "
            "and rural land toward Fort Meade where acreage clearing is routine."
        ),
        "context": (
            "Faith Works serves Bartow property owners dealing with overgrown county-line acreage, pond edges on "
            "south Polk lakes, and ditch lines along rural roads where vegetation blocks drainage paths each summer."
        ),
        "local_detail": (
            "Land toward Homeland and Fort Meade often involves longer fence runs and ranch-road access that need "
            "planning before equipment arrives."
        ),
        "property_types": [
            "Historic Bartow homes with large rear wooded sections",
            "County-seat commercial pads with brush perimeters",
            "South Polk acreage toward Fort Meade and Homeland",
            "Pond-adjacent rural homesteads off CR-640",
            "Vacant parcels near SR-60 commercial corridors",
        ],
        "common_jobs": [
            "Acreage clearing on south Polk parcels",
            "Pond bank cleanup on rural Bartow water features",
            "Commercial perimeter brush removal near downtown",
            "Ditch clearing on county-road frontage",
            "Property cleanup before sale or probate",
            "Forestry mulching on wooded homestead sections",
        ],
        "intent_routes": [
            {"label": "South Polk acreage", "slug": "acreage-cleanup", "text": "Clear overgrown acreage on Bartow and south Polk parcels."},
            {"label": "Pond and ditch work", "slug": "pond-bank-clearing", "text": "Clean private pond banks and outdoor ditch lines near Bartow."},
            {"label": "Commercial edges", "slug": "property-cleanup", "text": "Restore visibility on brush-choked commercial perimeters."},
            {"label": "Ranch road access", "slug": "access-road-clearing", "text": "Reopen access paths on Bartow rural properties."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve rural Bartow toward Fort Meade?",
                "Yes. South Polk acreage between Bartow and Fort Meade is within our travel range — send photos showing fence lines, pond edges, and road access.",
            ),
            (
                "Can Faith Works help with Bartow probate or estate property cleanup?",
                "Overgrown estate and vacant parcels in Bartow are common requests. Photo-based estimates help establish scope before any clearing begins.",
            ),
        ],
        "strip_note": "Bartow acreage, pond banks, and south Polk property cleanup.",
    },
    "haines-city-fl": {
        "meta_description": (
            "Land clearing and ditch work in Haines City, FL — US-27 growth corridor and acreage cleanup. "
            "Faith Works from Auburndale. Photo-based estimates for Polk County properties."
        ),
        "hook": (
            "Haines City straddles the US-27 corridor between Winter Haven and Davenport, where fast residential "
            "growth meets older citrus acreage and drainage ditches that need regular clearing."
        ),
        "context": (
            "New subdivisions near Posner Park and Legacy Park often back up to unmanaged conservation strips, "
            "former grove land, and pond edges that outpace what standard lawn crews handle with mowers alone."
        ),
        "local_detail": (
            "Properties along Old Polk City Road and toward Dundee frequently need fence line and ditch work "
            "combined when summer growth closes access between lots."
        ),
        "property_types": [
            "New-build lots with rear conservation overgrowth",
            "Former citrus acreage being converted near US-27",
            "Pond-adjacent homes in eastern Haines City",
            "Commercial pads along US-27 with brush perimeters",
            "Vacant parcels awaiting development near Posner Park",
        ],
        "common_jobs": [
            "Rear lot clearing on new Haines City subdivisions",
            "Ditch and swale cleanup along US-27 frontage",
            "Fence line reopening on grove-transition parcels",
            "Pond bank brush removal on private retention areas",
            "Forestry mulching on sapling-choked acreage",
            "Lot cleanup before builder handoff or resale",
        ],
        "intent_routes": [
            {"label": "US-27 ditch lines", "slug": "ditch-clearing", "text": "Clear vegetation from drainage paths along Haines City road frontage."},
            {"label": "New subdivision edges", "slug": "land-clearing", "text": "Open overgrown rear sections on Haines City build sites."},
            {"label": "Conservation borders", "slug": "fence-line-clearing", "text": "Reopen fence lines where growth meets subdivision boundaries."},
            {"label": "Retention pond banks", "slug": "pond-bank-clearing", "text": "Cut back brush on private pond and retention edges in Haines City."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works clear land behind new Haines City subdivisions?",
                "Yes. Rear conservation buffers and former grove edges behind new Haines City homes are frequent requests — photos showing property lines help confirm scope.",
            ),
            (
                "Can you work along the US-27 corridor in Haines City?",
                "US-27 frontage properties with ditch lines and overgrown acreage are within our Polk County service area. Send address and photos for estimate review.",
            ),
        ],
        "strip_note": "Haines City US-27 ditch lines, subdivision edges, and acreage cleanup.",
    },
    "davenport-fl": {
        "meta_description": (
            "Land clearing and lot cleanup in Davenport, FL — I-4 corridor and ChampionsGate acreage. "
            "Faith Works brush cutting and pond work from Auburndale. Free estimates."
        ),
        "hook": (
            "Davenport's I-4 position ties vacation-rental neighborhoods, ChampionsGate development, and former "
            "citrus land where overgrown lots and pond banks need equipment-based clearing."
        ),
        "context": (
            "Short-term rental properties and long-term homes alike often have rear acreage, retention ponds, "
            "and fence lines that grow shut between seasons — especially on parcels transitioning from agriculture "
            "to residential use north of US-192."
        ),
        "local_detail": (
            "Land toward Four Corners and the Osceola line mixes Polk citrus remnants with newer plats where "
            "access roads and ditch maintenance must be planned before compact equipment arrives."
        ),
        "property_types": [
            "ChampionsGate area lots with rear wooded buffers",
            "Vacation rental properties with overgrown side yards",
            "Former citrus parcels near US-27 and I-4",
            "Retention pond edges on newer Davenport plats",
            "Acreage toward Four Corners awaiting build prep",
        ],
        "common_jobs": [
            "Lot clearing before vacation rental improvements",
            "Retention pond bank brush cutback",
            "Fence line reopening on I-4 corridor parcels",
            "Forestry mulching on former grove sections",
            "Access road clearing on multi-acre Davenport land",
            "Debris removal after storm events along I-4",
        ],
        "intent_routes": [
            {"label": "I-4 corridor lots", "slug": "lot-cleanup", "text": "Clear overgrown Davenport lots before sale, build, or rental turnover."},
            {"label": "ChampionsGate acreage", "slug": "land-clearing", "text": "Open wooded buffers and rear sections on Davenport corridor properties."},
            {"label": "Retention pond edges", "slug": "pond-cleanup", "text": "Clean brush on private retention and pond banks in Davenport subdivisions."},
            {"label": "Grove-transition mulching", "slug": "forestry-mulching", "text": "Mulch saplings on former citrus land around Davenport."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Davenport near ChampionsGate and I-4?",
                "Yes. Davenport properties along the I-4 and US-27 corridors are within our travel range from Auburndale — send photos and your Davenport address for scope review.",
            ),
            (
                "Can you clear overgrown vacation rental lots in Davenport?",
                "Rental turnover and listing prep often need rear lot and fence line clearing. Photo-based estimates help confirm access and vegetation density before scheduling.",
            ),
        ],
        "strip_note": "Davenport I-4 corridor lots, retention ponds, and grove-transition clearing.",
    },
    "lake-wales-fl": {
        "meta_description": (
            "Land clearing and acreage cleanup in Lake Wales, FL — Ridge citrus, scrub, and lake edges. "
            "Faith Works forestry mulching from Auburndale. Photo estimates for Polk properties."
        ),
        "hook": (
            "Lake Wales sits on the Lake Wales Ridge with rolling scrub, citrus heritage, and small lakes where "
            "pond banks, grove edges, and rural acreage routinely need clearing beyond mower reach."
        ),
        "context": (
            "From downtown near Bok Tower to rural land toward Frostproof, Lake Wales properties mix historic "
            "neighborhoods, ranch parcels, and former grove land where saplings and undergrowth reclaim fence "
            "lines and access paths each rainy season."
        ),
        "local_detail": (
            "Scrub and sandhill terrain toward Babson Park and Eagle Ridge often requires forestry mulching "
            "rather than hand clearing — scope is confirmed from photos showing slope and tree density."
        ),
        "property_types": [
            "Ridge citrus and grove-transition acreage",
            "Lake Pierce and lake-adjacent homesteads",
            "Historic Lake Wales homes with large rear sections",
            "Scrub and sandhill parcels toward Babson Park",
            "Vacant land near SR-60 awaiting development",
        ],
        "common_jobs": [
            "Forestry mulching on Ridge scrub and sapling regrowth",
            "Pond bank clearing on Lake Wales lake edges",
            "Fence line reopening on citrus and ranch parcels",
            "Trail clearing across multi-acre Ridge land",
            "Acreage cleanup before listing or estate sale",
            "Ditch maintenance on rural Lake Wales frontage",
        ],
        "intent_routes": [
            {"label": "Ridge acreage mulching", "slug": "forestry-mulching", "text": "Mulch scrub and saplings on Lake Wales Ridge parcels."},
            {"label": "Lake edge banks", "slug": "pond-bank-clearing", "text": "Trim brush on private lake and pond banks around Lake Wales."},
            {"label": "Ranch access paths", "slug": "trail-clearing", "text": "Reopen trails and access routes across Lake Wales acreage."},
            {"label": "Grove fence lines", "slug": "fence-line-clearing", "text": "Clear overgrown fence runs on former citrus land near Lake Wales."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works handle Lake Wales Ridge scrub and sandhill terrain?",
                "Ridge scrub and sapling regrowth around Lake Wales are common forestry mulching jobs — send photos showing terrain, access, and vegetation type for accurate scope.",
            ),
            (
                "Can Faith Works travel from Auburndale to Lake Wales for acreage work?",
                "Lake Wales is within our Polk County service radius. Photo-based estimates and scheduling are handled from our Auburndale base before equipment mobilization.",
            ),
        ],
        "strip_note": "Lake Wales Ridge scrub, grove edges, and lake bank clearing.",
    },
    "polk-city-fl": {
        "meta_description": (
            "Land clearing and pond work in Polk City, FL — I-4 north Polk and Lake Florence edges. "
            "Faith Works brush cutting from Auburndale. Free photo estimates for local properties."
        ),
        "hook": (
            "Polk City is a small I-4 community north of Lakeland where Lake Florence frontage, rural acreage, "
            "and new growth toward Gibsonia create steady demand for ditch and pond bank clearing."
        ),
        "context": (
            "Faith Works handles Polk City jobs on properties where rear wooded sections, pond edges, and county "
            "ditch lines have outgrown routine maintenance — especially on larger lots between the interstate "
            "and Old Polk City Road corridors."
        ),
        "local_detail": (
            "Lake Florence-adjacent homes often need bank brush cut back for visibility and mosquito control "
            "without disturbing seawalls — access and slope are reviewed from photos first."
        ),
        "property_types": [
            "Lake Florence adjacent homes with overgrown banks",
            "I-4 corridor acreage toward Gibsonia",
            "Rural homesteads with long fence lines",
            "Newer plats with rear conservation buffers",
            "Vacant parcels along Old Polk City Road",
        ],
        "common_jobs": [
            "Lake Florence pond bank brush removal",
            "Ditch clearing on north Polk county roads",
            "Rear lot clearing on oversized Polk City parcels",
            "Fence line reopening on rural acreage",
            "Forestry mulching on wooded homestead sections",
            "Property cleanup before sale on I-4 corridor land",
        ],
        "intent_routes": [
            {"label": "Lake Florence banks", "slug": "pond-bank-clearing", "text": "Clean private banks along Lake Florence in Polk City."},
            {"label": "North Polk ditches", "slug": "ditch-clearing", "text": "Clear vegetation from drainage ditches on Polk City frontage."},
            {"label": "I-4 corridor acreage", "slug": "acreage-cleanup", "text": "Cleanup overgrown acreage on Polk City and Gibsonia parcels."},
            {"label": "Homestead fence lines", "slug": "fence-line-clearing", "text": "Reopen fence runs on rural Polk City properties."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Polk City near Lake Florence?",
                "Yes. Lake Florence bank work and north Polk acreage clearing are within our service area — send photos of bank slope, access, and vegetation for estimate review.",
            ),
            (
                "How far is Polk City from Faith Works in Auburndale?",
                "Polk City is a reasonable travel distance from our Auburndale headquarters within north and central Polk County — address and photos confirm scheduling.",
            ),
        ],
        "strip_note": "Polk City Lake Florence banks, I-4 acreage, and ditch line clearing.",
    },
    "mulberry-fl": {
        "meta_description": (
            "Private road clearing, land clearing, pond bank work, and acreage cleanup in Mulberry, FL. "
            "Faith Works clears south Polk ranch access, brush, and overgrowth."
        ),
        "hook": (
            "Mulberry's phosphate heritage and rural south Polk location mean large acreage, pond edges, and "
            "long fence lines where brush regrowth needs forestry equipment rather than hand labor."
        ),
        "context": (
            "Properties between Mulberry and Bartow often combine ranch access roads, private lanes, retention ponds, "
            "and former agricultural edges where summer growth closes paths and obscures property boundaries before "
            "owners notice until access becomes difficult. That is why private road clearing, driveway-edge clearing, "
            "and acreage cleanup are priority services for Mulberry property owners."
        ),
        "local_detail": (
            "Land toward Nichols and Fort Green frequently involves multi-acre fence runs and pond banks where "
            "work is staged in sections after photo review confirms equipment access points."
        ),
        "property_types": [
            "South Polk ranch acreage with overgrown access roads",
            "Phosphate-area rural homesteads with pond edges",
            "Former agricultural parcels with sapling regrowth",
            "Commercial and industrial pads with brush perimeters",
            "Estate parcels needing cleanup before transfer",
        ],
        "common_jobs": [
            "Private road and access road clearing on Mulberry ranch properties",
            "Driveway edge clearing where brush narrows equipment access",
            "Pond bank brush removal on rural water features",
            "Forestry mulching on multi-acre south Polk land",
            "Fence line reopening on long ranch boundaries",
            "Ditch clearing on CR-640 and rural frontage",
        ],
        "intent_routes": [
            {"label": "Private roads and ranch access", "slug": "access-road-clearing", "text": "Reopen overgrown private roads, driveway edges, and access paths on Mulberry acreage."},
            {"label": "South Polk mulching", "slug": "forestry-mulching", "text": "Mulch saplings and thick brush on Mulberry multi-acre land."},
            {"label": "Rural pond banks", "slug": "pond-bank-clearing", "text": "Cut back brush on private pond edges near Mulberry."},
            {"label": "Estate acreage cleanup", "slug": "acreage-cleanup", "text": "Restore usable acreage on overgrown Mulberry properties."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works clear private roads and ranch access in Mulberry?",
                "Yes. Private road clearing, ranch access paths, and long driveway edges are common Mulberry requests — send photos showing the path, width, entry point, and where access needs to be restored.",
            ),
            (
                "Can Faith Works clear land near Mulberry's phosphate and industrial areas?",
                "We clear private outdoor property you own or maintain — send photos of the work area, access routes, and any obstacles so scope stays accurate for Mulberry jobs.",
            ),
        ],
        "strip_note": "Mulberry private road clearing, south Polk acreage, and pond bank work.",
    },
    "fort-meade-fl": {
        "meta_description": (
            "Land clearing and fence line work in Fort Meade, FL — oldest Polk town and Peace River ranch land. "
            "Faith Works acreage cleanup from Auburndale. Free photo estimates."
        ),
        "hook": (
            "Fort Meade is Polk County's oldest community, where Peace River-area ranch land, historic homes, "
            "and rural acreage still depend on fence lines and access roads that brush closes off each season."
        ),
        "context": (
            "Faith Works serves Fort Meade owners with overgrown homestead sections, pond edges on south Polk "
            "water features, and ditch lines along county roads where drainage paths need clearing after heavy "
            "summer growth."
        ),
        "local_detail": (
            "Properties toward Bowling Green and the Hardee County line often involve longer travel access and "
            "cattle-fence boundaries that require staged clearing plans confirmed from photos."
        ),
        "property_types": [
            "Historic Fort Meade homes with large rear acreage",
            "Peace River-area ranch parcels with overgrown paths",
            "Rural homesteads with pond and ditch frontage",
            "Former grove edges toward Bartow",
            "Vacant south Polk land awaiting build or sale prep",
        ],
        "common_jobs": [
            "Fence line clearing on Fort Meade ranch boundaries",
            "Access road reopening on rural homesteads",
            "Pond bank brush removal on private water features",
            "Forestry mulching on wooded acreage sections",
            "Property cleanup for estate and probate parcels",
            "Ditch clearing on south Polk county roads",
        ],
        "intent_routes": [
            {"label": "Ranch fence lines", "slug": "fence-line-clearing", "text": "Reopen overgrown fence runs on Fort Meade ranch and acreage land."},
            {"label": "Homestead access", "slug": "access-road-clearing", "text": "Clear brush blocking access roads on Fort Meade rural properties."},
            {"label": "South Polk ponds", "slug": "pond-bank-clearing", "text": "Trim banks on private ponds and ditches near Fort Meade."},
            {"label": "Wooded acreage", "slug": "forestry-mulching", "text": "Mulch dense undergrowth on Fort Meade homestead sections."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works travel to Fort Meade for rural acreage clearing?",
                "Fort Meade and south Polk ranch land are within our service range from Auburndale — send photos of fence lines, access roads, and pond edges for estimate review.",
            ),
            (
                "Can you help with overgrown Fort Meade estate or family land?",
                "Estate and long-held family parcels in Fort Meade often need acreage cleanup before sale or transfer. Photo-based estimates establish scope before work begins.",
            ),
        ],
        "strip_note": "Fort Meade ranch fence lines, access roads, and south Polk acreage.",
    },
    "frostproof-fl": {
        "meta_description": (
            "Land clearing and citrus acreage work in Frostproof, FL — Ridge lakes and grove edges. "
            "Faith Works forestry mulching from Auburndale. Photo estimates for Polk properties."
        ),
        "hook": (
            "Frostproof anchors south Polk citrus country around lakes like Reedy and Clinch, where grove edges, "
            "scrub acreage, and lake banks need clearing that matches Ridge terrain and seasonal regrowth."
        ),
        "context": (
            "Faith Works handles Frostproof properties where former citrus land, sandhill scrub, and private "
            "lake frontage combine — fence lines and pond banks that standard maintenance cannot keep open "
            "without forestry mulching or brush cutting equipment."
        ),
        "local_detail": (
            "Land between Frostproof and Avon Park often shares Ridge drainage patterns where ditch lines and "
            "lake edges are cleared in coordinated sections after photo review."
        ),
        "property_types": [
            "Citrus grove edges and transition acreage",
            "Lake Reedy and Clinch adjacent properties",
            "Ridge scrub parcels with sapling regrowth",
            "Rural homesteads with long fence runs",
            "Vacant citrus land being prepared for new use",
        ],
        "common_jobs": [
            "Grove-edge and fence line clearing on citrus parcels",
            "Lake bank brush cutback on Frostproof water frontage",
            "Forestry mulching on Ridge scrub sections",
            "Trail reopening across multi-acre Frostproof land",
            "Ditch clearing on rural south Polk frontage",
            "Acreage cleanup before sale or grove transition",
        ],
        "intent_routes": [
            {"label": "Citrus grove edges", "slug": "fence-line-clearing", "text": "Clear overgrown fence and tree lines on Frostproof citrus acreage."},
            {"label": "Ridge lake banks", "slug": "pond-bank-clearing", "text": "Trim brush on private banks along Frostproof Ridge lakes."},
            {"label": "Scrub mulching", "slug": "forestry-mulching", "text": "Mulch saplings and scrub on south Polk Ridge parcels near Frostproof."},
            {"label": "Acreage trails", "slug": "trail-clearing", "text": "Reopen access trails across Frostproof multi-acre properties."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works clear former citrus land in Frostproof?",
                "Grove edges and citrus-transition acreage around Frostproof are common requests — send photos of tree lines, fence runs, and equipment access for scope review.",
            ),
            (
                "Can Faith Works work on Frostproof lake banks near Reedy or Clinch?",
                "Private lake and pond banks on Frostproof properties are within our service area — bank slope and access are confirmed from photos before scheduling.",
            ),
        ],
        "strip_note": "Frostproof citrus edges, Ridge lake banks, and scrub mulching.",
    },
    "dundee-fl": {
        "meta_description": (
            "Land clearing and pond bank work in Dundee, FL — small-town Polk between Winter Haven and Lake Wales. "
            "Faith Works brush cutting from Auburndale. Free photo estimates."
        ),
        "hook": (
            "Dundee is a compact Polk community between Winter Haven and Lake Wales where lake-adjacent lots, "
            "citrus remnants, and rural acreage need pond banks and fence lines cleared each growing season."
        ),
        "context": (
            "Faith Works serves Dundee property owners with overgrown rear sections, drainage ditches along "
            "county roads, and pond edges on small lakes where brush growth outpaces routine yard maintenance "
            "between Winter Haven and the Ridge."
        ),
        "local_detail": (
            "Properties along Dundee Road and toward Lake Hamilton often combine ditch maintenance with rear-lot "
            "clearing when summer growth closes sight lines and access paths."
        ),
        "property_types": [
            "Lake Hamilton adjacent homes with overgrown banks",
            "Small-town Dundee lots with rear wooded sections",
            "Citrus transition parcels toward Winter Haven",
            "Rural acreage with fence line overgrowth",
            "Vacant land near SR-544 development corridors",
        ],
        "common_jobs": [
            "Pond bank brush removal on Dundee lake edges",
            "Rear lot clearing on oversized Dundee parcels",
            "Ditch vegetation removal along county frontage",
            "Fence line reopening on citrus-transition land",
            "Forestry mulching on sapling-choked sections",
            "Lot cleanup before sale or new construction",
        ],
        "intent_routes": [
            {"label": "Lake Hamilton banks", "slug": "pond-bank-clearing", "text": "Clean private banks along Lake Hamilton and nearby Dundee water edges."},
            {"label": "Dundee rear lots", "slug": "land-clearing", "text": "Clear dense growth on overgrown Dundee residential parcels."},
            {"label": "County ditch lines", "slug": "ditch-clearing", "text": "Open drainage ditches and swales on Dundee road frontage."},
            {"label": "Small-acreage mulching", "slug": "forestry-mulching", "text": "Mulch undergrowth on Dundee citrus and acreage parcels."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Dundee between Winter Haven and Lake Wales?",
                "Yes. Dundee is within our eastern Polk County service area from Auburndale — send photos and your Dundee address for quick estimate review.",
            ),
            (
                "Can you clear pond banks near Lake Hamilton in Dundee?",
                "Lake-adjacent Dundee properties with overgrown banks are common — photos showing bank access and vegetation density help confirm scope before scheduling.",
            ),
        ],
        "strip_note": "Dundee lake banks, rear lots, and citrus-transition clearing.",
    },
    "eagle-lake-fl": {
        "meta_description": (
            "Land clearing, pond bank work, access path clearing, and brush removal in Eagle Lake, FL. "
            "Faith Works serves Lake Eloise-area properties from Auburndale."
        ),
        "hook": (
            "Eagle Lake is a quiet Polk community on the Winter Haven Chain of Lakes fringe where Lake Eloise "
            "frontage, canal edges, and small-acreage lots need pond bank and fence line clearing."
        ),
        "context": (
            "Faith Works handles Eagle Lake jobs where lake-adjacent properties, citrus remnants, and drainage "
            "ditches along local roads have grown beyond what lawn maintenance covers — especially on parcels "
            "between Winter Haven and Bartow. The same properties often need access path clearing, driveway edge "
            "cleanup, and brush removal before pond banks or fence lines can be maintained."
        ),
        "local_detail": (
            "Canal-side homes near Eagle Lake often need brush cut back for water access and visibility without "
            "disturbing seawalls — scope and equipment fit are confirmed from photos first."
        ),
        "property_types": [
            "Lake Eloise adjacent homes with overgrown banks",
            "Canal-front properties with brush-choked edges",
            "Small-acreage citrus transition parcels",
            "Residential lots with rear wooded buffers",
            "Vacant lake-country land awaiting build prep",
        ],
        "common_jobs": [
            "Lake Eloise pond bank brush removal",
            "Canal edge clearing on Eagle Lake waterfront lots",
            "Access path and driveway edge clearing on lake-country parcels",
            "Fence line reopening on small-acreage parcels",
            "Ditch clearing on Eagle Lake road frontage",
            "Storm debris cleanup on lake-canopy properties",
        ],
        "intent_routes": [
            {"label": "Lake Eloise banks", "slug": "pond-bank-clearing", "text": "Trim brush on private banks along Lake Eloise in Eagle Lake."},
            {"label": "Access paths and drive edges", "slug": "access-road-clearing", "text": "Clear overgrown drive edges and private paths on Eagle Lake properties."},
            {"label": "Lake-country lots", "slug": "land-clearing", "text": "Clear overgrown sections on Eagle Lake residential parcels."},
            {"label": "Storm debris haul-off", "slug": "storm-debris-cleanup", "text": "Remove limbs and brush after storms on Eagle Lake properties."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works work on Eagle Lake properties near Lake Eloise?",
                "Yes. Lake Eloise bank work and canal-edge clearing on Eagle Lake properties are within our Polk County service area — send photos for estimate review.",
            ),
            (
                "How close is Eagle Lake to Faith Works headquarters in Auburndale?",
                "Eagle Lake is a short travel distance from our Auburndale base, which supports quick photo review and scheduling for eastern Polk lake-country jobs.",
            ),
        ],
        "strip_note": "Eagle Lake Lake Eloise banks, canal edges, and lake-country lot clearing.",
    },
    "plant-city-fl": {
        "meta_description": (
            "Land clearing and acreage cleanup in Plant City, FL — strawberry country and I-4 corridor lots. "
            "Faith Works ditch and fence line work from Auburndale. Free photo estimates."
        ),
        "hook": (
            "Plant City is Hillsborough's agricultural hub along the I-4 corridor, where strawberry fields, "
            "rural acreage, and suburban edges create fence lines and ditches that need equipment-based clearing."
        ),
        "context": (
            "Faith Works serves Plant City owners with overgrown agricultural edges, pond and retention banks on "
            "newer plats, and ditch lines along rural roads where summer growth blocks drainage before harvest "
            "and building seasons."
        ),
        "local_detail": (
            "Land toward Dover and Turkey Creek often mixes farm fence runs with suburban lot rear sections "
            "where access width and equipment staging are confirmed from photos before mobilization."
        ),
        "property_types": [
            "Agricultural acreage with overgrown fence lines",
            "I-4 corridor commercial pads with brush perimeters",
            "Suburban Plant City lots with large rear sections",
            "Retention pond edges on newer subdivisions",
            "Vacant parcels near SR-60 and I-4 interchange",
        ],
        "common_jobs": [
            "Fence line clearing on Plant City farm and acreage parcels",
            "Ditch and swale cleanup along rural Plant City frontage",
            "Retention pond bank brush removal on subdivision edges",
            "Lot clearing before construction near I-4",
            "Forestry mulching on sapling-choked acreage",
            "Property cleanup for agricultural land transition",
        ],
        "intent_routes": [
            {"label": "Farm fence lines", "slug": "fence-line-clearing", "text": "Reopen overgrown fence runs on Plant City agricultural acreage."},
            {"label": "I-4 corridor lots", "slug": "lot-cleanup", "text": "Clear overgrown Plant City lots before build or sale."},
            {"label": "Rural ditch lines", "slug": "ditch-clearing", "text": "Open drainage ditches on Plant City road and farm frontage."},
            {"label": "Acreage overgrowth", "slug": "overgrowth-removal", "text": "Remove dense brush on Plant City acreage and field edges."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Plant City strawberry country and I-4 corridor properties?",
                "Plant City agricultural edges and I-4 corridor lots are within our travel range from Auburndale — send photos and address for scope confirmation.",
            ),
            (
                "Can Faith Works clear ditch lines on Plant City farm frontage?",
                "Outdoor ditch and swale clearing on private Plant City property is a common request — photos showing ditch location and access help establish accurate scope.",
            ),
        ],
        "strip_note": "Plant City farm fence lines, I-4 lots, and ditch clearing.",
    },
    "kissimmee-fl": {
        "meta_description": (
            "Land clearing and pond bank work in Kissimmee, FL — Osceola lake country and growth corridors. "
            "Faith Works brush cutting from Auburndale. Photo-based estimates for local properties."
        ),
        "hook": (
            "Kissimmee combines East Lake Tohopekaliga frontage, Narcoossee Road growth, and older lake-country "
            "neighborhoods where pond banks, retention areas, and rear acreage need clearing beyond mower service."
        ),
        "context": (
            "Faith Works handles Kissimmee properties where lake edges, conservation buffers behind new "
            "subdivisions, and ditch lines along rural Osceola roads have outgrown routine maintenance — "
            "especially on larger lots toward Poinciana and St. Cloud borders."
        ),
        "local_detail": (
            "Properties near Lake Tohopekaliga and Shingle Creek often need bank brush cut back for access "
            "and visibility — slope, seawall presence, and neighbor lines are reviewed from photos first."
        ),
        "property_types": [
            "Lake Tohopekaliga adjacent homes with overgrown banks",
            "Narcoossee Road corridor lots with rear conservation",
            "Retention pond edges on Kissimmee subdivisions",
            "Older lake-country neighborhoods with wooded rear sections",
            "Vacant Osceola acreage toward Poinciana",
        ],
        "common_jobs": [
            "Lake and pond bank brush removal on Kissimmee waterfront lots",
            "Rear lot clearing on Narcoossee corridor properties",
            "Retention area cleanup on subdivision edges",
            "Fence line reopening on Osceola acreage",
            "Forestry mulching on conservation-border overgrowth",
            "Storm debris haul-off after Osceola wind events",
        ],
        "intent_routes": [
            {"label": "Lake Toho banks", "slug": "pond-bank-clearing", "text": "Clean private banks along Kissimmee lake and pond frontage."},
            {"label": "Narcoossee corridor", "slug": "land-clearing", "text": "Clear overgrown rear sections on Kissimmee growth-corridor lots."},
            {"label": "Retention cleanup", "slug": "pond-cleanup", "text": "Trim brush on retention ponds and swales in Kissimmee subdivisions."},
            {"label": "Osceola storm debris", "slug": "storm-debris-cleanup", "text": "Haul storm limbs and brush from Kissimmee properties."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Kissimmee lakefront and Narcoossee Road properties?",
                "Kissimmee lake-country and growth-corridor properties are within our Osceola travel range from Auburndale — send photos and address for estimate review.",
            ),
            (
                "Can Faith Works clear conservation buffers behind Kissimmee homes?",
                "We clear private outdoor areas you own or maintain — not protected public conservation. Photos showing property lines and access confirm Kissimmee scope.",
            ),
        ],
        "strip_note": "Kissimmee lake banks, Narcoossee corridor lots, and retention cleanup.",
    },
    "st-cloud-fl": {
        "meta_description": (
            "Land clearing and lot cleanup in St. Cloud, FL — East Lake Tohopekaliga and Harmony area acreage. "
            "Faith Works from Auburndale. Pond banks and brush cutting. Free estimates."
        ),
        "hook": (
            "St. Cloud stretches from historic downtown lakefront to Harmony and Narcoossee growth corridors, "
            "where pond edges, conservation borders, and rural Osceola acreage need coordinated clearing."
        ),
        "context": (
            "Faith Works serves St. Cloud owners with overgrown rear sections on lake-country lots, ditch lines "
            "on rural frontage, and multi-acre parcels toward Holopaw where access roads and fence lines close "
            "off between mowing seasons."
        ),
        "local_detail": (
            "Harmony and Narcoossee-area properties often combine retention pond maintenance with rear-lot "
            "clearing when new construction meets older wooded buffers on the same parcel."
        ),
        "property_types": [
            "East Lake Tohopekaliga adjacent homes with bank overgrowth",
            "Harmony and Narcoossee subdivision rear buffers",
            "Rural St. Cloud acreage toward Holopaw",
            "Historic downtown lots with oversized rear sections",
            "Vacant Osceola land awaiting development prep",
        ],
        "common_jobs": [
            "Lake bank brush removal on St. Cloud waterfront properties",
            "Rear lot clearing on Harmony and Narcoossee plats",
            "Access road reopening on rural St. Cloud acreage",
            "Ditch clearing on Osceola county frontage",
            "Forestry mulching on wooded homestead sections",
            "Lot cleanup before St. Cloud construction or sale",
        ],
        "intent_routes": [
            {"label": "East Lake Toho edges", "slug": "pond-bank-clearing", "text": "Trim banks on St. Cloud lake and pond frontage properties."},
            {"label": "Harmony lot prep", "slug": "lot-cleanup", "text": "Clear overgrown St. Cloud lots in Harmony and growth areas."},
            {"label": "Rural access paths", "slug": "access-road-clearing", "text": "Reopen overgrown access roads on St. Cloud acreage."},
            {"label": "Wooded rear sections", "slug": "forestry-mulching", "text": "Mulch dense growth on St. Cloud multi-acre parcels."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve St. Cloud including Harmony and Narcoossee areas?",
                "St. Cloud growth corridors and lake-country neighborhoods are within our Osceola service range — send photos and your St. Cloud address for scope review.",
            ),
            (
                "Can Faith Works clear rural St. Cloud acreage toward Holopaw?",
                "Rural Osceola acreage on the St. Cloud outskirts is handled when photos confirm access, fence lines, and vegetation density for accurate estimates.",
            ),
        ],
        "strip_note": "St. Cloud lake banks, Harmony lots, and rural Osceola acreage.",
    },
    "poinciana-fl": {
        "meta_description": (
            "Land clearing and conservation-edge work in Poinciana, FL — large HOA community and Osceola acreage. "
            "Faith Works fence line clearing from Auburndale. Free photo estimates."
        ),
        "hook": (
            "Poinciana is one of Central Florida's largest planned communities, where conservation borders, "
            "retention ponds, and rear lot woods on oversized parcels create steady brush-clearing demand."
        ),
        "context": (
            "Faith Works handles Poinciana jobs where HOA-adjacent conservation strips, pond banks, and "
            "fence lines on Polk and Osceola sides of the community have outgrown what homeowners can manage "
            "with hand tools or standard lawn service."
        ),
        "local_detail": (
            "Properties backing to greenbelt and wetland buffers often need staged clearing that respects "
            "property lines and neighbor sight lines — scope is confirmed from photos before any work begins."
        ),
        "property_types": [
            "Homes backing to Poinciana conservation greenbelts",
            "Retention pond edges on community plats",
            "Oversized lots with rear wooded sections",
            "Vacant Poinciana parcels awaiting build prep",
            "Polk-side acreage toward Haines City borders",
        ],
        "common_jobs": [
            "Conservation-border fence line clearing on Poinciana lots",
            "Retention pond bank brush cutback",
            "Rear lot clearing on oversized Poinciana parcels",
            "Overgrowth removal before fencing or pool projects",
            "Forestry mulching on wooded rear sections",
            "Property cleanup for Poinciana listing prep",
        ],
        "intent_routes": [
            {"label": "Greenbelt edges", "slug": "fence-line-clearing", "text": "Reopen fence lines where Poinciana lots meet conservation buffers."},
            {"label": "Community pond banks", "slug": "pond-bank-clearing", "text": "Clean brush on private retention and pond edges in Poinciana."},
            {"label": "Rear lot reclaim", "slug": "overgrowth-removal", "text": "Remove dense rear growth on Poinciana residential parcels."},
            {"label": "Build-ready cleanup", "slug": "property-cleanup", "text": "Restore usable outdoor space on overgrown Poinciana properties."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works clear conservation borders on Poinciana properties?",
                "We clear private outdoor areas you own or maintain on Poinciana lots — not public conservation land. Photos showing property lines confirm scope before scheduling.",
            ),
            (
                "Can Faith Works work on both Polk and Osceola sides of Poinciana?",
                "Poinciana spans county lines — send your address and photos so we confirm county access, travel, and equipment fit for your specific lot.",
            ),
        ],
        "strip_note": "Poinciana conservation edges, retention ponds, and rear lot clearing.",
    },
    "orlando-fl": {
        "meta_description": (
            "Land clearing and overgrowth removal in Orlando, FL — urban lots, lakes, and retention ponds. "
            "Faith Works brush cutting from Auburndale. Photo-based estimates for Orange County."
        ),
        "hook": (
            "Orlando's mix of urban infill, lake-adjacent neighborhoods, and suburban oversized lots creates "
            "clearing needs on retention ponds, rear wooded sections, and vacant parcels standard crews avoid."
        ),
        "context": (
            "Faith Works serves Orlando property owners where rear acreage on oversized city lots, private lake "
            "edges, and brush-choked vacant land need compact equipment and brush cutting — access constraints "
            "are reviewed from gate measurements and photos before scheduling."
        ),
        "local_detail": (
            "Properties near Conway, Azalea Park, and southeast Orlando lake chains often combine pond bank "
            "work with rear lot clearing when summer growth closes usable yard space."
        ),
        "property_types": [
            "Oversized Orlando lots with rear wooded sections",
            "Lake Conway and Butler chain adjacent properties",
            "Vacant infill parcels awaiting development",
            "Commercial pads with unmanaged brush perimeters",
            "Subdivision retention pond edges needing cutback",
        ],
        "common_jobs": [
            "Rear lot clearing on oversized Orlando residential parcels",
            "Retention and lake bank brush removal",
            "Vacant lot cleanup before Orlando construction",
            "Commercial perimeter overgrowth removal",
            "Forestry mulching on sapling-choked sections",
            "Storm debris haul-off after Orange County storms",
        ],
        "intent_routes": [
            {"label": "Urban rear lots", "slug": "land-clearing", "text": "Clear dense rear growth on oversized Orlando city lots."},
            {"label": "Lake and retention banks", "slug": "pond-bank-clearing", "text": "Trim brush on private lake and retention edges in Orlando."},
            {"label": "Vacant lot prep", "slug": "lot-cleanup", "text": "Open overgrown Orlando vacant parcels before build or sale."},
            {"label": "Storm cleanup", "slug": "storm-debris-cleanup", "text": "Remove storm limbs and brush piles from Orlando properties."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Orlando with tight gate or alley access?",
                "Many Orlando lots have access constraints — send gate width, photos of the work area, and obstacles so we confirm compact equipment fit before scheduling.",
            ),
            (
                "Can Faith Works clear retention ponds on Orlando subdivision properties?",
                "Private retention and pond bank clearing on Orlando properties you maintain is common — photos showing bank slope and access confirm scope.",
            ),
        ],
        "strip_note": "Orlando rear lots, lake banks, and vacant parcel clearing.",
    },
    "ocoee-fl": {
        "meta_description": (
            "Land clearing and pond work in Ocoee, FL — West Orange lakes and suburban acreage. "
            "Faith Works brush cutting from Auburndale. Free photo estimates for local properties."
        ),
        "hook": (
            "Ocoee sits in West Orange between Orlando and Winter Garden, where Star Lake frontage, suburban "
            "oversized lots, and rural edges toward Clarcona need pond banks and rear sections cleared."
        ),
        "context": (
            "Faith Works handles Ocoee jobs where lake-adjacent homes, retention ponds on newer plats, and "
            "wooded rear buffers have outgrown routine lawn maintenance — especially on properties along "
            "Colonial Drive and Maguire Road corridors."
        ),
        "local_detail": (
            "Lakefront and lake-access properties near Star Lake and Lake Apopka fringe often need bank brush "
            "cut back without disturbing seawalls — equipment approach is confirmed from photos first."
        ),
        "property_types": [
            "Star Lake adjacent homes with overgrown banks",
            "West Orange suburban lots with rear wooded sections",
            "Retention pond edges on Ocoee subdivisions",
            "Properties toward Clarcona with rural acreage edges",
            "Vacant West Orange parcels awaiting build prep",
        ],
        "common_jobs": [
            "Lake bank brush removal on Ocoee waterfront lots",
            "Rear lot clearing on oversized Ocoee parcels",
            "Retention pond edge cleanup on subdivision properties",
            "Fence line reopening on West Orange acreage edges",
            "Lot cleanup before Ocoee construction projects",
            "Overgrowth removal on brush-choked side yards",
        ],
        "intent_routes": [
            {"label": "Star Lake banks", "slug": "pond-bank-clearing", "text": "Clean private banks on Ocoee lake and pond frontage."},
            {"label": "West Orange rear lots", "slug": "land-clearing", "text": "Clear wooded rear sections on Ocoee residential properties."},
            {"label": "Subdivision retention", "slug": "pond-cleanup", "text": "Trim brush on retention edges in Ocoee neighborhoods."},
            {"label": "Side yard overgrowth", "slug": "overgrowth-removal", "text": "Remove dense brush on narrow Ocoee side and rear yards."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Ocoee and West Orange lake-country properties?",
                "Ocoee lakefront and suburban lots are within our West Orange travel range from Auburndale — send photos and address for estimate review.",
            ),
            (
                "Can Faith Works work on tight Ocoee subdivision lots?",
                "Compact equipment fits many Ocoee properties when photos show gate width, slopes, and obstacles clearly before scheduling.",
            ),
        ],
        "strip_note": "Ocoee lake banks, West Orange rear lots, and retention cleanup.",
    },
    "winter-garden-fl": {
        "meta_description": (
            "Land clearing and lot cleanup in Winter Garden, FL — Plant Street area and West Orange lakes. "
            "Faith Works brush cutting from Auburndale. Photo-based estimates."
        ),
        "hook": (
            "Winter Garden blends historic Plant Street charm with fast West Orange growth, where small lakes, "
            "trail-adjacent lots, and new subdivisions create pond edges and rear woods needing clearing."
        ),
        "context": (
            "Faith Works serves Winter Garden owners with overgrown rear sections on lake-country lots, retention "
            "ponds on Horizon West plats, and rural edges toward Oakland where fence lines and ditch lines "
            "need equipment-based maintenance."
        ),
        "local_detail": (
            "Horizon West and Hamlin area properties often combine retention pond maintenance with rear-lot "
            "clearing when new construction meets older wooded buffers on the same parcel."
        ),
        "property_types": [
            "Historic Winter Garden homes with large rear sections",
            "Horizon West subdivision retention pond edges",
            "Lake Country and Johns Lake adjacent properties",
            "Hamlin and Hamlin Reserve lots with rear buffers",
            "Rural edges toward Oakland with acreage overgrowth",
        ],
        "common_jobs": [
            "Retention pond bank brush removal in Horizon West",
            "Rear lot clearing on Winter Garden lake-country parcels",
            "Fence line reopening on West Orange acreage edges",
            "Lot cleanup before Winter Garden construction",
            "Trail-adjacent overgrowth removal near West Orange Trail",
            "Forestry mulching on wooded rear homestead sections",
        ],
        "intent_routes": [
            {"label": "Horizon West retention", "slug": "pond-bank-clearing", "text": "Clean retention and pond banks in Winter Garden growth areas."},
            {"label": "Lake-country lots", "slug": "land-clearing", "text": "Clear overgrown rear sections on Winter Garden lake properties."},
            {"label": "Build prep cleanup", "slug": "lot-cleanup", "text": "Open Winter Garden lots before construction or sale."},
            {"label": "Acreage edge mulching", "slug": "forestry-mulching", "text": "Mulch saplings on wooded buffers toward Oakland and Hamlin."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Winter Garden including Horizon West and Hamlin?",
                "Winter Garden growth corridors and lake-country neighborhoods are within our West Orange service range — send photos for scope confirmation.",
            ),
            (
                "Can Faith Works clear land near the West Orange Trail in Winter Garden?",
                "Trail-adjacent private property clearing is handled when photos show property lines, access, and vegetation density for accurate Winter Garden estimates.",
            ),
        ],
        "strip_note": "Winter Garden retention ponds, lake-country lots, and Horizon West clearing.",
    },
    "apopka-fl": {
        "meta_description": (
            "Land clearing and acreage cleanup in Apopka, FL — Wekiwa Springs area and north Orange growth. "
            "Faith Works brush cutting from Auburndale. Free photo estimates."
        ),
        "hook": (
            "Apopka spans from Wekiwa Springs and Rock Springs Ridge to rural north Orange acreage, where "
            "pond edges, hammock woods, and oversized lots need clearing beyond standard lawn service."
        ),
        "context": (
            "Faith Works handles Apopka properties where rear wooded sections, retention ponds on new plats, "
            "and rural fence lines toward Zellwood have outgrown routine maintenance — especially on multi-acre "
            "parcels with oak hammock undergrowth."
        ),
        "local_detail": (
            "Rock Springs Ridge and Errol Estates properties often need pond bank and rear-lot work combined "
            "when summer growth closes golf-course-adjacent buffers and side-yard access."
        ),
        "property_types": [
            "Rock Springs Ridge homes with pond and rear overgrowth",
            "Wekiwa Springs area lots with hammock buffers",
            "North Orange rural acreage toward Zellwood",
            "Errol Estates and golf-community rear sections",
            "Vacant Apopka parcels awaiting development prep",
        ],
        "common_jobs": [
            "Pond bank brush removal on Apopka golf-community lots",
            "Rear hammock clearing on Wekiwa-area properties",
            "Fence line reopening on north Orange acreage",
            "Forestry mulching on oak hammock undergrowth",
            "Lot cleanup before Apopka construction",
            "Retention pond edge cleanup on new Apopka plats",
        ],
        "intent_routes": [
            {"label": "Wekiwa-area hammocks", "slug": "forestry-mulching", "text": "Mulch dense hammock growth on Apopka north Orange parcels."},
            {"label": "Community pond banks", "slug": "pond-bank-clearing", "text": "Trim banks on private ponds in Rock Springs Ridge and Errol Estates."},
            {"label": "North Orange acreage", "slug": "acreage-cleanup", "text": "Cleanup overgrown acreage on rural Apopka properties."},
            {"label": "Build-ready lots", "slug": "lot-cleanup", "text": "Clear vacant Apopka parcels before construction or sale."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Apopka including Wekiwa Springs and Rock Springs Ridge?",
                "Apopka lake-country and north Orange acreage are within our travel range — send photos and your Apopka address for estimate review.",
            ),
            (
                "Can Faith Works clear oak hammock undergrowth on Apopka properties?",
                "Oak hammock and dense undergrowth on Apopka lots often need forestry mulching — photos showing access and tree density confirm scope before scheduling.",
            ),
        ],
        "strip_note": "Apopka hammock woods, pond banks, and north Orange acreage.",
    },
    "clermont-fl": {
        "meta_description": (
            "Land clearing and pond bank work in Clermont, FL — rolling hills and Lake Minneola frontage. "
            "Faith Works brush cutting from Auburndale. Photo-based estimates for south Lake County."
        ),
        "hook": (
            "Clermont's rolling south Lake terrain around Lake Minneola, Lake Louisa, and the hills along "
            "US-27 creates pond banks, steep edges, and acreage where brush clearing needs careful access planning."
        ),
        "context": (
            "Faith Works serves Clermont owners with overgrown lakefront sections, retention ponds on new plats, "
            "and rural acreage toward Groveland where fence lines and ditch lines close off between rainy seasons "
            "on sloped Lake County land."
        ),
        "local_detail": (
            "Lake Minneola waterfront and hillside properties often need bank brush cut back on slopes where "
            "equipment approach and seawall proximity are confirmed from photos before work is scheduled."
        ),
        "property_types": [
            "Lake Minneola and Lake Louisa adjacent homes",
            "South Lake rolling-hill acreage with pond edges",
            "Subdivision retention ponds on Clermont plats",
            "Rural parcels toward Groveland with fence overgrowth",
            "Vacant hilltop land awaiting build prep",
        ],
        "common_jobs": [
            "Lake Minneola bank brush removal on waterfront lots",
            "Retention pond edge cleanup on Clermont subdivisions",
            "Fence line reopening on south Lake acreage",
            "Forestry mulching on sloped wooded sections",
            "Acreage cleanup before Clermont listing or build",
            "Ditch clearing on rural south Lake frontage",
        ],
        "intent_routes": [
            {"label": "Lake Minneola banks", "slug": "pond-bank-clearing", "text": "Trim brush on private banks along Clermont lake frontage."},
            {"label": "South Lake acreage", "slug": "acreage-cleanup", "text": "Clear overgrown acreage on rolling Clermont hill country."},
            {"label": "Hillside overgrowth", "slug": "overgrowth-removal", "text": "Remove dense brush on sloped Clermont residential sections."},
            {"label": "Rural fence lines", "slug": "fence-line-clearing", "text": "Reopen fence runs on Clermont south Lake parcels."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works handle sloped Clermont lakefront properties?",
                "Clermont hillside and lakefront banks are common — send photos showing slope, seawall presence, and equipment access so scope stays accurate.",
            ),
            (
                "Can Faith Works travel from Auburndale to Clermont for acreage work?",
                "Clermont south Lake properties are within our extended service range — address and photos confirm travel and scheduling before mobilization.",
            ),
        ],
        "strip_note": "Clermont lake banks, rolling acreage, and south Lake clearing.",
    },
    "leesburg-fl": {
        "meta_description": (
            "Land clearing and lake edge work in Leesburg, FL — Harris Chain lakes and historic downtown lots. "
            "Faith Works from Auburndale. Pond banks and acreage cleanup. Free estimates."
        ),
        "hook": (
            "Leesburg sits on the Harris Chain of Lakes with historic downtown neighborhoods, lakefront homes, "
            "and rural Lake County acreage where pond banks and wooded rear sections need regular clearing."
        ),
        "context": (
            "Faith Works handles Leesburg jobs where Lake Griffin, Lake Harris, and smaller chain lakes meet "
            "oversized in-town lots and rural land toward The Villages border — retention ponds and ditch lines "
            "on county roads also need summer cutback."
        ),
        "local_detail": (
            "Properties near Venetian Gardens and along US-441 often combine lake bank maintenance with rear-lot "
            "clearing when brush growth reduces usable yard space and water access."
        ),
        "property_types": [
            "Harris Chain lakefront homes with overgrown banks",
            "Historic Leesburg lots with large rear wooded sections",
            "Rural Lake County acreage toward Okahumpka",
            "Commercial pads along US-441 with brush perimeters",
            "Vacant lake-country parcels awaiting development",
        ],
        "common_jobs": [
            "Harris Chain pond bank brush removal",
            "Rear lot clearing on oversized Leesburg properties",
            "Ditch clearing on Lake County road frontage",
            "Forestry mulching on wooded homestead sections",
            "Property cleanup before Leesburg sale or probate",
            "Fence line reopening on rural Lake County acreage",
        ],
        "intent_routes": [
            {"label": "Harris Chain banks", "slug": "pond-bank-clearing", "text": "Clean private banks along Leesburg Harris Chain lake frontage."},
            {"label": "In-town rear lots", "slug": "land-clearing", "text": "Clear dense rear growth on oversized Leesburg city lots."},
            {"label": "Lake County ditches", "slug": "ditch-clearing", "text": "Open drainage ditches on Leesburg road and lake frontage."},
            {"label": "Rural acreage prep", "slug": "acreage-cleanup", "text": "Restore usable acreage on overgrown Leesburg properties."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Leesburg Harris Chain lakefront properties?",
                "Leesburg lakefront and chain-lake bank work are within our Lake County service range — send photos of bank slope and access for estimate review.",
            ),
            (
                "Can Faith Works clear rural Leesburg acreage toward Okahumpka?",
                "Rural Lake County acreage around Leesburg is handled when photos confirm fence lines, pond edges, and equipment access before scheduling.",
            ),
        ],
        "strip_note": "Leesburg Harris Chain banks, rear lots, and Lake County acreage.",
    },
    "mount-dora-fl": {
        "meta_description": (
            "Land clearing and pond work in Mount Dora, FL — Lake Dora frontage and rolling Lake County hills. "
            "Faith Works brush cutting from Auburndale. Photo-based estimates."
        ),
        "hook": (
            "Mount Dora's hillside Lake Dora setting and historic charm hide oversized lots with wooded rear "
            "sections, lake banks, and rural edges toward Tavares that need equipment-based brush clearing."
        ),
        "context": (
            "Faith Works serves Mount Dora owners where lakefront banks, hammock woods on rolling terrain, and "
            "fence lines on acreage toward Sorrento have outgrown hand-tool maintenance — access on sloped "
            "lake-country lots is reviewed from photos first."
        ),
        "local_detail": (
            "Lake Dora and Lake Gertrude adjacent properties often need bank brush cut back for views and access "
            "without disturbing historic landscaping — scope is confirmed from detailed photos."
        ),
        "property_types": [
            "Lake Dora waterfront homes with overgrown banks",
            "Historic Mount Dora lots with hammock rear sections",
            "Rolling-hill acreage toward Sorrento and Tavares",
            "Commercial edges near downtown Mount Dora",
            "Vacant lake-country parcels awaiting build prep",
        ],
        "common_jobs": [
            "Lake Dora pond bank brush removal",
            "Rear hammock clearing on Mount Dora hillside lots",
            "Fence line reopening on Lake County acreage",
            "Forestry mulching on wooded rolling sections",
            "Property cleanup for Mount Dora listing prep",
            "Trail reopening on multi-acre lake-country land",
        ],
        "intent_routes": [
            {"label": "Lake Dora banks", "slug": "pond-bank-clearing", "text": "Trim brush on private Lake Dora and Gertrude banks in Mount Dora."},
            {"label": "Hillside rear lots", "slug": "land-clearing", "text": "Clear wooded rear sections on Mount Dora rolling-lot properties."},
            {"label": "Lake Country trails", "slug": "trail-clearing", "text": "Reopen access trails on Mount Dora multi-acre parcels."},
            {"label": "Hammock mulching", "slug": "forestry-mulching", "text": "Mulch dense undergrowth on Mount Dora hammock sections."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works work on Mount Dora Lake Dora waterfront properties?",
                "Mount Dora lakefront bank clearing is common — send photos showing bank slope, seawall, and neighbor lines for accurate scope review.",
            ),
            (
                "Can Faith Works clear wooded sections on historic Mount Dora lots?",
                "Oversized Mount Dora lots with rear hammock woods are handled when photos confirm access width and vegetation density before scheduling.",
            ),
        ],
        "strip_note": "Mount Dora Lake Dora banks, hillside lots, and hammock clearing.",
    },
    "tavares-fl": {
        "meta_description": (
            "Land clearing and lake work in Tavares, FL — Lake County seat and Harris Chain waterfront. "
            "Faith Works acreage cleanup from Auburndale. Pond banks and ditch clearing."
        ),
        "hook": (
            "Tavares is the Lake County seat on the Harris Chain, where seaplane-base lakefront, downtown "
            "neighborhoods, and rural land toward Eustis need pond banks and acreage cleared each season."
        ),
        "context": (
            "Faith Works handles Tavares properties where Lake Eustis and Lake Dora chain edges, oversized "
            "in-town lots, and county-road ditch lines have outgrown routine maintenance — especially on parcels "
            "transitioning from rural Lake County use to residential build."
        ),
        "local_detail": (
            "Wooton Park area lakefront and downtown-adjacent lots often combine bank brush removal with rear-lot "
            "clearing when summer growth closes water views and side-yard access."
        ),
        "property_types": [
            "Harris Chain lakefront homes in Tavares",
            "Downtown Tavares lots with oversized rear sections",
            "Rural Lake County acreage toward Eustis borders",
            "Commercial pads with brush-choked perimeters",
            "Vacant waterfront parcels awaiting development",
        ],
        "common_jobs": [
            "Harris Chain bank brush removal on Tavares waterfront",
            "Rear lot clearing on downtown-adjacent Tavares properties",
            "Ditch clearing on Lake County road frontage",
            "Acreage cleanup on rural Tavares parcels",
            "Forestry mulching on wooded homestead sections",
            "Property cleanup before Tavares sale or build",
        ],
        "intent_routes": [
            {"label": "Chain lake banks", "slug": "pond-bank-clearing", "text": "Clean private banks along Tavares Harris Chain frontage."},
            {"label": "County seat lots", "slug": "lot-cleanup", "text": "Clear overgrown Tavares lots before construction or sale."},
            {"label": "Rural Lake ditches", "slug": "ditch-clearing", "text": "Open drainage ditches on Tavares county-road properties."},
            {"label": "Homestead acreage", "slug": "acreage-cleanup", "text": "Restore usable acreage on overgrown Tavares land."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Tavares lakefront near Wooton Park and the seaplane base?",
                "Tavares Harris Chain waterfront properties are within our Lake County range — send photos of bank access and vegetation for estimate review.",
            ),
            (
                "Can Faith Works clear rural Tavares acreage toward Eustis?",
                "Rural Lake County acreage around Tavares is handled when photos confirm fence lines, pond edges, and equipment access before scheduling.",
            ),
        ],
        "strip_note": "Tavares Harris Chain banks, downtown lots, and Lake County acreage.",
    },
    "groveland-fl": {
        "meta_description": (
            "Land clearing and acreage cleanup in Groveland, FL — south Lake and Green Swamp edge terrain. "
            "Faith Works forestry mulching from Auburndale. Free photo estimates."
        ),
        "hook": (
            "Groveland sits at south Lake County's edge toward the Green Swamp, where rolling acreage, pond "
            "edges, and rural homesteads need fence lines and access roads cleared after wet-season regrowth."
        ),
        "context": (
            "Faith Works serves Groveland owners with overgrown multi-acre sections, ditch lines on rural "
            "frontage, and pond banks on south Lake parcels where hammock woods and pasture edges mix — access "
            "planning matters on soft ground after heavy rain."
        ),
        "local_detail": (
            "Properties toward Mascotte and the Green Swamp fringe often involve longer fence runs and wet-area "
            "access that require photo review before equipment routes are confirmed."
        ),
        "property_types": [
            "South Lake multi-acre homesteads with pond edges",
            "Green Swamp fringe parcels with hammock overgrowth",
            "Rural Groveland acreage toward Clermont borders",
            "Former pasture land with sapling regrowth",
            "Vacant south Lake parcels awaiting build prep",
        ],
        "common_jobs": [
            "Access road clearing on Groveland acreage",
            "Pond bank brush removal on south Lake water features",
            "Forestry mulching on hammock and pasture edges",
            "Fence line reopening on multi-acre Groveland land",
            "Ditch clearing on rural south Lake frontage",
            "Acreage cleanup before Groveland sale or transition",
        ],
        "intent_routes": [
            {"label": "Swamp-edge acreage", "slug": "forestry-mulching", "text": "Mulch dense growth on Groveland Green Swamp fringe parcels."},
            {"label": "Homestead access", "slug": "access-road-clearing", "text": "Reopen overgrown access paths on Groveland rural properties."},
            {"label": "South Lake ponds", "slug": "pond-bank-clearing", "text": "Trim banks on private ponds and ditches near Groveland."},
            {"label": "Multi-acre cleanup", "slug": "acreage-cleanup", "text": "Restore usable acreage on overgrown Groveland homesteads."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works handle Groveland acreage near the Green Swamp?",
                "Groveland swamp-edge and south Lake acreage are within our service range — send photos showing access routes and wet areas for scope planning.",
            ),
            (
                "Can Faith Works clear fence lines on large Groveland homesteads?",
                "Multi-acre Groveland fence line clearing is common — photos of boundary runs and entry gates help confirm equipment approach before scheduling.",
            ),
        ],
        "strip_note": "Groveland swamp-edge acreage, access roads, and pond bank clearing.",
    },
    "brandon-fl": {
        "meta_description": (
            "Land clearing and lot cleanup in Brandon, FL — Hillsborough suburban lots and oak hammock edges. "
            "Faith Works brush cutting from Auburndale. Photo-based estimates."
        ),
        "hook": (
            "Brandon is Hillsborough's suburban core where oversized lots, oak hammocks, and retention ponds on "
            "established neighborhoods create rear-section and pond bank clearing needs mowers cannot handle."
        ),
        "context": (
            "Faith Works serves Brandon owners with overgrown rear woods on large suburban parcels, retention "
            "pond edges on community plats, and rural edges toward Lithia where fence lines and ditch lines "
            "need brush cutting equipment."
        ),
        "local_detail": (
            "Properties near Bloomingdale and along Lithia Pinecrest often combine oak hammock mulching with "
            "rear-lot clearing when saplings reclaim sections between professional mowing visits."
        ),
        "property_types": [
            "Established Brandon homes with large rear hammock sections",
            "Subdivision retention pond edges needing cutback",
            "Commercial pads along Brandon Boulevard with brush perimeters",
            "Rural-edge Brandon acreage toward Lithia",
            "Vacant Hillsborough parcels awaiting build prep",
        ],
        "common_jobs": [
            "Rear hammock clearing on oversized Brandon lots",
            "Retention pond bank brush removal",
            "Fence line reopening on Lithia-edge acreage",
            "Forestry mulching on sapling-choked sections",
            "Lot cleanup before Brandon construction or sale",
            "Storm debris haul-off after Hillsborough storms",
        ],
        "intent_routes": [
            {"label": "Suburban rear lots", "slug": "land-clearing", "text": "Clear dense rear growth on oversized Brandon residential parcels."},
            {"label": "Retention pond edges", "slug": "pond-bank-clearing", "text": "Trim brush on retention banks in Brandon subdivisions."},
            {"label": "Oak hammock mulching", "slug": "forestry-mulching", "text": "Mulch saplings and undergrowth on Brandon hammock sections."},
            {"label": "Storm debris removal", "slug": "storm-debris-cleanup", "text": "Haul limbs and brush after storms on Brandon properties."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Brandon including Bloomingdale and Lithia edges?",
                "Brandon suburban and rural-edge properties are within our Hillsborough travel range — send photos and address for estimate review.",
            ),
            (
                "Can Faith Works clear oak hammock rear sections on Brandon lots?",
                "Oak hammock overgrowth on large Brandon parcels often needs forestry mulching — photos showing access and tree density confirm scope before scheduling.",
            ),
        ],
        "strip_note": "Brandon rear hammocks, retention ponds, and suburban lot clearing.",
    },
    "tampa-fl": {
        "meta_description": (
            "Land clearing and property cleanup in Tampa, FL — urban lots, retention ponds, and vacant land. "
            "Faith Works brush cutting from Auburndale. Photo-based estimates for Hillsborough."
        ),
        "hook": (
            "Tampa spans dense urban neighborhoods, bay-adjacent communities, and suburban oversized lots where "
            "vacant parcels, retention ponds, and rear wooded sections need clearing standard lawn crews avoid."
        ),
        "context": (
            "Faith Works handles Tampa jobs on private properties where overgrown vacant land, commercial brush "
            "perimeters, and rear acreage on oversized city lots need compact equipment — gate width and access "
            "constraints are confirmed from photos before scheduling."
        ),
        "local_detail": (
            "Properties in East Tampa, Temple Terrace edges, and South Tampa oversized lots often combine "
            "retention pond maintenance with rear-lot clearing when summer growth reduces usable outdoor space."
        ),
        "property_types": [
            "Oversized Tampa lots with rear wooded sections",
            "Vacant urban and infill parcels awaiting development",
            "Commercial and industrial pads with brush perimeters",
            "Subdivision retention pond edges needing cutback",
            "Bay-adjacent properties with drainage and ditch frontage",
        ],
        "common_jobs": [
            "Vacant lot clearing before Tampa construction",
            "Rear lot brush removal on oversized city parcels",
            "Commercial perimeter overgrowth removal",
            "Retention pond bank brush cutback",
            "Debris removal and property cleanup for listings",
            "Forestry mulching on sapling-choked rear sections",
        ],
        "intent_routes": [
            {"label": "Vacant urban lots", "slug": "lot-cleanup", "text": "Open overgrown Tampa vacant parcels before build or sale."},
            {"label": "Rear city acreage", "slug": "land-clearing", "text": "Clear dense rear growth on oversized Tampa residential lots."},
            {"label": "Commercial perimeters", "slug": "property-cleanup", "text": "Restore visibility on brush-choked Tampa commercial edges."},
            {"label": "Retention and ditches", "slug": "pond-cleanup", "text": "Clean retention ponds and drainage edges on Tampa properties."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Tampa with tight urban lot access?",
                "Tampa urban lots often have gate and alley constraints — send gate measurements and photos of the work area so we confirm compact equipment fit.",
            ),
            (
                "Can Faith Works clear vacant land and commercial edges in Tampa?",
                "Vacant parcel and commercial perimeter clearing on private Tampa property is common — photo-based estimates establish scope before mobilization.",
            ),
        ],
        "strip_note": "Tampa vacant lots, rear acreage, and commercial perimeter clearing.",
    },
    "valrico-fl": {
        "meta_description": (
            "Land clearing and fence line work in Valrico, FL — Lithia Springs area and east Hillsborough acreage. "
            "Faith Works from Auburndale. Brush cutting and pond banks. Free estimates."
        ),
        "hook": (
            "Valrico blends established east Hillsborough neighborhoods with oak hammock acreage toward Lithia, "
            "where oversized lots, pond edges, and rural fence lines need clearing beyond routine lawn service."
        ),
        "context": (
            "Faith Works serves Valrico owners with overgrown rear hammock sections, retention ponds on plats, "
            "and multi-acre edges toward Dover where saplings and undergrowth reclaim fence lines and access "
            "paths each growing season."
        ),
        "local_detail": (
            "Properties near Lithia Springs and along Lithia Pinecrest Road often need combined fence line and "
            "rear-lot work when oak saplings close gaps between professional maintenance cycles."
        ),
        "property_types": [
            "Valrico homes with large oak hammock rear sections",
            "Lithia-edge acreage with overgrown fence lines",
            "Retention pond edges on Valrico subdivisions",
            "Rural Hillsborough parcels toward Dover",
            "Vacant east Hillsborough land awaiting build prep",
        ],
        "common_jobs": [
            "Oak hammock mulching on Valrico rear sections",
            "Fence line reopening on Lithia-edge acreage",
            "Retention pond bank brush removal",
            "Rear lot clearing before Valrico construction",
            "Access path reopening on multi-acre parcels",
            "Property cleanup for Valrico listing prep",
        ],
        "intent_routes": [
            {"label": "Hammock rear sections", "slug": "forestry-mulching", "text": "Mulch oak saplings and undergrowth on Valrico rear parcels."},
            {"label": "Lithia fence lines", "slug": "fence-line-clearing", "text": "Reopen overgrown fence runs on Valrico and Lithia-edge acreage."},
            {"label": "Subdivision ponds", "slug": "pond-bank-clearing", "text": "Trim retention banks on Valrico neighborhood properties."},
            {"label": "Build prep lots", "slug": "lot-cleanup", "text": "Clear overgrown Valrico lots before construction or sale."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Valrico and the Lithia Springs area?",
                "Valrico and east Hillsborough acreage toward Lithia are within our travel range — send photos and address for estimate review.",
            ),
            (
                "Can Faith Works clear large rear hammock sections on Valrico properties?",
                "Oak hammock overgrowth on Valrico lots often needs forestry mulching — photos showing access width and vegetation density confirm scope.",
            ),
        ],
        "strip_note": "Valrico oak hammocks, Lithia fence lines, and retention pond banks.",
    },
    "zephyrhills-fl": {
        "meta_description": (
            "Land clearing and acreage cleanup in Zephyrhills, FL — rolling Pasco hills and rural homesteads. "
            "Faith Works forestry mulching from Auburndale. Pond banks and ditch work."
        ),
        "hook": (
            "Zephyrhills is Pasco's hill country where rolling acreage, pond edges, and former agricultural land "
            "create fence lines, access roads, and ditch lines that brush closes off between seasons."
        ),
        "context": (
            "Faith Works handles Zephyrhills properties where rural homestead sections, retention ponds on "
            "newer plats, and county-road ditch frontage have outgrown hand-tool maintenance — especially on "
            "multi-acre parcels toward Dade City and Wesley Chapel borders."
        ),
        "local_detail": (
            "Land along SR-54 and toward Crystal Springs often mixes pasture-edge mulching with pond bank "
            "maintenance when summer growth obscures property boundaries and drainage paths."
        ),
        "property_types": [
            "Rolling Pasco acreage with pond and ditch frontage",
            "Rural Zephyrhills homesteads with long fence lines",
            "Former agricultural parcels with sapling regrowth",
            "Subdivision retention pond edges on Pasco plats",
            "Vacant hill-country land awaiting build prep",
        ],
        "common_jobs": [
            "Forestry mulching on Zephyrhills rolling acreage",
            "Pond bank brush removal on rural water features",
            "Ditch clearing on Pasco county-road frontage",
            "Fence line reopening on multi-acre homesteads",
            "Access road clearing on Zephyrhills ranch land",
            "Acreage cleanup before Pasco sale or transition",
        ],
        "intent_routes": [
            {"label": "Pasco hill acreage", "slug": "forestry-mulching", "text": "Mulch saplings and brush on rolling Zephyrhills parcels."},
            {"label": "Rural pond banks", "slug": "pond-bank-clearing", "text": "Trim banks on private ponds and ditches near Zephyrhills."},
            {"label": "County ditch lines", "slug": "ditch-clearing", "text": "Open drainage ditches on Zephyrhills road frontage."},
            {"label": "Homestead access", "slug": "access-road-clearing", "text": "Reopen overgrown access paths on Zephyrhills acreage."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Zephyrhills rolling acreage and rural homesteads?",
                "Zephyrhills hill-country and multi-acre properties are within our Pasco service range — send photos of fence lines and access for scope review.",
            ),
            (
                "Can Faith Works clear ditch lines on Zephyrhills county-road properties?",
                "Outdoor ditch clearing on private Zephyrhills frontage is common — photos showing ditch location and vegetation density confirm accurate scope.",
            ),
        ],
        "strip_note": "Zephyrhills rolling acreage, pond banks, and Pasco ditch clearing.",
    },
    "wesley-chapel-fl": {
        "meta_description": (
            "Land clearing and lot cleanup in Wesley Chapel, FL — Pasco growth corridor and new subdivisions. "
            "Faith Works brush cutting from Auburndale. Retention ponds and rear buffers. Free estimates."
        ),
        "hook": (
            "Wesley Chapel is one of Pasco's fastest-growing corridors, where new subdivisions, conservation "
            "buffers, and retention ponds on fresh plats create immediate demand for rear-lot and pond edge clearing."
        ),
        "context": (
            "Faith Works serves Wesley Chapel owners with overgrown conservation borders behind new homes, "
            "retention pond banks on Wiregrass and Seven Oaks plats, and rural edges toward Dade City where "
            "former pasture land regrows between build phases."
        ),
        "local_detail": (
            "Properties along SR-54 and SR-56 often need retention pond and rear-buffer clearing combined when "
            "builder-grade landscaping leaves wooded sections unmanaged after move-in."
        ),
        "property_types": [
            "New Wesley Chapel plats with rear conservation overgrowth",
            "Retention pond edges on Wiregrass area subdivisions",
            "Rural Pasco acreage toward Dade City borders",
            "Commercial pads on SR-54 with brush perimeters",
            "Vacant growth-corridor land awaiting development prep",
        ],
        "common_jobs": [
            "Conservation-buffer clearing on new Wesley Chapel lots",
            "Retention pond bank brush cutback on Pasco plats",
            "Rear lot clearing before fencing and pool projects",
            "Fence line reopening on rural Wesley Chapel acreage",
            "Lot cleanup on builder leftover wooded sections",
            "Forestry mulching on sapling-choked rear buffers",
        ],
        "intent_routes": [
            {"label": "New plat rear buffers", "slug": "overgrowth-removal", "text": "Remove dense rear growth on Wesley Chapel subdivision lots."},
            {"label": "Retention pond edges", "slug": "pond-bank-clearing", "text": "Clean retention banks on Wesley Chapel neighborhood properties."},
            {"label": "Build leftover clearing", "slug": "lot-cleanup", "text": "Clear unmanaged wooded sections on new Wesley Chapel homes."},
            {"label": "Pasco fence lines", "slug": "fence-line-clearing", "text": "Reopen fence runs on Wesley Chapel rural-edge acreage."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works clear conservation buffers on new Wesley Chapel homes?",
                "We clear private outdoor areas you own or maintain on Wesley Chapel lots — not public conservation. Photos showing property lines confirm scope.",
            ),
            (
                "Can Faith Works handle retention pond banks in Wesley Chapel subdivisions?",
                "Retention pond edge clearing on Wesley Chapel plats is common — send photos of bank slope and access for estimate review before scheduling.",
            ),
        ],
        "strip_note": "Wesley Chapel retention ponds, rear buffers, and new plat clearing.",
    },
    "dade-city-fl": {
        "meta_description": (
            "Land clearing and ranch acreage work in Dade City, FL — Pasco seat and rolling cattle country. "
            "Faith Works from Auburndale. Fence lines and access roads. Photo-based estimates."
        ),
        "hook": (
            "Dade City is Pasco County's seat in rolling cattle country, where ranch acreage, pond edges, and "
            "historic downtown edges need fence lines and access roads cleared after wet-season brush regrowth."
        ),
        "context": (
            "Faith Works handles Dade City properties where multi-acre homesteads, county-road ditch lines, and "
            "former agricultural edges toward Zephyrhills have outgrown routine maintenance — long fence runs "
            "and ranch roads are planned from photos before equipment mobilization."
        ),
        "local_detail": (
            "Land toward San Antonio and Trilby often involves cattle-fence boundaries and pond banks where "
            "work is staged in sections after photo review confirms entry gates and soft-ground access."
        ),
        "property_types": [
            "Dade City ranch acreage with overgrown access roads",
            "Historic downtown edges with large rear sections",
            "Rolling Pasco homesteads with pond and ditch frontage",
            "Former agricultural parcels with sapling regrowth",
            "Vacant Pasco hill-country land awaiting build prep",
        ],
        "common_jobs": [
            "Ranch access road clearing on Dade City acreage",
            "Fence line reopening on multi-acre Pasco homesteads",
            "Pond bank brush removal on rural water features",
            "Forestry mulching on pasture-edge sapling regrowth",
            "Ditch clearing on Pasco county-road frontage",
            "Acreage cleanup before Dade City sale or transition",
        ],
        "intent_routes": [
            {"label": "Ranch access roads", "slug": "access-road-clearing", "text": "Reopen overgrown ranch paths on Dade City acreage."},
            {"label": "Cattle fence lines", "slug": "fence-line-clearing", "text": "Clear overgrown fence runs on Dade City ranch boundaries."},
            {"label": "Pasco pond banks", "slug": "pond-bank-clearing", "text": "Trim banks on private ponds and ditches near Dade City."},
            {"label": "Pasture-edge mulching", "slug": "forestry-mulching", "text": "Mulch saplings on former agricultural Dade City parcels."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Dade City ranch and multi-acre Pasco properties?",
                "Dade City ranch acreage with access roads and fence lines is within our Pasco range — send photos of boundaries and entry gates for scope planning.",
            ),
            (
                "Can Faith Works travel from Auburndale to Dade City for acreage clearing?",
                "Dade City is within our extended Pasco service area — address and photos confirm travel and scheduling before equipment mobilization.",
            ),
        ],
        "strip_note": "Dade City ranch access, fence lines, and Pasco acreage clearing.",
    },
    "wauchula-fl": {
        "meta_description": (
            "Land clearing and acreage cleanup in Wauchula, FL — Hardee County cattle and citrus country. "
            "Faith Works forestry mulching from Auburndale. Fence lines and pond banks."
        ),
        "hook": (
            "Wauchula is Hardee County's agricultural hub where cattle ranchland, citrus edges, and rural "
            "homesteads depend on fence lines, access roads, and pond banks that brush reclaims each season."
        ),
        "context": (
            "Faith Works serves Wauchula owners with overgrown ranch sections, ditch lines on county roads, and "
            "pond edges on rural Hardee parcels where forestry mulching handles sapling regrowth faster than "
            "hand clearing on multi-acre boundaries."
        ),
        "local_detail": (
            "Properties toward Zolfo Springs and Bowling Green often involve long fence runs and pasture ponds "
            "where staged clearing plans are confirmed from aerial or ground photos before work begins."
        ),
        "property_types": [
            "Hardee County ranch acreage with overgrown access roads",
            "Citrus and pasture transition parcels",
            "Rural Wauchula homesteads with pond edges",
            "Commercial pads along US-17 with brush perimeters",
            "Vacant Hardee land awaiting agricultural or build transition",
        ],
        "common_jobs": [
            "Fence line clearing on Wauchula ranch boundaries",
            "Access road reopening on Hardee County acreage",
            "Pond bank brush removal on rural water features",
            "Forestry mulching on citrus and pasture edges",
            "Ditch clearing on Hardee county-road frontage",
            "Acreage cleanup before Wauchula sale or estate transfer",
        ],
        "intent_routes": [
            {"label": "Hardee ranch fences", "slug": "fence-line-clearing", "text": "Reopen overgrown fence runs on Wauchula ranch acreage."},
            {"label": "Rural access paths", "slug": "access-road-clearing", "text": "Clear brush blocking access roads on Wauchula properties."},
            {"label": "Pasture pond banks", "slug": "pond-bank-clearing", "text": "Trim banks on private ponds and ditches near Wauchula."},
            {"label": "Citrus-edge mulching", "slug": "forestry-mulching", "text": "Mulch saplings on agricultural transition parcels in Wauchula."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works travel to Wauchula for Hardee County ranch clearing?",
                "Wauchula and Hardee County acreage are within our extended rural service range — send photos of fence lines, access roads, and pond edges for estimate review.",
            ),
            (
                "Can Faith Works clear citrus and pasture edges in Wauchula?",
                "Agricultural transition parcels around Wauchula often need fence line and forestry mulching work — photos confirm vegetation type and access before scheduling.",
            ),
        ],
        "strip_note": "Wauchula ranch fences, Hardee acreage, and pasture pond banks.",
    },
    "sebring-fl": {
        "meta_description": (
            "Land clearing and lake work in Sebring, FL — Highlands lake country and Circle district lots. "
            "Faith Works brush cutting from Auburndale. Pond banks and acreage cleanup."
        ),
        "hook": (
            "Sebring anchors Highlands County lake country around Lake Jackson and the historic Circle, where "
            "lakefront lots, rural acreage, and downtown edges need pond banks and rear sections cleared."
        ),
        "context": (
            "Faith Works handles Sebring properties where lake-adjacent homes, wooded rear sections on oversized "
            "lots, and rural Highlands acreage toward Avon Park have outgrown routine maintenance — sandy Ridge "
            "terrain often favors forestry mulching on sapling regrowth."
        ),
        "local_detail": (
            "Properties near the Circle and along US-27 often combine lake bank maintenance with rear-lot "
            "clearing when summer growth closes water views and side-yard access on lake-country parcels."
        ),
        "property_types": [
            "Lake Jackson and Sebring lakefront homes",
            "Historic Circle area lots with rear wooded sections",
            "Rural Highlands acreage toward Avon Park",
            "Commercial pads on US-27 with brush perimeters",
            "Vacant lake-country parcels awaiting build prep",
        ],
        "common_jobs": [
            "Lake bank brush removal on Sebring waterfront properties",
            "Rear lot clearing on oversized Circle district lots",
            "Forestry mulching on Ridge sapling regrowth",
            "Fence line reopening on rural Highlands acreage",
            "Ditch clearing on Sebring county-road frontage",
            "Property cleanup before Highlands sale or probate",
        ],
        "intent_routes": [
            {"label": "Sebring lake banks", "slug": "pond-bank-clearing", "text": "Clean private banks on Sebring lake and pond frontage."},
            {"label": "Circle district lots", "slug": "land-clearing", "text": "Clear overgrown rear sections on Sebring in-town properties."},
            {"label": "Highlands acreage", "slug": "acreage-cleanup", "text": "Restore usable acreage on overgrown Sebring rural parcels."},
            {"label": "Ridge sapling mulching", "slug": "forestry-mulching", "text": "Mulch saplings on sandy Highlands sections near Sebring."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Sebring lakefront and Circle district properties?",
                "Sebring lake-country and in-town lots are within our extended Highlands travel range — send photos and address for scope confirmation.",
            ),
            (
                "Can Faith Works clear rural Sebring acreage toward Avon Park?",
                "Rural Highlands acreage around Sebring is handled when photos confirm fence lines, pond edges, and equipment access before scheduling.",
            ),
        ],
        "strip_note": "Sebring lake banks, Circle district lots, and Highlands acreage.",
    },
    "avon-park-fl": {
        "meta_description": (
            "Land clearing and acreage cleanup in Avon Park, FL — Highlands lakes and rural Ridge land. "
            "Faith Works forestry mulching from Auburndale. Pond banks and fence lines."
        ),
        "hook": (
            "Avon Park sits among Highlands lakes and Ridge scrub where lakefront homes, air-base-area "
            "neighborhoods, and rural acreage need pond banks and fence lines cleared each growing season."
        ),
        "context": (
            "Faith Works serves Avon Park owners with overgrown lake edges, wooded homestead sections, and "
            "county-road ditch lines where sandy Ridge terrain and sapling regrowth respond well to forestry "
            "mulching rather than prolonged hand clearing."
        ),
        "local_detail": (
            "Properties toward Frostproof and Lake Glenada often combine lake bank brush removal with acreage "
            "fence line work when summer growth obscures boundaries on multi-lot rural parcels."
        ),
        "property_types": [
            "Highlands lakefront homes with overgrown banks",
            "Avon Park in-town lots with rear wooded sections",
            "Ridge scrub acreage with sapling regrowth",
            "Rural homesteads with long fence lines",
            "Vacant Highlands parcels awaiting build or sale prep",
        ],
        "common_jobs": [
            "Lake bank brush removal on Avon Park waterfront lots",
            "Forestry mulching on Ridge scrub sections",
            "Fence line reopening on rural Highlands acreage",
            "Rear lot clearing on Avon Park residential parcels",
            "Ditch clearing on county-road frontage",
            "Acreage cleanup before Avon Park listing or transition",
        ],
        "intent_routes": [
            {"label": "Highlands lake edges", "slug": "pond-bank-clearing", "text": "Trim banks on private lake frontage in Avon Park."},
            {"label": "Ridge scrub mulching", "slug": "forestry-mulching", "text": "Mulch saplings and scrub on Avon Park Ridge acreage."},
            {"label": "Rural fence lines", "slug": "fence-line-clearing", "text": "Reopen overgrown fence runs on Avon Park homesteads."},
            {"label": "Rear lot reclaim", "slug": "overgrowth-removal", "text": "Remove dense rear growth on Avon Park residential properties."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Avon Park lakefront and Ridge scrub properties?",
                "Avon Park lake-country and scrub acreage are within our extended Highlands range — send photos of banks, fence lines, and access for estimate review.",
            ),
            (
                "Can Faith Works travel from Auburndale to Avon Park for acreage work?",
                "Avon Park is within our extended south-central Florida service area — address and photos confirm travel and scheduling before mobilization.",
            ),
        ],
        "strip_note": "Avon Park lake banks, Ridge scrub mulching, and fence line clearing.",
    },
    "arcadia-fl": {
        "meta_description": (
            "Land clearing and ranch work in Arcadia, FL — DeSoto County cattle country and Peace River land. "
            "Faith Works from Auburndale. Access roads and fence lines. Free photo estimates."
        ),
        "hook": (
            "Arcadia is DeSoto County's cattle and citrus center where ranch acreage, Peace River-area land, "
            "and historic downtown edges need access roads and fence lines cleared after seasonal brush regrowth."
        ),
        "context": (
            "Faith Works handles Arcadia properties where multi-acre ranch sections, pond edges on rural water "
            "features, and ditch lines along US-17 frontage have outgrown hand-tool maintenance — long boundary "
            "runs are staged from photos before equipment routes are set."
        ),
        "local_detail": (
            "Land toward Fort Ogden and Nocatee often involves cattle-fence boundaries and pasture ponds where "
            "clearing is planned in sections after photo review confirms gates and soft-ground access."
        ),
        "property_types": [
            "DeSoto County ranch acreage with overgrown access roads",
            "Citrus and cattle transition parcels",
            "Peace River-area rural homesteads",
            "Historic Arcadia edges with large rear sections",
            "Vacant DeSoto land awaiting agricultural transition",
        ],
        "common_jobs": [
            "Ranch access road clearing on Arcadia acreage",
            "Fence line reopening on DeSoto County boundaries",
            "Pond bank brush removal on rural water features",
            "Forestry mulching on pasture and citrus edges",
            "Ditch clearing on US-17 and county-road frontage",
            "Acreage cleanup before Arcadia sale or estate transfer",
        ],
        "intent_routes": [
            {"label": "DeSoto ranch access", "slug": "access-road-clearing", "text": "Reopen overgrown ranch paths on Arcadia acreage."},
            {"label": "Cattle fence lines", "slug": "fence-line-clearing", "text": "Clear overgrown fence runs on Arcadia ranch boundaries."},
            {"label": "Rural pond banks", "slug": "pond-bank-clearing", "text": "Trim banks on private ponds and ditches near Arcadia."},
            {"label": "Pasture-edge mulching", "slug": "forestry-mulching", "text": "Mulch saplings on DeSoto agricultural transition parcels."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works travel to Arcadia for DeSoto County ranch clearing?",
                "Arcadia ranch acreage with access roads and fence lines is within our extended rural range — send photos of boundaries and entry gates for scope planning.",
            ),
            (
                "Can Faith Works clear Peace River-area acreage near Arcadia?",
                "Rural DeSoto parcels around Arcadia are handled when photos confirm pond edges, fence runs, and equipment access before scheduling.",
            ),
        ],
        "strip_note": "Arcadia ranch access, DeSoto fence lines, and pasture pond banks.",
    },
    "the-villages-fl": {
        "meta_description": (
            "Land clearing and overgrowth removal in The Villages, FL — conservation edges and oversized lots. "
            "Faith Works brush cutting from Auburndale. Pond banks and fence lines. Free estimates."
        ),
        "hook": (
            "The Villages spans Sumter, Lake, and Marion counties where golf-community lots, conservation "
            "borders, and retention ponds create rear-buffer and pond edge clearing needs beyond HOA mowing."
        ),
        "context": (
            "Faith Works serves Villages property owners on private outdoor areas where conservation greenbelts, "
            "retention ponds, and oversized lot rear sections have outgrown routine maintenance — scope respects "
            "property lines and neighbor buffers confirmed from photos."
        ),
        "local_detail": (
            "Properties backing to golf course roughs and wetland buffers often need staged brush cutback that "
            "restores usable yard space without crossing into protected common areas."
        ),
        "property_types": [
            "Villages homes backing to conservation and wetland buffers",
            "Retention pond edges on community plats",
            "Oversized Villages lots with rear wooded sections",
            "Golf-community properties with rough-adjacent overgrowth",
            "Lake County Villages parcels toward Fenney and Brownwood",
        ],
        "common_jobs": [
            "Conservation-border overgrowth removal on Villages lots",
            "Retention pond bank brush cutback",
            "Rear lot clearing on oversized Villages parcels",
            "Fence line reopening where lots meet greenbelts",
            "Property cleanup for Villages listing prep",
            "Storm debris haul-off after central Florida wind events",
        ],
        "intent_routes": [
            {"label": "Greenbelt edges", "slug": "overgrowth-removal", "text": "Remove dense growth where Villages lots meet conservation buffers."},
            {"label": "Community pond banks", "slug": "pond-bank-clearing", "text": "Trim brush on private retention edges in The Villages."},
            {"label": "Rear lot reclaim", "slug": "property-cleanup", "text": "Restore usable outdoor space on overgrown Villages properties."},
            {"label": "Buffer fence lines", "slug": "fence-line-clearing", "text": "Reopen fence runs on Villages lots adjacent to greenbelts."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works clear conservation borders on Villages properties?",
                "We clear private outdoor areas you own or maintain on Villages lots — not HOA common areas or protected conservation. Photos showing property lines confirm scope.",
            ),
            (
                "Can Faith Works work in The Villages across Sumter, Lake, and Marion sections?",
                "The Villages spans multiple counties — send your address and photos so we confirm travel, access, and equipment fit for your specific lot.",
            ),
        ],
        "strip_note": "The Villages conservation edges, retention ponds, and rear lot clearing.",
    },
    "bushnell-fl": {
        "meta_description": (
            "Land clearing and acreage cleanup in Bushnell, FL — Sumter County I-75 corridor and rural land. "
            "Faith Works from Auburndale. Fence lines and pond banks. Photo-based estimates."
        ),
        "hook": (
            "Bushnell sits along the I-75 corridor in Sumter County where rural acreage, pond edges, and "
            "homestead fence lines toward Webster and Lake Panasoffkee need clearing after wet-season regrowth."
        ),
        "context": (
            "Faith Works serves Bushnell owners with overgrown multi-acre sections, ditch lines on county roads, "
            "and pond banks on rural Sumter parcels where access roads and fence runs close off between mowing "
            "seasons on soft pasture ground."
        ),
        "local_detail": (
            "Properties toward Lake Panasoffkee and the Villages fringe often combine pond bank brush removal "
            "with acreage fence line work when summer growth obscures boundaries and drainage paths."
        ),
        "property_types": [
            "Sumter County rural acreage with pond edges",
            "I-75 corridor homesteads with overgrown access roads",
            "Lake Panasoffkee adjacent properties with bank overgrowth",
            "Former pasture land with sapling regrowth",
            "Vacant Sumter parcels awaiting build or sale prep",
        ],
        "common_jobs": [
            "Fence line clearing on Bushnell multi-acre homesteads",
            "Pond bank brush removal on Lake Panasoffkee edges",
            "Access road reopening on rural Sumter acreage",
            "Forestry mulching on pasture-edge sapling regrowth",
            "Ditch clearing on Bushnell county-road frontage",
            "Acreage cleanup before Sumter sale or transition",
        ],
        "intent_routes": [
            {"label": "Sumter acreage fences", "slug": "fence-line-clearing", "text": "Reopen overgrown fence runs on Bushnell rural parcels."},
            {"label": "Panasoffkee banks", "slug": "pond-bank-clearing", "text": "Trim banks on private water edges near Bushnell and Lake Panasoffkee."},
            {"label": "Rural access roads", "slug": "access-road-clearing", "text": "Clear brush blocking access paths on Bushnell acreage."},
            {"label": "Pasture-edge mulching", "slug": "forestry-mulching", "text": "Mulch saplings on former pasture land around Bushnell."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Bushnell and Sumter County rural acreage?",
                "Bushnell multi-acre properties with fence lines and pond banks are within our Sumter service range — send photos for estimate review.",
            ),
            (
                "Can Faith Works clear land near Lake Panasoffkee in Bushnell?",
                "Lake Panasoffkee-adjacent Bushnell properties with overgrown banks are handled when photos confirm bank slope and equipment access before scheduling.",
            ),
        ],
        "strip_note": "Bushnell Sumter acreage, Panasoffkee banks, and fence line clearing.",
    },
    "bradenton-fl": {
        "meta_description": (
            "Land clearing and lot cleanup in Bradenton, FL — Manatee River area and coastal-inland lots. "
            "Faith Works brush cutting from Auburndale. Pond banks and debris removal. Free estimates."
        ),
        "hook": (
            "Bradenton blends Manatee River waterfront, established neighborhoods, and east Manatee acreage "
            "where retention ponds, oak hammocks, and vacant parcels need clearing beyond standard lawn service."
        ),
        "context": (
            "Faith Works handles Bradenton properties where oversized lot rear sections, retention pond edges on "
            "community plats, and rural edges toward Myakka need brush cutting equipment — salt-air vegetation "
            "and hammock woods often require forestry mulching on sapling regrowth."
        ),
        "local_detail": (
            "Properties in East Bradenton and toward Lakewood Ranch borders often combine retention pond "
            "maintenance with rear-lot clearing when summer growth closes usable yard space on larger parcels."
        ),
        "property_types": [
            "Bradenton homes with large oak hammock rear sections",
            "Manatee River-area lots with drainage and pond edges",
            "Retention pond edges on Bradenton subdivisions",
            "East Manatee acreage toward Myakka borders",
            "Vacant Manatee parcels awaiting build or sale prep",
        ],
        "common_jobs": [
            "Rear hammock clearing on oversized Bradenton lots",
            "Retention pond bank brush removal",
            "Vacant lot cleanup before Bradenton construction",
            "Forestry mulching on sapling-choked sections",
            "Fence line reopening on east Manatee acreage",
            "Storm debris haul-off after Manatee County storms",
        ],
        "intent_routes": [
            {"label": "Bradenton rear lots", "slug": "land-clearing", "text": "Clear dense rear growth on oversized Bradenton residential parcels."},
            {"label": "Retention pond edges", "slug": "pond-bank-clearing", "text": "Trim brush on retention banks in Bradenton neighborhoods."},
            {"label": "Vacant lot prep", "slug": "lot-cleanup", "text": "Open overgrown Bradenton vacant parcels before build or sale."},
            {"label": "Storm debris haul-off", "slug": "storm-debris-cleanup", "text": "Remove storm limbs and brush from Bradenton properties."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Bradenton including east Manatee and river-area properties?",
                "Bradenton suburban and acreage properties are within our Manatee travel range — send photos and address for scope confirmation.",
            ),
            (
                "Can Faith Works clear oak hammock rear sections in Bradenton?",
                "Oak hammock overgrowth on large Bradenton lots often needs forestry mulching — photos showing access and vegetation density confirm scope before scheduling.",
            ),
        ],
        "strip_note": "Bradenton rear hammocks, retention ponds, and Manatee lot clearing.",
    },
    "parrish-fl": {
        "meta_description": (
            "Land clearing and lot cleanup in Parrish, FL — North River Ranch growth and east Manatee acreage. "
            "Faith Works brush cutting from Auburndale. Retention ponds and rear buffers."
        ),
        "hook": (
            "Parrish is Manatee's fast-growing north corridor where North River Ranch, new subdivisions, and "
            "rural acreage toward Duette create conservation buffers and retention ponds needing clearing."
        ),
        "context": (
            "Faith Works serves Parrish owners with overgrown rear sections on new plats, retention pond banks "
            "on growth-corridor communities, and rural fence lines on east Manatee land where pasture edges "
            "regrow between build phases and agricultural use."
        ),
        "local_detail": (
            "North River Ranch and Fort Hamer area properties often need conservation-buffer and retention pond "
            "work combined when builder landscaping leaves wooded rear sections unmanaged after closing."
        ),
        "property_types": [
            "North River Ranch lots with rear conservation overgrowth",
            "Retention pond edges on Parrish growth-corridor plats",
            "East Manatee rural acreage with fence line overgrowth",
            "New Parrish subdivisions with unmanaged rear buffers",
            "Vacant Manatee land toward Duette awaiting prep",
        ],
        "common_jobs": [
            "Conservation-buffer clearing on new Parrish lots",
            "Retention pond bank brush cutback on growth plats",
            "Rear lot clearing before fencing projects",
            "Fence line reopening on east Manatee acreage",
            "Forestry mulching on sapling-choked rear sections",
            "Lot cleanup on builder leftover wooded parcels",
        ],
        "intent_routes": [
            {"label": "North River Ranch buffers", "slug": "overgrowth-removal", "text": "Remove dense rear growth on Parrish growth-corridor lots."},
            {"label": "Retention pond edges", "slug": "pond-bank-clearing", "text": "Clean retention banks on Parrish subdivision properties."},
            {"label": "New plat cleanup", "slug": "lot-cleanup", "text": "Clear unmanaged wooded sections on new Parrish homes."},
            {"label": "East Manatee fences", "slug": "fence-line-clearing", "text": "Reopen fence runs on Parrish rural-edge acreage."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve Parrish including North River Ranch?",
                "Parrish growth-corridor and North River Ranch properties are within our Manatee service range — send photos and address for estimate review.",
            ),
            (
                "Can Faith Works clear conservation buffers on new Parrish homes?",
                "We clear private outdoor areas you own or maintain on Parrish lots — not public conservation. Photos showing property lines confirm scope before scheduling.",
            ),
        ],
        "strip_note": "Parrish North River Ranch buffers, retention ponds, and new plat clearing.",
    },
}
