#!/usr/bin/env python3
"""news-image-20261122 entrypoint (v11): copy entry.png to /output/entry.png.

Stdlib only. No network. Deterministic: the output bytes are exactly the
input bytes, so two runs are byte-identical.

v11 is the Superbot fix-plan round on the v10 redesign: one clock at
17:00 (NOW moved from 22:00 onto the 17:00 tick, ATP stays NOT YET),
ALSO ON kept at 27 rows with the left column clipped so no string
crosses into the right column, the rate chip numeral re-sized so its
rightmost pixel lands clear of the chip border, "8 DEAD" in all three
places, red restricted to four uses, and the footer lifted so its second
line ends at y=1010 (14px bottom margin). The self-check below pins the
v11 layout strings and the v11 acceptance geometry, so a later edit
cannot silently re-break a reviewer blocker.
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
    """v11 self-check: fail loudly if any v11 layout string regresses.

    Reads build/front.html (the rendered page) and verifies the strings
    the v11 fix plan depends on. The build fails instead of shipping a
    page that re-breaks a reviewer blocker.
    """
    path = os.path.join(HERE, "build", "front.html")
    if not os.path.isfile(path):
        raise SystemExit(f"missing {path}")
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    problems = []

    # --- lead (Russia #02, the full-width 1024x300 block) ---
    # step 9: "8 DEAD" in the banner, the headline and the counts row.
    if "UKRAINE &middot; 8 DEAD" not in html:
        problems.append("lead banner 'UKRAINE · 8 DEAD' missing")
    if "8 KILLED" in html:
        problems.append("stale '8 KILLED' still present (step 9: all three say DEAD)")
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

    # step 11: lead kicker carries the story number, closing the 02 hole.
    if "02 &middot; UKRAINE" not in html:
        problems.append("lead kicker '02 · UKRAINE' missing (step 11)")

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

    # step 4: rate chip numeral re-sized so its rightmost pixel lands
    # near x=993 (6px clear of the x=999 border). At 2x: 34px font.
    # (v10 was 44px, no padding, and the numeral crossed the border by
    # 2px. The plan's "26px display" would make it WIDER, not narrower:
    # the numeral is 87px wide at 40px/2x and the chip's content box is
    # only 90px wide, so the pixel target is what the size is computed
    # from. Padding does not shift centred text in this render, so the
    # size alone carries the fix.)
    if ".ratechip .r { font-size:34px;" not in html:
        problems.append("rate chip numeral must be 34px at 2x (step 4)")

    # step 3: bars keep the six numbers, tone only (6px, one step darker).
    if ".nfig .bar { height:12px; background:#A89B7E;" not in html:
        problems.append("numbers bars must be 12px #A89B7E (step 3)")

    # --- timeline: 4 events + ONE clock at 17:00 (ruling 1 / step 8) ---
    for ev in ("PERU M6.9", "BANDA SEA M6.9", "HK POLLS CLOSE", "ATP FINAL"):
        if ev not in html:
            problems.append(f"timeline missing {ev}")
    if "NOW 17:00" not in html:
        problems.append("timeline 'NOW 17:00' missing (step 8)")
    if "22:00" in html:
        problems.append("stale '22:00' still present (step 8: one clock, 17:00)")

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

    # step 1: the status dot lives inside the thumbnail (6px in from its
    # top and right edge), so it can no longer collide with a kicker.
    if ".card .vdot { position:absolute; left:144px; top:24px;" not in html:
        problems.append("card .vdot must sit inside the thumbnail (step 1)")

    # ruling 4: CLAIM dot is amber, not red-brown.
    if 'vdot" style="background:#D98E00;"' not in cards_html:
        problems.append("card 01 CLAIM dot must be amber #D98E00 (ruling 4)")
    if 'vdot" style="background:#A63A2E;"' in cards_html:
        problems.append("a card vdot is still #A63A2E (ruling 4: CLAIM is amber)")

    # ruling 4: card 04 flame and card 05 target are burnt orange, so
    # they read as illustration, not status.
    if 'M66 46 L72 26 L78 46 Z" fill="#C65D00"' not in html:
        problems.append("card 04 flame must be burnt orange #C65D00 (ruling 4)")
    if 'M84 46 L90 32 L96 46 Z" fill="#D98E00"' not in html:
        problems.append("card 04 second flame must be #D98E00 (ruling 4)")
    if 'r="8" fill="#C65D00"' not in html:
        problems.append("card 05 target centre must be burnt orange (ruling 4)")
    if 'M56 40 L104 88" stroke="#C65D00"' not in html:
        problems.append("card 05 target slash must be burnt orange (ruling 4)")
    if 'r="8" fill="#B01E1E"' in html:
        problems.append("card 05 target centre is still red (ruling 4)")

    # step 5: card 10 dek is two lines of counts only; "results tonight"
    # lives in DATE CHECK, not on the card.
    if "856 candidates &middot;<br>723 seats" not in cards_html:
        problems.append("card 10 dek must be '856 candidates · / 723 seats' (step 5)")
    if "results tonight" in cards_html:
        problems.append("'results tonight' must not be on card 10 (step 5)")

    # step 6: card 09 thumbnail keeps 50%, drops the 0% label.
    if "50%" not in cards_html:
        problems.append("card 09 '50%' label missing (step 6)")
    if ">0%<" in cards_html:
        problems.append("card 09 '0%' label must be dropped (step 6)")

    # --- map: 12 pins, each numbered and slugged (step 11 audit) ---
    map_start = html.index("<!-- MAP")
    map_end = html.index("<!-- DATE CHECK")
    map_html = html[map_start:map_end]
    pins = map_html.count("<circle cx=")
    if pins != 12:
        problems.append(f"map pins must be 12 (found {pins})")
    for num in ("01", "02", "03", "04", "05", "10", "11", "17", "18", "19", "23", "27"):
        if f">{num}</text>" not in map_html:
            problems.append(f"map pin number {num} missing (step 11)")
    for slug in (
        "CPH", "GOF", "LVIV", "ANTALYA", "BAH", "BAY",
        "MOY", "HKG", "BND", "PER", "BSB", "SINALOA",
    ):
        if f">{slug}</text>" not in map_html:
            problems.append(f"map pin slug {slug} missing (step 11)")

    # --- ALSO ON list: 27 rows, left column clipped, pitches balanced ---
    # step 2: left column is 348px at 2x with a clip guard, so no string
    # can cross into the right column (right-column numbers start at
    # x=833 display; the cap puts the clip at x=830 display).
    if '.lst .col { position:absolute; top:20px; width:336px; overflow:hidden; }' not in html:
        problems.append("list .col must have the overflow clip guard (step 2)")
    if 'style="left:0; width:348px;"' not in html:
        problems.append("list left column must be 348px at 2x (step 2)")
    # step 3: left 14 rows at 9.5px pitch, right 13 at 10.2px pitch.
    if ".lst .col.r .row { line-height:20.4px; }" not in html:
        problems.append("list right column pitch must be 20.4px at 2x (step 3)")
    # step 2 copy fixes: row 21 outlet to WaPo, row 35 to ST.
    if "Hegseth memo curbs defence &mdash; WaPo" not in html:
        problems.append("row 21 outlet must be 'WaPo' (step 2)")
    if "Wash Post" in html:
        problems.append("stale 'Wash Post' still present (step 2)")
    if "Zverev, Alcaraz in final &mdash; ST" not in html:
        problems.append("row 35 outlet must be 'ST' (step 2)")
    if "in final &mdash; Straits" in html:
        problems.append("stale row 35 'Straits' still present (step 2)")
    # step 10: row 27 credit matches the band's source line.
    if "700,000 displaced &mdash; Islamic Relief" not in html:
        problems.append("row 27 credit must be 'Islamic Relief' (step 10)")
    if "UN News" in html:
        problems.append("stale 'UN News' still present (step 10)")
    # ruling 4: ALSO ON numerals are ink, not red.
    if ".lst .row .n { font-weight:bold; color:#191919; }" not in html:
        problems.append("ALSO ON numerals must be ink #191919 (ruling 4)")

    # --- DATE CHECK: 4 columns, as-of settled to 17:00 UTC ---
    if "As of 22 Nov, 17:00 UTC" not in html:
        problems.append("DATE CHECK as-of 'As of 22 Nov, 17:00 UTC' missing")
    if "Includes items that broke 19&ndash;21 Nov" not in html:
        problems.append("DATE CHECK 'Includes items that broke 19–21 Nov' missing")
    for col in ("HELD", "LEFT OUT", "NOT YET", "CORRECTIONS"):
        if col not in html:
            problems.append(f"DATE CHECK column {col} missing")

    # --- step 7 vertical geometry: the 10px reclaim ---
    # Map band top 1544 / height 286 at 2x => bottom 1830 (915 display);
    # DATE CHECK top 1830 (915 display); footer line 2 top 2006 at 2x
    # => its ink ends at y=1010 display, a 14px bottom margin.
    if ".mapbox { position:absolute; left:48px; top:1544px; width:1240px; height:286px;" not in html:
        problems.append("mapbox must be top 1544 / height 286 at 2x (step 7)")
    if ".lst { position:absolute; left:1312px; top:1544px; width:688px; height:286px; }" not in html:
        problems.append("list block must be top 1544 / height 286 at 2x (step 7)")
    if ".dc { position:absolute; left:48px; top:1830px;" not in html:
        problems.append("DATE CHECK must be top 1830 at 2x (step 7)")
    if 'class="foot" style="top:1990px;"' not in html:
        problems.append("footer line 1 must be top 1990 at 2x (step 7)")
    if 'class="foot" style="top:2006px;"' not in html:
        problems.append("footer line 2 must be top 2006 at 2x (step 7)")

    # --- 36 story slots: 1 lead + 8 cards + 27 list rows ---
    slots = (
        html.count('<div class="leadtext">')
        + html.count('<div class="card"')
        + html.count('<div class="row">')
    )
    if slots != 36:
        problems.append(f"story slots must be 36 (found {slots})")

    if problems:
        raise SystemExit("front.html v11 check failed:\n- " + "\n- ".join(problems))
    print(
        f"front.html v11 check ok: 1 lead + {cards} cards + 27 list rows = "
        f"36 slots; {pins} map pins; clock 17:00; footer ends 1010"
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
