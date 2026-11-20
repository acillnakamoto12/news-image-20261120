# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/acillnakamoto12/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/acillnakamoto12/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world's news of Friday, 20 November 2026: Trump, Xi and Putin signing a peace declaration in Shenzhen, the UN court ruling that Myanmar committed genocide, a Houthi missile damaging Riyadh's PIF Tower, Russia's overnight attack on Kyiv, the AI sell-off sinking Asian markets, and the COP31 draft dropping its fossil fuel pledge. The date it sums up is printed on the image itself.

## How it was made

`generate.py` (Python 3 + Pillow, no network) draws `entry.png` (1024×1024) from `news.json` — six stories verified against Reuters, BusinessWorld, Bloomberg, Insurance Journal and COP31 reporting of 20 November 2026, laid out as a newspaper front page: masthead with the date, one lead story, five more across regions and fields. `main.ts` (Node 22, standard library only) copies the image to the output directory; it writes the same bytes on every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=8w050qy5&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
