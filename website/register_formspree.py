#!/usr/bin/env python3
"""Register Faith Works estimate forms with Formspree.

Creates the form endpoint and triggers Formspree's verification email to
tyler@faithworksclearing.com (required for first-time Formspree users).

Usage:
  python website/register_formspree.py

After Tyler confirms the Formspree email, rebuild the site:
  python website/_build_site.py
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ID_FILE = ROOT / "formspree-id.txt"
TARGET_EMAIL = "tyler@faithworksclearing.com"
BRAND = "Faith Works Outdoor Services"


def save_form_id(form_id: str) -> None:
    ID_FILE.write_text(form_id.strip() + "\n", encoding="utf-8")
    print(f"Saved form ID to {ID_FILE}")


def register_via_formspree_api() -> str | None:
    """Try Formspree CLI deploy if FORMSPREE_DEPLOY_KEY is set."""
    deploy_key = os.environ.get("FORMSPREE_DEPLOY_KEY", "").strip()
    if not deploy_key:
        return None
    config = ROOT / "formspree.json"
    if not config.exists():
        return None
    import subprocess

    result = subprocess.run(
        ["npx", "@formspree/cli", "deploy", "-k", deploy_key],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        return None
    if ID_FILE.exists():
        return ID_FILE.read_text(encoding="utf-8").strip()
    return None


def trigger_verification_email(form_id: str) -> None:
    payload = {
        "name": "Faith Works Form Activation",
        "email": TARGET_EMAIL,
        "phone": "(863) 272-1596",
        "job_location": "Auburndale, FL",
        "service": "Land Clearing",
        "message": (
            "This is the initial Formspree activation submission for "
            f"{BRAND}. Tyler — please confirm the Formspree verification email "
            "so estimate requests from faithworksclearing.com can be delivered."
        ),
        "_subject": f"Activate {BRAND} contact forms",
        "_replyto": TARGET_EMAIL,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://formspree.io/f/{form_id}",
        data=data,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "FaithWorksODS-SiteSetup/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            print(f"Formspree response ({resp.status}): {body}")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"Formspree HTTP {exc.code}: {body}")
        if exc.code in (200, 201, 302):
            return
        raise


def main() -> None:
    existing = os.environ.get("FORMSPREE_FORM_ID", "").strip()
    if existing:
        save_form_id(existing)
        print(f"Using FORMSPREE_FORM_ID={existing}")
        trigger_verification_email(existing)
        return

    if ID_FILE.exists():
        form_id = ID_FILE.read_text(encoding="utf-8").strip()
        if form_id and form_id != "PLACEHOLDER":
            print(f"Form ID already saved: {form_id}")
            trigger_verification_email(form_id)
            return

    deployed = register_via_formspree_api()
    if deployed:
        trigger_verification_email(deployed)
        return

    print(
        "No Formspree form ID found.\n\n"
        "Option A — Dashboard (recommended for first-time setup):\n"
        f"  1. Go to https://formspree.io/register and sign up with {TARGET_EMAIL}\n"
        "  2. Verify the email Formspree sends to that inbox\n"
        f"  3. Create a new form -> set target email to {TARGET_EMAIL}\n"
        "  4. Copy the form ID from Integration (e.g. xyzabcde)\n"
        f"  5. Save it: echo YOUR_FORM_ID > \"{ID_FILE}\"\n"
        "  6. Re-run: python website/register_formspree.py\n"
        "  7. Rebuild: python website/_build_site.py\n\n"
        "Option B — CLI deploy:\n"
        "  1. Create a Formspree project at https://formspree.io\n"
        "  2. Set FORMSPREE_DEPLOY_KEY in your environment\n"
        "  3. Re-run this script\n"
    )


if __name__ == "__main__":
    main()
