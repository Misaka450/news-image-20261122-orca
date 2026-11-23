# news-image-20261122-orca

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Misaka450/news-image-20261122-orca/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Misaka450/news-image-20261122-orca/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

"The World Daily" — one 1024×1024 broadsheet front page that sums up the world's news of Sunday 22 November 2026: a red scoreboard of the day's hard numbers, a solid region band whose segment widths encode story counts, four lead stories carried by code-drawn spot illustrations, unequal editorial columns and a DATE CHECK bar. Submitted to [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)'s “Sum up 22 November's world news in one image” bounty.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the committed `entry.png` into the output directory (default `/output`). To regenerate the image from the source tables, `pip install pillow && python3 build.py`.