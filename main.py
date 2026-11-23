#!/usr/bin/env python3
"""news-image-20261122 entrypoint (v16): copy entry.png to /output/entry.png.

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
   COP failure since 2009 move into lead 1's dek and source line.

2. 2x5 top-image cards (stories 4-13). The 2x4 left-image cards are
   replaced by 2 rows x 5 columns = 10 cards, each top-wide
   illustration (374x120 at 2x, ~40% of the 300px card) + kicker pill
   + badge pill on the art + region/topic + serif head + dek + source.
   ALL placeholder/icon art is gone: the 28 GAZA and 18 SINALOA
   map-circle placeholders, the 05 COPENHAGEN bar chart, the 10 HK
   ballot-box icon, the 34 LAS VEGAS checker flag are all concrete
   flat-vector scene illustrations with backgrounds (city/smoke,
   Nyhavn, polling station, desert town, dohyo ring, night race,
   Andes/seismograph, hospital, tennis court, dusty road). Total
   illustrations: 13 (3 leads + 10 cards) — the top-3 visual
   threshold.

3. Real world map. The grey grid is replaced by a real continent
   vector outline: ocean #DCEBF7, land #E5E7D9, stroke #C9C9B8. The
   giant ink pins (r=26) shrink to small region-coloured numbered
   dots (r=12, white 15px numerals): Europe #2F5D8A, Middle East
   #2E7A7A, Asia #B97A1E, Americas #4A7A3D, Africa #8A5A28. The messy
   English slugs (LAS, GOF, BAH, FUK) are dropped — numbers only,
   matching cards 1-13. Pin geography is TRUE lat/lon order now
   (v15.3 fixed Antalya < Gaza < Bahrain; v16 also fixes the
   pre-existing HKG distortion: Hong Kong 22.3N sits SOUTH of Bahrain
   26N, cy 94 > 86). Pin cy order: GOF 16 < CPH 30 < Turin 54 <
   Antalya 70 < Gaza 80 < Bahrain 86 < HKG 94 < Moyale 110 < Peru 150
   / Brasilia 148. The Med cluster is tight (Antalya-Gaza 29.7px,
   Gaza-Bahrain 28.6px centre-to-centre at r=12) and was measured
   before placing, not eyeballed.

4. Renumber + rewrite ALSO ON. Strict visual-order numbering across
   the whole page: leads 1-3, grid 4-13, ALSO ON 14-25. Cut from 24
   fragments to 12 high-quality items. Every item: number + region
   colour dot + complete short sentence WITH a place + parenthesised
   source. Font 17px (was 16px), rows 38px pitch, 2 columns x 6 rows.

5. Compress top chrome. The UTC timeline is now a dark navy bar
   (#14213D, top-1 style) with white text and an amber NOW; the
   numbers stay in the same six even columns (ink check band
   unchanged); the region bar is one thin 28px chip row (was 36px).
   All 6 numbers are kept (98.79%, 0, 6.9, 7th, 11, 75th — all
   verified 22 Nov, six different stories) and the UTC timeline keeps
   NOW on the 17:00 tick.

Story assignment (all verified in news-20261122.md; no new facts;
no date other than 22 Nov on any story, number, or card):
- Leads: 1 COP31 (03, CONFIRMED, "COP31 draft · Reuters · 35% by
  2035 · 1.5°C overshoot"); 2 Bahrain (01, CLAIM, "AL JAZEERA ·
  TASS"); 3 Sparta II (04, CONFIRMED, "EURONEWS · REUTERS").
- Grid: 4 Gaza (28, CONFIRMED, REUTERS · MIDDLE EAST EYE); 5
  Copenhagen (05, CONFIRMED, BBC · NYT); 6 Hong Kong (10, OFFICIAL,
  INFO.GOV.HK); 7 Sinaloa (18, CONFIRMED, REUTERS · AP); 8 Fukuoka
  (16, CONFIRMED, ABEMA · TACHIAI); 9 Las Vegas (34, OFFICIAL,
  FORMULA 1); 10 Peru (17, OFFICIAL, USGS · AP); 11 Brasilia (19,
  CONFIRMED, REUTERS · BLOOMBERG); 12 Turin (35, CONFIRMED, STRAITS
  TIMES); 13 Moyale (27, CONFIRMED, ISLAMIC RELIEF · UN).
- ALSO ON 14-25: 14 Berlin Zelenskyy (06, Anadolu Agency); 15 EU
  Costa budget (07, Politico); 16 Shenzhen Trump-Putin-Xi (12, ABC
  News); 17 Delhi Pakistani minister (14, Dawn); 18 Brazil Supercell
  (20, Straits Times); 19 Washington Hegseth memo (21, Washington
  Post); 20 Khartoum kitchens (24, Sudan Tribune); 21 Badme troops
  (26, DW); 22 Hormuz Pugh swim (29, Straits Times); 23 Sydney Fred
  Nile (31, ABC News); 24 Markets Bitcoin (33, Reuters); 25 New York
  Anthropic (22, CNBC).

Badge tally CHANGE (flagged to the parent): v15.3's footer tally
"6 confirmed · 2 official · 1 claim" counted its 9 badges. v16 has
13 badged stories, so the tally is recomputed as "9 confirmed · 3
official · 1 claim" (confirmed: COP31, Sparta II, Gaza, Copenhagen,
Sinaloa, Onosato, Brasilia, Turin, Moyale; official: HK, Verstappen,
Peru; claim: Bahrain). Keeping 6·2·1 would be false.

Single-source CONFIRMED note: card 12 (Turin, story 35) prints only
"STRAITS TIMES" — the research file names no other outlet for story
35, and its own badge table marks 35 ATP as CONFIRMED (semis
confirmed; final "today"). The lead is the same pattern (COP31 draft
text + Reuters = two sources in effect). No source is invented.

DATE CHECK: ATP final is a card now (12), so NOT YET is HK seat
results only. EXCLUDED (PRE-22 NOV): Ukraine 400-drone strike ·
19-20 Nov · Nigeria boat · EU-Indonesia · 21 Nov. LEFT OUT: ICJ
verdict, 19 Nov · FBI probe, unconfirmed. OFFICIAL REVISIONS: HK:
5,640 registered voters (subsector).

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
    if "25 STORIES &middot; 13 PINS" not in html:
        problems.append("masthead tally must be '25 STORIES · 13 PINS' (v16: 3 leads + 10 cards + 12 list rows, 13 map pins)")
    if "33 STORIES" in html or "34 STORIES" in html:
        problems.append("stale '33/34 STORIES' still present (v16 has 25)")
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
    if 'class="nowmark" style="left:1487px;"' not in tl_band:
        problems.append(
            "NOW marker must sit at left 1487px at 2x (64px wide, centred), "
            "ring centred 8px left of the 17:00 tick at 1527px (v15.2 fix 5, kept in v16)"
        )
    if ".nowmark { position:absolute; top:226px; width:64px; text-align:center; font-size:18px; font-weight:bold; color:#F2A900; }" not in html:
        problems.append("NOW marker must be amber #F2A900 on the dark bar (v16 change 5)")
    if 'left:360px; top:270px; width:1360px; height:2px; background:#F6F1E5;' not in tl_band:
        problems.append("timeline axis rule must be cream #F6F1E5 and end at 1720px (width 1360px) (v16 change 5: was ink on light)")
    for tx in (359, 647, 935, 1223, 1527):
        if f'left:{tx}px; top:264px; width:2px; height:12px; background:#F6F1E5;' not in tl_band:
            problems.append(f"timeline tick mark at left {tx}px missing (v16 change 5: cream ticks on dark)")

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
    if n21 != 1 or "Nigeria boat &middot; EU&ndash;Indonesia &middot; 21 Nov" not in html:
        problems.append(
            f"'21 Nov' must appear exactly once (DATE CHECK EXCLUDED: "
            f"Nigeria boat + EU–Indonesia deal share one '21 Nov') "
            f"(found {n21}) (v16)"
        )
    if "190+" in html:
        problems.append("'190+ nations' must not appear (v15: not in the research file)")
    if "700,000 displaced" not in html:
        problems.append("card 13 head must keep the full value '700,000 displaced' (v16: Moyale is a card now, not a list row)")

    # --- v16 region chips: one thin 28px row; counts for the new 25 stories ---
    if ".key { position:absolute; top:446px; height:28px; }" not in html:
        problems.append("region chips must be one thin 28px row at top 446 at 2x (v16 change 5: was 36px at 474)")
    for reg in (
        "MIDDLE EAST 3", "EUROPE 6", "ASIA 5", "AMERICAS 5",
        "AFRICA 3", "OCEANIA 1", "MKT+SPORT 2",
    ):
        if reg not in html:
            problems.append(f"region chip missing {reg} (v16: counts for the new 25 stories)")
    for stale in ("MIDDLE EAST 4", "ASIA 7", "AMERICAS 7", "AFRICA 4", "OCEANIA 2", "MKT+SPORT 3"):
        if stale in html:
            problems.append(f"stale v15.3 region count '{stale}' still present (v16)")
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
        "No consensus in the closing plenary &mdash; the first COP failure since 2009. The draft never mentioned fossil fuels.",
        "Bahrain: industrial fire, no injuries. The claim is not independently verified.",
        "Sparta II burns &middot; drifts into Finnish waters. 16 crew evacuated.",
    ):
        if dek not in html:
            problems.append(f"lead dek '{dek[:40]}...' missing (v16 change 1)")
    for src in (
        "COP31 draft &middot; Reuters &middot; 35% by 2035 &middot; 1.5&deg;C overshoot",
        "AL JAZEERA &middot; TASS",
        "EURONEWS &middot; REUTERS",
    ):
        if src not in html:
            problems.append(f"lead source '{src}' missing (v16 change 1)")
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
        "13 &middot; MOYALE",
    ):
        if kick not in html:
            problems.append(f"card kicker pill '{kick}' missing (v16 change 2)")
    for head in (
        "Strike kills 3 in<br>Gaza City",
        "Russia paid gang<br>to kill rapper",
        "HK votes: turnout<br>98.79%",
        "&rsquo;El Chapo Isidro&rsquo;<br>captured",
        "Onosato wins<br>7th Emperor&rsquo;s Cup",
        "Verstappen wins<br>Las Vegas GP",
        "M6.9 quake shakes<br>Peru",
        "Bolsonaro in<br>intensive care",
        "Zverev and Alcaraz<br>reach ATP final",
        "700,000 displaced<br>in Moyale",
    ):
        if head not in html:
            problems.append(f"card headline '{head}' missing (v16 change 2)")
    for dek in (
        "Death toll since truce now 1,671",
        "Plot foiled &middot; 2 charged, attach&eacute; expelled",
        "856 candidates &middot; 723 seats",
        "11 killed in clashes &middot; $5m reward",
        "Beats Wakamotoharu in a playoff &middot; 13-2",
        "75th career win &middot; 35 lead changes",
        "No damage reported &middot; 00:09 UTC",
        "Ex-president, 71 &middot; stable, conscious",
        "Final today, 17:00 UTC &middot; Turin",
        "~30,000 fled into Kenya",
    ):
        if dek not in html:
            problems.append(f"card dek '{dek}' missing (v16 change 2)")
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
        "ISLAMIC RELIEF &middot; UN",
    ):
        if src not in html:
            problems.append(f"card source '{src}' missing (v16 change 2)")
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
    # the 13 badges: 9 CONFIRMED, 3 OFFICIAL, 1 CLAIM (v16 tally change).
    if html.count("badgepill b-conf") != 9:
        problems.append(f"CONFIRMED badges must be 9 (leads 1, 3 + cards 4, 5, 7, 8, 11, 12, 13) (found {html.count('badgepill b-conf')}) (v16)")
    if html.count("badgepill b-off") != 3:
        problems.append(f"OFFICIAL badges must be 3 (cards 6, 9, 10) (found {html.count('badgepill b-off')}) (v16)")
    if html.count("badgepill b-claim") != 1:
        problems.append(f"CLAIM badges must be 1 (lead 2 Bahrain) (found {html.count('badgepill b-claim')}) (v16)")
    if "&#10003; CLAIM" in html:
        problems.append("CLAIM badge must not carry a check mark (winners' legend: only CONFIRMED/OFFICIAL are checked)")
    if ".b-conf { background:#E6F4EA; color:#137333; border-color:#81C995; }" not in html:
        problems.append("CONFIRMED capsule colours must be #E6F4EA/#137333/#81C995 (v15 P1, kept in v16)")
    if ".b-off { background:#E8F0FE; color:#1967D2; border-color:#8AB4F8; }" not in html:
        problems.append("OFFICIAL capsule colours must be #E8F0FE/#1967D2/#8AB4F8 (v15 P1, kept in v16)")
    if ".b-rep { background:#FEF7E0; color:#B06000; border-color:#FDD663; }" not in html:
        problems.append("REPORTED capsule colours must be #FEF7E0/#B06000/#FDD663 (v15 P1, kept in v16)")
    if ".b-claim { background:#FCE8E6; color:#C5221F; border-color:#F28B82; }" not in html:
        problems.append("CLAIM capsule colours must be #FCE8E6/#C5221F/#F28B82 (v15 P1, kept in v16)")
    # v15.2 fix 3 (kept): every CONFIRMED card with two research-file
    # sources prints both. Card 12 (Turin) is the documented exception:
    # the research file names only Straits Times for story 35, and its
    # own badge table marks 35 ATP as CONFIRMED — no source is invented.
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
    # pin positions (map-local, measured before placing: Med cluster
    # Antalya-Gaza 29.7px, Gaza-Bahrain 28.6px at r=12).
    pin_cy = {}
    pin_fill = {}
    for m in re.finditer(
        r'<circle cx="(\d+)" cy="(\d+)" r="12" fill="(#[0-9A-F]+)"/><text x="\d+" y="\d+">(\d+)</text>',
        map_html,
    ):
        pin_cy[m.group(4)] = int(m.group(2))
        pin_fill[m.group(4)] = m.group(3)
    for want in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"):
        if want not in pin_cy:
            problems.append(f"map pin {want} circle not found (v16 change 3)")
    # region colours: EU blue (3, 5, 12), ME teal (1, 2, 4), AS amber
    # (6, 8), AM green (7, 9, 10, 11), AF brown (13).
    want_fill = {
        "1": "#2E7A7A", "2": "#2E7A7A", "4": "#2E7A7A",
        "3": "#2F5D8A", "5": "#2F5D8A", "12": "#2F5D8A",
        "6": "#B97A1E", "8": "#B97A1E",
        "7": "#4A7A3D", "9": "#4A7A3D", "10": "#4A7A3D", "11": "#4A7A3D",
        "13": "#8A5A28",
    }
    for num, col in want_fill.items():
        if num in pin_fill and pin_fill[num] != col:
            problems.append(f"map pin {num} must be region colour {col} (found {pin_fill[num]}) (v16 change 3)")
    # v16: TRUE lat order — Antalya (70) < Gaza (80) < Bahrain (86),
    # and Hong Kong (94) SOUTH of Bahrain (the v15.3 distortion is
    # fixed: HK 22.3N < Bahrain 26N). Moyale (110) south of HKG;
    # Peru/Brasilia the southernmost.
    if all(k in pin_cy for k in ("1", "4", "2", "6", "13", "10", "11")):
        if not (pin_cy["1"] < pin_cy["4"] < pin_cy["2"]):
            problems.append(
                f"pin latitudes wrong: ANTALYA cy={pin_cy['1']}, GAZA "
                f"cy={pin_cy['4']}, BAH cy={pin_cy['2']} "
                f"(need ANTALYA < GAZA < BAH) (v15.3 fix, kept in v16)"
            )
        if not (pin_cy["2"] < pin_cy["6"]):
            problems.append(
                f"pin latitudes wrong: BAH cy={pin_cy['2']}, HKG "
                f"cy={pin_cy['6']} (need BAH < HKG: Hong Kong 22.3N is "
                f"south of Bahrain 26N — the v15.3 distortion is fixed in v16)"
            )
        if not (pin_cy["6"] < pin_cy["13"] < pin_cy["10"] and pin_cy["13"] < pin_cy["11"]):
            problems.append(
                f"pin latitudes wrong: HKG cy={pin_cy['6']}, MOYALE "
                f"cy={pin_cy['13']}, PER cy={pin_cy['10']}, BSB "
                f"cy={pin_cy['11']} (need HKG < MOYALE < PER/BSB) (v16)"
            )

    # --- v16 ALSO ON: 12 items, 2 cols x 6 rows, place + sentence + source ---
    if ".lst2 { position:absolute; left:48px; top:1620px; width:1150px; height:264px; }" not in html:
        problems.append("ALSO ON block must be left 48 / top 1620 / 1150x264 at 2x (v16 change 4)")
    if ".lst2 .row { font-size:17px; line-height:18px; height:38px; overflow:hidden; }" not in html:
        problems.append("ALSO ON rows must be 17px / lh 18 / 38px pitch at 2x (v16 change 4)")
    if ".lst { position:absolute;" in html:
        problems.append("old v15 '.lst' CSS still present (v16: .lst2)")
    if "ALSO ON SUNDAY 22 NOVEMBER &mdash; 12 MORE STORIES" not in html:
        problems.append("ALSO ON header must read 'ALSO ON SUNDAY 22 NOVEMBER — 12 MORE STORIES' (v16 change 4)")
    if "24 MORE STORIES" in html or "25 MORE STORIES" in html:
        problems.append("stale '24/25 MORE STORIES' still present (v16 has 12)")
    rows = re.findall(r'<div class="row">.*?</div>', html)
    if len(rows) != 12:
        problems.append(f"ALSO ON rows must be 12 (found {len(rows)}) (v16 change 4)")
    for num in ("14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25"):
        if f'<span class="n">{num}</span>' not in html:
            problems.append(f"ALSO ON number {num} missing (v16 change 4: strict 14-25 numbering)")
    for item in (
        "<b>Berlin:</b> Zelenskyy calls NATO membership the best guarantee",
        "<b>EU:</b> Costa proposes &euro;44bn more cuts, 3% Big Tech tax",
        "<b>Shenzhen:</b> first Trump&ndash;Putin&ndash;Xi meeting called positive",
        "<b>Delhi:</b> Pakistani minister visits India, first since 2023",
        "<b>Brazil:</b> Supercell storm kills 3, damages thousands of homes",
        "<b>Washington:</b> Hegseth memo curbs US&ndash;Canada defence ties",
        "<b>Khartoum:</b> charity kitchens shut down, starvation looms",
        "<b>Badme:</b> troops mass on the Ethiopia&ndash;Eritrea border",
        "<b>Hormuz:</b> Pugh swims the strait in 3 days to flag war damage",
        "<b>Sydney:</b> ex-NSW MP Fred Nile dies aged 92",
        "<b>Markets:</b> Bitcoin falls to $55,252, then rebounds",
        "<b>New York:</b> Anthropic shares fall 6% on day 2 after IPO",
    ):
        if item not in html:
            problems.append(f"ALSO ON item '{item[:40]}...' missing (v16 change 4)")
    for rsrc in (
        "(Anadolu Agency)", "(Politico)", "(ABC News)", "(Dawn)",
        "(Straits Times)", "(Washington Post)", "(Sudan Tribune)",
        "(DW)", "(Reuters)", "(CNBC)",
    ):
        if rsrc not in html:
            problems.append(f"ALSO ON source '{rsrc}' missing (v16 change 4: every item carries its source)")
    if "Sources: Reuters, BBC, NYT, AP, Euronews, Al Jazeera, TASS, Politico, Dawn, DW, ABC News, Straits Times, Washington Post, Sudan Tribune, Info.gov.hk, Formula 1, Abema, Tachiai, Islamic Relief, UN, CNBC" not in html:
        problems.append("shared credit line missing (v16)")
    if 'style="position:absolute; left:48px; top:1886px; width:1952px;' not in html:
        problems.append("credit line must sit at top 1886px full width (v16)")
    if "Drawn scenes are illustrations" not in html:
        problems.append("credit line must say 'Drawn scenes are illustrations' (v16)")
    if "Figures checked in 2+ sources or attributed" not in html:
        problems.append("credit line must say 'Figures checked in 2+ sources or attributed' (v16)")

    # --- v16 DATE CHECK: full-width red box, ATP final is a card now ---
    if ".dc { position:absolute; left:48px; top:1900px; width:1952px; height:94px; border:3px solid #C62828; background:#FDF2F2; }" not in html:
        problems.append("DATE CHECK must be the red box: 3px #C62828 border, #FDF2F2 bg, top 1900, height 94 (v16: taller, the 3-line EXCLUDED column must fit inside the border)")
    if 'class="redbar"' not in html:
        problems.append("DATE CHECK left red bar missing (v16)")
    if ".dc .redbar { position:absolute; left:0; top:0; width:10px; height:88px; background:#C62828; }" not in html:
        problems.append("DATE CHECK red bar must be 10px wide #C62828 (v16: 94-6 border-box)")
    if ".dc .l b { color:#C62828; }" not in html:
        problems.append("DATE CHECK title must be #C62828 (v16)")
    if "<b>DATE CHECK</b> &nbsp;&mdash;&nbsp; everything on this page happened on 22 November 2026" not in html:
        problems.append("DATE CHECK title line must be 'DATE CHECK — everything on this page happened on 22 November 2026' (v16)")
    if ".dc .col { position:absolute; top:28px; width:460px; font-size:17px; line-height:18px; }" not in html:
        problems.append("DATE CHECK columns must be 17px / lh 18 at top 28 at 2x (v16: header + 2 body lines fit in the 88px content area)")
    for col in ("EXCLUDED (PRE-22 NOV)", "LEFT OUT", "NOT YET (POST-17:00 UTC)", "OFFICIAL REVISIONS"):
        if col not in html:
            problems.append(f"DATE CHECK column {col} missing (v16)")
    if "CORRECTIONS" in html or "HELD" in html:
        problems.append("stale DATE CHECK column 'CORRECTIONS'/'HELD' still present (v16)")
    if "Ukraine 400-drone strike &middot; 19&ndash;20 Nov &middot; Nigeria boat &middot; EU&ndash;Indonesia &middot; 21 Nov" not in html:
        problems.append("DATE CHECK must exclude the Ukraine strike + Nigeria boat + EU–Indonesia with their dates (v16)")
    if "ICJ verdict, 19 Nov &middot; FBI probe, unconfirmed" not in html:
        problems.append("DATE CHECK LEFT OUT must read 'ICJ verdict, 19 Nov · FBI probe, unconfirmed' (v16)")
    if "HK seat results tonight" not in html:
        problems.append("DATE CHECK NOT YET must read 'HK seat results tonight' (v16)")
    if "HK: 5,640 registered voters (subsector)" not in html:
        problems.append("DATE CHECK revisions must read 'HK: 5,640 registered voters (subsector)' (v16)")
    if ".dc .col .h .notyet { color:#D98E00; }" not in html:
        problems.append("DATE CHECK NOT YET must be amber (v12 step 5, kept in v16)")
    dc_start = html.index("<!-- DATE CHECK")
    dc_end = html.index('<div class="foot"')
    dc_html = html[dc_start:dc_end]
    if "ATP" in dc_html:
        problems.append("DATE CHECK must not mention the ATP final (v16: it is card 12 now, NOT YET is HK seat results only)")
    if "Nigeria boat capsize" in html:
        problems.append("stale 'Nigeria boat capsize' still present (v15.2 fix 1: shortened to 'Nigeria boat' so both 21-Nov items share one line)")

    # --- v16 footer: tally is 9 confirmed · 3 official · 1 claim (13 badges) ---
    if html.count("9 confirmed &middot; 3 official &middot; 1 claim") != 1:
        problems.append(
            "footer verification tally '9 confirmed · 3 official · 1 claim' "
            "must appear once (v16: 13 badges, not v15.3's 9)"
        )
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

    # --- 25 story slots: 3 leads + 10 cards + 12 list rows ---
    slots = (
        html.count('<div class="lead"')
        + html.count('<div class="card2"')
        + html.count('<div class="row">')
    )
    if slots != 25:
        problems.append(f"story slots must be 25 (found {slots}) (v16: 3 leads + 10 cards + 12 rows)")

    if problems:
        raise SystemExit("front.html v16 check failed:\n- " + "\n- ".join(problems))
    print(
        f"front.html v16 check ok: 3-column leads + 2x5 top-image grid (13 scene illustrations, badges on the art); 6 numbers, all 22 Nov; "
        f"3 leads + {cards} cards + 12 list rows = 25 slots; 13 map pins on real continents "
        f"(ANTALYA < GAZA < BAH < HKG, true lat order); timeline dark bar, NOW on the 17:00 tick; DATE CHECK red box, ATP is a card now; "
        f"tally 9 confirmed · 3 official · 1 claim; red #B01E1E x2; footer ends 2040"
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
