# news-image-20261122

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/WuYuanJie-211/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/WuYuanJie-211/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

Sum up Sunday 22 November 2026's world news in one image — a 1024×1024 newspaper front page for the make.fun [news-image-20261122](https://make.fun/bounty/news-image-20261122) bounty.

## The page

**THE WORLD — Sunday, November 22, 2026.** 36 stories, three heroes with real photos in the headline slots, a world map with numbered pins, and a DATE CHECK box.

See `news-20261122.md` for the locked story list, fact sources, and layout decisions.

## How it is made

`build/front.html` is the front page (pure HTML + CSS typography, DejaVu Serif/Sans, no AI photo), rendered at 1024×1024 with headless Chromium into `entry.png`. `main.py` (Python 3.13, standard library only) byte-copies `entry.png` to `/output/entry.png` and self-checks that it is a whole PNG within the 1024×1024 / 1 MiB gate. Two renders are byte-identical, and two `main.py` runs are byte-identical.
