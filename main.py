#!/usr/bin/env python3
"""news-image-20261122 entrypoint (v10): copy entry.png to /output/entry.png.

Stdlib only. No network. Deterministic: the output bytes are exactly the
input bytes, so two runs are byte-identical.

v10 is the Superbot-plan redesign: one full-width lead (Russia #02), 8
horizontal cards, 27 ALSO ON rows, 36 story slots total, and a 4-column
DATE CHECK. The self-check below pins the v10 layout strings so a later
edit cannot silently re-break a reviewer blocker.
"""
import hashlib
import os
import re
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"
MAX_BYTES = 1024 * 1024


def check_front() -> None:
    """v10 self-check: fail loudly if any v10 layout string regresses.

    Reads build/front.html (the rendered page) and verifies the strings
    the v10 redesign depends on. The build fails instead of shipping a
    page that re-breaks a reviewer blocker.
    """
    path = os.path.join(HERE, "build", "front.html")
    if not os.path.isfile(path):
        raise SystemExit(f"missing {path}")
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    problems = []

    # --- lead (Russia #02, the full-width 1024x300 block) ---
    if "UKRAINE &middot; 8 KILLED" not in html:
        problems.append("lead banner 'UKRAINE · 8 KILLED' missing")
    if "400 DRONES," not in html:
        problems.append("lead headline '400 DRONES,' missing")
    if "MISSILES STRIKE" not in html:
        problems.append("lead headline 'MISSILES STRIKE' missing")
    if "UKRAINE: 8 DEAD" not in html:
        problems.append("lead headline 'UKRAINE: 8 DEAD' missing")
    if "Six died in Kyiv, two in Lviv" not in html:
        problems.append("lead dek 'Six died in Kyiv, two in Lviv' missing")
    if "27 of the missiles were ballistic" not in html:
        problems.append("lead dek ballistic count missing")
    if "Zelenskyy &middot; Euronews &middot; Al Jazeera" not in html:
        problems.append("lead sources 'Zelenskyy · Euronews · Al Jazeera' missing")

    # Lead headline must be exactly 3 lines (2 <br>) and each line short
    # enough to fit the 740px text column at 68px (<=18 chars). This is
    # the check that catches the v10 first-render wrap bug (5 lines).
    m = re.search(r'<div class="head">(.*?)</div>', html, re.S)
    if not m:
        problems.append("lead .head not found")
    else:
        lines = m.group(1).split("<br>")
        if len(lines) != 3:
            problems.append(f"lead headline must be 3 lines (found {len(lines)})")
        for line in lines:
            if len(line.strip()) > 18:
                problems.append(
                    f"lead headline line too long ({len(line.strip())} chars): "
                    f"{line.strip()!r}"
                )

    # --- numbers row: 6 people-counts + rate chip ---
    for num in ("700,000", "350,000", "30,000", "1,671", "856", "24"):
        if num not in html:
            problems.append(f"numbers row missing {num}")
    if "98.79%" not in html:
        problems.append("rate chip '98.79%' missing")
    if "5,640 VOTERS" not in html:
        problems.append("rate chip '5,640 VOTERS' missing")

    # --- timeline: 4 events + NOW 22:00 ---
    for ev in ("PERU M6.9", "BANDA SEA M6.9", "HK POLLS CLOSE", "ATP FINAL"):
        if ev not in html:
            problems.append(f"timeline missing {ev}")
    if "NOW 22:00" not in html:
        problems.append("timeline 'NOW 22:00' missing")

    # --- region strip: 7 regions, 36 stories ---
    for reg in (
        "MIDDLE EAST 4", "EUROPE 7", "ASIA 8", "AMERICAS 7",
        "AFRICA 5", "OCEANIA 2", "MKT+SPORT 3",
    ):
        if reg not in html:
            problems.append(f"region strip missing {reg}")

    # --- cards: 8 horizontal cards, each with a verification dot + source ---
    # (scope the source count to the cards block: the lead carries its own
    # .src div, so a whole-file count is 9, not 8)
    cards_start = html.index("<!-- SECONDARY CARDS")
    cards_end = html.index("<!-- MAP")
    cards_html = html[cards_start:cards_end]
    cards = cards_html.count('<div class="card"')
    if cards != 8:
        problems.append(f"cards must be 8 (found {cards})")
    vdots = cards_html.count('<div class="vdot"')
    if vdots != 8:
        problems.append(f"card verification dots must be 8 (found {vdots})")
    srcs = cards_html.count('<div class="src">')
    if srcs != 8:
        problems.append(f"card sources must be 8 (found {srcs})")
    # the 9 featured stories: 6 CONFIRMED, 2 OFFICIAL, 1 CLAIM
    if html.count("6 confirmed &middot; 2 official &middot; 1 claim") != 1:
        problems.append(
            "footer verification tally '6 confirmed · 2 official · 1 claim' "
            "must appear once"
        )

    # --- map: 12 pins ---
    map_start = html.index("<!-- MAP")
    map_end = html.index("<!-- DATE CHECK")
    map_html = html[map_start:map_end]
    pins = map_html.count("<circle cx=")
    if pins != 12:
        problems.append(f"map pins must be 12 (found {pins})")

    # --- DATE CHECK: 4 columns, as-of settled to 17:00 UTC ---
    if "As of 22 Nov, 17:00 UTC" not in html:
        problems.append("DATE CHECK as-of 'As of 22 Nov, 17:00 UTC' missing")
    if "Includes items that broke 19&ndash;21 Nov" not in html:
        problems.append("DATE CHECK 'Includes items that broke 19–21 Nov' missing")
    for col in ("HELD", "LEFT OUT", "NOT YET", "CORRECTIONS"):
        if col not in html:
            problems.append(f"DATE CHECK column {col} missing")

    # --- 36 story slots: 1 lead + 8 cards + 27 list rows ---
    slots = (
        html.count('<div class="leadtext">')
        + html.count('<div class="card"')
        + html.count('<div class="row">')
    )
    if slots != 36:
        problems.append(f"story slots must be 36 (found {slots})")

    if problems:
        raise SystemExit("front.html v10 check failed:\n- " + "\n- ".join(problems))
    print(
        f"front.html v10 check ok: 1 lead + {cards} cards + 27 list rows = "
        f"36 slots; {pins} map pins"
    )


def self_check(data: bytes) -> None:
    """Fail loudly unless the entry is a valid 1024x1024 PNG under 1 MiB."""
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png too big: {len(data)} bytes > {MAX_BYTES}")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        raise SystemExit(f"entry.png is {width}x{height}, want 1024x1024")
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        raise SystemExit("entry.png is truncated: missing IEND chunk")


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    verify_only = "--verify-only" in args
    check_front()
    if not os.path.isfile(SRC):
        print(f"missing {SRC}", file=sys.stderr)
        return 1
    with open(SRC, "rb") as fh:
        data = fh.read()
    self_check(data)
    print(f"entry.png {len(data)} bytes sha256={hashlib.sha256(data).hexdigest()}")
    if verify_only:
        return 0
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
