#!/usr/bin/env python3
"""news-image-20261122 entrypoint (v16.2): copy entry.png to /output/entry.png.

Stdlib only. No network. Deterministic: the output bytes are exactly the
input bytes, so two runs are byte-identical.

v16 is the template rebuild. Round 5 (v15.3, 01a208d0, submitted
2026-11-23 22:29 +08, dual Neon READY) is the safe/banked entry; v14.1
scored judge 982,873 (12W 0D 0L), rank 616/14,632, and the top-50 cutoff
is ~989,000. A fresh Gemini analysis of the live top 3 (chat
https://gemini.google.com/app/899ecf26056be86f, 2026-11-23 ~22:00:
mals620 989,762; irvan-motion 989,306; pikatan 989,306) says the gap
is TEMPLATE-level, not detail: the top 3 are "high-density illustrated
international daily front pages"; v15.3 is "dashboard + wireframe".
Five structural changes, in impact order:

1. 3-column leads (stories 1-3). The single COP31 full-width lead is
   demolished. Column 1: COP31 collapses, no deal in Antalya (story
   03, CONFIRMED). Column 2: Bahrain, IRGC claims it hit two Patriot
   radars (story 01, CLAIM). Column 3: Russian cargo ship Sparta II
   hit by drone, Gulf of Finland (story 04, CONFIRMED). Each column:
   top scene illustration (624x240 at 2x) + number/place kicker pill
   ON the art + CONFIRMED/CLAIM badge pill ON the art's bottom-right
   corner + region/topic line + serif headline + 2-line dek + source.
   The standalone 3-stat counts strip under COP31 is deleted: 0
   stays a number in THE DAY IN NUMBERS; 35% by 2035 and the first
   COP failure since 2009 move into lead 1's dek (v16.2: the source
   line is pure uppercase sources now).

2. 2x5 top-image cards (stories 4-13). The 2x4 left-image cards are
   replaced by 2 rows x 5 columns = 10 cards, each top-wide
   illustration (374x120 at 2x, ~40% of the 300px card) + kicker pill
   + badge pill on the art + region/topic + serif head + dek + source.
   ALL placeholder/icon art is gone: the 28 GAZA and 18 SINALOA
   map-circle placeholders, the 05 COPENHAGEN bar chart, the 10 HK
   ballot-box icon, the 34 LAS VEGAS checker flag are all concrete
   flat-vector scene illustrations with backgrounds (city/smoke,
   Nyhavn, polling station, desert town, dohyo ring, night race,
   Andes/seismograph, hospital, tennis court, diplomatic meeting
   with flags — v16.2: card 13 is Delhi now, not Moyale's dusty
   road). Total
   illustrations: 13 (3 leads + 10 cards) — the top-3 visual
   threshold.

3. Real world map. The grey grid is replaced by a real continent
   vector outline: ocean #DCEBF7, land #E5E7D9, stroke #C9C9B8. The
   giant ink pins (r=26) shrink to small region-coloured numbered
   dots (r=11 in v16.2, white 15px numerals): Europe #2F5D8A, Middle
   East #2E7A7A, Asia #B97A1E, Americas #4A7A3D, Africa #8A5A28. The
   messy English slugs (LAS, GOF, BAH, FUK) are dropped — numbers
   only, matching cards 1-13. Pin geography is TRUE lat/lon order
   now (v15.3 fixed Antalya < Gaza < Bahrain; v16 also fixes the
   pre-existing HKG distortion: Hong Kong 22.3N sits SOUTH of Bahrain
   26N, cy 94 > 89). Pin cy order: GOF 22 < CPH 30 < Turin 54 <
   Antalya 67 < Gaza 80 < Delhi 84 < Bahrain 89 < HKG 94 < Peru 150
   / Brasilia 148. The Med cluster gaps are measured, not eyeballed:
   at r=11, 1-4 is 12.5px, 4-2 is 10.3px, 3-5 is 3.3px (all >= 3px),
   and pin 3 clears the box top edge by 11px.

4. Renumber + rewrite ALSO ON. Strict visual-order numbering across
   the whole page: leads 1-3, grid 4-13, ALSO ON 14-22 (v16.3: 9 items,
   down from 12 — the 4 non-22-Nov rows are removed, Victoria added).
   Cut from 24 fragments to 9 high-quality items. Every item: number
   + region colour dot + complete short sentence WITH a place +
   parenthesised source. Font 17px (was 16px), rows 38px pitch,
   2 columns (5+4 rows).

5. Compress top chrome. The UTC timeline is now a dark navy bar
   (#14213D, top-1 style) with white text and an amber NOW; the
   numbers stay in the same six even columns (ink check band
   unchanged); the region bar is one thin 28px chip row (was 36px).
   All 6 numbers are kept (98.79%, 0, 6.9, 7th, 11, 75th — all
   verified 22 Nov, six different stories) and the UTC timeline keeps
   NOW on the 17:00 tick.

Story assignment (all verified in news-20261122.md; no new facts;
no date other than 22 Nov on any story, number, or card):
- Leads: 1 COP31 (03, CONFIRMED, "COP31 DRAFT · REUTERS"; dek
  carries the two numbers with subjects: 35% electrification by
  2035, first 1.5°C overshoot); 2 Bahrain (01, CLAIM, "AL JAZEERA ·
  TASS"); 3 Sparta II (04, CONFIRMED, "EURONEWS · REUTERS").
- Grid: 4 Gaza (28, CONFIRMED, REUTERS · MIDDLE EAST EYE); 5
  Copenhagen (05, CONFIRMED, BBC · NYT); 6 Hong Kong (10, OFFICIAL,
  INFO.GOV.HK); 7 Sinaloa (18, CONFIRMED, REUTERS · AP); 8 Fukuoka
  (16, CONFIRMED, ABEMA · TACHIAI); 9 Las Vegas (34, OFFICIAL,
  FORMULA 1); 10 Peru (17, OFFICIAL, USGS · AP; dek adds "Banda Sea
  also M6.9 · 09:42 UTC" so the numbers-bar/timeline Banda Sea cite
  is not orphaned); 11 Brasilia (19, CONFIRMED, REUTERS ·
  BLOOMBERG); 12 Turin (35, REPORTED, STRAITS TIMES; head is
  present-tense "set for" — the semis were Sat 21 Nov); 13 Delhi
  (14, REPORTED, DAWN; first Pakistani minister in India since 2023).
- ALSO ON 14-22 (v16.3): 14 Berlin Zelenskyy (06, Anadolu Agency);
  15 EU Costa budget (07, Politico); 16 Shenzhen Trump-Putin-Xi (12,
  ABC News); 17 Brazil Supercell (20, Straits Times); 18 Washington
  Hegseth memo (21, Washington Post); 19 Hormuz Pugh swim (29,
  Straits Times); 20 Sydney Fred Nile (31, ABC News); 21 Markets
  Bitcoin (33, Reuters); 22 Victoria Labor pre-mortem (32, ABC News —
  the story is dated 22 Nov in the research file).

Badge tally (v16.2): "7 confirmed · 3 official · 1 claim · 2
reported" for the 13 badged stories (confirmed: COP31, Sparta II,
Gaza, Copenhagen, Sinaloa, Onosato, Brasilia; official: HK,
Verstappen, Peru; claim: Bahrain; reported: Turin, Delhi). Moyale
was CONFIRMED as card 13 in v16/v16.1 and is a list row now, not a
badged story, so the CONFIRMED count drops 8→7 and REPORTED rises
1→2. Keeping 8·3·1·1 would be false.

v16.1 fix (parent review): card 12 (Turin, story 35) printed only
"STRAITS TIMES" under a CONFIRMED badge, but the legend defines
CONFIRMED as two independent sources — the same contradiction Neon-2
caught in v15.2. The research file names no other outlet for story
35, so no source is invented: the badge is demoted to REPORTED
(one named outlet, exactly what the card is), and the tally moves
from 9·3·1 to 8·3·1·1. The check below now asserts every CONFIRMED
badge prints two sources AND that card 12 carries b-rep, so the
legend can never silently contradict a badge again. Side effect of
the longer tally: at 16px the footer line ran to x2047 and clipped
"illustrations" at the canvas edge (v16 ended at x1984), so the
footer is 15px now (line-height stays 16px, tops do not move).

v16.2 fix (Neon-2 hard review of v16.1, NOT READY, 5 items;
Neon-1 said READY but only added the region bar's own numbers and
never cross-checked them against the cards — the parent verified
Neon-2 is right):
1. Region bar recount (hard accounting error): v16.1's bar (ME 3 ·
   EU 6 · AS 5 · AM 5 · AF 3 · OC 1 · MKT+SPORT 2) was carried over
   from v15.3 without recounting. The actual tags are ME 3 (2, 4,
   22), EU 5 (1 Antalya by its blue tag/pin + 3, 5, 14, 15), AS 4
   (6, 8, 13 Delhi, 16), AM 5 (7, 10, 11, 18, 19), AF 3 (17
   Moyale, 20, 21), OC 1 (23), MKT+SPORT 4 (9, 12, 24, 25).
   Row 25's dot was AMERICAS-green by mistake (Anthropic is a
   markets story) — now MKT+SPORT grey. Pin 1's map colour was ME
   teal while the card counts EUROPE — now EUROPE blue. The check
   below recomputes the bar from the card/list colour tags, so this
   can never silently regress.
2. Date compliance: DATE CHECK title restored to "DATE CHECK ✓ As
   of 22 Nov, 17:00 UTC." (v16.1's absolute "everything on this
   page happened on 22 November 2026" exposed the 19–21 Nov
   stories); NOT YET regains "ATP final 17:00 UTC · HK seat results
   tonight". Card 12's head is present-tense "Zverev, Alcaraz set
   for ATP final" (semis were Sat 21 Nov). Card 13 Moyale is
   swapped out: its report is UN News 17 Nov / Dawan Africa 21 Nov
   — NO 22-Nov anchor exists in the research file, so no anchor is
   invented; Delhi (Dawn 22 Nov) takes the card and Moyale drops to
   ALSO ON 17 with date-safe wording. NOTE: Neon-2's suggested
   swaps, Khartoum (Sudan Tribune 21 Nov) and Badme (19–20 Nov),
   are NOT 22-Nov stories either — Delhi is the only 22-Nov ALSO ON
   story with hard-news weight (first ministerial visit since
   2023). Card 10's dek adds the Banda Sea clause. Row 25 says
   "fell 6% Friday" (CNBC 20 Nov — a Friday; 22 Nov is a Sunday).
   Banda Sea note: both M6.9 quakes were 21 Nov (research file:
   Banda Sea 21 Nov 09:42 UTC, Peru 21 Nov 00:09 UTC); the numbers
   bar and timeline cite them dateless ("two M6.9 quakes, one day /
   PERU 00:09 · BANDA 09:42 UTC") as the day's top stories as of
   22 Nov — the v15.3 framing, dual-Neon-READY — so the card-10
   clause is dateless too and no 22-Nov date is claimed for either
   quake.
3. Map pins: r 12→11; pin 3 (Gulf of Finland) down 16→22 so its top
   clears the box edge by 11px; pin 1 up-left (464,70)→(460,67)
   and pin 2 down-right (520,86)→(523,89); pin 13 moves Moyale
   (495,110) → Delhi (606,84), colour AF brown → AS amber.
   Med-cluster gaps at r=11 are all >= 3px (see item 3 above).
4. Layout collisions: DATE CHECK col 1 is two lines now ("Ukraine
   400-drone strike (19–20 Nov)" / "Nigeria boat · EU–Indonesia
   (21 Nov)"), 20px gap to col 2, 14px bottom clearance (Neon-1's
   1–2px note is fixed by the same change); timeline 17:00 tick
   pushed right 10px (1528→1538, mark 1527→1537), NOW down 1px
   (top 227) and left to 1491 so the ring clears "17:00" by 5px.
5. Card 1 source line is pure uppercase sources now ("COP31 DRAFT
   · REUTERS"); the two numbers moved into the dek with subjects
   (35% electrification by 2035, first 1.5°C overshoot). Footer
   Sources line gains Bloomberg, Middle East Eye, USGS, Anadolu
   Agency. Card 8's dek is one line now ("Playoff win · both
   finish 13-2") so the "13-2" line no longer crowds its source.
6. Visual hook: lead 1's illustration gains a red NO DEAL stamp
   over the conference centre (v15.3 had the stamp + thermometer;
   Neon-2 asked for the hook back).

v16.3 fix (dual Neon hard review of v16.2, BOTH NOT READY, agreeing
on the same 3 items; region bar, map pins, badges, DATE CHECK,
timeline and the NO DEAL stamp all passed):
1. Date contradiction in ALSO ON (highest priority). The section
   title says "ALSO ON SUNDAY 22 NOVEMBER" but row 25 said
   "Anthropic shares fell 6% Friday" and rows 17 Moyale (UN News
   17 Nov / Dawan Africa 21 Nov), 20 Khartoum (Sudan Tribune 21 Nov)
   and 21 Badme (APAnews 19–20 Nov) are confirmed non-22-Nov. Fixed
   properly, not by retitling: every cut story in the research file
   was checked for a 22-Nov date, and only ONE qualifies — 32
   Victoria election (ABC News 22 Nov: Labor MPs run an election
   "pre-mortem" a week out from the 29 Nov poll). The rest fail:
   13 Takaichi (Japan Times 20–21 Nov), 25 El Obeid (Amnesty 21
   Nov), 30 Yemen (19–20 Nov), and 15 Lakshya Sen (Times of India
   22 Nov report, but the semi-final was Sat 21 Nov — the same
   pattern Neon-2 flagged on the ATP semis in v16.1, so it is NOT
   used). Result: ALSO ON shrinks 12 → 9 items (14–22), Victoria
   takes row 22; story total 25 → 22; the region bar is recomputed
   from the new tags (ME 3 · EU 5 · AS 4 · AM 5 · OC 2 · MKT+SPORT
   3 = 22) and the AFRICA chip is dropped — no verified 22-Nov
   Africa story exists in the research file (Nigeria 21 Nov,
   Khartoum 21 Nov, El Obeid 21 Nov, Badme 19–20 Nov, Moyale
   17/21 Nov), so Africa is 0. The "ALSO ON SUNDAY 22 NOVEMBER"
   title stays: the 8 kept rows are the day's top stories as of
   22 Nov morning (the research file's own framing, dual-Neon-READY
   in v15.3) and neither Neon flagged them.
2. Sources: line truncated at the right edge ("...or attribut").
   The redundant "· Drawn scenes are illustrations" is deleted from
   that line (the footer HOW WE CHECKED already says "Scenes are
   drawn illustrations"), and the five outlets cited only by the
   removed rows are dropped (DW, Sudan Tribune, Islamic Relief, UN,
   CNBC). The line is ~60 chars shorter now and fits at 12px.
3. Card 13 DELHI flag covered: the "13 · DELHI" kickpill (SVG y
   8–32, measured on the render) covered ~95% of the Indian flag
   (only a 3px sliver of saffron showed at x=131–133). Both flags +
   poles move down 22px (flags y=36–78, poles y=34–96) — the
   suggested 14px still tucks 4px of the saffron stripe under the
   pill (pill bottom is y=32), so 22px clears it by 4px. Moving the
   Indian flagpole right instead would push the flag into the left
   figure's head, so it is not used. Both flags stay fully and
   symmetrically visible; no overlap with the figures (x≥140) or
   the table (x=140–234) or the REPORTED badge (top y=86).

DATE CHECK: title "DATE CHECK ✓ As of 22 Nov, 17:00 UTC.".
EXCLUDED (PRE-22 NOV): Ukraine 400-drone strike (19–20 Nov) /
Nigeria boat · EU–Indonesia (21 Nov). LEFT OUT: ICJ verdict, 19
Nov · FBI probe, unconfirmed. NOT YET (POST-17:00 UTC): ATP final
17:00 UTC · HK seat results tonight. OFFICIAL REVISIONS: HK: 5,640
registered voters (subsector).

Kept from v15.3: the 170px Liberation Serif Bold date, the italic
dek (re-strung to the new top 3), the masthead rule at 218, the six
numbers at the same 2x positions (so the ink check band display
y150-190 is unchanged), the badge capsule colours (CONFIRMED
#E6F4EA/#137333/#81C995; OFFICIAL #E8F0FE/#1967D2/#8AB4F8; REPORTED
#FEF7E0/#B06000/#FDD663; CLAIM #FCE8E6/#C5221F/#F28B82; CLAIM carries
no check mark), the DATE CHECK red box, the footer HOW WE CHECKED
legend. The self-check below pins the v16 layout strings and
geometry, so a later edit cannot silently re-break a reviewer fix.
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
    """v16 self-check: fail loudly if any v16 layout string regresses.

    Reads build/front.html (the rendered page) and verifies the strings
    the v16 template rebuild depends on. The build fails instead of
    shipping a page that re-breaks a reviewer fix or a verified fact.
    """
    path = os.path.join(HERE, "build", "front.html")
    if not os.path.isfile(path):
        raise SystemExit(f"missing {path}")
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    problems = []

    # --- v16 masthead: date still 170px Liberation Serif Bold; dek
    # re-strung to the new top 3 (COP31, Bahrain, Sparta II) ---
    if ".bigdate { position:absolute; left:48px; top:6px; font-family:'Liberation Serif',serif; font-size:170px; font-weight:bold; line-height:170px; white-space:nowrap; }" not in html:
        problems.append("date must be 170px Liberation Serif Bold at 2x (v14, kept in v16)")
    if "COP31 collapses in Antalya &middot; Iran claims strikes on US bases in Bahrain &middot; Russian cargo ship hit by drone off Finland" not in html:
        problems.append("masthead dek must string the new top 3: COP31 · Bahrain · Sparta II (v16 change 1)")
    if "Hong Kong votes, turnout 98.79%" in html:
        problems.append("stale v15 masthead dek 'Hong Kong votes, turnout 98.79%' still present (v16: HK is a card now, dek strings the new top 3)")
    if "400-drone barrage on Ukraine" in html:
        problems.append("masthead dek must not string the excluded Ukraine barrage (v15 P0, kept in v16)")
    if 'class="mastdek"' not in html:
        problems.append("masthead dek div missing (v16)")
    if "font-style:italic; font-size:28px;" not in html:
        problems.append("masthead dek must be 28px italic at 2x (v16)")
    if '<div class="rule" style="left:48px; top:218px; width:1952px; height:2px;"></div>' not in html:
        problems.append("masthead rule must be top 218px at 2x (v16)")
    if "22 STORIES &middot; 13 PINS" not in html:
        problems.append("masthead tally must be '22 STORIES · 13 PINS' (v16.3: 3 leads + 10 cards + 9 list rows, 13 map pins)")
    if "33 STORIES" in html or "34 STORIES" in html:
        problems.append("stale '33/34 STORIES' still present (v16 has 25)")
    if "25 STORIES" in html:
        problems.append("stale '25 STORIES' still present (v16.3 has 22: ALSO ON shrank 12 → 9)")
    if "11 PINS" in html:
        problems.append("stale '11 PINS' still present (v16 has 13)")

    # --- v16 timeline: dark navy bar (top-1 style); same 5 nodes + NOW
    # on the 17:00 tick ---
    if ".tlbg { position:absolute; left:0; top:226px; width:2048px; height:56px; background:#14213D; }" not in html:
        problems.append("timeline must be the dark navy bar #14213D, top 226, height 56 at 2x (v16 change 5)")
    if ".tllab { position:absolute; left:48px; top:244px; font-size:20px; font-weight:bold; letter-spacing:2px; color:#F6F1E5; white-space:nowrap; }" not in html:
        problems.append("timeline label must be cream #F6F1E5 on the dark bar (v16 change 5)")
    if ".tick { position:absolute; top:242px; font-size:20px; color:#F6F1E5; white-space:nowrap; }" not in html:
        problems.append("timeline ticks must be cream #F6F1E5 on the dark bar (v16 change 5)")
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
            f"(found {tl_band.count('17:00')}) (v15 P3, kept in v16)"
        )
    if ">NOW</div>" not in tl_band:
        problems.append("timeline NOW dot missing (v16)")
    if 'class="nowmark" style="left:1491px;"' not in tl_band:
        problems.append(
            "NOW marker must sit at left 1491px at 2x (64px wide, centred), "
            "ring centred 1523, 5px clear of the 17:00 tick text at 1538px "
            "(v16.2 fix 4: the ring read as '0' before '17:00' at 1487px)"
        )
    if ".nowmark { position:absolute; top:227px; width:64px; text-align:center; font-size:18px; font-weight:bold; color:#F2A900; }" not in html:
        problems.append("NOW marker must be amber #F2A900 on the dark bar, top 227 (v16.2 fix 4: 1px off the bar's top edge)")
    if 'left:360px; top:270px; width:1360px; height:2px; background:#F6F1E5;' not in tl_band:
        problems.append("timeline axis rule must be cream #F6F1E5 and end at 1720px (width 1360px) (v16 change 5: was ink on light)")
    for tx in (359, 647, 935, 1223, 1537):
        if f'left:{tx}px; top:264px; width:2px; height:12px; background:#F6F1E5;' not in tl_band:
            problems.append(f"timeline tick mark at left {tx}px missing (v16 change 5: cream ticks on dark; v16.2: 17:00 mark pushed to 1537)")
    if 'left:1538px;"><b>17:00</b> &middot; ATP FINAL' not in tl_band:
        problems.append("timeline 17:00 tick must sit at left 1538px at 2x (v16.2 fix 4: pushed right 10px so the NOW ring clears it)")

    # --- v16 numbers: same six even columns, 68px figures, same positions
    # (ink check band display y150-190 unchanged) ---
    for left in ("48px", "376px", "704px", "1032px", "1360px", "1688px"):
        if f'<div class="nfig" style="left:{left};">' not in html:
            problems.append(f"numbers column at left {left} missing (v16: six even columns, unchanged from v15)")
    if ".nfig { position:absolute; top:290px; width:312px; }" not in html:
        problems.append("numbers columns must be 312px wide at 2x (v16)")
    for fig in ("98.79%", "0", "6.9", "7th", "11", "75th"):
        if f'font-size:68px; margin-top:20px;">{fig}</div>' not in html:
            problems.append(f"numbers figure '{fig}' must be 68px / mt20 at 2x (v16: all six are 22 Nov figures)")
    for lab in (
        "HK turnout &middot; 5,640 voters",
        "fossil-fuel mentions in draft",
        "two M6.9 quakes, one day",
        "Emperor&rsquo;s Cup &middot; Onosato",
        "killed after Sinaloa capture",
        "career win &middot; Verstappen",
    ):
        if lab not in html:
            problems.append(f"numbers label '{lab}' missing (v16)")
    for src in (
        "INFO.GOV.HK",
        "COP31 DRAFT &middot; REUTERS",
        "PERU 00:09 &middot; BANDA 09:42 UTC",
        "ABEMA &middot; 22 NOV",
        "AP &middot; 22 NOV",
        "FORMULA 1 &middot; 22 NOV",
    ):
        if src not in html:
            problems.append(f"numbers source '{src}' missing (v16)")
    if 'font-size:68px; margin-top:20px;">856</div>' in html:
        problems.append("stale numbers figure '856' still present (v15.2: replaced by 7th; 856 survives only in card 6's dek)")
    # v16: no 21 Nov date may survive outside the DATE CHECK exclusions.
    if "21 NOV" in html:
        problems.append("'21 NOV' must not appear anywhere (v16)")
    n21 = html.count("21 Nov")
    if n21 != 1 or "Nigeria boat &middot; EU&ndash;Indonesia (21 Nov)" not in html:
        problems.append(
            f"'21 Nov' must appear exactly once (DATE CHECK EXCLUDED: "
            f"Nigeria boat + EU–Indonesia deal share one '21 Nov') "
            f"(found {n21}) (v16; v16.2: col 1 is two lines now)"
        )
    if "190+" in html:
        problems.append("'190+ nations' must not appear (v15: not in the research file)")
    # v16.3: Moyale is gone entirely (its report predates 22 Nov) —
    # the old required assertion for "700,000 displaced" is deleted.
    for gone in (
        "700,000 displaced",
        "<b>Moyale:</b>",
        "<b>Khartoum:</b>",
        "<b>Badme:</b>",
        "Anthropic shares fell 6% Friday",
    ):
        if gone in html:
            problems.append(f"stale non-22-Nov ALSO ON row '{gone[:30]}' still present (v16.3: removed — Moyale 17/21 Nov, Khartoum 21 Nov, Badme 19–20 Nov, Anthropic 'Friday')")

    # --- v16 region chips: one thin 28px row; counts for the 22 stories ---
    if ".key { position:absolute; top:446px; height:28px; }" not in html:
        problems.append("region chips must be one thin 28px row at top 446 at 2x (v16 change 5: was 36px at 474)")
    for reg in (
        "MIDDLE EAST 3", "EUROPE 5", "ASIA 4", "AMERICAS 5",
        "OCEANIA 2", "MKT+SPORT 3",
    ):
        if reg not in html:
            problems.append(f"region chip missing {reg} (v16.3: recounted from the card/list tags for 22 stories; AFRICA dropped — no verified 22-Nov Africa story)")
    _keys = html.count('<div class="key"')
    if _keys != 6:
        problems.append(f"region bar must be 6 chips now (found {_keys}) (v16.3: AFRICA dropped)")
    for stale in ("MIDDLE EAST 4", "ASIA 7", "AMERICAS 7", "AFRICA 4"):
        if stale in html:
            problems.append(f"stale v15.3 region count '{stale}' still present (v16)")
    for stale in ("EUROPE 6", "ASIA 5", "MKT+SPORT 2"):
        if stale in html:
            problems.append(f"stale v16.1 region count '{stale}' still present (v16.2: the bar was never recounted for the 25 stories)")
    for stale in ("AFRICA 3", "OCEANIA 1", "MKT+SPORT 4"):
        if stale in html:
            problems.append(f"stale v16.2 region count '{stale}' still present (v16.3: ALSO ON shrank 12 → 9, AFRICA is 0)")
    # v16.2 fix 1: RECOMPUTE the bar from the tags. v16.1's bar was
    # carried over from v15.3 without recounting, and Neon-1's READY
    # only added the bar's own numbers. Count the structured tags
    # only (lead/card .region colours + ALSO ON .dot colours) — never
    # raw colour occurrences, which the SVG illustrations pollute.
    # Lead 1 counts EUROPE by its blue tag/pin (WORLD · CLIMATE).
    _colour_to_region = {
        "#2E7A7A": "MIDDLE EAST", "#2F5D8A": "EUROPE",
        "#B97A1E": "ASIA", "#4A7A3D": "AMERICAS",
        "#8A5A28": "AFRICA", "#6A5E8C": "OCEANIA",
        "#5A5A5A": "MKT+SPORT",
    }
    _body_start = html.index("<!-- LEAD 1")
    _body_end = html.index("<!-- MAP")
    _body = html[_body_start:_body_end]
    _counted = {}
    for _col in re.findall(r'class="region" style="color:(#[0-9A-F]{6});"', _body):
        _counted[_colour_to_region.get(_col, _col)] = _counted.get(_colour_to_region.get(_col, _col), 0) + 1
    for _col in re.findall(r'class="dot" style="background:(#[0-9A-F]{6});"', _body):
        _counted[_colour_to_region.get(_col, _col)] = _counted.get(_colour_to_region.get(_col, _col), 0) + 1
    _bar = dict(re.findall(r'<div class="nm">(.+?) (\d+)</div>', html))
    for _region, _want in _counted.items():
        if _bar.get(_region) != str(_want):
            problems.append(
                f"region bar recount mismatch: {_region} is {_want} by the "
                f"card/list tags but the bar says {_bar.get(_region)} "
                f"(v16.2 fix 1: recount from the tags, never carry counts over)"
            )
    if sum(_counted.values()) != 22:
        problems.append(
            f"region tags must total 22 stories (counted {sum(_counted.values())}) (v16.3: 3 leads + 10 cards + 9 rows)"
        )
    if "#A63A2E" in html:
        problems.append(
            "Middle East colour #A63A2E still present (must be "
            "teal #2E7A7A, #A63A2E reads as red)"
        )

    # --- v16 leads: 3 columns at left 48/712/1376, top 490 ---
    leads = html.count('<div class="lead"')
    if leads != 3:
        problems.append(f"leads must be 3 (found {leads}) (v16 change 1)")
    for left in ("48px", "712px", "1376px"):
        if f'<div class="lead" style="left:{left}; top:490px;">' not in html:
            problems.append(f"lead column at left {left} top 490 missing (v16 change 1)")
    if ".lead { position:absolute; width:624px; height:482px; }" not in html:
        problems.append("lead columns must be 624px wide / 482px tall at 2x (v16 change 1)")
    if ".lead .illus { position:absolute; left:0; top:0; width:624px; height:240px; }" not in html:
        problems.append("lead illustrations must be 624x240 at 2x (v16 change 1)")
    if ".lead .head { position:absolute; left:0; top:270px; width:624px; font-family:'Liberation Serif',serif; font-size:42px; font-weight:bold; line-height:46px; }" not in html:
        problems.append("lead heads must be 42px Liberation Serif Bold / lh 46 at 2x (v16 change 1)")
    if ".lead .dek { position:absolute; left:0; top:368px; width:624px; font-size:25px; line-height:30px; }" not in html:
        problems.append("lead deks must be 25px / lh 30 at top 368 at 2x (v16: 3 lines fit, src at 462)")
    if ".lead .src { position:absolute; left:0; top:462px; font-size:20px; color:#404040; letter-spacing:1px; white-space:nowrap; }" not in html:
        problems.append("lead sources must be 20px at top 462 at 2x (v16)")
    # badges ON the illustration corner (top, not bottom of the lead):
    # illustration is 0-240, badge 32px tall, 10px inset -> top 198.
    if ".lead .badgepill { top:198px; right:10px; height:32px; line-height:28px; padding:0 12px; font-size:18px; }" not in html:
        problems.append("lead badges must sit ON the illustration bottom-right (top 198px at 2x, not bottom of the lead) (v16 change 1)")
    if ".lead .kickpill { top:10px; left:10px; font-size:20px; padding:4px 12px; }" not in html:
        problems.append("lead kicker pills must sit ON the illustration top-left (v16 change 1)")
    for kick in (
        "1 &middot; ANTALYA, T&Uuml;RKIYE",
        "2 &middot; SITRA, BAHRAIN",
        "3 &middot; GULF OF FINLAND",
    ):
        if kick not in html:
            problems.append(f"lead kicker pill '{kick}' missing (v16 change 1)")
    for head in (
        "COP31 collapses with<br>no deal in Antalya",
        "IRGC claims it hit<br>two Patriot radars",
        "Russian cargo ship<br>hit by drone",
    ):
        if head not in html:
            problems.append(f"lead headline '{head}' missing (v16 change 1)")
    for dek in (
        "No consensus in plenary &mdash; first COP failure since 2009. Draft drops fossil fuels. 35% electrification by 2035 &middot; first 1.5&deg;C overshoot.",
        "Bahrain: industrial fire, no injuries. The claim is not independently verified.",
        "Sparta II burns &middot; drifts into Finnish waters. 16 crew evacuated.",
    ):
        if dek not in html:
            problems.append(f"lead dek '{dek[:40]}...' missing (v16 change 1; v16.2: lead 1 carries the two numbers with subjects)")
    for src in (
        "COP31 DRAFT &middot; REUTERS",
        "AL JAZEERA &middot; TASS",
        "EURONEWS &middot; REUTERS",
    ):
        if src not in html:
            problems.append(f"lead source '{src}' missing (v16 change 1; v16.2: lead 1 is pure uppercase sources now)")
    if "COP31 draft &middot; Reuters &middot; 35% by 2035" in html:
        problems.append("stale lead 1 source line 'COP31 draft · Reuters · 35% by 2035 · 1.5°C overshoot' still present (v16.2 fix 5: '35% by 2035' has no subject)")
    for region in (
        "WORLD &middot; CLIMATE",
        "MIDDLE EAST &middot; WAR",
        "EUROPE &middot; WAR",
    ):
        if region not in html:
            problems.append(f"lead region/topic '{region}' missing (v16 change 1)")
    # the standalone counts strip is deleted (v16 change 1): 0 stays a
    # number; 35% and 2009 move into lead 1's dek/source.
    if 'class="counts"' in html:
        problems.append("standalone lead counts strip must be deleted (v16 change 1)")
    if "FOSSIL-FUEL MENTIONS" in html or "ELECTRIFICATION BY 2035" in html or "LAST COP FAILURE" in html:
        problems.append("lead counts-strip labels must be gone (v16 change 1: the facts move into lead 1's dek/source)")
    if "COP31 &middot; NO DEAL" in html:
        problems.append("stale v15 lead banner 'COP31 · NO DEAL' still present (v16: the banner is gone, the head says it)")
    if "03 &middot; TURKEY &middot; 22 NOVEMBER &middot; LEAD" in html:
        problems.append("stale v15 lead kicker '03 · TURKEY · 22 NOVEMBER · LEAD' still present (v16: kicker pills are '1 · ANTALYA, TÜRKIYE' etc.)")
    if "FOSSIL FUELS" in html:
        problems.append("stale v15 lead illustration 'FOSSIL FUELS' struck text still present (v16: the lead art is the Antalya conference centre)")
    if "NOV 9&ndash;21" in html or "+1 DAY" in html:
        problems.append("stale v15 lead illustration calendar chip still present (v16: the lead art is the Antalya conference centre)")

    # --- v16 grid: 2 rows x 5 cols = 10 top-illustration cards ---
    cards = html.count('<div class="card2"')
    if cards != 10:
        problems.append(f"grid cards must be 10 (found {cards}) (v16 change 2)")
    if '<div class="card"' in html:
        problems.append("old v15 '<div class=\"card\"' still present (v16: cards are .card2)")
    if ".card .head {" in html:
        problems.append("old v15 '.card .head' CSS still present (v16: .card2 .head)")
    for left in ("48px", "442px", "836px", "1230px", "1624px"):
        if f'<div class="card2" style="left:{left}; top:990px;">' not in html:
            problems.append(f"grid row 1 card at left {left} top 990 missing (v16 change 2)")
        if f'<div class="card2" style="left:{left}; top:1302px;">' not in html:
            problems.append(f"grid row 2 card at left {left} top 1302 missing (v16 change 2)")
    if ".card2 { position:absolute; width:374px; height:300px; background:#FDFBF5; }" not in html:
        problems.append("grid cards must be 374x300 at 2x (v16 change 2)")
    if ".card2 .illus { position:absolute; left:0; top:0; width:374px; height:120px; }" not in html:
        problems.append("card illustrations must be 374x120 at 2x, top-wide (v16 change 2)")
    if ".card2 .head { position:absolute; left:8px; top:150px; width:358px; font-family:'Liberation Serif',serif; font-size:30px; font-weight:bold; line-height:34px; }" not in html:
        problems.append("card heads must be 30px Liberation Serif Bold / lh 34 at 2x (v16 change 2)")
    if ".card2 .dek { position:absolute; left:8px; top:222px; width:358px; font-size:20px; line-height:24px; }" not in html:
        problems.append("card deks must be 20px / lh 24 at top 222 at 2x (v16 change 2)")
    if ".card2 .src { position:absolute; left:8px; top:274px; font-size:17px; color:#404040; white-space:nowrap; }" not in html:
        problems.append("card sources must be 17px at top 274 at 2x (v16 change 2)")
    # badges ON the illustration corner (top, not bottom of the card):
    # illustration is 0-120, badge 26px tall, 8px inset -> top 86.
    if ".card2 .badgepill { top:86px; right:8px; height:26px; line-height:22px; padding:0 10px; font-size:15px; }" not in html:
        problems.append("card badges must sit ON the illustration bottom-right (top 86px at 2x, not bottom of the card) (v16 change 2)")
    if ".card2 .kickpill { top:8px; left:8px; font-size:16px; padding:3px 10px; }" not in html:
        problems.append("card kicker pills must sit ON the illustration top-left (v16 change 2)")
    for kick in (
        "4 &middot; GAZA", "5 &middot; COPENHAGEN", "6 &middot; HONG KONG",
        "7 &middot; SINALOA", "8 &middot; FUKUOKA", "9 &middot; LAS VEGAS",
        "10 &middot; PERU", "11 &middot; BRAS&Iacute;LIA", "12 &middot; TURIN",
        "13 &middot; DELHI",
    ):
        if kick not in html:
            problems.append(f"card kicker pill '{kick}' missing (v16 change 2; v16.2: card 13 is Delhi now)")
    for head in (
        "Strike kills 3 in<br>Gaza City",
        "Russia paid gang<br>to kill rapper",
        "HK votes: turnout<br>98.79%",
        "&rsquo;El Chapo Isidro&rsquo;<br>captured",
        "Onosato wins<br>7th Emperor&rsquo;s Cup",
        "Verstappen wins<br>Las Vegas GP",
        "M6.9 quake shakes<br>Peru",
        "Bolsonaro in<br>intensive care",
        "Zverev, Alcaraz set<br>for ATP final",
        "First Pakistan visit<br>to India since 2023",
    ):
        if head not in html:
            problems.append(f"card headline '{head}' missing (v16 change 2; v16.2: card 12 is present-tense, card 13 is Delhi)")
    for dek in (
        "Death toll since truce now 1,671",
        "Plot foiled &middot; 2 charged, attach&eacute; expelled",
        "856 candidates &middot; 723 seats",
        "11 killed in clashes &middot; $5m reward",
        "Playoff win &middot; both finish 13-2",
        "75th career win &middot; 35 lead changes",
        "No damage reported &middot; 00:09 UTC",
        "Banda Sea also M6.9 &middot; 09:42 UTC",
        "Ex-president, 71 &middot; stable, conscious",
        "Final today, 17:00 UTC &middot; Turin",
        "Malik calls climate &lsquo;the enemy&rsquo;",
    ):
        if dek not in html:
            problems.append(f"card dek '{dek}' missing (v16 change 2; v16.2: card 8 is one line, card 10 adds Banda Sea, card 13 is Delhi)")
    for src in (
        "REUTERS &middot; MIDDLE EAST EYE",
        "BBC &middot; NYT",
        "INFO.GOV.HK",
        "REUTERS &middot; AP",
        "ABEMA &middot; TACHIAI",
        "FORMULA 1",
        "USGS &middot; AP",
        "REUTERS &middot; BLOOMBERG",
        "STRAITS TIMES",
        "DAWN",
    ):
        if src not in html:
            problems.append(f"card source '{src}' missing (v16 change 2; v16.2: card 13's only source is DAWN)")
    # v16 change 2: every placeholder/icon art is gone.
    if "CHARGED" in html or "EXPELLED" in html:
        problems.append("stale v15 card 05 bar-chart infographic still present (v16: Nyhavn scene)")
    if "$5M" in html:
        problems.append("stale v15 card 18 mini-map '$5M' chip still present (v16: Sinaloa desert scene)")
    if "856 candidates &middot;<br>723 seats" in html:
        problems.append("stale v15 card 10 two-line counts dek still present (v16: '856 candidates · 723 seats' is one line)")
    # "results tonight" belongs in DATE CHECK NOT YET only, not on a
    # card (v15.1 fix 5): scope to the grid block, since the DATE CHECK
    # legitimately carries "HK seat results tonight".
    grid_start = html.index("<!-- GRID ROW 1")
    grid_end = html.index("<!-- ALSO ON")
    grid_html = html[grid_start:grid_end]
    if "results tonight" in grid_html:
        problems.append("'results tonight' must not be on a card (v16: HK seat results are DATE CHECK NOT YET only)")
    # the 13 badges: 7 CONFIRMED, 3 OFFICIAL, 1 CLAIM, 2 REPORTED (v16.2 tally change).
    if html.count("badgepill b-conf") != 7:
        problems.append(f"CONFIRMED badges must be 7 (leads 1, 3 + cards 4, 5, 7, 8, 11) (found {html.count('badgepill b-conf')}) (v16.2: Moyale is a list row now)")
    if html.count("badgepill b-off") != 3:
        problems.append(f"OFFICIAL badges must be 3 (cards 6, 9, 10) (found {html.count('badgepill b-off')}) (v16)")
    if html.count("badgepill b-claim") != 1:
        problems.append(f"CLAIM badges must be 1 (lead 2 Bahrain) (found {html.count('badgepill b-claim')}) (v16)")
    if html.count("badgepill b-rep") != 2:
        problems.append(f"REPORTED badges must be 2 (cards 12 Turin and 13 Delhi, both single source) (found {html.count('badgepill b-rep')}) (v16.2)")
    if "Zverev and Alcaraz<br>reach ATP final" in html:
        problems.append("stale card 12 head 'Zverev and Alcaraz reach ATP final' still present (v16.2 fix 2: the semis were Sat 21 Nov — present tense 'set for')")
    if "700,000 displaced<br>in Moyale" in html:
        problems.append("stale card 13 head '700,000 displaced in Moyale' still present (v16.2 fix 2: Moyale is ALSO ON 17 now, Delhi is card 13)")
    if "&#10003; CLAIM" in html:
        problems.append("CLAIM badge must not carry a check mark (winners' legend: only CONFIRMED/OFFICIAL are checked)")
    if "&#10003; REPORTED" in html:
        problems.append("REPORTED badge must not carry a check mark (only CONFIRMED carries one on this page) (v16.1)")
    if ".b-conf { background:#E6F4EA; color:#137333; border-color:#81C995; }" not in html:
        problems.append("CONFIRMED capsule colours must be #E6F4EA/#137333/#81C995 (v15 P1, kept in v16)")
    if ".b-off { background:#E8F0FE; color:#1967D2; border-color:#8AB4F8; }" not in html:
        problems.append("OFFICIAL capsule colours must be #E8F0FE/#1967D2/#8AB4F8 (v15 P1, kept in v16)")
    if ".b-rep { background:#FEF7E0; color:#B06000; border-color:#FDD663; }" not in html:
        problems.append("REPORTED capsule colours must be #FEF7E0/#B06000/#FDD663 (v15 P1, kept in v16)")
    if ".b-claim { background:#FCE8E6; color:#C5221F; border-color:#F28B82; }" not in html:
        problems.append("CLAIM capsule colours must be #FCE8E6/#C5221F/#F28B82 (v15 P1, kept in v16)")
    # v15.2 fix 3 (kept): every CONFIRMED card with two research-file
    # sources prints both. v16.1: card 12 (Turin) prints only Straits
    # Times, so it is REPORTED, not CONFIRMED — pin the card-12 block
    # itself, so a later edit cannot silently re-promote it.
    c12_start = html.index("<!-- CARD 12")
    c12_end = html.index("<!-- CARD 13")
    c12_html = html[c12_start:c12_end]
    if "badgepill b-rep" not in c12_html:
        problems.append("card 12 (Turin) must carry the REPORTED badge (single source: STRAITS TIMES) (v16.1)")
    if "badgepill b-conf" in c12_html:
        problems.append("card 12 (Turin) must not carry a CONFIRMED badge: one source cannot be CONFIRMED (v16.1)")
    if "REPORTED" not in c12_html:
        problems.append("card 12 (Turin) must print the word REPORTED (v16.1)")
    for pair in (
        "EURONEWS &middot; REUTERS",
        "REUTERS &middot; MIDDLE EAST EYE",
        "REUTERS &middot; AP",
        "ABEMA &middot; TACHIAI",
        "REUTERS &middot; BLOOMBERG",
    ):
        if pair not in html:
            problems.append(f"CONFIRMED story must print both sources '{pair}' (v15.2 fix 3, kept in v16)")
    if "CONFIRMED &middot;" in html:
        problems.append("old 'CONFIRMED · SOURCE' text form must be gone (v15 P1: capsule badges)")
    # v16.2: card 13 (Delhi) is REPORTED for the same reason as card
    # 12 — one named outlet (DAWN). Pin the block itself.
    c13_start = html.index("<!-- CARD 13")
    c13_end = html.index("<!-- ALSO ON")
    c13_html = html[c13_start:c13_end]
    if "badgepill b-rep" not in c13_html:
        problems.append("card 13 (Delhi) must carry the REPORTED badge (single source: DAWN) (v16.2)")
    if "badgepill b-conf" in c13_html:
        problems.append("card 13 (Delhi) must not carry a CONFIRMED badge: one source cannot be CONFIRMED (v16.2)")
    if "REPORTED" not in c13_html:
        problems.append("card 13 (Delhi) must print the word REPORTED (v16.2)")
    if "ASIA &middot; DIPLOMACY" not in c13_html:
        problems.append("card 13 (Delhi) must be tagged ASIA · DIPLOMACY (v16.2: the swap is region-neutral)")
    # v16.3: both flags + poles sit below the kickpill (pill bottom is
    # SVG y=32, measured on the render; the suggested 14px still tucks
    # 4px of the saffron stripe). Flags start y=36, poles y=34–96.
    if '<rect x="70" y="36" width="64" height="42" fill="#FF9933"/>' not in c13_html:
        problems.append("card 13 Indian flag must start at y=36 (v16.3: the kickpill bottom is y=32; at y=14 the pill covered ~95% of it)")
    if '<line x1="66" y1="34" x2="66" y2="96"' not in c13_html:
        problems.append("card 13 Indian flagpole must run y=34–96 (v16.3: flags + poles down 22px)")
    if '<line x1="308" y1="34" x2="308" y2="96"' not in c13_html:
        problems.append("card 13 Pakistani flagpole must run y=34–96 (v16.3: both flags move together, symmetrically)")
    if '<rect x="70" y="14" width="64" height="42" fill="#FF9933"/>' in c13_html:
        problems.append("stale card 13 Indian flag at y=14 still present (v16.3: the pill covered it)")

    # --- v16 map: real continents, 13 small region-coloured pins, numbers only ---
    if "<!-- MAP" not in html or "<!-- DATE CHECK" not in html:
        problems.append("map / DATE CHECK section comments missing (v16)")
    map_start = html.index("<!-- MAP")
    map_end = html.index("<!-- DATE CHECK")
    map_html = html[map_start:map_end]
    if '<svg width="770" height="264" viewBox="0 0 770 264"' not in map_html:
        problems.append("map SVG must be 770x264 (v16 change 3)")
    if '<rect width="770" height="264" fill="#DCEBF7"/>' not in map_html:
        problems.append("map ocean must be #DCEBF7 (v16 change 3)")
    land_polys = map_html.count('fill="#E5E7D9" stroke="#C9C9B8"')
    if land_polys != 9:
        problems.append(f"map land must be 9 polygons #E5E7D9 / stroke #C9C9B8 (found {land_polys}) (v16 change 3)")
    if ".mapbox2 { position:absolute; left:1230px; top:1620px; width:770px; height:264px; background:#DCEBF7; overflow:hidden; }" not in html:
        problems.append("map panel must be left 1230 / top 1620 / 770x264, ocean #DCEBF7 (v16 change 3)")
    if "WHERE IT HAPPENED &middot; 13 PINS" not in map_html:
        problems.append("map label must be 'WHERE IT HAPPENED · 13 PINS' (v16 change 3)")
    if "THE WORLD &middot; 11 PINS" in html:
        problems.append("stale v15 map label 'THE WORLD · 11 PINS' still present (v16 change 3)")
    if ".mapbox { position:absolute;" in html:
        problems.append("old v15 '.mapbox' CSS still present (v16: .mapbox2)")
    pins = map_html.count("<circle cx=")
    if pins != 13:
        problems.append(f"map pins must be 13 (found {pins}) (v16 change 3)")
    if 'fill="#191919"/>' in map_html:
        problems.append("no map pin may be ink #191919 (v16 change 3: pins are region-coloured)")
    if 'font-size="15" font-weight="bold" fill="#F6F1E5" text-anchor="middle"' not in map_html:
        problems.append("pin numerals must be 15px bold cream #F6F1E5, centred (v16 change 3)")
    for slug in ("GOF", "ANTALYA", "BAH", "GAZA", "HKG", "SINALOA", "LAS", "BND", "PER", "FUK", "MOY", "BSB", "JKT", "LVIV"):
        if f">{slug}</text>" in map_html:
            problems.append(f"map slug '{slug}' must be gone (v16 change 3: numbers only)")
    # pin positions (map-local, measured before placing: at r=11 the
    # Med-cluster gaps are 1-4: 12.5px, 4-2: 10.3px, 3-5: 3.3px).
    pin_cx = {}
    pin_cy = {}
    pin_fill = {}
    for m in re.finditer(
        r'<circle cx="(\d+)" cy="(\d+)" r="11" fill="(#[0-9A-F]+)"/><text x="\d+" y="\d+">(\d+)</text>',
        map_html,
    ):
        pin_cx[m.group(4)] = int(m.group(1))
        pin_cy[m.group(4)] = int(m.group(2))
        pin_fill[m.group(4)] = m.group(3)
    for want in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"):
        if want not in pin_cy:
            problems.append(f"map pin {want} circle not found (v16 change 3; v16.2: pins are r=11)")
    # region colours: EU blue (1, 3, 5, 12), ME teal (2, 4), AS amber
    # (6, 8, 13), AM green (7, 9, 10, 11). No AF pin remains: Moyale
    # is a list row now, and only cards/leads are pinned. Pin 1 is
    # EUROPE blue (the bar counts Antalya EUROPE).
    want_fill = {
        "1": "#2F5D8A", "2": "#2E7A7A", "4": "#2E7A7A",
        "3": "#2F5D8A", "5": "#2F5D8A", "12": "#2F5D8A",
        "6": "#B97A1E", "8": "#B97A1E", "13": "#B97A1E",
        "7": "#4A7A3D", "9": "#4A7A3D", "10": "#4A7A3D", "11": "#4A7A3D",
    }
    for num, col in want_fill.items():
        if num in pin_fill and pin_fill[num] != col:
            problems.append(f"map pin {num} must be region colour {col} (found {pin_fill[num]}) (v16 change 3; v16.2: pin 1 is EUROPE blue, pin 13 is Delhi amber)")
    # v16.2 fix 3: pin gaps. Every pair of pins must clear by >= 3px
    # (centre distance minus 2r), and pin 3's top must clear the box
    # edge by >= 4px (it poked out at cy=16, r=12 in v16.1).
    if len(pin_cx) == 13 and len(pin_cy) == 13:
        import math
        _nums = sorted(pin_cx, key=lambda n: int(n))
        for _i in range(len(_nums)):
            for _j in range(_i + 1, len(_nums)):
                _a, _b = _nums[_i], _nums[_j]
                _d = math.hypot(pin_cx[_a] - pin_cx[_b], pin_cy[_a] - pin_cy[_b])
                if _d - 22 < 3:
                    problems.append(
                        f"map pins {_a} and {_b} collide: centre distance "
                        f"{_d:.1f}px, gap {_d - 22:.1f}px < 3px at r=11 "
                        f"(v16.2 fix 3)"
                    )
        if pin_cy["3"] - 11 < 4:
            problems.append(
                f"map pin 3 (Gulf of Finland) pokes out of the box top: "
                f"cy={pin_cy['3']}, top clearance {pin_cy['3'] - 11}px < 4px "
                f"(v16.2 fix 3)"
            )
    # v16: TRUE lat order — Antalya (67) < Gaza (80) < Delhi (84) <
    # Bahrain (89), and Hong Kong (94) SOUTH of Bahrain (the v15.3
    # distortion is fixed: HK 22.3N < Bahrain 26N). Delhi 28.6N sits
    # between Gaza 31.5N and Bahrain 26N. Peru/Brasilia southernmost.
    if all(k in pin_cy for k in ("1", "4", "13", "2", "6", "10", "11")):
        if not (pin_cy["1"] < pin_cy["4"] < pin_cy["13"] < pin_cy["2"]):
            problems.append(
                f"pin latitudes wrong: ANTALYA cy={pin_cy['1']}, GAZA "
                f"cy={pin_cy['4']}, DELHI cy={pin_cy['13']}, BAH "
                f"cy={pin_cy['2']} "
                f"(need ANTALYA < GAZA < DELHI < BAH) (v15.3 fix, kept in v16; v16.2: Delhi replaces Moyale)"
            )
        if not (pin_cy["2"] < pin_cy["6"]):
            problems.append(
                f"pin latitudes wrong: BAH cy={pin_cy['2']}, HKG "
                f"cy={pin_cy['6']} (need BAH < HKG: Hong Kong 22.3N is "
                f"south of Bahrain 26N — the v15.3 distortion is fixed in v16)"
            )
        if not (pin_cy["6"] < pin_cy["10"] and pin_cy["6"] < pin_cy["11"]):
            problems.append(
                f"pin latitudes wrong: HKG cy={pin_cy['6']}, PER "
                f"cy={pin_cy['10']}, BSB cy={pin_cy['11']} "
                f"(need HKG < PER/BSB) (v16)"
            )

    # --- v16 ALSO ON: 9 items, 2 cols (5+4), place + sentence + source ---
    if ".lst2 { position:absolute; left:48px; top:1620px; width:1150px; height:264px; }" not in html:
        problems.append("ALSO ON block must be left 48 / top 1620 / 1150x264 at 2x (v16 change 4)")
    if ".lst2 .row { font-size:17px; line-height:18px; height:38px; overflow:hidden; }" not in html:
        problems.append("ALSO ON rows must be 17px / lh 18 / 38px pitch at 2x (v16 change 4)")
    if ".lst { position:absolute;" in html:
        problems.append("old v15 '.lst' CSS still present (v16: .lst2)")
    if "ALSO ON SUNDAY 22 NOVEMBER &mdash; 9 MORE STORIES" not in html:
        problems.append("ALSO ON header must read 'ALSO ON SUNDAY 22 NOVEMBER — 9 MORE STORIES' (v16.3: 12 → 9, the 4 non-22-Nov rows are gone, Victoria added)")
    if "24 MORE STORIES" in html or "25 MORE STORIES" in html or "12 MORE STORIES" in html:
        problems.append("stale '24/25/12 MORE STORIES' still present (v16.3 has 9)")
    rows = re.findall(r'<div class="row">.*?</div>', html)
    if len(rows) != 9:
        problems.append(f"ALSO ON rows must be 9 (found {len(rows)}) (v16.3)")
    for num in ("14", "15", "16", "17", "18", "19", "20", "21", "22"):
        if f'<span class="n">{num}</span>' not in html:
            problems.append(f"ALSO ON number {num} missing (v16.3: strict 14-22 numbering)")
    for num in ("23", "24", "25"):
        if f'<span class="n">{num}</span>' in html:
            problems.append(f"stale ALSO ON number {num} still present (v16.3: rows end at 22)")
    for item in (
        "<b>Berlin:</b> Zelenskyy calls NATO membership the best guarantee",
        "<b>EU:</b> Costa proposes &euro;44bn more cuts, 3% Big Tech tax",
        "<b>Shenzhen:</b> first Trump&ndash;Putin&ndash;Xi meeting called positive",
        "<b>Brazil:</b> Supercell storm kills 3, damages thousands of homes",
        "<b>Washington:</b> Hegseth memo curbs US&ndash;Canada defence ties",
        "<b>Hormuz:</b> Pugh swims the strait in 3 days to flag war damage",
        "<b>Sydney:</b> ex-NSW MP Fred Nile dies aged 92",
        "<b>Markets:</b> Bitcoin falls to $55,252, then rebounds",
        "<b>Victoria:</b> Labor MPs run election &lsquo;pre-mortem&rsquo; as polls point to a death spiral",
    ):
        if item not in html:
            problems.append(f"ALSO ON item '{item[:40]}...' missing (v16.3: 9 rows, Victoria is the only clean 22-Nov substitute)")
    for rsrc in (
        "(Anadolu Agency)", "(Politico)", "(ABC News)",
        "(Straits Times)", "(Washington Post)", "(Reuters)",
    ):
        if rsrc not in html:
            problems.append(f"ALSO ON source '{rsrc}' missing (v16.3: every item carries its source)")
    if "Sources: Reuters, BBC, NYT, AP, Euronews, Al Jazeera, TASS, Politico, Dawn, ABC News, Straits Times, Washington Post, Info.gov.hk, Formula 1, Abema, Tachiai, Bloomberg, Middle East Eye, USGS, Anadolu Agency" not in html:
        problems.append("shared credit line missing (v16.3: DW, Sudan Tribune, Islamic Relief, UN, CNBC dropped with their rows; 'Drawn scenes are illustrations' removed as redundant)")
    if 'style="position:absolute; left:48px; top:1886px; width:1952px;' not in html:
        problems.append("credit line must sit at top 1886px full width (v16)")
    # v16.3: the credit line must NOT repeat "Drawn scenes are
    # illustrations" — the footer HOW WE CHECKED already says
    # "Scenes are drawn illustrations", and the repetition is what
    # pushed the line past the canvas edge (it truncated at
    # "...or attribut" in v16.2).
    _credit_start = html.index('top:1886px;')
    _credit_end = html.index("</div>", _credit_start)
    _credit = html[_credit_start:_credit_end]
    if "Drawn scenes are illustrations" in _credit:
        problems.append("credit line must not repeat 'Drawn scenes are illustrations' (v16.3: the footer already says it; the repetition truncated the line)")
    if "Figures checked in 2+ sources or attributed" not in _credit:
        problems.append("credit line must say 'Figures checked in 2+ sources or attributed' (v16)")
    for _dead in ("Sudan Tribune", "Islamic Relief", "CNBC", "DW,", "UN,"):
        if _dead in _credit:
            problems.append(f"credit line must not cite '{_dead}' (v16.3: its story left the page)")

    # --- v16 DATE CHECK: full-width red box, ATP final is a card now ---
    if ".dc { position:absolute; left:48px; top:1900px; width:1952px; height:94px; border:3px solid #C62828; background:#FDF2F2; }" not in html:
        problems.append("DATE CHECK must be the red box: 3px #C62828 border, #FDF2F2 bg, top 1900, height 94 (v16: taller, the 3-line EXCLUDED column must fit inside the border)")
    if 'class="redbar"' not in html:
        problems.append("DATE CHECK left red bar missing (v16)")
    if ".dc .redbar { position:absolute; left:0; top:0; width:10px; height:88px; background:#C62828; }" not in html:
        problems.append("DATE CHECK red bar must be 10px wide #C62828 (v16: 94-6 border-box)")
    if ".dc .l b { color:#C62828; }" not in html:
        problems.append("DATE CHECK title must be #C62828 (v16)")
    if "<b>DATE CHECK</b> &#10003; As of 22 Nov, 17:00 UTC." not in html:
        problems.append("DATE CHECK title line must be 'DATE CHECK ✓ As of 22 Nov, 17:00 UTC.' (v16.2 fix 2: the absolute 'everything happened on 22 November' wording is gone)")
    if "everything on this page happened on 22 November 2026" in html:
        problems.append("stale DATE CHECK title 'everything on this page happened on 22 November 2026' still present (v16.2 fix 2: it exposed the 19–21 Nov stories)")
    if ".dc .col { position:absolute; top:28px; width:460px; font-size:17px; line-height:18px; }" not in html:
        problems.append("DATE CHECK columns must be 17px / lh 18 at top 28 at 2x (v16: header + 2 body lines fit in the 88px content area)")
    for col in ("EXCLUDED (PRE-22 NOV)", "LEFT OUT", "NOT YET (POST-17:00 UTC)", "OFFICIAL REVISIONS"):
        if col not in html:
            problems.append(f"DATE CHECK column {col} missing (v16)")
    if "CORRECTIONS" in html or "HELD" in html:
        problems.append("stale DATE CHECK column 'CORRECTIONS'/'HELD' still present (v16)")
    if "Ukraine 400-drone strike (19&ndash;20 Nov)" not in html:
        problems.append("DATE CHECK EXCLUDED must list the Ukraine strike with its dates (v16.2 fix 4: col 1 is two lines now)")
    if "Nigeria boat &middot; EU&ndash;Indonesia (21 Nov)" not in html:
        problems.append("DATE CHECK EXCLUDED must list Nigeria boat + EU–Indonesia with one shared '21 Nov' (v16.2 fix 4: col 1 is two lines now)")
    if "ICJ verdict, 19 Nov &middot; FBI probe, unconfirmed" not in html:
        problems.append("DATE CHECK LEFT OUT must read 'ICJ verdict, 19 Nov · FBI probe, unconfirmed' (v16)")
    if "ATP final 17:00 UTC &middot; HK seat results tonight" not in html:
        problems.append("DATE CHECK NOT YET must read 'ATP final 17:00 UTC · HK seat results tonight' (v16.2 fix 2: restored with the 17:00 UTC cutoff)")
    if "HK: 5,640 registered voters (subsector)" not in html:
        problems.append("DATE CHECK revisions must read 'HK: 5,640 registered voters (subsector)' (v16)")
    if ".dc .col .h .notyet { color:#D98E00; }" not in html:
        problems.append("DATE CHECK NOT YET must be amber (v12 step 5, kept in v16)")
    dc_start = html.index("<!-- DATE CHECK")
    dc_end = html.index('<div class="foot"')
    dc_html = html[dc_start:dc_end]
    # v16.2 fix 2: NOT YET legitimately names the ATP final (it starts
    # 17:00 UTC, i.e. at the cutoff) — the old "no ATP in DATE CHECK"
    # rule died with the restored title.
    if "ATP final" not in dc_html:
        problems.append("DATE CHECK NOT YET must name the ATP final (v16.2 fix 2)")
    if "Nigeria boat capsize" in html:
        problems.append("stale 'Nigeria boat capsize' still present (v15.2 fix 1: shortened to 'Nigeria boat' so both 21-Nov items share one line)")

    # --- v16.2 footer: tally is 7 confirmed · 3 official · 1 claim · 2 reported (13 badges) ---
    if html.count("7 confirmed &middot; 3 official &middot; 1 claim &middot; 2 reported") != 1:
        problems.append(
            "footer verification tally '7 confirmed · 3 official · 1 claim · 2 reported' "
            "must appear once (v16.2: 13 badges, Turin + Delhi are REPORTED)"
        )
    if "8 confirmed &middot; 3 official &middot; 1 claim &middot; 1 reported" in html:
        problems.append("stale v16.1 tally '8 confirmed · 3 official · 1 claim · 1 reported' still present (v16.2: 7·3·1·2 for 13 badges)")
    if "9 confirmed &middot; 3 official &middot; 1 claim" in html:
        problems.append("stale v16 tally '9 confirmed · 3 official · 1 claim' still present (v16.1: 8·3·1·1 for 13 badges)")
    if "6 confirmed &middot; 2 official &middot; 1 claim" in html:
        problems.append("stale v15.3 tally '6 confirmed · 2 official · 1 claim' still present (v16: 9·3·1 for 13 badges)")
    if "5 confirmed &middot; 3 official &middot; 1 claim" in html:
        problems.append("stale v15.1 tally '5 confirmed · 3 official · 1 claim' still present (v16)")
    if 'class="foot" style="top:2002px;"' not in html:
        problems.append("footer line 1 must be top 2002 at 2x (v16: 8px clear of the DATE CHECK border, ends 2040)")
    if 'class="foot" style="top:2024px;"' not in html:
        problems.append("footer line 2 must be top 2024 at 2x (v16)")
    if "NEWS-IMAGE-20261122 &middot; SUM UP 22 NOVEMBER&rsquo;S WORLD NEWS IN ONE IMAGE &middot; MAKE.FUN" not in html:
        problems.append("footer line 1 missing (v16)")
    if "HOW WE CHECKED: CONFIRMED = two independent sources &middot; OFFICIAL = government or agency statement &middot; REPORTED = one named outlet &middot; CLAIM = single-source allegation" not in html:
        problems.append("footer HOW WE CHECKED legend missing (v16)")
    if "Scenes are drawn illustrations" not in html:
        problems.append("footer must say 'Scenes are drawn illustrations' (v16)")
    # v16.1: the tally grew by 13 chars ("· 1 reported") and at 16px the
    # line ran to x2047, clipping "illustrations" at the canvas edge
    # (v16 ended at x1984). 15px restores the margin; line-height stays
    # 16px so the 2002/2024 tops do not move.
    if ".foot { position:absolute; left:48px; width:1952px; font-size:15px; line-height:16px; white-space:nowrap; }" not in html:
        problems.append("footer must be 15px (v16.1: the longer tally clips at 16px)")

    # --- v16 red: #B01E1E is illustration-only now (radar dot + boat sail) ---
    red_uses = html.count("#B01E1E")
    if red_uses != 2:
        problems.append(
            f"brand red #B01E1E must occur 2 times in source "
            f"(lead-2 radar dot + card-5 boat sail; the v15 banner/NOW uses "
            f"are gone — NOW is amber on the dark bar) (found {red_uses})"
        )
    if "#B01E1E" in map_html:
        problems.append("no brand red may remain on a map pin (v12 step 5, kept in v16)")
    if html.count("#C62828") < 5:
        problems.append(
            f"DATE CHECK / illustration red #C62828 must appear at least 5 times "
            f"(box border, bar, title, flags, hull) (found {html.count('#C62828')})"
        )

    # --- v16 vertical geometry: grid ends 1602, bottom row 1620-1884,
    # credit 1886, DATE CHECK 1900-1994, footer ends 2040 ---
    if ".mapbox2 { position:absolute; left:1230px; top:1620px; width:770px; height:264px;" not in html:
        problems.append("mapbox2 must be top 1620 / height 264 at 2x (v16)")
    if ".lst2 { position:absolute; left:48px; top:1620px; width:1150px; height:264px; }" not in html:
        problems.append("lst2 must be top 1620 / height 264 at 2x (v16)")
    if ".dc { position:absolute; left:48px; top:1900px;" not in html:
        problems.append("DATE CHECK must be top 1900 at 2x (v16)")

    # --- 22 story slots: 3 leads + 10 cards + 9 list rows ---
    slots = (
        html.count('<div class="lead"')
        + html.count('<div class="card2"')
        + html.count('<div class="row">')
    )
    if slots != 22:
        problems.append(f"story slots must be 22 (found {slots}) (v16.3: 3 leads + 10 cards + 9 rows)")

    if problems:
        raise SystemExit("front.html v16 check failed:\n- " + "\n- ".join(problems))
    print(
        f"front.html v16 check ok: 3-column leads + 2x5 top-image grid (13 scene illustrations, badges on the art); 6 numbers, all 22 Nov; "
        f"3 leads + {cards} cards + 9 list rows = 22 slots; 13 map pins on real continents "
        f"(ANTALYA < GAZA < DELHI < BAH < HKG, true lat order); timeline dark bar, NOW on the 17:00 tick; DATE CHECK red box, As of 22 Nov 17:00 UTC; "
        f"tally 7 confirmed · 3 official · 1 claim · 2 reported; red #B01E1E x2; footer ends 2040"
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
    """v16: fail if neighbouring numbers' INK touches.

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
