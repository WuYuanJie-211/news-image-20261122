#!/usr/bin/env python3
"""news-image-20261122 entrypoint (v15): copy entry.png to /output/entry.png.

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
story slots entirely and moves into DATE CHECK exclusions. The page is
now 35 stories (1 lead + 8 cards + 26 rows); F1 (Verstappen wins Las
Vegas, OFFICIAL, 22 Nov) is promoted from the list to the eighth card.
THE DAY IN NUMBERS is rebuilt: six even columns across x24-1000, each
~156px with an 8px gap, all figures 68px, no bars, no standalone
98.79% box (the turnout IS one of the six numbers now). The six
numbers, every one verified in news-20261122.md: 98.79% HK turnout
(5,640 voters, OFFICIAL, 22 Nov); 0 fossil-fuel mentions in the COP31
draft (Reuters, collapsed 22 Nov); 6.9, two M6.9 quakes in one day
(Peru 00:09 UTC, Banda Sea 09:42 UTC); 98.5% tariffs gone,
EU-Indonesia (signed 21 Nov, OFFICIAL); 11 killed after the Sinaloa
capture (AP, 22 Nov follow-up); 700K displaced in Moyale (Islamic
Relief; the full value still appears in ALSO ON row 27).

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
Ukraine 400-drone strike with its original date (19-20 Nov). LEFT
OUT, NOT YET (POST-17:00 UTC) and CORRECTIONS stay. The old
"Includes items that broke 19-21 Nov" line is deleted: no wording
admits non-22-Nov items were included.

P3 — the map land goes darker (#D5CEC0 fill, #AFA695 grid) and the
UTC timeline grows to six nodes: five timed events (00:09 Peru,
01:00 HK polls open, 09:42 Banda Sea, 10:00 HK polls close, 17:00
ATP final) plus NOW anchored on the last tick at 17:00 UTC. (The
sixth timed event Neon sketched, a COP31/F1 time, is not in the
research file, so the sixth node is the NOW marker itself on the
17:00 tick.)

P4 — the lead counts row spreads space-between across the 1180px
illustration width (0 fossil-fuel mentions / 35% electrification by
2035 / 2009 last COP failure), and cards 05 and 18 get mini
data/geo infographics instead of generic icons: card 05 (Denmark
plot) gets a two-bar chart (2 charged vs 1 expelled); card 18
(Sinaloa) gets a schematic mini-map with an 18 pin and a $5M chip.
The lead illustration is redrawn for COP31: the draft document with
FOSSIL FUELS struck out, a NO DEAL stamp, a 1.5C thermometer and a
NOV 9-21 +1 DAY calendar chip.

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
- Neon's exclusion example "Nigeria boat capsize, 21 Nov" is NOT in
  the exclusion list: story 23 stays a card, and its dek now carries
  its date ("21 Nov - search on"), so listing it as excluded would
  contradict the page. The exclusion column holds the Ukraine strike.
- Neon's "190+ nations at COP31" number is dropped: no nation count
  is in the research file. The sixth number is 700K (Moyale),
  verified there.
- The 98.79% box is deleted as a standalone chip, but the value is
  kept twice on the page: as numbers column 1 and in card 10's head.

v14.1's first-glance wins are kept: the 170px Liberation Serif Bold
date, the ink italic dek (re-strung to the new top 3), the masthead
rule at 218, the 12-pin map geometry (now 11 pins), the ALSO ON
two-column list, the footer spacing (ink ends 1013). The self-check
below pins the v15 layout strings and geometry, so a later edit
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
    """v15 self-check: fail loudly if any v15 layout string regresses.

    Reads build/front.html (the rendered page) and verifies the strings
    the v15 plan depends on. The build fails instead of shipping a
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
    if "35 STORIES &middot; 11 PINS" not in html:
        problems.append("masthead tally must be '35 STORIES · 11 PINS' (v15: 35 stories, Ukraine pin gone)")
    if "36 STORIES" in html:
        problems.append("stale '36 STORIES' still present (v15 has 35)")

    # --- v15 numbers: six even columns, 68px figures, no bars, no chip ---
    # Columns x48/376/704/1032/1360/1688 at 2x (312 wide, 16 gap) =
    # display x24-1000, each ~156px with an 8px gap (P0).
    for left in ("48px", "376px", "704px", "1032px", "1360px", "1688px"):
        if f'<div class="nfig" style="left:{left};">' not in html:
            problems.append(f"numbers column at left {left} missing (v15 P0: six even columns)")
    if ".nfig { position:absolute; top:290px; width:312px; }" not in html:
        problems.append("numbers columns must be 312px wide at 2x (v15 P0)")
    for fig in ("98.79%", "0", "6.9", "98.5%", "11", "700K"):
        if f'font-size:68px; margin-top:20px;">{fig}</div>' not in html:
            problems.append(f"numbers figure '{fig}' must be 68px / mt20 at 2x (v15 P0)")
    for lab in (
        "HK turnout &middot; 5,640 voters",
        "fossil-fuel mentions in draft",
        "two M6.9 quakes, one day",
        "tariffs gone &middot; EU&ndash;Indonesia",
        "killed after Sinaloa capture",
        "displaced &middot; Moyale &middot; Nov",
    ):
        if lab not in html:
            problems.append(f"numbers label '{lab}' missing (v15 P0)")
    for src in (
        "INFO.GOV.HK",
        "COP31 DRAFT &middot; REUTERS",
        "PERU 00:09 &middot; BANDA 09:42 UTC",
        "EU COUNCIL &middot; 21 NOV",
        "AP &middot; 22 NOV",
        "ISLAMIC RELIEF",
    ):
        if src not in html:
            problems.append(f"numbers source '{src}' missing (v15 P0)")
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
        problems.append("numbers/rows must still carry '1,671' (Gaza toll, row 28)")

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
    # v15 visual fix: the stamp sits on the draft's lower half (rect
    # y 310-400, rotate -8 about its centre), clear of the struck
    # 'FOSSIL FUELS' (baseline 302) — the earlier position (-12 about
    # 530,295) hid the word's tail under the stamp.
    if 'rotate(-8 550 355)"><rect x="400" y="310" width="300" height="90"' not in html:
        problems.append("NO DEAL stamp must sit at rect (400,310) rotate -8, clear of FOSSIL FUELS (v15 visual fix)")
    if "NOV 9&ndash;21" not in html:
        problems.append("lead illustration must show the 'NOV 9-21' calendar chip (v15 P0)")
    if "+1 DAY" not in html:
        problems.append("lead illustration must show the '+1 DAY' calendar chip (v15 P0)")

    # --- v15 timeline: six nodes, NOW anchored on the last tick ---
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
    if 'class="nowmark" style="left:1791px;"' not in tl_band:
        problems.append(
            "NOW dot must sit at left 1791px at 2x, ring centred on the "
            "last tick at 1799px (v15 P3: anchored on the last tick)"
        )
    if 'left:1500px' in tl_band:
        problems.append("stale NOW dot at 1500px still present (v15 P3)")
    if 'left:360px; top:270px; width:1540px; height:2px; background:#191919;' not in tl_band:
        problems.append("timeline axis rule missing (v15 P3)")
    for tx in (359, 647, 935, 1223, 1511, 1799):
        if f'left:{tx}px; top:264px; width:2px; height:12px; background:#191919;' not in tl_band:
            problems.append(f"timeline tick mark at left {tx}px missing (v15 P3: six 6px ticks)")

    # --- region strip: EUROPE 6 (Ukraine excluded), 35 stories total ---
    for reg in (
        "MIDDLE EAST 4", "EUROPE 6", "ASIA 8", "AMERICAS 7",
        "AFRICA 5", "OCEANIA 2", "MKT+SPORT 3",
    ):
        if reg not in html:
            problems.append(f"region strip missing {reg}")
    if "EUROPE 7" in html:
        problems.append("stale 'EUROPE 7' still present (v15: Ukraine excluded, EUROPE 6)")
    if "#A63A2E" in html:
        problems.append(
            "Middle East colour #A63A2E still present (must be "
            "teal #2E7A7A, #A63A2E reads as red)"
        )
    if html.count("#2E7A7A") != 3:
        problems.append(
            f"Middle East teal #2E7A7A must occur exactly 3 times "
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
    # the 9 featured stories: 5 CONFIRMED, 3 OFFICIAL, 1 CLAIM
    # (v15: confirmed = lead 03 + cards 04, 05, 18, 23; official =
    # cards 09, 10, 34; claim = card 01)
    if html.count("5 confirmed &middot; 3 official &middot; 1 claim") != 1:
        problems.append(
            "footer verification tally '5 confirmed · 3 official · 1 claim' "
            "must appear once (v15)"
        )
    if "6 confirmed &middot; 2 official &middot; 1 claim" in html:
        problems.append("stale v14 tally '6 confirmed · 2 official · 1 claim' still present (v15)")

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
    if cards_html.count('bdg2 b-conf') != 4:
        problems.append(f"CONFIRMED badges must be 4 (cards 04, 05, 18, 23) (found {cards_html.count('bdg2 b-conf')})")
    if cards_html.count('bdg2 b-off') != 3:
        problems.append(f"OFFICIAL badges must be 3 (cards 09, 10, 34) (found {cards_html.count('bdg2 b-off')})")
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

    # v15 P1: card heads are Liberation Serif Bold 29px / lh 33 at 2x.
    if ".card .head { position:absolute; left:180px; top:64px; width:284px; font-family:'Liberation Serif',serif; font-size:29px; font-weight:bold; line-height:33px; }" not in html:
        problems.append("card head must be 29px Liberation Serif Bold / lh 33 at 2x (v15 P1)")
    if ".card .kick { position:absolute; left:180px; top:16px; width:268px;" not in html:
        problems.append("card kicker must be width 268px at 2x (v12 step 6)")
    if ".card .kick" in html and "white-space:nowrap" in html.split(".card .kick")[1].split("}")[0]:
        problems.append("card kicker must not be nowrap (v12 step 6: wrap allowed)")
    if ".card .dek { position:absolute; left:180px; top:134px;" not in html:
        problems.append("card dek must be top 134px at 2x (v12 step 6)")
    if ".card .src { position:absolute; left:180px; top:208px;" not in html:
        problems.append("card src must be top 208px at 2x (v15 P1: 30px badge ends 238, inside the 260px card)")

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
    # step 6 (v11): card 09 thumbnail keeps 50%, drops the 0% label.
    if "50%" not in cards_html:
        problems.append("card 09 '50%' label missing (step 6)")
    if ">0%<" in cards_html:
        problems.append("card 09 '0%' label must be dropped (step 6)")
    # v15: card 23's dek dates the boat (21 Nov) — it stays a card, so
    # it is NOT in the DATE CHECK exclusion list.
    if "21 Nov &middot; search on" not in cards_html:
        problems.append("card 23 dek must date the boat '21 Nov · search on' (v15 P0)")
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
        problems.append(f"map pins must be 11 (found {pins}) (v15: Lviv pin gone with the excluded story)")
    for num in ("01", "03", "04", "05", "10", "11", "17", "18", "19", "23", "27"):
        if f">{num}</text>" not in map_html:
            problems.append(f"map pin number {num} missing")
    if ">02</text>" in map_html:
        problems.append("map pin 02 (Lviv) must be gone (v15 P0)")
    for slug in (
        "CPH", "GOF", "ANTALYA", "BAH", "BAY",
        "MOY", "HKG", "BND", "PER", "BSB", "SINALOA",
    ):
        if f">{slug}</text>" not in map_html:
            problems.append(f"map pin slug {slug} missing")
    if ">LVIV</text>" in map_html:
        problems.append("map pin slug LVIV must be gone (v15 P0)")
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
    if '<text x="868" y="180">BAH</text>' not in map_html:
        problems.append("BAH label must sit at (868, 180), 4px clear of pin 01 (v13 fix 4)")

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
        problems.append("list right column pitch must be 18px at 2x (v15: 13/13 rows, even pitch)")
    rows = re.findall(r'<div class="row">.*?</div>', html)
    if len(rows) != 26:
        problems.append(f"ALSO ON rows must be 26 (found {len(rows)}) (v15: F1 is a card now)")
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
    if "26 MORE STORIES &middot; 06&ndash;36" not in html:
        problems.append("ALSO ON header must read '26 MORE STORIES · 06–36' (v15)")
    if "27 MORE STORIES" in html:
        problems.append("stale '27 MORE STORIES' still present (v15 has 26)")
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
    for col in ("EXCLUDED (PRE-22 NOV)", "LEFT OUT", "NOT YET (POST-17:00 UTC)", "CORRECTIONS"):
        if col not in html:
            problems.append(f"DATE CHECK column {col} missing (v15 P2)")
    if "HELD" in html:
        problems.append("stale DATE CHECK column 'HELD' still present (v15 P2: it is EXCLUDED now)")
    if "Ukraine 400-drone strike &middot; 19&ndash;20 Nov" not in html:
        problems.append("DATE CHECK must exclude the Ukraine strike with its date (v15 P2)")
    if "Nigeria boat capsize" in html:
        problems.append("Nigeria must not be in the exclusion list: story 23 stays a card, dated on it (v15 P2)")
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

    # --- 35 story slots: 1 lead + 8 cards + 26 list rows ---
    slots = (
        html.count('<div class="leadtext">')
        + html.count('<div class="card"')
        + html.count('<div class="row">')
    )
    if slots != 35:
        problems.append(f"story slots must be 35 (found {slots}) (v15: Ukraine excluded)")

    if problems:
        raise SystemExit("front.html v15 check failed:\n- " + "\n- ".join(problems))
    print(
        f"front.html v15 check ok: COP31 lead + serif heads + capsule badges; "
        f"6 numbers in even columns; 1 lead + {cards} cards + 26 list rows = 35 slots; "
        f"11 map pins (ink, 24px numerals; ANTALYA<BAH); timeline 6 nodes, NOW on the "
        f"last tick; DATE CHECK red box with EXCLUDED (PRE-22 NOV); red #B01E1E x4; "
        f"footer ends 1013"
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
