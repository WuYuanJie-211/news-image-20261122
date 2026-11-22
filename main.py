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
    """v7 self-check: fail loudly if any v7 string regresses in the source.

    Reads build/front.html (the rendered page) and verifies the strings the
    v7 fix round depends on. The build fails instead of shipping a page
    that re-breaks a reviewer blocker.
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
    if problems:
        raise SystemExit("front.html v7 check failed:\n- " + "\n- ".join(problems))
    print(f"front.html v7 check ok: {badges} CONFIRMED cards, all with 2 outlets")


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
