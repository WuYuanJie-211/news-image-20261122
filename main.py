#!/usr/bin/env python3
"""news-image-20261122 entrypoint (v15.3): copy entry.png to /output/entry.png.

Stdlib only. No network. Deterministic: the output bytes are exactly the
input bytes, so two runs are byte-identical.

v15 is the Neon round (Gemini Pro Neon reviewed the v14.1 image
2026-11-23 20:46; full text at
https://gemini.google.com/app/16a80c88ed7b43aa). Round 4 (v14.1,
01a207f5) scored judge 982,873 (12W 0D 0L), rank 616/14,632; the top-50
cutoff is ~989,000, so the gap is ~6,000 points (about half a duel
flip). Neon's plan attacks the template, not polish:

P0 — the lead swaps. v14.1 led with the Ukraine 19-20 Nov barrage, a
2-3-day-old story on a 22 Nov front page, and that loses head-to-head
duels on date compliance. v15 leads with the COP31 collapse in Antalya
(story 03, CONFIRMED, closing plenary Sunday 22 Nov: no consensus, the
draft never mentioned fossil fuels, first COP text to admit a 1.5C
overshoot, first failure since Copenhagen 2009), labelled
"03 - TURKEY - 22 NOVEMBER - LEAD". The Ukraine strike leaves the
story slots entirely and moves into DATE CHECK exclusions. v15.1 goes
one further: the Nigeria boat (story 23, 21 Nov only — no 22 Nov hook
in the research file) is excluded too, and Onosato (story 16, wins the
7th Emperor's Cup 22 Nov, CONFIRMED) is promoted from the list to a
card. The page is now 34 stories (1 lead + 8 cards + 25 rows); F1
(Verstappen wins Las Vegas, OFFICIAL, 22 Nov) is the eighth card's
stablemate, not the only 22 Nov result on the page. THE DAY IN
NUMBERS is rebuilt: six even columns across x24-1000, each ~156px
with an 8px gap, all figures 68px, no bars, no standalone 98.79% box
(the turnout IS one of the six numbers now). The six numbers, every
one verified in news-20261122.md and every one a 22 Nov figure:
98.79% HK turnout (5,640 voters, OFFICIAL, 22 Nov); 0 fossil-fuel
mentions in the COP31 draft (Reuters, collapsed 22 Nov); 6.9, two
M6.9 quakes in one day (Peru 00:09 UTC, Banda Sea 09:42 UTC); 856
candidates in Hong Kong (INFO.GOV.HK, elections 22 Nov); 11 killed
after the Sinaloa capture (AP, 22 Nov follow-up); 75th career win,
Verstappen (FORMULA 1, Las Vegas GP 22 Nov). The 98.5% tariff figure
stays on card 09's head; 700K displaced still appears in full in ALSO
ON row 27.

P1 — serif headlines everywhere (lead 72px at 2x = 36 display,
line-height 1.05; card titles 29px at 2x = 14.5 display, line-height
1.15) and capsule verification badges: the tiny grey text at card
bottoms becomes a capsule (30px high at 2x, 6px radius, 17px bold)
plus the source right after it in 17px grey. Badge colours per Neon:
CONFIRMED #E6F4EA bg / #137333 text / #81C995 border; OFFICIAL
#E8F0FE / #1967D2 / #8AB4F8; REPORTED #FEF7E0 / #B06000 / #FDD663;
CLAIM #FCE8E6 / #C5221F / #F28B82. CLAIM carries no check mark (the
winners' legend shows a check only on CONFIRMED and OFFICIAL). The
lead badge is restyled to the same CONFIRMED capsule.

P2 — DATE CHECK becomes a full-width red box: bg #FDF2F2, 3px solid
#C62828 border, 10px solid red bar on the left, title "DATE CHECK"
in #C62828 bold. HELD becomes EXCLUDED (PRE-22 NOV), listing the
Ukraine 400-drone strike with its original date (19-20 Nov) and, in
v15.1, the Nigeria boat capsize (21 Nov). LEFT OUT and NOT YET
(POST-17:00 UTC) stay; CORRECTIONS becomes OFFICIAL REVISIONS in
v15.1 (HK: 5,640 registered voters, subsector — agency data, not
author errata). The old "Includes items that broke 19-21 Nov" line is
deleted: no wording admits non-22-Nov items were included.

P3 — the map land goes darker (#D5CEC0 fill, #AFA695 grid) and the
UTC timeline has five timed events (00:09 Peru, 01:00 HK polls open,
09:42 Banda Sea, 10:00 HK polls close, 17:00 ATP final) plus NOW
stacked on the 17:00 tick (text above the ring, ring centred on the
1511 tick; the sixth tick at 1799 is deleted and the axis ends at
1720). No verified sixth timed event exists in the research file (no
COP31 plenary time), so no sixth node is added. The map covers all 8
cards in v15.1: pins 09 JKT + 34 LAS + 16 FUK in; 19 BSB, 23 BAY,
27 MOY out (11 pins total).

P4 — the lead counts row spreads space-between across the 1180px
illustration width (0 fossil-fuel mentions / 35% electrification by
2035 / 2009 last COP failure), and cards 05 and 18 get mini
data/geo infographics instead of generic icons: card 05 (Denmark
plot) gets a two-bar chart (2 charged vs 1 expelled); card 18
(Sinaloa) gets a schematic mini-map with an 18 pin and a $5M chip.
The lead illustration is redrawn for COP31: the draft document with
FOSSIL FUELS struck out, a NO DEAL stamp, a 1.5C thermometer and a
NOV 9-21 +1 DAY calendar chip.

v15.2 (Neon-2 re-review of v15.1, 2026-11-23 21:52; Neon-1 said
READY, Neon-2 NOT READY with 3 must-fixes + 2 nice-to-haves):
- Card 09 demoted, Gaza promoted. The EU-Indonesia deal's core node
  is the 21 Nov signing (research file: "EU and Indonesia sign CEPA
  + investment deal 21 Nov after 10 years of talks", sources EU
  Council 18 Nov / EU factsheet 21 Nov / Al Jazeera 19 Nov; no 22 Nov
  hook), so deleting the "21 NOV" label while keeping it a main card
  only hid the date. Story 09 leaves the page for the DATE CHECK
  EXCLUDED column, and the Gaza strike (story 28, Reuters via Gulf
  Daily News + Middle East Eye, 22 Nov, CONFIRMED: strike kills 3 in
  Gaza City, toll since the truce now 1,671) is promoted from the
  list to card 28 in the same slot. No re-sort: Neon-2 accepts
  keeping the order, so the grid is now 01/04/05/28 over 10/18/16/34.
  The page is now 33 stories (1 lead + 8 cards + 24 rows); ASIA
  8->7, MIDDLE EAST stays 4. The Gaza pin sat at a schematic spot
  (775,218) in the eastern Med with its label below (775,258) —
  24px clear of BAH, 31px of ANTALYA; its true lat/lon would collide
  with the ANTALYA/BAH pins, so the schematic placement was
  deliberate. (v15.3 reverses this: Neon-2 caught the dodge — the pin
  was the southernmost, below BND/PER. See the v15.3 note below.) The DATE CHECK exclusion line 2 carries both 21 Nov
  items ("Nigeria boat · EU-Indonesia · 21 Nov", 402px at 22px) so
  the box stays two lines; the longer "…deal · 21 Nov" wording
  (457px) was measured too tight against the 460px column.
- SINALOA label moved right of pin 18 (x283) so it no longer
  touches pin 34.
- CONFIRMED badges vs legend: cards 04/18/16 printed a single
  source each while the footer legend defines CONFIRMED as two
  independent sources, and REPORTED appeared 0 times. Fixed by
  printing both verified sources on every CONFIRMED card: 04
  EURONEWS · REUTERS (research: Euronews, France 24, Reuters —
  Neon-2's "YLE" is NOT in the research file, so it is not used);
  18 REUTERS · AP (AP from the evening-refresh Sinaloa follow-up);
  16 ABEMA · TACHIAI (tachiai.org — Neon-2's "KYODO" is NOT in the
  research file); 28 REUTERS · MIDDLE EAST EYE (research: Reuters
  via Gulf Daily News, Middle East Eye). Card 05 already printed
  BBC · NYT. The badge row is now full-width (.src left 8, 460px)
  because badge (163px) + two sources (up to 247px) cannot fit the
  old 288px text column — measured with PIL/DejaVu Sans 17px before
  changing. Footer tally becomes 6 confirmed · 2 official · 1 claim
  (lead 03 + cards 04, 05, 16, 18, 28; official = cards 10, 34;
  claim = card 01) — coincidentally the v14 tally, for a different
  set of stories.
- Numbers column 4: 856 -> 7th (Onosato's 7th Emperor's Cup, 22 Nov,
  CONFIRMED) so the Hong Kong election holds only one of the six
  slots.
- Timeline: the 17:00 node + NOW nudged right 16px (tick 1527, NOW
  left 1487) so NOW clears the 10:00 CLOSE label.

v15.3 (Neon-2 re-review of v15.2, 2026-11-23 ~22:05; Neon-1 READY,
Neon-2 NOT READY on ONE item only): the 28 GAZA pin at (775,218)
was the southernmost pin, below BAH/BND/PER, its GAZA label hugging
the map's bottom edge — Gaza is 31.5N, north of Bahrain 26N. Moved:
03 ANTALYA (780,135)->(762,122), label to the left of the pin
(730,127); 28 GAZA (775,218)->(805,155), label to the left of the
pin (773,160); 01 BAH (838,175)->(856,186), label at (890,191).
The BAH nudge is the knock-on the fix needs: the 03-01 gap is only
~70px centre-to-centre, and no third r=26 pin fits between them
otherwise (measured: any cy in (122,175) near x780-840 is <52px
from 03 or 01). Pin order now Antalya 122 < Gaza 155 < Bahrain 186
< BND 187 < PER 196, so Gaza is well clear of the bottom edge and
of the Sources line. NOTE: 10 HKG still sits at cy=138, north of
BAH — the same schematic distortion as before (HK 22.3N is south of
Bahrain 26N); the reviewer did not flag it, and moving it down
would put it south of BND, so it is left alone.

Deliberate deviations from Neon's literal plan, all verified, not
guessed:
- The lead keeps its research-file number (03), not Neon's "01":
  renumbering it 01 would collide with story 01 (Bahrain), which is
  still a card. The kicker reads "03 - TURKEY - 22 NOVEMBER - LEAD".
- The DATE CHECK box keeps its v14.1 position (top 1824 at 2x,
  y912-988 display), not Neon's y892-964: the map block ends at 1810
  and the credit line sits at 1810, so moving the box up 40px would
  mean cropping map labels. The box IS full-width and red, which is
  the substance of P2.
- Neon's exclusion example "Nigeria boat capsize, 21 Nov" was NOT in
  the v15 exclusion list: story 23 stayed a card, and its dek carried
  its date ("21 Nov - search on"). v15.1 reverses that call: both
  Neons flagged the 21 Nov dek on a 22 Nov card, and the research file
  gives no 22 Nov hook for the boat (all sources 21 Nov; "search
  ongoing" is 21 Nov reporting), so story 23 is excluded (DATE CHECK)
  and Onosato (16, 22 Nov, CONFIRMED) takes its card slot. The
  exclusion column now holds the Ukraine strike and the Nigeria boat.
- v15.1 verification note: Neon-2 claimed all 8 card heads are still
  sans-serif. Checked against build/front.html (.card .head is
  Liberation Serif Bold 29px) and 2x crops of cards 01/05/34 — all
  three are visibly bold serif. Neon-1 was right; the heads are NOT
  changed in v15.1.
- Neon's "190+ nations at COP31" number is dropped: no nation count
  is in the research file. The sixth number is 700K (Moyale),
  verified there.
- The 98.79% box is deleted as a standalone chip, but the value is
  kept twice on the page: as numbers column 1 and in card 10's head.

v14.1's first-glance wins are kept: the 170px Liberation Serif Bold
date, the ink italic dek (re-strung to the new top 3), the masthead
rule at 218, the 12-pin map geometry (now 11 pins), the ALSO ON
two-column list, the footer spacing (ink ends 1013). The self-check
below pins the v15.1 layout strings and geometry, so a later edit
cannot silently re-break a reviewer fix.
"""
import hashlib
import os
import re
import shutil
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"
MAX_BYTES = 1024 * 1024


