#!/usr/bin/env python3
"""Compress logos, hero art, and gallery WebPs for faster PageSpeed delivery."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "Images"
GALLERY = ROOT / "Gallery"
CARDS = GALLERY / "cards"

LOGO_SRC = IMAGES / "fw-logo3.png"
LOGO_WEBP = IMAGES / "fw-logo3.webp"
LOGO_WEBP_144 = IMAGES / "fw-logo3-144.webp"
LOGO_ICON_PNG = IMAGES / "fw-logo3-192.png"

HERO_DESKTOP = "photo-of-all-equipment.webp"
HERO_MOBILE = "excavator-and-truck-photo.webp"

CARD_MAX = 640
CARD_QUALITY = 62
HERO_DESKTOP_MAX = 1920
HERO_DESKTOP_QUALITY = 74
HERO_MOBILE_LCP_MAX = 960
HERO_MOBILE_LCP_QUALITY = 62
HERO_MOBILE_MAX = 1280
HERO_MOBILE_QUALITY = 68
GALLERY_MASTER_MAX = 1600
GALLERY_MASTER_QUALITY = 72
LOGO_QUALITY = 78


def save_webp(img: Image.Image, dest: Path, quality: int) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
    if img.mode == "RGBA":
        img.save(dest, "WEBP", quality=quality, method=6, lossless=False)
    else:
        img.convert("RGB").save(dest, "WEBP", quality=quality, method=6, lossless=False)


def resize_max(img: Image.Image, max_edge: int) -> Image.Image:
    w, h = img.size
    if max(w, h) <= max_edge:
        return img
    if w >= h:
        nw = max_edge
        nh = int(h * (max_edge / w))
    else:
        nh = max_edge
        nw = int(w * (max_edge / h))
    return img.resize((nw, nh), Image.Resampling.LANCZOS)


def optimize_logo() -> None:
    if not LOGO_SRC.exists():
        print(f"Skip logo — missing {LOGO_SRC}")
        return

    with Image.open(LOGO_SRC) as src:
        rgba = src.convert("RGBA")
        save_webp(resize_max(rgba, 288), LOGO_WEBP, LOGO_QUALITY + 4)
        save_webp(resize_max(rgba, 144), LOGO_WEBP_144, LOGO_QUALITY)

        icon = resize_max(rgba, 192)
        flat = Image.new("RGBA", icon.size, (0, 0, 0, 0))
        flat.alpha_composite(icon)
        rgb = Image.new("RGB", flat.size, (10, 10, 10))
        rgb.paste(flat, mask=flat.split()[-1])
        rgb.save(LOGO_ICON_PNG, "PNG", optimize=True, compress_level=9)
        shutil.copy2(LOGO_ICON_PNG, IMAGES / "Logo.png")

    for path in (LOGO_WEBP, LOGO_WEBP_144, LOGO_ICON_PNG):
        print(f"Logo -> {path.name} ({path.stat().st_size // 1024} KB)")


def optimize_gallery_webp(path: Path, max_edge: int, quality: int) -> None:
    with Image.open(path) as img:
        out = resize_max(img, max_edge)
        save_webp(out, path, quality)


def optimize_heroes() -> None:
    desktop = GALLERY / HERO_DESKTOP
    mobile = GALLERY / HERO_MOBILE
    heroes = GALLERY / "heroes"
    if desktop.exists():
        optimize_gallery_webp(desktop, HERO_DESKTOP_MAX, HERO_DESKTOP_QUALITY)
        print(f"Hero desktop -> {desktop.name} ({desktop.stat().st_size // 1024} KB)")
    if mobile.exists():
        with Image.open(mobile) as img:
            heroes.mkdir(parents=True, exist_ok=True)
            lcp = resize_max(img, HERO_MOBILE_LCP_MAX)
            lcp_dest = heroes / mobile.name
            save_webp(lcp, lcp_dest, HERO_MOBILE_LCP_QUALITY)
            print(f"Hero LCP mobile -> heroes/{mobile.name} ({lcp_dest.stat().st_size // 1024} KB)")
        optimize_gallery_webp(mobile, HERO_MOBILE_MAX, HERO_MOBILE_QUALITY)
        print(f"Hero mobile gallery -> {mobile.name} ({mobile.stat().st_size // 1024} KB)")


def build_card_variants() -> None:
    if CARDS.exists():
        shutil.rmtree(CARDS)
    CARDS.mkdir(parents=True, exist_ok=True)

    skip = {"gallery-manifest.json"}
    for path in sorted(GALLERY.glob("*.webp")):
        if path.name in skip:
            continue
        with Image.open(path) as img:
            card = resize_max(img, CARD_MAX)
            dest = CARDS / path.name
            save_webp(card, dest, CARD_QUALITY)
        print(f"Card -> cards/{path.name} ({dest.stat().st_size // 1024} KB)")


def recompress_gallery_masters() -> None:
    skip = {HERO_DESKTOP, HERO_MOBILE}
    for path in sorted(GALLERY.glob("*.webp")):
        if path.name in skip or path.name == "gallery-manifest.json":
            continue
        before = path.stat().st_size
        optimize_gallery_webp(path, GALLERY_MASTER_MAX, GALLERY_MASTER_QUALITY)
        after = path.stat().st_size
        print(f"Gallery -> {path.name} ({before // 1024} KB -> {after // 1024} KB)")


def main() -> None:
    optimize_logo()
    recompress_gallery_masters()
    optimize_heroes()
    build_card_variants()
    print("Image optimization complete.")


if __name__ == "__main__":
    main()
