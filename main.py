#!/usr/bin/env python3
"""news-image-20261122 entrypoint (v12): copy entry.png to /output/entry.png.

Stdlib only. No network. Deterministic: the output bytes are exactly the
input bytes, so two runs are byte-identical.

v12 is the Superbot v12 fix-plan round on v11 (Quick NOT READY: the right
ALSO ON column had NO right margin, so rows 25/28/30/34 were clipped by
the canvas edge, and row 06 was cut to "Anadol" by an overflow:hidden
with no ellipsis). The v12 geometry rebuilds the ALSO ON block as a real
2-column grid (list origin x=656 display, left 656-824, gutter 824-840,
right 840-1008, 16px right margin; both columns 168px), drops the
per-row source (one shared credit line under the block), settles red to
exactly 4 canvas clusters, lets kickers wrap to two lines with a common
body offset, and turns the timeline chip into a time-free NOW dot on the
17:00 tick (placed left of the tick so it cannot overlap the label). The self-check below pins the v12 layout strings and the
v12 acceptance geometry, so a later edit cannot silently re-break a
reviewer blocker.

Grid reconciliation (Superbot's steps 1 and 9 disagree, neither gives
two 176px columns): the mapbox ends at x=644 display and the list
starts at x=656 (the v11 origin), so two equal columns + a 16px gutter
+ a 16px right margin fit in 656-1008 display as 168px each. The gate
(no ink within 2px of x=1008 / x=832 / the canvas edge) is met by this
grid: the gutter 824-840 contains x=832, and the right column ends at
x=1008. Row type is 9px display (18px at 2x); the plan's 12px
line-height cannot fit 14 rows in the 252px row area, so the pitches
are 18px (left) / 19.38px (right) at 2x, which balance 14/13 rows to
the same baseline. Pin badges are r=26 at 2x (the plan's "20px" does
not map to the 2x coordinate system); numerals are 12px display
(24px at 2x) tabular, as specified. Row type is 8px display (16px at
2x): the plan's 9px display truncates the longest row (30) to "Aug…",
so 16px is used and every row fits in full.
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
    """v12 self-check: fail loudly if any v12 layout string regresses.

    Reads build/front.html (the rendered page) and verifies the strings
    the v12 fix plan depends on. The build fails instead of shipping a
    page that re-breaks a reviewer blocker.
    """
    path = os.path.join(HERE, "build", "front.html")
    if not os.path.isfile(path):
        raise SystemExit(f"missing {path}")
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    problems = []

    # --- lead (Russia #02, the full-width 1024x300 block) ---
    # step 9 (v11): "8 DEAD" in the banner, the headline and the counts row.
    if "UKRAINE &middot; 8 DEAD" not in html:
        problems.append("lead banner 'UKRAINE · 8 DEAD' missing")
    if "8 KILLED" in html:
        problems.append("stale '8 KILLED' still present (all three say DEAD)")
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

    # step 11 (v11): lead kicker carries the story number, closing the 02 hole.
    if "02 &middot; UKRAINE" not in html:
        problems.append("lead kicker '02 · UKRAINE' missing")

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

    # step 4 (v11): rate chip numeral re-sized so its rightmost pixel lands
    # near x=993 (6px clear of the x=999 border). At 2x: 34px font.
    if ".ratechip .r { font-size:34px;" not in html:
        problems.append("rate chip numeral must be 34px at 2x (step 4)")

    # step 3 (v11): bars keep the six numbers, tone only (6px, one step darker).
    if ".nfig .bar { height:12px; background:#A89B7E;" not in html:
        problems.append("numbers bars must be 12px #A89B7E (step 3)")

    # --- timeline: 4 events + ONE clock at 17:00 (v12 step 7) ---
    # The 17:00 tick keeps its label; the right chip is a time-free NOW
    # dot aligned to that tick, so the band carries exactly one "17:00".
    for ev in ("PERU M6.9", "BANDA SEA M6.9", "HK POLLS CLOSE", "ATP FINAL"):
        if ev not in html:
            problems.append(f"timeline missing {ev}")
    if "NOW 17:00" in html:
        problems.append("timeline chip must be time-free 'NOW' (v12 step 7)")
    if "22:00" in html:
        problems.append("stale '22:00' still present (one clock, 17:00)")
    tl_start = html.index("<!-- THE DAY IN UTC")
    tl_end = html.index("<!-- THE DAY IN NUMBERS")
    tl_band = html[tl_start:tl_end]
    if tl_band.count("17:00") != 1:
        problems.append(
            f"timeline band must carry exactly one '17:00' "
            f"(found {tl_band.count('17:00')}) (v12 step 7, gate 3)"
        )
    if ">NOW</div>" not in tl_band:
        problems.append("timeline NOW dot missing (v12 step 7)")
    if 'class="nowmark" style="left:1520px;"' not in tl_band:
        problems.append("NOW dot must sit at left 1520px, on the 17:00 tick")

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

    # step 1 (v11): the status dot lives inside the thumbnail (6px in from
    # its top and right edge), so it can no longer collide with a kicker.
    if ".card .vdot { position:absolute; left:144px; top:24px;" not in html:
        problems.append("card .vdot must sit inside the thumbnail (step 1)")

    # ruling 4 (v11): CLAIM dot is amber, not red-brown.
    if 'vdot" style="background:#D98E00;"' not in cards_html:
        problems.append("card 01 CLAIM dot must be amber #D98E00 (ruling 4)")
    if 'vdot" style="background:#A63A2E;"' in cards_html:
        problems.append("a card vdot is still #A63A2E (ruling 4: CLAIM is amber)")

    # ruling 4 (v11): card 04 flame and card 05 target are burnt orange, so
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

    # step 5 (v11): card 10 dek is two lines of counts only; "results
    # tonight" lives in DATE CHECK, not on the card.
    if "856 candidates &middot;<br>723 seats" not in cards_html:
        problems.append("card 10 dek must be '856 candidates · / 723 seats' (step 5)")
    if "results tonight" in cards_html:
        problems.append("'results tonight' must not be on card 10 (step 5)")

    # step 6 (v11): card 09 thumbnail keeps 50%, drops the 0% label.
    if "50%" not in cards_html:
        problems.append("card 09 '50%' label missing (step 6)")
    if ">0%<" in cards_html:
        problems.append("card 09 '0%' label must be dropped (step 6)")

    # v12 step 6: kickers may wrap to two lines (no nowrap) inside a
    # 268px box, and every card uses the same body top offset (head 64,
    # dek 134, src 212 at 2x), so a two-line kicker cannot push the body
    # out of the card. Assertion: kicker box <= card box - 14px
    # (180 + 268 = 448 <= 476 - 28 = 448 at 2x, i.e. 14px display).
    if ".card .kick { position:absolute; left:180px; top:16px; width:268px;" not in html:
        problems.append("card kicker must be width 268px at 2x (v12 step 6)")
    if ".card .kick" in html and "white-space:nowrap" in html.split(".card .kick")[1].split("}")[0]:
        problems.append("card kicker must not be nowrap (v12 step 6: wrap allowed)")
    if ".card .head { position:absolute; left:180px; top:64px;" not in html:
        problems.append("card head must be top 64px at 2x (v12 step 6)")
    if ".card .dek { position:absolute; left:180px; top:134px;" not in html:
        problems.append("card dek must be top 134px at 2x (v12 step 6)")
    if ".card .src { position:absolute; left:180px; top:212px;" not in html:
        problems.append("card src must be top 212px at 2x (v12 step 6)")

    # --- map: 12 pins, each numbered and slugged, all ink (v12 steps 5+8) ---
    map_start = html.index("<!-- MAP")
    map_end = html.index("<!-- DATE CHECK")
    map_html = html[map_start:map_end]
    pins = map_html.count("<circle cx=")
    if pins != 12:
        problems.append(f"map pins must be 12 (found {pins})")
    for num in ("01", "02", "03", "04", "05", "10", "11", "17", "18", "19", "23", "27"):
        if f">{num}</text>" not in map_html:
            problems.append(f"map pin number {num} missing")
    for slug in (
        "CPH", "GOF", "LVIV", "ANTALYA", "BAH", "BAY",
        "MOY", "HKG", "BND", "PER", "BSB", "SINALOA",
    ):
        if f">{slug}</text>" not in map_html:
            problems.append(f"map pin slug {slug} missing")
    # v12 step 5: every pin is neutral ink with a white numeral; no region
    # colour may remain on a pin (the region strip carries the colours).
    if map_html.count('fill="#191919"/>') < 12:
        problems.append("all 12 map pins must be ink #191919 (v12 step 5)")
    for region_fill in ("#2F5D8A", "#A63A2E", "#8A5A28", "#B97A1E", "#4A7A3D"):
        if region_fill in map_html:
            problems.append(
                f"region fill {region_fill} still on a map pin (v12 step 5)"
            )
    # v12 step 8: numerals are 12px display (24px at 2x) on every pin.
    if map_html.count('font-size="24"') != 12:
        problems.append(
            f"all 12 pin numerals must be 24px at 2x "
            f"(found {map_html.count('font-size=\"24\"')}) (v12 step 8)"
        )

    # --- ALSO ON list: 27 rows in a real 2-column grid (v12 steps 1-4) ---
    # step 1 grid, display px (1024 file): list origin 656, left 656-824,
    # gutter 824-840 (contains x=832), right 840-1008, margin 1008-1024.
    # At 2x: .lst left 1312 width 704; left col width 336; right col left 368.
    if '.lst .col { position:absolute; top:20px; width:336px; overflow:hidden; }' not in html:
        problems.append("list .col must have the overflow clip guard (v12 step 1)")
    if 'style="left:0; width:336px;"' not in html:
        problems.append("list left column must be 336px at 2x (v12 step 1)")
    if 'style="left:368px;"' not in html:
        problems.append("list right column must start at left 368px at 2x (v12 step 1)")
    if ".lst { position:absolute; left:1312px; top:1544px; width:704px; height:272px; }" not in html:
        problems.append("list block must be left 1312 / width 704 / height 272 at 2x (v12 step 1)")
    # step 2: rows are 8px display (16px at 2x). The plan's 9px display
    # (18px at 2x) truncates the longest row (30, "350,000 displaced
    # since August") to "Aug…" even after the source is dropped, so 16px
    # is used: every row then fits its 168px column in full. The plan's
    # 12px line-height cannot fit 14 rows in the 252px row area, so the
    # pitches are 18px (left) / 19.38px (right) at 2x, balancing 14/13
    # rows to the same baseline.
    if ".lst .row { font-size:16px; line-height:18px;" not in html:
        problems.append("list rows must be 16px / 18px at 2x (v12 step 2)")
    if ".lst .col.r .row { line-height:19.38px; }" not in html:
        problems.append("list right column pitch must be 19.38px at 2x (v12 step 2)")
    # step 2: no per-row source; one shared credit line under the block.
    rows = re.findall(r'<div class="row">.*?</div>', html)
    if len(rows) != 27:
        problems.append(f"ALSO ON rows must be 27 (found {len(rows)})")
    for row in rows:
        if " &mdash; " in row:
            problems.append(f"row still carries a per-row source (v12 step 2): {row[:60]!r}")
            break
    if "Sources: Anadolu" not in html:
        problems.append("shared credit line 'Sources: Anadolu …' missing (v12 step 2)")
    if 'style="position:absolute; left:48px; top:1816px; width:1952px;' not in html:
        problems.append("credit line must sit at top 1816px full width (v12 step 2)")
    # step 3: header reconciles the row count with the page-wide index.
    if "27 MORE STORIES &middot; 06&ndash;36" not in html:
        problems.append("ALSO ON header must read '27 MORE STORIES · 06–36' (v12 step 3)")
    # step 4: overflow is defined (ellipsis + 4px display right inset),
    # never a bare overflow:hidden that cuts a word mid-glyph.
    if "text-overflow:ellipsis; padding-right:8px;" not in html:
        problems.append("list rows need ellipsis + 8px right inset at 2x (v12 step 4)")
    # ruling 4 (v11): ALSO ON numerals are ink, not red.
    if ".lst .row .n { font-weight:bold; color:#191919; }" not in html:
        problems.append("ALSO ON numerals must be ink #191919")

    # --- DATE CHECK: 4 columns, as-of settled to 17:00 UTC (v12 step 5) ---
    if "As of 22 Nov, 17:00 UTC" not in html:
        problems.append("DATE CHECK as-of 'As of 22 Nov, 17:00 UTC' missing")
    if "Includes items that broke 19&ndash;21 Nov" not in html:
        problems.append("DATE CHECK 'Includes items that broke 19–21 Nov' missing")
    for col in ("HELD", "LEFT OUT", "NOT YET", "CORRECTIONS"):
        if col not in html:
            problems.append(f"DATE CHECK column {col} missing")
    # v12 step 5: DATE CHECK title is ink, the box border is 1px ink at
    # 40%, NOT YET is amber. Red is no longer used here.
    if ".dc .l b { color:#191919; }" not in html:
        problems.append("DATE CHECK title must be ink (v12 step 5)")
    if "border:1px solid rgba(25,25,25,0.4);" not in html:
        problems.append("DATE CHECK border must be 1px ink at 40% (v12 step 5)")
    if ".dc .col .h .notyet { color:#D98E00; }" not in html:
        problems.append("DATE CHECK NOT YET must be amber (v12 step 5)")

    # --- red, settled to exactly 4 canvas clusters (v12 step 5, gate 2) ---
    # The brand red #B01E1E occurs 5 times in the source, which renders as
    # 4 clusters: the NOW text + its ring are adjacent (1 cluster), the
    # lead banner (1), the card 01 radar dot (1), the card 03 flag (1).
    # Every other former red use (DATE CHECK title/border, NOT YET, all
    # 12 pins) is now ink or amber.
    red_uses = html.count("#B01E1E")
    if red_uses != 5:
        problems.append(
            f"brand red #B01E1E must occur 5 times in source (= 4 canvas "
            f"clusters) (found {red_uses}) (v12 step 5, gate 2)"
        )
    if "#B01E1E" in map_html:
        problems.append("no brand red may remain on a map pin (v12 step 5)")

    # --- vertical geometry (v12 step 2): map/lst end at 1816, credit line
    # 1816-1830, DATE CHECK top 1830, footer ends at y=1010 display ---
    if ".mapbox { position:absolute; left:48px; top:1544px; width:1240px; height:272px;" not in html:
        problems.append("mapbox must be top 1544 / height 272 at 2x (v12 step 2)")
    if ".dc { position:absolute; left:48px; top:1830px;" not in html:
        problems.append("DATE CHECK must be top 1830 at 2x")
    if 'class="foot" style="top:1990px;"' not in html:
        problems.append("footer line 1 must be top 1990 at 2x")
    if 'class="foot" style="top:2006px;"' not in html:
        problems.append("footer line 2 must be top 2006 at 2x")

    # --- 36 story slots: 1 lead + 8 cards + 27 list rows ---
    slots = (
        html.count('<div class="leadtext">')
        + html.count('<div class="card"')
        + html.count('<div class="row">')
    )
    if slots != 36:
        problems.append(f"story slots must be 36 (found {slots})")

    if problems:
        raise SystemExit("front.html v12 check failed:\n- " + "\n- ".join(problems))
    print(
        f"front.html v12 check ok: 1 lead + {cards} cards + 27 list rows = "
        f"36 slots; {pins} map pins (ink, 24px numerals); clock 17:00 x1; "
        f"red 5 source uses = 4 canvas clusters; footer ends 1010"
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
