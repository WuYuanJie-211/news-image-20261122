#!/usr/bin/env python3
"""news-image-20261122 entrypoint: copy entry.png to /output/entry.png.

Stdlib only. No network. Deterministic: the output bytes are exactly the
input bytes, so two runs are byte-identical.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"
MAX_BYTES = 1024 * 1024


def check_front() -> None:
    """v9 self-check: fail loudly if any v7/v8/v9 string regresses in the source.

    Reads build/front.html (the rendered page) and verifies the strings the
    v7, v8 and v9 fix rounds depend on. The build fails instead of shipping a
    page that re-breaks a reviewer blocker.
    """
    import re

    path = os.path.join(HERE, "build", "front.html")
    if not os.path.isfile(path):
        raise SystemExit(f"missing {path}")
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    low = html.lower()
    problems = []
    if "weekend" in low:
        problems.append("WEEKEND still on the page (B1: use EARLIER THIS WEEK)")
    if "overnight" in low:
        problems.append("overnight still on the page (B2: use 19-20 Nov)")
    if "cet" in low:
        problems.append("CET still on the page (use 17:00 UTC)")
    if "5,640 votes cast" in html:
        problems.append("5,640 votes cast still present (B4: use 5,640 voters)")
    if "SIN</div>" in html:
        problems.append("standalone SIN pin label still present (use SINALOA)")
    if "LVIV &middot; 8 KILLED NATIONWIDE" in html:
        problems.append("old LVIV banner still present (use UKRAINE · 8 KILLED)")
    if "10 years<br>on" in html or "10 years on" in html:
        problems.append("10 years on still present (use after 10 years of talks)")
    if "EARLIER THIS WEEK" not in html:
        problems.append("EARLIER THIS WEEK missing (B1)")
    if "UKRAINE &middot; 8 KILLED" not in html:
        problems.append("UKRAINE · 8 KILLED banner missing")
    if "17:00 UTC" not in html:
        problems.append("17:00 UTC missing")
    if html.count("5,640 voters") < 2:
        problems.append("5,640 voters must appear in both the HK card and the stat (B4)")
    # v8 B1: the DATE CHECK must use the narrowed wording, not the v7
    # universal claims (Quick's v7 blocker: 35 of 36 stories show no date,
    # and Texans 19 Nov / trilateral 19 Nov sit in the main list).
    if "Every story carries the date" in html:
        problems.append(
            "v7 DATE CHECK claim still present (B1: use the narrowed wording)"
        )
    if html.count("carried above") != 1:
        problems.append(
            f"DATE CHECK must say 'carried above' exactly once "
            f"(found {html.count('carried above')}) (B1)"
        )
    if "5,709" in html:
        problems.append("derived 5,709 printed (B4: never print the derived total)")
    if "LVV" in html:
        problems.append("LVV still present (inset label must read LVIV)")
    if "AYT" in html:
        problems.append("AYT still present (inset label must read ANTALYA)")
    if 'font-size="12" font-weight="bold" fill="#FFFFFF" text-anchor="middle">B</text>' not in html:
        problems.append("inset pin B must be 12px (14px renders as a vertical bar)")
    # v9 blocker: the LEFT OUT row must use the DATE CHECK's own test
    # (completed pre-edition, not carried), not the old stricter test
    # (first reported before today's edition) that Quick's v8 blocker
    # objected to. The source encodes the apostrophe as &rsquo;, so check
    # both the entity form and the literal form, anywhere in the file.
    if (
        "first reported before today&rsquo;s edition" in html
        or "first reported before today's edition" in html
    ):
        problems.append(
            "old LEFT OUT reason still present (v9 blocker: use "
            "'completed before edition, not carried')"
        )
    if html.count("completed before edition, not carried") != 1:
        problems.append(
            f"LEFT OUT must say 'completed before edition, not carried' "
            f"exactly once (found {html.count('completed before edition, not carried')}) "
            f"(v9 blocker)"
        )
    if html.count("completed pre-edition items not carried above") != 1:
        problems.append(
            f"DATE CHECK must say 'completed pre-edition items not carried "
            f"above' exactly once "
            f"(found {html.count('completed pre-edition items not carried above')}) "
            f"(B1)"
        )
    # B3: every CONFIRMED card badge must name two outlets, scoped to the
    # big-cards block (heroes carry their sources in .src, not .so).
    cards = html[html.index("<!-- BIG CARDS"):html.index("<!-- MAP")]
    badges = len(re.findall(r'<div class="bdg b-conf">CONFIRMED</div>', cards))
    so_lines = re.findall(r'<div class="so">CONFIRMED &middot; ([^<]+)</div>', cards)
    two = [x for x in so_lines if "&middot;" in x]
    if not (badges == len(so_lines) == len(two)):
        problems.append(
            f"CONFIRMED badges ({badges}) != CONFIRMED .so lines ({len(so_lines)}) "
            f"!= two-outlet lines ({len(two)}) (B3)"
        )
    # 36 story slots: 1 lead hero + 2 side heroes + 10 big cards + 23 list rows.
    slots = (
        html.count('<div class="lead">')
        + html.count('<div class="rhero"')
        + html.count('<div class="bcard"')
        + html.count('<div class="row"')
    )
    if slots != 36:
        problems.append(f"story slots must be 36 (found {slots})")
    if problems:
        raise SystemExit("front.html v9 check failed:\n- " + "\n- ".join(problems))
    print(f"front.html v9 check ok: {badges} CONFIRMED cards, all with 2 outlets; 36 slots")


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