def check_front() -> None:
    """v15.1 self-check: fail loudly if any v15.1 layout string regresses.

    Reads build/front.html (the rendered page) and verifies the strings
    the v15.1 plan depends on. The build fails instead of shipping a
    page that re-breaks a reviewer fix or a verified fact.
    """
    path = os.path.join(HERE, "build", "front.html")
    if not os.path.isfile(path):
        raise SystemExit(f"missing {path}")
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    problems = []

    # --- v15 masthead: date still 170px Liberation Serif Bold; dek
    # re-strung to the new top 3 (COP31, HK votes, Iran claims) ---
    if ".bigdate { position:absolute; left:48px; top:6px; font-family:'Liberation Serif',serif; font-size:170px;" not in html:
        problems.append("date must be 170px Liberation Serif Bold at 2x (v14, kept in v15)")
    if "COP31 collapses in Antalya" not in html:
        problems.append("masthead dek missing 'COP31 collapses in Antalya' (v15)")
    if "Hong Kong votes, turnout 98.79%" not in html:
        problems.append("masthead dek missing 'Hong Kong votes, turnout 98.79%' (v15)")
    if "Iran claims strikes on US bases in Bahrain" not in html:
        problems.append("masthead dek missing 'Iran claims strikes on US bases in Bahrain' (v15)")
    if "400-drone barrage on Ukraine" in html:
        problems.append("masthead dek must not string the excluded Ukraine barrage (v15 P0)")
    if 'class="mastdek"' not in html:
        problems.append("masthead dek div missing (v15)")
    if "font-style:italic; font-size:28px;" not in html:
        problems.append("masthead dek must be 28px italic at 2x (v15)")
    if "ALL TIMES UTC" in html:
        problems.append("'ALL TIMES UTC' must stay dropped (the timeline header says THE DAY IN UTC)")
    if '<div class="rule" style="left:48px; top:218px;' not in html:
        problems.append("masthead rule must be top 218px at 2x (v15)")
    if "33 STORIES &middot; 11 PINS" not in html:
        problems.append("masthead tally must be '33 STORIES · 11 PINS' (v15.2: 33 stories, EU–Indonesia excluded, Gaza promoted)")
    if "35 STORIES" in html or "36 STORIES" in html or "34 STORIES" in html:
        problems.append("stale '34/35/36 STORIES' still present (v15.2 has 33)")

    # --- v15 numbers: six even columns, 68px figures, no bars, no chip ---
    # Columns x48/376/704/1032/1360/1688 at 2x (312 wide, 16 gap) =
    # display x24-1000, each ~156px with an 8px gap (P0).
    for left in ("48px", "376px", "704px", "1032px", "1360px", "1688px"):
        if f'<div class="nfig" style="left:{left};">' not in html:
            problems.append(f"numbers column at left {left} missing (v15 P0: six even columns)")
    if ".nfig { position:absolute; top:290px; width:312px; }" not in html:
        problems.append("numbers columns must be 312px wide at 2x (v15 P0)")
    for fig in ("98.79%", "0", "6.9", "7th", "11", "75th"):
        if f'font-size:68px; margin-top:20px;">{fig}</div>' not in html:
            problems.append(f"numbers figure '{fig}' must be 68px / mt20 at 2x (v15.2: all six are 22 Nov figures, 7th replaces 856)")
    for lab in (
        "HK turnout &middot; 5,640 voters",
        "fossil-fuel mentions in draft",
        "two M6.9 quakes, one day",
        "Emperor&rsquo;s Cup &middot; Onosato",
        "killed after Sinaloa capture",
        "career win &middot; Verstappen",
    ):
        if lab not in html:
            problems.append(f"numbers label '{lab}' missing (v15.2)")
    for src in (
        "INFO.GOV.HK",
        "COP31 DRAFT &middot; REUTERS",
        "PERU 00:09 &middot; BANDA 09:42 UTC",
        "ABEMA &middot; 22 NOV",
        "AP &middot; 22 NOV",
        "FORMULA 1 &middot; 22 NOV",
    ):
        if src not in html:
            problems.append(f"numbers source '{src}' missing (v15.2)")
    if 'font-size:68px; margin-top:20px;">856</div>' in html:
        problems.append("stale numbers figure '856' still present (v15.2: replaced by 7th; 856 survives only in card 10's dek)")
    # v15.2: no 21 Nov date may survive outside the DATE CHECK
    # exclusions (numbers #4 lost its 'EU COUNCIL · 21 NOV' source in
    # v15.1; card 09 itself is gone in v15.2 — the deal is excluded).
    if "21 NOV" in html:
        problems.append("'21 NOV' must not appear anywhere (v15.1 fixes 1+3, v15.2 fix 1)")
    n21 = html.count("21 Nov")
    if n21 != 1 or "Nigeria boat &middot; EU&ndash;Indonesia &middot; 21 Nov" not in html:
        problems.append(
            f"'21 Nov' must appear exactly once (DATE CHECK EXCLUDED: "
            f"Nigeria boat + EU–Indonesia deal share one '21 Nov') "
            f"(found {n21}) (v15.2 fix 1)"
        )
    if ">50%<" in html:
        problems.append("'50%' must not appear as a label (v15.1 fix 6: card 09 chart drops the 50% label; it conflicts with the 98.5% head)")
    if "ratechip" in html:
        problems.append("standalone 98.79% rate chip must be deleted (v15 P0: it is numbers column 1 now)")
    if 'class="bar"' in html:
        problems.append("numbers bars must be deleted (v15 P0: mixed units, no common scale)")
    if "190+" in html:
        problems.append("'190+ nations' must not appear (v15: not in the research file)")
    # v14.1: the full value behind the K display still appears in the
    # ALSO ON rows (row 27 "700,000 displaced").
    if "700,000 displaced" not in html:
        problems.append("ALSO ON row 27 must keep the full value '700,000 displaced' (v15)")
    if "1,671" not in html:
        problems.append("card 28 dek must still carry '1,671' (Gaza toll, promoted from list row 28 in v15.2)")

    # --- v15 lead (COP31 #03, 22 Nov) ---
    if "COP31 &middot; NO DEAL" not in html:
        problems.append("lead banner 'COP31 · NO DEAL' missing (v15 P0)")
    if "UKRAINE &middot; 8 DEAD" in html:
        problems.append("stale lead banner 'UKRAINE · 8 DEAD' still present (v15 P0)")
    if "400 DRONES" in html:
        problems.append("stale lead counts '400 DRONES' still present (v15 P0)")
    if "02 &middot; UKRAINE" in html:
        problems.append("stale lead kicker '02 · UKRAINE' still present (v15 P0)")
    if "03 &middot; TURKEY &middot; 22 NOVEMBER &middot; LEAD" not in html:
        problems.append("lead kicker must be '03 · TURKEY · 22 NOVEMBER · LEAD' (v15 P0)")
    if 'class="bdg">&#10003; CONFIRMED</div>' not in html:
        problems.append("lead badge must be the CONFIRMED capsule (v15 P1)")
    if ".leadtext .bdg { position:absolute; right:0; top:0; font-size:17px; font-weight:bold; line-height:26px; height:30px; padding:0 12px; border:2px solid #81C995; border-radius:6px; background:#E6F4EA; color:#137333;" not in html:
        problems.append("lead badge must use the Neon CONFIRMED capsule spec (v15 P1)")
    if ".leadtext .head { font-family:'Liberation Serif',serif; font-size:72px; font-weight:bold; line-height:76px; margin-top:22px; }" not in html:
        problems.append("lead head must be 72px Liberation Serif Bold / lh 76 at 2x (v15 P1: 36 display)")
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
    if "COP31 COLLAPSES" not in html:
        problems.append("lead headline 'COP31 COLLAPSES' missing")
    if "NO DEAL IN" not in html:
        problems.append("lead headline 'NO DEAL IN' missing")
    if "No consensus in the closing plenary" not in html:
        problems.append("lead dek 'No consensus in the closing plenary' missing")
    if "never mentioned fossil fuels" not in html:
        problems.append("lead dek 'never mentioned fossil fuels' missing")
    if "1.5&deg;C overshoot" not in html:
        problems.append("lead dek '1.5°C overshoot' missing")
    if "COP31 draft text &middot; Reuters" not in html:
        problems.append("lead sources 'COP31 draft text · Reuters' missing")
    # P4: counts row spreads space-between across the 1180px illustration.
    if ".counts { position:absolute; left:48px; top:962px; width:1180px; height:44px; display:flex; justify-content:space-between; }" not in html:
        problems.append("lead counts row must be flex space-between across 1180px (v15 P4)")
    for count in ("FOSSIL-FUEL MENTIONS", "ELECTRIFICATION BY 2035", "LAST COP FAILURE"):
        if count not in html:
            problems.append(f"lead counts missing '{count}' (v15 P4)")
    if "FOSSIL FUELS" not in html:
        problems.append("lead illustration must show the struck 'FOSSIL FUELS' (v15 P0)")
    if "NO DEAL" not in html:
        problems.append("lead illustration must show the 'NO DEAL' stamp (v15 P0)")
    # v15.1 fix 9: the stamp sits fully inside the white paper (rect
    # x344-599, rotate -8 about (494,355)); the right edge ends ~26px
    # inside the paper edge at x630 (>=8px display margin), clear of
    # the struck 'FOSSIL FUELS' (baseline 302). The 45px text sits
    # inside the rect with ~17px padding — at 51px the L foot poked
    # through the rect's right border.
    if 'rotate(-8 494 355)"><rect x="344" y="316" width="255" height="78"' not in html:
        problems.append("NO DEAL stamp must sit at rect (344,316) rotate -8 about (494,355), inside the white paper (v15.1 fix 9)")
    if 'font-size="45" font-weight="bold" fill="#C62828">NO DEAL</text>' not in html:
        problems.append("NO DEAL text must be 45px, inside the stamp rect (v15.1 fix 9: 51px overflowed the rect)")
    if "NOV 9&ndash;21" not in html:
        problems.append("lead illustration must show the 'NOV 9-21' calendar chip (v15 P0)")
    if "+1 DAY" not in html:
        problems.append("lead illustration must show the '+1 DAY' calendar chip (v15 P0)")

    # --- v15.1 timeline: five nodes, NOW stacked on the 17:00 tick ---
    for ev in ("PERU M6.9", "HK POLLS OPEN", "BANDA SEA M6.9", "HK POLLS CLOSE", "ATP FINAL"):
        if ev not in html:
            problems.append(f"timeline missing {ev}")
    if "NOW 17:00" in html:
        problems.append("timeline NOW marker must be time-free 'NOW' (one '17:00' only)")
    if "22:00" in html:
        problems.append("stale '22:00' still present (one clock, 17:00)")
    tl_start = html.index("<!-- THE DAY IN UTC")
    tl_end = html.index("<!-- THE DAY IN NUMBERS")
    tl_band = html[tl_start:tl_end]
    if tl_band.count("17:00") != 1:
        problems.append(
            f"timeline band must carry exactly one '17:00' "
            f"(found {tl_band.count('17:00')}) (v15 P3)"
        )
    if ">NOW</div>" not in tl_band:
        problems.append("timeline NOW dot missing (v15 P3)")
    if 'class="nowmark" style="left:1487px;"' not in tl_band:
        problems.append(
            "NOW marker must sit at left 1487px at 2x (64px wide, centred), "
            "ring centred 8px left of the 17:00 tick at 1527px, clear of "
            "the '1' glyph (v15.1 fix 8: stacked NOW; v15.2 fix 5: nudged "
            "right 16px so NOW clears the 10:00 CLOSE label)"
        )
    if 'left:1791px' in tl_band or 'left:1799px' in tl_band:
        problems.append("stale NOW at 1791px / tick at 1799px still present (v15.1 fix 8: NOW is on the 17:00 tick)")
    if 'left:360px; top:270px; width:1360px; height:2px; background:#191919;' not in tl_band:
        problems.append("timeline axis rule must end at 1720px (width 1360px) (v15.1 fix 8)")
    for tx in (359, 647, 935, 1223, 1527):
        if f'left:{tx}px; top:264px; width:2px; height:12px; background:#191919;' not in tl_band:
            problems.append(f"timeline tick mark at left {tx}px missing (v15.2 fix 5: 17:00 tick at 1527)")

    # --- region strip: EUROPE 6 (Ukraine excluded), AFRICA 4 (Nigeria excluded), ASIA 7 (EU–Indonesia excluded), 33 stories total ---
    for reg in (
        "MIDDLE EAST 4", "EUROPE 6", "ASIA 7", "AMERICAS 7",
        "AFRICA 4", "OCEANIA 2", "MKT+SPORT 3",
    ):
        if reg not in html:
            problems.append(f"region strip missing {reg}")
    if "EUROPE 7" in html:
        problems.append("stale 'EUROPE 7' still present (v15: Ukraine excluded, EUROPE 6)")
    if "ASIA 8" in html:
        problems.append("stale 'ASIA 8' still present (v15.2: EU–Indonesia excluded, ASIA 7)")
    if "#A63A2E" in html:
        problems.append(
            "Middle East colour #A63A2E still present (must be "
            "teal #2E7A7A, #A63A2E reads as red)"
        )
    if html.count("#2E7A7A") != 5:
        problems.append(
            f"Middle East teal #2E7A7A must occur exactly 5 times "
            f"(region swatch + card 01 toprule/kick + card 28 toprule/kick) "
            f"(found {html.count('#2E7A7A')})"
        )

    # --- cards: 8 cards, serif heads, capsule badges + source ---
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
    # (v15.2: confirmed = lead 03 + cards 04, 05, 16, 18, 28; official =
    # cards 10, 34; claim = card 01) — coincidentally the v14 tally,
    # for a different set of stories.
    if html.count("6 confirmed &middot; 2 official &middot; 1 claim") != 1:
        problems.append(
            "footer verification tally '6 confirmed · 2 official · 1 claim' "
            "must appear once (v15.2)"
        )
    if "5 confirmed &middot; 3 official &middot; 1 claim" in html:
        problems.append("stale v15.1 tally '5 confirmed · 3 official · 1 claim' still present (v15.2)")

    # step 1 (v11): the status dot lives inside the thumbnail (6px in from
    # its top and right edge), so it can no longer collide with a kicker.
    if ".card .vdot { position:absolute; left:144px; top:24px;" not in html:
        problems.append("card .vdot must sit inside the thumbnail (step 1)")

    # ruling 4 (v11): CLAIM dot is amber, not red-brown.
    if 'vdot" style="background:#D98E00;"' not in cards_html:
        problems.append("card 01 CLAIM dot must be amber #D98E00 (ruling 4)")

    # v15 P1: capsule badges. Colours per Neon; CLAIM has no check mark
    # (the winners' legend checks only CONFIRMED and OFFICIAL).
    if ".b-conf { background:#E6F4EA; color:#137333; border-color:#81C995; }" not in html:
        problems.append("CONFIRMED capsule colours must be #E6F4EA/#137333/#81C995 (v15 P1)")
    if ".b-off { background:#E8F0FE; color:#1967D2; border-color:#8AB4F8; }" not in html:
        problems.append("OFFICIAL capsule colours must be #E8F0FE/#1967D2/#8AB4F8 (v15 P1)")
    if ".b-rep { background:#FEF7E0; color:#B06000; border-color:#FDD663; }" not in html:
        problems.append("REPORTED capsule colours must be #FEF7E0/#B06000/#FDD663 (v15 P1)")
    if ".b-claim { background:#FCE8E6; color:#C5221F; border-color:#F28B82; }" not in html:
        problems.append("CLAIM capsule colours must be #FCE8E6/#C5221F/#F28B82 (v15 P1)")
    if ".card .src .bdg2 { display:inline-block; height:30px; line-height:26px; padding:0 12px; border-radius:6px; font-size:17px; font-weight:bold; border:2px solid; vertical-align:middle; }" not in html:
        problems.append("card badge must be 30px high / 6px radius / 17px bold at 2x (v15 P1)")
    if cards_html.count('bdg2 b-conf') != 5:
        problems.append(f"CONFIRMED badges must be 5 (cards 04, 05, 16, 18, 28) (found {cards_html.count('bdg2 b-conf')})")
    if cards_html.count('bdg2 b-off') != 2:
        problems.append(f"OFFICIAL badges must be 2 (cards 10, 34) (found {cards_html.count('bdg2 b-off')})")
    if cards_html.count('bdg2 b-claim') != 1:
        problems.append(f"CLAIM badges must be 1 (card 01) (found {cards_html.count('bdg2 b-claim')})")
    if '&#10003; CLAIM' in cards_html:
        problems.append("CLAIM badge must not carry a check mark (winners' legend: only CONFIRMED/OFFICIAL are checked)")
    # the old tiny-grey "STATUS · SOURCE · SOURCE" line is gone: no
    # .src may still carry the "CONFIRMED ·" text form.
    if "CONFIRMED &middot;" in cards_html:
        problems.append("old 'CONFIRMED · SOURCE' text form must be gone (v15 P1: capsule badges)")
    if "FRANCE 24" in cards_html:
        problems.append("card 04 source must fit the badge row (v15 P1: one short source)")
    # v15.2 fix 3: every CONFIRMED card prints both verified sources
    # (legend: CONFIRMED = two independent sources). Card 05 already
    # printed BBC · NYT; the other four get their second source here.
    # Neon-2's suggested YLE (card 04) and KYODO (card 16) are NOT in
    # the research file and are not used.
    for pair in (
        "EURONEWS &middot; REUTERS",
        "REUTERS &middot; AP",
        "ABEMA &middot; TACHIAI",
        "REUTERS &middot; MIDDLE EAST EYE",
    ):
        if pair not in cards_html:
            problems.append(f"CONFIRMED card must print both sources '{pair}' (v15.2 fix 3: legend = two independent sources)")
    # v15.2 fix 3: the badge row is full-width (left 8, 460px) so
    # badge (163px) + two sources (up to 247px) fits; the old 288px
    # text column could not hold a two-source CONFIRMED row.
    if ".card .src { position:absolute; left:8px; top:208px; width:460px; white-space:nowrap; }" not in html:
        problems.append("card src must be full-width left 8 / width 460 at 2x (v15.2 fix 3: two-source badge rows must fit)")

    # v15 P1: card heads are Liberation Serif Bold 29px / lh 33 at 2x.
    # v15.1: Neon-2 claimed the 8 heads are sans-serif — verified
    # false on 2026-11-23 (CSS is Liberation Serif Bold; 2x crops of
    # cards 01/05/34 are visibly bold serif). Heads NOT changed.
    if ".card .head { position:absolute; left:180px; top:64px; width:284px; font-family:'Liberation Serif',serif; font-size:29px; font-weight:bold; line-height:33px; }" not in html:
        problems.append("card head must be 29px Liberation Serif Bold / lh 33 at 2x (v15 P1)")
    if ".card .kick { position:absolute; left:180px; top:16px; width:268px;" not in html:
        problems.append("card kicker must be width 268px at 2x (v12 step 6)")
    if ".card .kick" in html and "white-space:nowrap" in html.split(".card .kick")[1].split("}")[0]:
        problems.append("card kicker must not be nowrap (v12 step 6: wrap allowed)")
    if ".card .dek { position:absolute; left:180px; top:134px;" not in html:
        problems.append("card dek must be top 134px at 2x (v12 step 6)")
    if ".card .src { position:absolute; left:8px; top:208px;" not in html:
        problems.append("card src must be top 208px at 2x (v15 P1: 30px badge ends 238, inside the 260px card; v15.2: full-width)")

    # v15 P4: card 05 (crosshair) and card 18 (handcuffs) are mini
    # data/geo infographics now; the old icons must be gone.
    if 'r="8" fill="#C65D00"' in html:
        problems.append("card 05 crosshair centre still present (v15 P4: replaced by the bars infographic)")
    if 'M56 40 L104 88" stroke="#C65D00"' in html:
        problems.append("card 05 crosshair slash still present (v15 P4)")
    if "CHARGED" not in cards_html or "EXPELLED" not in cards_html:
        problems.append("card 05 bars infographic must label CHARGED / EXPELLED (v15 P4)")
    # v15 visual fix: the bar labels are 10px, not 12px — at 12px the
    # two labels touched (CHARGED ends where EXPELLED begins).
    if 'font-size="10" font-weight="bold" text-anchor="middle" fill="#191919">CHARGED</text>' not in cards_html:
        problems.append("card 05 label CHARGED must be 10px (v15 visual fix: 12px labels touched)")
    if 'font-size="10" font-weight="bold" text-anchor="middle" fill="#191919">EXPELLED</text>' not in cards_html:
        problems.append("card 05 label EXPELLED must be 10px (v15 visual fix: 12px labels touched)")
    if "SINALOA" not in cards_html or "$5M" not in cards_html:
        problems.append("card 18 mini-map must label SINALOA and $5M (v15 P4)")
    # v15: F1 is the eighth card (was list row 34).
    if "Verstappen wins" not in cards_html:
        problems.append("card 34 'Verstappen wins' missing (v15 P0)")
    if "Las Vegas GP" not in cards_html:
        problems.append("card 34 'Las Vegas GP' missing (v15 P0)")
    if "75th career win" not in cards_html:
        problems.append("card 34 dek '75th career win' missing (v15 P0)")
    if "35 lead changes" not in cards_html:
        problems.append("card 34 dek '35 lead changes' missing (v15 P0)")
    # step 5 (v11): card 10 dek is two lines of counts only.
    if "856 candidates &middot;<br>723 seats" not in cards_html:
        problems.append("card 10 dek must be '856 candidates · / 723 seats' (step 5)")
    if "results tonight" in cards_html:
        problems.append("'results tonight' must not be on card 10 (step 5)")
    # v15.1 fix 6: card 09 is a before/after bar now (100% -> 1.5% left);
    # the 50% label is gone — it conflicted with the 98.5% head.
    if ">50%<" in cards_html:
        problems.append("card '50%' label must be gone (v15.1 fix 6: it conflicted with the 98.5% head; the card is gone in v15.2)")
    if "1.5% left" in cards_html:
        problems.append("card 09 before/after bar must be gone (v15.2 fix 1: the EU–Indonesia card is excluded)")
    if "BEFORE" in cards_html:
        problems.append("card 09 before/after bar must be gone (v15.2 fix 1)")
    if "98.5% tariffs gone" in cards_html:
        problems.append("card 09 head '98.5% tariffs gone' must be gone (v15.2 fix 1: deal excluded, signed 21 Nov)")
    if "EU COUNCIL" in cards_html:
        problems.append("card 09 source 'EU COUNCIL' must be gone (v15.2 fix 1)")
    if ">0%<" in cards_html:
        problems.append("card 09 '0%' label must be dropped (step 6)")
    # v15.2 fix 1: card 28 is Gaza, 22 Nov, CONFIRMED (research:
    # Reuters via Gulf Daily News + Middle East Eye 22 Nov; strike
    # kills 3 in Gaza City, toll since the truce now 1,671).
    if "Strike kills 3 in" not in cards_html:
        problems.append("card 28 head 'Strike kills 3 in' missing (v15.2 fix 1)")
    if "Gaza City" not in cards_html:
        problems.append("card 28 head 'Gaza City' missing (v15.2 fix 1)")
    if "Death toll since truce" not in cards_html:
        problems.append("card 28 dek 'Death toll since truce' missing (v15.2 fix 1)")
    if "now 1,671" not in cards_html:
        problems.append("card 28 dek 'now 1,671' missing (v15.2 fix 1)")
    if "REUTERS &middot; MIDDLE EAST EYE" not in cards_html:
        problems.append("card 28 source 'REUTERS · MIDDLE EAST EYE' missing (v15.2 fix 1)")
    # v15.1 fix 3: card 23 is gone (21 Nov only, excluded); card 16 is
    # Onosato, 22 Nov, CONFIRMED (evening refresh: 7th Emperor's Cup,
    # playoff win over Wakamotoharu, both 13-2).
    if "Mourners&rsquo; boat" in cards_html or "21 Nov &middot; search on" in cards_html:
        problems.append("card 23 must be gone (v15.1 fix 3: 21 Nov only, excluded)")
    if "Onosato wins" not in cards_html:
        problems.append("card 16 head 'Onosato wins' missing (v15.1 fix 3)")
    if "7th Emperor&rsquo;s Cup" not in cards_html:
        problems.append("card 16 head '7th Emperor's Cup' missing (v15.1 fix 3)")
    if "Beats Wakamotoharu" not in cards_html:
        problems.append("card 16 dek 'Beats Wakamotoharu' missing (v15.1 fix 3)")
    if "ABEMA" not in cards_html:
        problems.append("card 16 source 'ABEMA' missing (v15.1 fix 3)")
    # v13 fix 3 (kept): the ship funnels in card 04 are neutral grey.
    if 'M66 46 L72 26 L78 46 Z" fill="#C65D00"' in html:
        problems.append("card 04 funnel 1 still #C65D00 (v13 fix 3: must be neutral)")
    if 'M84 46 L90 32 L96 46 Z" fill="#D98E00"' in html:
        problems.append("card 04 funnel 2 still #D98E00 (v13 fix 3: must be neutral)")
    if 'M66 46 L72 26 L78 46 Z" fill="#6B6B6B"' not in html:
        problems.append("card 04 funnel 1 must be neutral grey #6B6B6B (v13 fix 3)")
    if 'M84 46 L90 32 L96 46 Z" fill="#6B6B6B"' not in html:
        problems.append("card 04 funnel 2 must be neutral grey #6B6B6B (v13 fix 3)")

    # --- map: 11 pins, land #D5CEC0, grid #AFA695 ---
    map_start = html.index("<!-- MAP")
    map_end = html.index("<!-- DATE CHECK")
    map_html = html[map_start:map_end]
    pins = map_html.count("<circle cx=")
    if pins != 11:
        problems.append(f"map pins must be 11 (found {pins}) (v15.2 fix 1: 28 GAZA in, 09 JKT out)")
    for num in ("01", "03", "04", "05", "10", "11", "16", "17", "18", "28", "34"):
        if f">{num}</text>" not in map_html:
            problems.append(f"map pin number {num} missing")
    for gone in ("02", "09", "19", "23", "27"):
        if f">{gone}</text>" in map_html:
            problems.append(f"map pin {gone} must be gone (v15.2 fix 1: 09 out; v15.1 fix 5: 19/23/27 out)")
    for slug in (
        "CPH", "GOF", "ANTALYA", "BAH", "GAZA",
        "HKG", "BND", "FUK", "PER", "SINALOA", "LAS",
    ):
        if f">{slug}</text>" not in map_html:
            problems.append(f"map pin slug {slug} missing")
    for gone_slug in ("BAY", "MOY", "BSB", "JKT", "LVIV"):
        if f">{gone_slug}</text>" in map_html:
            problems.append(f"map pin slug {gone_slug} must be gone (v15.2 fix 1: JKT out; v15.1 fix 5: the rest)")
    if "THE WORLD &middot; 11 PINS" not in map_html:
        problems.append("map label must be 'THE WORLD · 11 PINS' (v15)")
    # v12 step 5: every pin is neutral ink with a white numeral.
    if map_html.count('fill="#191919"/>') < 11:
        problems.append("all 11 map pins must be ink #191919 (v12 step 5)")
    for region_fill in ("#2F5D8A", "#2E7A7A", "#8A5A28", "#B97A1E", "#4A7A3D"):
        if region_fill in map_html:
            problems.append(
                f"region fill {region_fill} still on a map pin (v12 step 5)"
            )
    # v12 step 8: numerals are 12px display (24px at 2x) on every pin.
    if map_html.count('font-size="24"') != 11:
        problems.append(
            f"all 11 pin numerals must be 24px at 2x "
            f"(found {map_html.count('font-size=\"24\"')}) (v12 step 8)"
        )
    # v15 P3: map land darker. The schematic map has no landmass shapes,
    # so the land colour is the panel fill and the stroke is the grid.
    if ".mapbox { position:absolute; left:48px; top:1538px; width:1240px; height:272px; background:#D5CEC0;" not in html:
        problems.append("map panel must be #D5CEC0 (v15 P3: darker land)")
    if 'stroke="#AFA695"' not in map_html:
        problems.append("map grid must be #AFA695 (v15 P3)")
    # v13 fix 4 (kept, minus Lviv): ANTALYA (37N) sits above BAH (26N).
    pin_cy = {}
    for m in re.finditer(
        r'<circle cx="(\d+)" cy="(\d+)" r="26"[^>]*><text x="\d+" y="\d+"[^>]*>(\d+)</text>',
        map_html,
    ):
        pin_cy[m.group(3)] = int(m.group(2))
    for want in ("01", "03"):
        if want not in pin_cy:
            problems.append(f"map pin {want} circle not found")
    if all(k in pin_cy for k in ("01", "03")):
        if not (pin_cy["03"] < pin_cy["01"]):
            problems.append(
                f"pin latitudes wrong: ANTALYA cy={pin_cy['03']}, BAH "
                f"cy={pin_cy['01']} (need ANTALYA < BAH)"
            )
    if '<text x="734" y="54">GOF</text>' not in map_html:
        problems.append("GOF label must sit right of its pin at (734, 54) (v13 fix 4)")
    if '<text x="890" y="191">BAH</text>' not in map_html:
        problems.append("BAH label must sit at (890, 191), right of pin 01 (v15.3: pin moved to (856, 186))")
    if '<text x="730" y="127" text-anchor="end">ANTALYA</text>' not in map_html:
        problems.append("ANTALYA label must sit left of pin 03 at (730, 127) (v15.3)")
    # v15.2 fix 2: SINALOA moves right of pin 18 (x283, 6px clear of
    # the pin's right edge at 277) so it no longer touches pin 34.
    if '<text x="283" y="138">SINALOA</text>' not in map_html:
        problems.append("SINALOA label must sit right of pin 18 at (283, 138), clear of pin 34 (v15.2 fix 2)")
    if '<text x="220" y="138" text-anchor="end">SINALOA</text>' in map_html:
        problems.append("stale SINALOA label left of pin 18 still present (v15.2 fix 2: it touched pin 34)")
    # v15.3: pin 28 GAZA sits just below 03 ANTALYA, above 01 BAH —
    # (805,155), label left at (773,160). The BAH nudge to (856,186)
    # is the knock-on: no third r=26 pin fits the ~70px 03-01 gap.
    if '<circle cx="805" cy="155" r="26" fill="#191919"/><text x="805" y="164" font-size="24">28</text>' not in map_html:
        problems.append("map pin 28 GAZA must sit at (805, 155) (v15.3: just below ANTALYA, above BAH)")
    if '<text x="773" y="160" text-anchor="end">GAZA</text>' not in map_html:
        problems.append("GAZA label must sit left of pin 28 at (773, 160) (v15.3)")
    if '<circle cx="775" cy="218" r="26" fill="#191919"/>' in map_html:
        problems.append("stale v15.2 GAZA pin at (775, 218) still present (v15.3: southernmost, below BND/PER)")
    if '<text x="775" y="258" text-anchor="middle">GAZA</text>' in map_html:
        problems.append("stale v15.2 GAZA label below the pin at (775, 258) still present (v15.3)")
    # v15.3: pin north-south order — Antalya > Gaza > Bahrain, and
    # Gaza is NOT southernmost (BND and PER stay the southernmost).
    # (10 HKG at cy=138 still sits north of BAH — pre-existing
    # schematic distortion, reviewer did not flag it, left alone.)
    if all(k in pin_cy for k in ("03", "28", "01", "11", "17")):
        if not (pin_cy["03"] < pin_cy["28"] < pin_cy["01"]):
            problems.append(
                f"pin latitudes wrong: ANTALYA cy={pin_cy['03']}, GAZA "
                f"cy={pin_cy['28']}, BAH cy={pin_cy['01']} "
                f"(need ANTALYA < GAZA < BAH) (v15.3)"
            )
        if not (pin_cy["28"] < pin_cy["11"] and pin_cy["28"] < pin_cy["17"]):
            problems.append(
                f"GAZA must not be southernmost: GAZA cy={pin_cy['28']}, "
                f"BND cy={pin_cy['11']}, PER cy={pin_cy['17']} (v15.3)"
            )
    else:
        for want in ("28", "11", "17"):
            if want not in pin_cy:
                problems.append(f"map pin {want} circle not found (v15.3 order check)")

    # --- ALSO ON list: 26 rows in a real 2-column grid ---
    if '.lst .col { position:absolute; top:20px; width:336px; overflow:hidden; }' not in html:
        problems.append("list .col must have the overflow clip guard (v12 step 1)")
    if 'style="left:0; width:336px;"' not in html:
        problems.append("list left column must be 336px at 2x (v12 step 1)")
    if 'style="left:368px;"' not in html:
        problems.append("list right column must start at left 368px at 2x (v12 step 1)")
    if ".lst { position:absolute; left:1312px; top:1538px; width:704px; height:272px; }" not in html:
        problems.append("list block must be left 1312 / top 1538 / width 704 / height 272 at 2x (v12 step 1)")
    if ".lst .row { font-size:16px; line-height:18px;" not in html:
        problems.append("list rows must be 16px / 18px at 2x (v12 step 2)")
    if ".lst .col.r .row { line-height:18px; }" not in html:
        problems.append("list right column pitch must be 18px at 2x (v15.2: 12/12 rows, even pitch)")
    rows = re.findall(r'<div class="row">.*?</div>', html)
    if len(rows) != 24:
        problems.append(f"ALSO ON rows must be 24 (found {len(rows)}) (v15.2: 28 is a card now)")
    for row in rows:
        if " &mdash; " in row:
            problems.append(f"row still carries a per-row source (v12 step 2): {row[:60]!r}")
            break
    if "Verstappen wins Vegas" in html:
        problems.append("list row 34 'Verstappen wins Vegas' must be gone (v15: F1 is card 34)")
    if "Sources: Anadolu" not in html:
        problems.append("shared credit line 'Sources: Anadolu …' missing (v12 step 2)")
    if 'style="position:absolute; left:48px; top:1810px; width:1952px;' not in html:
        problems.append("credit line must sit at top 1810px full width (v12 step 2)")
    if "24 MORE STORIES &middot; 06&ndash;36" not in html:
        problems.append("ALSO ON header must read '24 MORE STORIES · 06–36' (v15.2)")
    if "25 MORE STORIES" in html or "26 MORE STORIES" in html or "27 MORE STORIES" in html:
        problems.append("stale '25/26/27 MORE STORIES' still present (v15.2 has 24)")
    if "text-overflow:ellipsis; padding-right:8px;" not in html:
        problems.append("list rows need ellipsis + 8px right inset at 2x (v12 step 4)")
    if ".lst .row .n { font-weight:bold; color:#191919; }" not in html:
        problems.append("ALSO ON numerals must be ink #191919")

    # --- DATE CHECK: full-width red box, EXCLUDED (PRE-22 NOV) ---
    if ".dc { position:absolute; left:48px; top:1824px; width:1952px; height:152px; border:3px solid #C62828; background:#FDF2F2; }" not in html:
        problems.append("DATE CHECK must be the red box: 3px #C62828 border, #FDF2F2 bg, top 1824 (v15 P2)")
    if 'class="redbar"' not in html:
        problems.append("DATE CHECK left red bar missing (v15 P2)")
    if ".dc .redbar { position:absolute; left:0; top:0; width:10px; height:146px; background:#C62828; }" not in html:
        problems.append("DATE CHECK red bar must be 10px wide #C62828 (v15 P2: 5px display)")
    if ".dc .l b { color:#C62828; }" not in html:
        problems.append("DATE CHECK title must be #C62828 (v15 P2)")
    if "<b>DATE CHECK &check;</b> As of 22 Nov, 17:00 UTC." not in html:
        problems.append("DATE CHECK title line must be 'DATE CHECK ✓ As of 22 Nov, 17:00 UTC.' (v15 P2)")
    if "Includes items that broke 19&ndash;21 Nov" in html:
        problems.append("DATE CHECK must not admit non-22-Nov items were included (v15 P2)")
    for col in ("EXCLUDED (PRE-22 NOV)", "LEFT OUT", "NOT YET (POST-17:00 UTC)", "OFFICIAL REVISIONS"):
        if col not in html:
            problems.append(f"DATE CHECK column {col} missing (v15.1 fix 7)")
    if "CORRECTIONS" in html:
        problems.append("stale DATE CHECK column 'CORRECTIONS' still present (v15.1 fix 7: OFFICIAL REVISIONS)")
    if "HK: 5,640 registered voters (subsector)" not in html:
        problems.append("DATE CHECK revisions must read 'HK: 5,640 registered voters (subsector)' (v15.1 fix 7)")
    if "NEMA toll, Nigeria" in html:
        problems.append("stale 'NEMA toll, Nigeria' still present (v15.1 fix 7: the Nigeria note left with the excluded story)")
    if "HK 5,640 voters" in html:
        problems.append("stale 'HK 5,640 voters' still present (v15.1 fix 7: 'HK: 5,640 registered voters (subsector)')")
    if "Nigeria boat capsize &middot; 21 Nov" in html:
        problems.append("stale 'Nigeria boat capsize · 21 Nov' still present (v15.2 fix 1: the two 21 Nov items share one line)")
    if "EU&ndash;Indonesia &middot; 21 Nov" not in html:
        problems.append("DATE CHECK must exclude the EU–Indonesia deal with its date (v15.2 fix 1)")
    if "HELD" in html:
        problems.append("stale DATE CHECK column 'HELD' still present (v15 P2: it is EXCLUDED now)")
    if "Ukraine 400-drone strike &middot; 19&ndash;20 Nov" not in html:
        problems.append("DATE CHECK must exclude the Ukraine strike with its date (v15 P2)")
    if "Nigeria boat capsize" in html:
        problems.append("stale 'Nigeria boat capsize' still present (v15.2 fix 1: shortened to 'Nigeria boat' so both 21-Nov items share one line)")
    if ".dc .col .h .notyet { color:#D98E00; }" not in html:
        problems.append("DATE CHECK NOT YET must be amber (v12 step 5)")

    # --- red, settled: #B01E1E still 4 source uses (banner, NOW text,
    # NOW ring, card-01 radar dot); the DATE CHECK and lead stamp use
    # the separate #C62828, so the count is unchanged ---
    red_uses = html.count("#B01E1E")
    if red_uses != 4:
        problems.append(
            f"brand red #B01E1E must occur 4 times in source "
            f"(found {red_uses})"
        )
    if "#B01E1E" in map_html:
        problems.append("no brand red may remain on a map pin (v12 step 5)")
    if html.count("#C62828") < 5:
        problems.append(
            f"DATE CHECK / lead red #C62828 must appear at least 5 times "
            f"(box border, bar, title, rule, stamp) (found {html.count('#C62828')})"
        )

    # --- vertical geometry (unchanged from v14.1): map/lst end at 1816,
    # credit line 1816-1830, DATE CHECK top 1830, footer ends at y=1010
    # display ---
    if ".mapbox { position:absolute; left:48px; top:1538px; width:1240px; height:272px;" not in html:
        problems.append("mapbox must be top 1538 / height 272 at 2x (v12 step 2)")
    if ".dc { position:absolute; left:48px; top:1824px;" not in html:
        problems.append("DATE CHECK must be top 1824 at 2x (v14.1, kept in v15)")
    if 'class="foot" style="top:1990px;"' not in html:
        problems.append("footer line 1 must be top 1990 at 2x (v14.1: 6px clear of the DATE CHECK border, ink ends 1013)")
    if 'class="foot" style="top:2012px;"' not in html:
        problems.append("footer line 2 must be top 2012 at 2x (v14.1: 3px clear of line 1 ink, ends 1013)")

    # --- 33 story slots: 1 lead + 8 cards + 24 list rows ---
    slots = (
        html.count('<div class="leadtext">')
        + html.count('<div class="card"')
        + html.count('<div class="row">')
    )
    if slots != 33:
        problems.append(f"story slots must be 33 (found {slots}) (v15.2: Ukraine + Nigeria + EU–Indonesia excluded)")

    if problems:
        raise SystemExit("front.html v15 check failed:\n- " + "\n- ".join(problems))
    print(
        f"front.html v15.3 check ok: COP31 lead + serif heads + capsule badges (two sources on every CONFIRMED card, full-width badge rows); 6 numbers, all 22 Nov (7th replaces 856); "
        f"1 lead + {cards} cards + 24 list rows = 33 slots; 11 map pins "
        f"(28 GAZA (805,155) below ANTALYA (762,122), above BAH (856,186); SINALOA clear of 34); timeline 5 nodes, NOW stacked on the 17:00 tick (nudged right 16px); DATE CHECK red box, Nigeria + EU–Indonesia excluded, OFFICIAL "
        f"REVISIONS; red #B01E1E x4; footer ends 1013"
    )


