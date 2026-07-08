#!/usr/bin/env python3
"""Verify JSON-LD schema coverage across generated Faith Works HTML pages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGE_EXPECTATIONS = {
    "index.html": {
        "required": ["Organization", "WebSite", "WebPage", "FAQPage", "BreadcrumbList", "ImageObject"],
    },
    "services.html": {
        "required": ["Organization", "WebSite", "WebPage", "CollectionPage", "BreadcrumbList", "ItemList"],
    },
    "about.html": {
        "required": ["Organization", "WebPage", "AboutPage", "BreadcrumbList"],
    },
    "contact.html": {
        "required": ["Organization", "WebPage", "ContactPage", "BreadcrumbList"],
    },
    "gallery.html": {
        "required": ["Organization", "WebPage", "CollectionPage", "BreadcrumbList", "ImageObject"],
    },
    "service-areas.html": {
        "required": ["Organization", "WebPage", "CollectionPage", "BreadcrumbList", "ItemList"],
    },
    "privacy-policy.html": {
        "required": ["Organization", "WebPage", "BreadcrumbList"],
    },
    "image-use-policy.html": {
        "required": ["Organization", "WebPage", "BreadcrumbList"],
    },
}

SERVICE_EXPECTATIONS = {
    "required": ["Organization", "WebPage", "Service", "BreadcrumbList", "FAQPage"],
}

AREA_CITY_EXPECTATIONS = {
    "required": ["Organization", "WebPage", "City", "BreadcrumbList", "FAQPage"],
}

AREA_COUNTY_EXPECTATIONS = {
    "required": ["Organization", "WebPage", "AdministrativeArea", "BreadcrumbList", "FAQPage", "ItemList"],
}


def load_graphs(html: str) -> list[dict]:
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>',
        html,
        flags=re.DOTALL,
    )
    graphs: list[dict] = []
    for block in blocks:
        data = json.loads(block.strip())
        if "@graph" in data:
            graphs.extend(data["@graph"])
        else:
            graphs.append(data)
    return graphs


def type_names(node: dict) -> set[str]:
    value = node.get("@type", [])
    if isinstance(value, str):
        return {value}
    return set(value)


def all_types(graphs: list[dict]) -> set[str]:
    names: set[str] = set()
    for node in graphs:
        names.update(type_names(node))
    return names


def check_page(path: Path, required: set[str]) -> list[str]:
    html = path.read_text(encoding="utf-8")
    graphs = load_graphs(html)
    if not graphs:
        return [f"{path.relative_to(ROOT)}: no JSON-LD found"]
    found = all_types(graphs)
    missing = sorted(required - found)
    if missing:
        return [f"{path.relative_to(ROOT)}: missing {', '.join(missing)}"]
    return []


def main() -> int:
    errors: list[str] = []

    for rel, spec in PAGE_EXPECTATIONS.items():
        errors.extend(check_page(ROOT / rel, set(spec["required"])))

    for path in sorted(ROOT.glob("*.html")):
        if path.name in PAGE_EXPECTATIONS or path.name in {"404.html", "thank-you.html"}:
            continue
        errors.extend(check_page(path, set(SERVICE_EXPECTATIONS["required"])))

    for path in sorted((ROOT / "areas").glob("*.html")):
        if "county" in path.stem:
            errors.extend(check_page(path, set(AREA_COUNTY_EXPECTATIONS["required"])))
        else:
            errors.extend(check_page(path, set(AREA_CITY_EXPECTATIONS["required"])))

    if errors:
        print("Schema verification failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    page_count = len(list(ROOT.glob("*.html"))) + len(list((ROOT / "areas").glob("*.html")))
    print(f"Schema verification passed for {page_count} HTML pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
