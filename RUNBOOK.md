# Fin Ticks — automated carousel cycle (RUNBOOK)

You are running ONE scheduled cycle for the Instagram account **@finticksmalayalam** ("Fin Ticks — Your Daily Market Pulse"), an English-language financial news brand for Indian investors. Each cycle publishes **exactly one** 5-slide carousel, **fully automatically — do not ask the user for approval**. Work through every step below in order. Time zone is always IST (Asia/Kolkata).

Fixed facts:
- Instagram account id (Windsor.ai connector `instagram`): `17841467826754821`
- Publishing tool: Windsor.ai `execute_action`, connector `instagram`, action `create_carousel_post`
- Public image host: this repo, served from `https://raw.githubusercontent.com/madhurrasoolksd-debug/insta-carousels-finticks/main/<path>`
- Renderer: `python3 pipeline/render.py <post.json> <outdir>` → `slide-1..5.png` and `.jpg` (1080×1350)
- Worked example of a finished post: `posts/2026-11-08-afternoon/` (post.json, caption, record.json)

## 0. Setup
1. Repo is already cloned (see the scheduled task prompt). `git pull` first so the history is current.
2. Check `python3 -c "import playwright, PIL"`. If missing: `pip install --break-system-packages playwright pillow && python3 -m playwright install chromium`.
3. Read `log/history.json` (all past posts), `log/learnings.md` (if present) and the last 3 `posts/*/record.json`.
4. Post folder for this run: `posts/<YYYY-MM>/<YYYY-MM-DD>-<cycle>/` (one sub-folder per month keeps each directory well under GitHub's 3,000-entry limit) where cycle is `morning`, `afternoon` or `evening`. **If that folder already has a record.json with status `published`, stop: this cycle already ran.** Never publish twice for one cycle.

## 1. Research (aim for 10–20 searches)
Cycle focus (still pick the most important story overall):
- **morning (≈8 AM)**: overnight US/global close, Asian open, GIFT Nifty, crude/gold/rupee, pre-market India, results due today, overnight corporate/regulatory announcements.
- **afternoon (≈1 PM)**: midday Indian market moves, results and corporate announcements released this morning, RBI/SEBI circulars, IPO subscriptions/listings, Asian/European developments.
- **evening (≈7 PM)**: Indian market close (Sensex/Nifty levels, sectors, FII/DII data), results after hours, US pre-market/macro data, central-bank decisions, big policy news.
- Weekends/holidays: markets are shut — prioritise weekly wrap, policy/regulatory news, global events, week-ahead (results calendar, IPOs, data releases). Never describe a closed market as moving today.

Cover: NSE/BSE, Sensex/Nifty, US markets, major companies, earnings, IPOs, M&A, RBI/SEBI/Fed/other central banks, inflation/rates/GDP, banking/fintech, commodities (gold, crude), currencies, market-moving geopolitics, global economy.

Prefer: Reuters, Bloomberg, CNBC/CNBC-TV18, Economic Times, Moneycontrol, Business Standard, Financial Times, Mint, PTI, official NSE/BSE/RBI/SEBI/company IR pages. Use WebSearch with mode "standard" first, "extended" when results look stale; WebFetch articles for exact figures.

## 2. Freshness and verification (mandatory)
For each candidate:
- Find the ORIGINAL publication date/time. It must be new since the previous cycle (normally within the last ~12 hours; evening may use the day's close). Reject republished old stories and old developments getting renewed attention.
- Confirm every number you will use in **at least two credible sources**, or one primary/official source. If sources disagree, use the figure two sources agree on, or leave it out. Note every discrepancy in record.json.
- Reject anything you cannot verify as current. **Never invent statistics, quotes, announcements or market moves.** Never fabricate a story — if the top categories are thin, research other categories until you find a verified, genuinely important one.

## 3. Rank and pick ONE story
Score each shortlisted story out of 100:
- Market impact 25 · Relevance to Indian investors/traders 20 · Economic significance 15 · Company/industry impact 10 · Novelty/timeliness 15 · Public interest 10 · Engagement potential 5.
Duplicate check against `log/history.json`: do not repeat a story already posted, and avoid repeating the same main topic tag as the previous two posts (e.g. three Sensex-rally posts in a row) unless there is a genuinely major new development. Prefer real financial significance over trending headlines.

## 4. Write the 5 slides (post.json)
Exactly 5 slides, one cohesive story, in this order and these renderer types:
1. `cover` — ATTENTION HEADLINE. `kicker` (short context tag), `title` (≤ 8 words, curiosity-driven, never misleading; wrap 1–3 words in `*…*` for orange), optional `stat` + `stat_label` + `stat_sub` (the single most important verified number), optional `compare` (exactly 2 boxes `{k, v, tone: up|dn|or}`). Do not use both `sub` and `compare`.
2. `facts` — WHAT HAPPENED. `title`, `stats` (exactly 4 cards `{k, v, d, tone}`; `v` ≤ 8 characters), `points` (2–3 bullets, ≤ 90 characters each). Facts, figures, companies, dates.
3. `chart` — WHY IT MATTERS. `title`, `caption` (what/when the bars show), `bars` (4–7 real verified % values `{name, v, hl}`), `why` (exactly 4 boxes `{h, t}`, `t` ≤ 55 characters). Who is affected and why. If there is no honest bar data, use type `facts` again with a "why" focus rather than inventing bars.
4. `split` — MARKET IMPACT. `actual` (3 verified reactions that already happened) vs `watch` (3 things to watch — clearly forward-looking, no unsupported predictions), optional `note` (context/disclaimer, ≤ 140 characters).
5. `takeaways` — KEY TAKEAWAYS. 3 points (≤ 95 characters each), `cta` "Follow for daily market news that matters" (or a close variant).
Top-level `sources`: short publication list with dates, e.g. "Reuters, Business Standard, NSE (Nov 9, 2026)". `**bold**` = white emphasis, `*text*` = orange accent.

Render: `python3 pipeline/render.py posts/<folder>/post.json posts/<folder>/` . If it exits with an overflow error, shorten the named slides and re-render. Then **look at all 5 PNGs with the Read tool**: check spelling, numbers vs record, nothing clipped or overlapping, the story flows 1→5. Fix and re-render until clean. Delete the .png/.html files before committing; keep the .jpg files.

## 5. Caption (caption.txt) — SEO
Structure:
1. First line = hook that **contains the primary search keyword** (e.g. "Sensex and Nifty rally 10% while Wall Street crashes 📈").
2. What happened (2–3 sentences, key figures).
3. Why it matters.
4. Secondary keywords woven in naturally (company names, index names, sector, policy terms). No keyword stuffing.
5. One genuine discussion question.
6. "Follow @finticksmalayalam for daily stock market news that matters."
7. "Sources: …. Not investment advice."
8. Last line: **exactly 5 hashtags**, specific to the story (mix 1–2 broad like #StockMarketIndia, #Sensex, #Nifty50 with 3–4 topic-specific). No banned/irrelevant/over-broad tags (#love, #instagood, #money, #trading alone).
Check with code: total ≤ 2,200 characters and `len(re.findall(r"#\w+", caption)) == 5`.

## 6. Record (record.json)
Write `posts/<folder>/record.json` like the example: cycle, headline, original_publication (source, time, url for each), official_announcement_url, verification_timestamp, importance_score, shortlist (with scores and rejection reasons), selection_reason, key_facts (each fact with its sources), discrepancies_resolved, seo_keywords {primary, secondary[]}, alt_text (one sentence per slide), status, caption.

## 7. Host the images
First make the story card: `python3 pipeline/story.py posts/<folder>` → `posts/<folder>/story.jpg` (1080×1920, cover slide inside a "New post" frame). Look at it with the Read tool.
`git add posts/<folder>` (jpgs incl. story.jpg, post.json, caption.txt, record.json), commit with message "Add <folder> carousel" and the trailer lines `Co-Authored-By: Claude <noreply@anthropic.com>`, then `git pull --rebase && git push`. Then curl each of the 5 raw URLs; all must return 200 `image/jpeg` (retry for up to 2 minutes — raw.githubusercontent can lag).

## 8. Publish (fully automatic)
Call `execute_action` (connector `instagram`, action `create_carousel_post`, account `17841467826754821`) with `image_urls` = the 5 raw URLs in order 1→5 and `caption` = caption.txt.
- On error: record it, wait ~60 s, and **before retrying** check with `get_data` (fields `media_id, media_permalink, media_caption, timestamp`, `date_preset: "last_1dT"`) that the post did not actually go out. Retry up to 3 times in total.
- **Verify**: `get_data` with fields `media_id, media_permalink, media_type, timestamp`, filter `media_id eq <id>`, `date_preset "last_1dT"` (do not use force_refresh — trial plan). Only a returned permalink counts as success. Never report a post as published without it.

## 8b. Share to story (only after the carousel is verified live)
Call `execute_action` (connector `instagram`, action `create_story`, account `17841467826754821`) with `image_url` = the raw URL of `posts/<folder>/story.jpg` (curl it first: 200 `image/jpeg`). Stories take no caption. Make **one** attempt plus at most one retry after ~60 s. A story failure must never block or undo the carousel — just record `story: {status, media_id or error}` in record.json and mention it in the summary. Never post a story if the carousel did not publish.

## 9. Log and learn
- Update record.json status → `published` with `published: {media_id, url, time}` (or `failed` with the error).
- Append to `log/history.json`: `{date, cycle, story, score, topic_tags, url, time, status}`.
- Performance: pull `get_data` for the last 14 days with fields `media_id, media_permalink, timestamp, media_reach, media_views, media_like_count, media_comments_count, media_shares, media_saved, media_follows, media_engagement` and write `log/performance.json` (engagement rate = media_engagement / media_reach). In the **evening** cycle, append 3–5 dated bullet learnings to `log/learnings.md` (which hooks, topics, formats and hashtags earn the most saves/shares/follows) and apply them in later cycles — but never trade accuracy for engagement.
- Commit and push the log changes.

## 10. Finish
End with a short summary: story, score, post URL, story shared yes/no (or the failure and what was tried). If publishing failed after retries, say so plainly at the top so the user is notified.
