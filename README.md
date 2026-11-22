# One image of 21 November 2026's world news

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) [![rank](https://make.fun/badge/news-image-20261121/nothing010101/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) [![reward](https://make.fun/badge/news-image-20261121/nothing010101/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Entry for the [make.fun](https://make.fun) bounty
[`news-image-20261121`](https://make.fun/bounty/news-image-20261121): sum up
Saturday 21 November 2026's world news in one image.

## What it draws

A dense newspaper front page, "THE WORLD IN ONE DAY — SATURDAY 21 NOVEMBER
2026 — 36 STORIES, 7 REGIONS": one lead story and a 4x9 grid of 35 more,
plus a "by the numbers" box. Same density as the winning 20 Nov entries
(33–36 stories).

- **Lead — Iran strikes US bases in Bahrain.** Tehran says it hit two US
  positions; Bahrain reports an industrial fire, no injuries.
- **AI sell-off pushes US into correction** · **FBI and USDA hacked** ·
  **Democrats win 259 House seats** · **US loses measles-free status** ·
  **Bayer pays $7.25bn over Roundup** · **Mamdani: close Rikers by 2032** ·
  **GTA VI makes $3.79bn in a day** · **Riemann proof verified** ·
  **COP31 runs past deadline** · **Denmark: Russia murder plot** ·
  **Russian ship ablaze off Finland** · **France seeks UN action on Myanmar**
  · **EU-Indonesia deal signed** · **EU budget: 1.78tn euro plan** ·
  **Belgium strike to ground all flights** · **Russian missile hits Kryvyi Rih**
  · **Two tankers hit near Hormuz** · **Houthis hit Riyadh skyscraper** ·
  **Basra power plant fire kills four** · **Lebanon: Israel must withdraw** ·
  **US, Israel weigh new Iran strikes** · **Suneung exam cheating scandal** ·
  **Indonesia fires burn 7.1m acres** · **Air Niugini jet in emergency landing**
  · **Afghan mortar blast kills four students** · **Quad, ASEAN summits:
  takeaways** · **Bangladesh dengue: 3 more dead** · **Iran pitches 3 plans at
  SCO forum** · **Nigeria boat capsize kills 24** · **S. Africa: 600 women
  killed** · **ANC fights to keep key cities** · **Mexico captures Chapo
  Isidro** · **Peru quake 6.9 shakes Andes** · **Argentina okays $50bn LNG
  project** · **Haiti: three dead after blast**.

Every story was verified against real reporting dated Saturday 21 November
2026 (OneTurn 21 Nov day report, Reuters, CNN, WSJ, AP, Al Jazeera, The
Hindu, UN News, IANS, France 24, Scientific American, IntelChron 21 Nov
brief, InformedClearly 21 Nov summary, Horizon 21 Nov). See `report.md` for
the full list with sources.

## Run

```sh
python3 main.py   # writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output)
```

Pure Python 3.13 standard library, no network, deterministic — two runs
write byte-identical output. The program draws the PNG itself (own PNG
encoder, drawing primitives and 5x7 bitmap font); 1024x1024, ~37 KB.
