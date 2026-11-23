#!/usr/bin/env python3
"""news-image-20261122 entrypoint (v14): copy entry.png to /output/entry.png.

Stdlib only. No network. Deterministic: the output bytes are exactly the
input bytes, so two runs are byte-identical.

v14 is the SUBSTANTIAL round on v13 (Quick ruled v13 READY with no
blocking fixes, so v14 changes first-glance impact, not defects).
v13 scored judge 969,381 (10W 1D 1L), +2,886 vs round 2; the top-50
cutoff is ~989,000, so the gap is ~20,000 points (about 2 duel flips).
Per the score-gap study, the gap is the TEMPLATE, not polish: the
winners make the DATE the biggest type (~90px serif, full width), put
a dek under it stringing the top stories, and show 6 big numbers
prominently. v14 does three things, all first-glance:
1. Date 120px DejaVu Serif -> 170px Liberation Serif Bold at 2x
   (60 -> 85 display, +42%), the single biggest first-glance change;
   DejaVu Serif is too wide (144px = 2166px, overflows the 2048 page),
   Liberation Serif Bold 170px = 1938px and fits. The masthead grows
   78px (rule 140->218).
2. New ink italic dek under the date (28px at 2x, serif italic, INK
   not red so the red=3 rule holds): "COP31 collapses in Antalya ·
   Russia's 400-drone barrage on Ukraine · Iran claims strikes on US
   bases in Bahrain" — the top 3 stories, exactly like both 11-22
   winners. "ALL TIMES UTC" is dropped (the timeline header says
   THE DAY IN UTC); "36 STORIES · 12 PINS" moves to the dek line,
   right-aligned. No story, date, number or source changes.
3. Numbers bigger: largest 56->68px, middle 52->60px, smallest
   40->48px at 2x (28->34 / 26->30 / 20->24 display), shared
   baseline kept at 378. The winners' numbers are ~44px display;
   34px is a big step toward that.
Space comes from the lead illustration (520->468px tall at 2x,
viewBox 1180x494 squashed 5% via preserveAspectRatio=none).
Everything below the masthead shifts +78; everything below the lead
shifts +26 (masthead +78 minus lead -52).
The self-check below pins the v14 layout strings and the v14
acceptance geometry, so a later edit cannot silently re-break a
reviewer blocker or the v14 first-glance changes.

NOT a fix (already correct, do not "fix"): Superbot claimed card 02
(Lviv) is missing and the footer tally is wrong. That is a misread.
Story 02 IS the lead ("02 · UKRAINE · 19-20 NOVEMBER · LEAD"), so the
page has 1 lead (02) + 8 cards + 27 rows = 36 stories, and the footer
"6 confirmed · 2 official · 1 claim" is correct (confirmed = lead 02 +
cards 03, 04, 05, 18, 23). No card 02 is added, the tally is untouched.

v13 fixes, in order:
1. Card 04 credit line overflow: "CONFIRMED · EURONEWS · FRANCE 24"
   ended past the card's right edge (x~759 vs card edge 754). Now
   "CONFIRMED · EURONEWS · F24", ending inside the card.
2. NOW touches "17:00": the band read "NOW17:00 · ATP FINAL". The NOW
   marker moved left (1520 -> 1500px at 2x), giving a 13px display gap
   to "17:00" (>= 8px required).
3. Red recoloured off red: the Middle East category colour #A63A2E
   reads as red, so it is now teal #2E7A7A (swatch, card 01 kicker,
   card 01 top rule). The COP31 flag in card 03 and both ship funnels
   in card 04 are now neutral grey #6B6B6B. The only red left is the
   accent red #B01E1E: banner fill, NOW marker, card-01 radar dot
   (4 source uses = 3 canvas clusters).
4. Map pin latitudes: BAH (26N) sat above ANTALYA (37N) and level with
   LVIV (50N). Reordered so LVIV cy < ANTALYA cy < BAH cy (100 < 135
   < 175 at 2x). GOF label nudged off the map top edge (to the right
   of its pin); BAH label given a 4px gap from pin 01.
5. UTC strip tick: a visible axis (thin rule + a tick mark under each
   of the four times, including one at 17:00) is now drawn under the
   time labels, so the NOW dot aligns to a real tick.
6. Sources line under the map: left at 12px (6px display). The gap
   between the mapbox bottom (1816) and the DATE CHECK top (1830) is
   only 14px at 2x, so a larger font would collide with the box or be
   truncated by ellipsis. Noted, not changed.

The self-check below pins the v14 layout strings and the v14
acceptance geometry, so a later edit cannot silently re-break a
reviewer blocker or a v14 first-glance change.
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
    """v14 self-check: fail loudly if any v14 layout string regresses.

    Reads build/front.html (the rendered page) and verifies the strings
    the v13 fix list depends on. The build fails instead of shipping a
    page that re-breaks a reviewer blocker.
    """
    path = os.path.join(HERE, "build", "front.html")
    if not os.path.isfile(path):
        raise SystemExit(f"missing {path}")
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    problems = []

    # --- v14 masthead: date 144px at 2x (72 display), ink italic dek ---
    if ".bigdate { position:absolute; left:48px; top:6px; font-family:'Liberation Serif',serif; font-size:170px;" not in html:
        problems.append("date must be 170px Liberation Serif Bold at 2x (v14: 85 display, up from 120/60)")
    if "COP31 collapses in Antalya" not in html:
        problems.append("masthead dek missing 'COP31 collapses in Antalya' (v14)")
    if "400-drone barrage on Ukraine" not in html:
        problems.append("masthead dek missing '400-drone barrage on Ukraine' (v14)")
    if "Iran claims strikes on US bases in Bahrain" not in html:
        problems.append("masthead dek missing 'Iran claims strikes on US bases in Bahrain' (v14)")
    if 'class="mastdek"' not in html:
        problems.append("masthead dek div missing (v14)")
    if "font-style:italic; font-size:28px;" not in html:
        problems.append("masthead dek must be 28px italic at 2x (v14)")
    if "ALL TIMES UTC" in html:
        problems.append("'ALL TIMES UTC' must be dropped in v14 (the timeline header says THE DAY IN UTC)")
    if '<div class="rule" style="left:48px; top:218px;' not in html:
        problems.append("masthead rule must be top 218px at 2x (v14: masthead grew 78px)")

    # --- v14 numbers: 68/60/48 at 2x, shared baseline 378 ---
    if 'font-size:68px; margin-top:20px;">700,000' not in html:
        problems.append("numbers '700,000' must be 68px / mt20 at 2x (v14)")
    if 'font-size:68px; margin-top:20px;">350,000' not in html:
        problems.append("numbers '350,000' must be 68px / mt20 at 2x (v14)")
    if 'font-size:60px; margin-top:28px;">30,000' not in html:
        problems.append("numbers '30,000' must be 60px / mt28 at 2x (v14)")
    if 'font-size:60px; margin-top:28px;">1,671' not in html:
        problems.append("numbers '1,671' must be 60px / mt28 at 2x (v14)")
    if 'font-size:48px; margin-top:40px;">856' not in html:
        problems.append("numbers '856' must be 48px / mt40 at 2x (v14)")
    if 'font-size:48px; margin-top:40px;">24' not in html:
        problems.append("numbers '24' must be 48px / mt40 at 2x (v14)")

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
    # v13 correction: story 02 IS the lead (Superbot's "missing card 02"
    # is a misread); the kicker must stay, and no card 02 may be added.
    if "02 &middot; UKRAINE" not in html:
        problems.append("lead kicker '02 · UKRAINE' missing")
    if html.count('<div class="card"') != 8:
        problems.append("cards must be exactly 8 (no card 02 may be added)")

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

    # --- timeline: 4 events + ONE clock at 17:00 (v12 step 7, v13 fixes 2+5) ---
    # The 17:00 tick keeps its label; the right chip is a time-free NOW
    # dot aligned to that tick, so the band carries exactly one "17:00".
    # v13 fix 2: the NOW marker moved left (1500px at 2x) so it clears
    # "17:00" by >= 8px display (measured 13px on the render).
    # v13 fix 5: a visible axis (rule + one tick per time, incl. 17:00)
    # is drawn under the labels, so the NOW dot aligns to a real tick.
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
            f"(found {tl_band.count('17:00')}) (v12 step 7, gate 5)"
        )
    if ">NOW</div>" not in tl_band:
        problems.append("timeline NOW dot missing (v12 step 7)")
    if 'class="nowmark" style="left:1500px;"' not in tl_band:
        problems.append(
            "NOW dot must sit at left 1500px at 2x (v13 fix 2: 13px clear "
            "of '17:00'; 1520px left only ~3px)"
        )
    if 'left:1520px' in tl_band:
        problems.append("stale NOW dot at 1520px still present (v13 fix 2)")
    # v13 fix 5: axis rule + 4 tick marks under the four times.
    if 'left:360px; top:270px; width:1540px; height:2px; background:#191919;' not in tl_band:
        problems.append("timeline axis rule missing (v13 fix 5)")
    for tx in (359, 759, 1179, 1599):
        if f'left:{tx}px; top:264px; width:2px; height:12px; background:#191919;' not in tl_band:
            problems.append(f"timeline tick mark at left {tx}px missing (v13 fix 5)")

    # --- region strip: 7 regions, 36 stories ---
    for reg in (
        "MIDDLE EAST 4", "EUROPE 7", "ASIA 8", "AMERICAS 7",
        "AFRICA 5", "OCEANIA 2", "MKT+SPORT 3",
    ):
        if reg not in html:
            problems.append(f"region strip missing {reg}")
    # v13 fix 3: the Middle East category colour is teal #2E7A7A, not
    # the deep red #A63A2E (which reads as red). It must appear exactly
    # 3 times (legend swatch, card 01 kicker, card 01 top rule), and the
    # old red must be gone from the whole file.
    if "#A63A2E" in html:
        problems.append(
            "Middle East colour #A63A2E still present (v13 fix 3: must be "
            "teal #2E7A7A, #A63A2E reads as red)"
        )
    if html.count("#2E7A7A") != 3:
        problems.append(
            f"Middle East teal #2E7A7A must occur exactly 3 times "
            f"(found {html.count('#2E7A7A')}) (v13 fix 3)"
        )

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
    # (v13 correction: confirmed = lead 02 + cards 03, 04, 05, 18, 23;
    # Superbot's "missing 6th confirmed" is the lead, not a missing card)
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

    # v13 fix 1: card 04 credit line must fit inside the card. "FRANCE 24"
    # overflowed past the card's right edge (x~759 vs edge 754); it is now
    # "F24". The old long form must be gone.
    if "FRANCE 24" in cards_html:
        problems.append(
            "card 04 source still 'FRANCE 24' (v13 fix 1: overflows the "
            "card; must be 'F24')"
        )
    if "CONFIRMED &middot; EURONEWS &middot; F24" not in cards_html:
        problems.append("card 04 source must be 'CONFIRMED · EURONEWS · F24' (v13 fix 1)")

    # v13 fix 3: the COP31 flag in card 03 is neutral grey, not red.
    if 'x="129" y="20" width="26" height="15" fill="#B01E1E"' in html:
        problems.append("COP31 flag still red #B01E1E (v13 fix 3: must be neutral)")
    if 'x="129" y="20" width="26" height="15" fill="#6B6B6B"' not in html:
        problems.append("COP31 flag must be neutral grey #6B6B6B (v13 fix 3)")

    # v13 fix 3: the ship funnels in card 04 are neutral grey, not orange/red.
    # (v11 ruling 4 called them "burnt orange" #C65D00/#D98E00; both
    # reviewers counted them as red in v12, so they go to ink-neutral grey.)
    if 'M66 46 L72 26 L78 46 Z" fill="#C65D00"' in html:
        problems.append("card 04 funnel 1 still #C65D00 (v13 fix 3: must be neutral)")
    if 'M84 46 L90 32 L96 46 Z" fill="#D98E00"' in html:
        problems.append("card 04 funnel 2 still #D98E00 (v13 fix 3: must be neutral)")
    if 'M66 46 L72 26 L78 46 Z" fill="#6B6B6B"' not in html:
        problems.append("card 04 funnel 1 must be neutral grey #6B6B6B (v13 fix 3)")
    if 'M84 46 L90 32 L96 46 Z" fill="#6B6B6B"' not in html:
        problems.append("card 04 funnel 2 must be neutral grey #6B6B6B (v13 fix 3)")
    # card 05 target centre/slash stay burnt orange (a target, not a flag/ship).
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
    for region_fill in ("#2F5D8A", "#2E7A7A", "#8A5A28", "#B97A1E", "#4A7A3D"):
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
    # v13 fix 4: pin latitudes in north-south order. Parse the three
    # Europe/Middle East pin circle cy values (2x) and require
    # LVIV (50N) < ANTALYA (37N) < BAH (26N). In v12 BAH sat above
    # ANTALYA and level with LVIV (112 vs 145 vs 108); v13 is 100/135/175.
    pin_cy = {}
    for m in re.finditer(
        r'<circle cx="(\d+)" cy="(\d+)" r="26"[^>]*><text x="\d+" y="\d+"[^>]*>(\d+)</text>',
        map_html,
    ):
        pin_cy[m.group(3)] = int(m.group(2))
    for want in ("01", "02", "03"):
        if want not in pin_cy:
            problems.append(f"map pin {want} circle not found (v13 fix 4)")
    if all(k in pin_cy for k in ("01", "02", "03")):
        if not (pin_cy["02"] < pin_cy["03"] < pin_cy["01"]):
            problems.append(
                f"pin latitudes wrong: LVIV cy={pin_cy['02']}, ANTALYA "
                f"cy={pin_cy['03']}, BAH cy={pin_cy['01']} (v13 fix 4: "
                f"need LVIV < ANTALYA < BAH)"
            )
    # v13 fix 4: GOF label off the map top edge (was y=16, crowding the
    # ALSO ON header); BAH label clear of pin 01 (was touching at x=864).
    if '<text x="702" y="16" text-anchor="middle">GOF</text>' in map_html:
        problems.append("GOF label still at the map top edge (v13 fix 4)")
    if '<text x="734" y="54">GOF</text>' not in map_html:
        problems.append("GOF label must sit right of its pin at (734, 54) (v13 fix 4)")
    if '<text x="864" y="117">BAH</text>' in map_html:
        problems.append("BAH label still touching pin 01 (v13 fix 4)")
    if '<text x="868" y="180">BAH</text>' not in map_html:
        problems.append("BAH label must sit at (868, 180), 4px clear of pin 01 (v13 fix 4)")

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
    if ".lst { position:absolute; left:1312px; top:1570px; width:704px; height:272px; }" not in html:
        problems.append("list block must be left 1312 / top 1570 / width 704 / height 272 at 2x (v12 step 1, v14 +26)")
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
    if 'style="position:absolute; left:48px; top:1842px; width:1952px;' not in html:
        problems.append("credit line must sit at top 1842px full width (v12 step 2, v14 +26)")
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

    # --- red, settled to the accent reds only (v13 fix 3, gate 3) ---
    # The brand red #B01E1E occurs 4 times in the source, which renders
    # as 3 clusters: the lead banner (1), the NOW text + its ring
    # adjacent (1), the card 01 radar dot (1). In v12 it was 5 uses =
    # 4 clusters (the 4th was the COP31 flag, now neutral grey). The
    # Middle East category is teal, the COP31 flag and ship funnels are
    # grey, so no other red remains on the canvas.
    red_uses = html.count("#B01E1E")
    if red_uses != 4:
        problems.append(
            f"brand red #B01E1E must occur 4 times in source (= 3 canvas "
            f"clusters: banner, NOW, radar dot) (found {red_uses}) "
            f"(v13 fix 3, gate 3)"
        )
    if "#B01E1E" in map_html:
        problems.append("no brand red may remain on a map pin (v12 step 5)")

    # --- vertical geometry (v12 step 2): map/lst end at 1816, credit line
    # 1816-1830, DATE CHECK top 1830, footer ends at y=1010 display ---
    if ".mapbox { position:absolute; left:48px; top:1570px; width:1240px; height:272px;" not in html:
        problems.append("mapbox must be top 1570 / height 272 at 2x (v12 step 2, v14 +26)")
    if ".dc { position:absolute; left:48px; top:1856px;" not in html:
        problems.append("DATE CHECK must be top 1856 at 2x (v14 +26)")
    if 'class="foot" style="top:2006px;"' not in html:
        problems.append("footer line 1 must be top 2006 at 2x (v14: up 10px so it ends ~1013, near v13's 1010)")
    if 'class="foot" style="top:2020px;"' not in html:
        problems.append("footer line 2 must be top 2020 at 2x (v14: ends ~1013)")

    # --- 36 story slots: 1 lead + 8 cards + 27 list rows ---
    slots = (
        html.count('<div class="leadtext">')
        + html.count('<div class="card"')
        + html.count('<div class="row">')
    )
    if slots != 36:
        problems.append(f"story slots must be 36 (found {slots})")

    if problems:
        raise SystemExit("front.html v13 check failed:\n- " + "\n- ".join(problems))
    print(
        f"front.html v14 check ok: date 170px LibSerif + ink dek + numbers 68/60/48; "
        f"1 lead + {cards} cards + 27 list rows = 36 slots; {pins} map pins "
        f"(ink, 24px numerals; LVIV<ANTALYA<BAH); clock 17:00 x1; NOW 13px "
        f"clear; red 4 source uses = 3 canvas clusters; ME teal; footer "
        f"ends 1013"
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
