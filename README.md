# The Monday Ledger — 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Hellboys87/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Hellboys87/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A newspaper front page that sums up the world's news of **Monday 23 November 2026** in one image — an entry for the make.fun [news-image-20261123](https://make.fun/bounty/news-image-20261123) bounty ($100 in USDC, 50 paid places).

Lead story: COP31 in Antalya ends in failure — no deal, after the draft dropped all mention of fossil fuels. Also covered: the Sparta II ablaze in the Gulf of Finland, Russian missiles on Polish soil and today's NATO council, the Kyiv-region drone strike, Estonia sealing its Russian border, the UK–EU Brexit reset, the Cikande factory fire, South Korea's AI exam-cheating resignation, the ICJ's genocide ruling on Myanmar, and sport — England 37–12 New Zealand and India's record 720/9.

## How it works

`entry.png` is pre-drawn locally by `render.py` (PIL + DejaVu fonts, run on the builder's machine). The shipped program, `main.ts`, is Node 22 standard library only: it just copies that finished image to the output directory, so it needs no fonts, no packages and no network, and every run writes identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png (1024x1024 PNG, under 1 MiB)
```

To re-draw the front page from scratch:

```sh
python3 render.py   # writes entry.png
```

## License

MIT — see [LICENSE](LICENSE).
