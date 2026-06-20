#!/usr/bin/env python3
"""Convert Gallery HEIC/JPG sources to WebP alongside originals in Gallery/."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pillow_heif
from PIL import Image

pillow_heif.register_heif_opener()

ROOT = Path(__file__).resolve().parent.parent
GALLERY_DIR = ROOT / "Gallery"

# slug -> (alt text, gallery label)
META = {
    "excavator-and-truck-photo": (
        "Kubota excavator and dump trailer on a residential pool dig-out site in Polk County Florida",
        "Pool Digging",
    ),
    "excavator-photo": (
        "Kubota mini excavator on a land clearing and excavation job site",
        "Land Clearing",
    ),
    "photo-of-all-equipment": (
        "Faith Works Outdoor Services fleet — Kubota excavator, tractor with loader, pickup, dump trailer, and flatbed trailer",
        "Equipment",
    ),
    "stump-before-ground-leveled": (
        "Tree stump removal site before ground leveling and cleanup in a residential yard",
        "Land Clearing",
    ),
    "stump-during-removal-1": (
        "Kubota excavator removing a tree stump during an active land clearing job",
        "Land Clearing",
    ),
    "stump-during-removal-2": (
        "Excavator pulling a tree stump and root ball during stump removal",
        "Land Clearing",
    ),
    "stump-during-removal": (
        "Mini excavator working to extract a tree stump from the ground",
        "Land Clearing",
    ),
    "stump-post-removal-1": (
        "Property after tree stump removal with excavated soil ready for leveling",
        "Land Clearing",
    ),
    "stump-post-removal": (
        "Completed tree stump removal with cleared ground and debris pile on site",
        "Land Clearing",
    ),
    "stump-prior-to-removal": (
        "Large tree stump in a yard before Faith Works stump removal service begins",
        "Land Clearing",
    ),
    "tractor": (
        "Kubota compact tractor with loader attachment on a Central Florida job site",
        "Equipment",
    ),
    "tractor-moving-item-with-grapple": (
        "Kubota tractor using a grapple attachment to move brush and debris during property cleanup",
        "Debris Removal",
    ),
    "tractor-with-box-blade-leveling-ground": (
        "Kubota tractor with box blade leveling and grading ground after stump removal",
        "Land Clearing",
    ),
}

HERO_DESKTOP = "photo-of-all-equipment.webp"
HERO_MOBILE = "excavator-and-truck-photo.webp"


def slugify(name: str) -> str:
    stem = Path(name).stem.strip().lower()
    stem = stem.replace("&", " and ")
    stem = re.sub(r"[^\w\s-]", "", stem)
    stem = re.sub(r"\s+", "-", stem)
    stem = re.sub(r"-+", "-", stem).strip("-")
    # disambiguate numbered duplicates
    stem = stem.replace("(1)", "-1").replace("(2)", "-2")
    stem = stem.replace("(", "-").replace(")", "")
    stem = re.sub(r"-+", "-", stem).strip("-")
    return stem


def save_webp(img: Image.Image, dest: Path, max_width: int = 1600, quality: int = 74) -> None:
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.Resampling.LANCZOS)
    if img.mode == "RGBA":
        img.save(dest, "WEBP", quality=quality, method=6)
    else:
        img.convert("RGB").save(dest, "WEBP", quality=quality, method=6)


def convert_all() -> list[tuple[str, str, str]]:
    GALLERY_DIR.mkdir(parents=True, exist_ok=True)

    for old in GALLERY_DIR.glob("*.webp"):
        old.unlink()

    entries: list[tuple[str, str, str]] = []
    seen: dict[str, int] = {}

    for src in sorted(GALLERY_DIR.iterdir()):
        if src.suffix.lower() not in {".heic", ".jpg", ".jpeg", ".png"}:
            continue

        slug = slugify(src.name)
        if slug in seen:
            seen[slug] += 1
            slug = f"{slug}-{seen[slug]}"
        else:
            seen[slug] = 1

        webp_name = f"{slug}.webp"
        dest = GALLERY_DIR / webp_name

        with Image.open(src) as img:
            save_webp(img, dest)

        alt, label = META.get(slug, (slug.replace("-", " ").capitalize(), "Gallery"))
        entries.append((webp_name, alt, label))
        print(f"OK {src.name} -> {webp_name}")

    manifest = {
        "hero_desktop": HERO_DESKTOP,
        "hero_mobile": HERO_MOBILE,
        "gallery": [{"file": f, "alt": a, "label": l} for f, a, l in entries],
    }
    (GALLERY_DIR / "gallery-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return entries


if __name__ == "__main__":
    convert_all()