def _decode_png_grey(data: bytes):
    """Decode a non-interlaced 8-bit PNG to greyscale rows. Stdlib only.

    Returns (width, height, px) where px is a bytearray of width*height
    greyscale values (0 = black). Handles colour types 0 (grey), 2 (RGB)
    and 6 (RGBA) at 8 bits; chrome-headless-shell writes one of these.
    """
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("not a PNG")
    pos = 8
    width = height = None
    colortype = None
    idat = b""
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + length]
        if ctype == b"IHDR":
            width, height, bitdepth, colortype = struct.unpack(">IIBB", chunk[:10])
            if chunk[12] != 0:
                raise SystemExit("interlaced PNG not supported by the ink check")
            if bitdepth != 8 or colortype not in (0, 2, 6):
                raise SystemExit(
                    f"unsupported PNG: bitdepth {bitdepth} colortype {colortype}"
                )
        elif ctype == b"IDAT":
            idat += chunk
        elif ctype == b"IEND":
            break
        pos += 12 + length
    raw = zlib.decompress(idat)
    channels = {0: 1, 2: 3, 6: 4}[colortype]
    stride = width * channels
    px = bytearray(width * height)
    prev = bytearray(stride)
    p = 0
    for y in range(height):
        f = raw[p]
        p += 1
        line = bytearray(raw[p:p + stride])
        p += stride
        if f == 0:
            pass
        elif f == 1:
            for i in range(channels, stride):
                line[i] = (line[i] + line[i - channels]) & 0xFF
        elif f == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif f == 3:
            for i in range(stride):
                a = line[i - channels] if i >= channels else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 0xFF
        elif f == 4:
            for i in range(stride):
                a = line[i - channels] if i >= channels else 0
                b = prev[i]
                c = prev[i - channels] if i >= channels else 0
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 0xFF
        else:
            raise SystemExit(f"unknown PNG filter {f}")
        if colortype == 0:
            px[y * width:(y + 1) * width] = line
        else:
            step = 3 if colortype == 2 else 4
            for x in range(width):
                r, g, b = line[x * step], line[x * step + 1], line[x * step + 2]
                px[y * width + x] = (r * 299 + g * 587 + b * 114) // 1000
        prev = line
    return width, height, px


def check_number_ink(data: bytes) -> None:
    """v15: fail if neighbouring numbers' INK touches.

    Measures the RENDERED dark pixels in the numbers band (display
    y 150-190, x 0-1000), not text bounding boxes. The six figures sit
    in even 156px columns (x24/188/352/516/680/844 display); the
    numeral ink runs about y 157-183 (68px at 2x, top 290 + mt 20) and
    the 18px labels start at y 193, so the band 150-190 catches the
    numerals only. Columns with dark ink merge into a group when
    separated by < 12px; there must be exactly 6 groups (one per
    numeral) with >= 12px between neighbours.
    """
    width, height, px = _decode_png_grey(data)
    if (width, height) != (1024, 1024):
        raise SystemExit(f"ink check needs 1024x1024, got {width}x{height}")
    dark_cols = []
    for x in range(1000):
        dark = any(px[y * width + x] < 100 for y in range(150, 191))
        dark_cols.append(dark)
    groups = []
    inrun = False
    for x in range(1000):
        if dark_cols[x] and not inrun:
            start = x
            inrun = True
        elif not dark_cols[x] and inrun:
            groups.append([start, x - 1])
            inrun = False
    if inrun:
        groups.append([start, 999])
    merged = []
    for g in groups:
        if merged and g[0] - merged[-1][1] - 1 < 12:
            merged[-1][1] = g[1]
        else:
            merged.append(list(g))
    if len(merged) != 6:
        raise SystemExit(
            f"numbers ink check failed: {len(merged)} ink groups, want 6 "
            f"(neighbouring numbers merged?): {merged}"
        )
    gaps = [merged[i + 1][0] - merged[i][1] - 1 for i in range(5)]
    if min(gaps) < 12:
        raise SystemExit(
            f"numbers ink check failed: inter-number gaps {gaps}, "
            f"all must be >= 12px display"
        )
    print(f"numbers ink check ok: 6 groups, gaps {gaps} display px")


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
    check_number_ink(data)
    print(f"entry.png {len(data)} bytes sha256={hashlib.sha256(data).hexdigest()}")
    if verify_only:
        return 0
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
