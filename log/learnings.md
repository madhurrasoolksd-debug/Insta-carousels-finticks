# Learnings

- 2026-11-08: First post (Sensex 7-day rally vs Wall Street crash). Baseline - no data yet.

- 2026-11-08 (evening review): Windsor insights still report 0 reach/engagement for both posts (cached data lags on the trial plan), so there is no performance signal yet. Do not draw conclusions until at least 24-48h of data exist.
- 2026-11-08: Back-to-back Muhurat posts (afternoon preview, evening result) - next cycles should switch topic (earnings, macro, global, IPOs) to avoid topic fatigue.
- 2026-11-08: Year-in-review numbers (Samvat returns, FPI flows) vary widely between outlets; computing returns from verified closing levels and stating the basis avoided publishing conflicting figures.
- 2026-11-08: Hypothesis to test: contrast hooks ("X fell, Y rose") and a bar chart of index returns are save-friendly; compare saves/shares of the two Nov 8 posts once data arrives.

- 2026-11-09 (evening review): Insights for all 5 posts (Nov 8-9) still read 0 on Windsor's cached trial data, ~36h after the first post. Still no performance signal; if zeros persist past 72h, treat it as a data-pipeline issue (cache/permissions), not as real zero reach.
- 2026-11-09: Rotating topics worked for sourcing (AI/Nvidia -> FPI tax -> brokerage calls/market close); keep that rotation and avoid two market-close posts in a row on Wednesday when markets reopen.
- 2026-11-09: Brokerage target stories (Citi 28,000, HSBC overweight) pair well with the evening close; always label targets as forecasts and give the upside basis only when two sources agree.
- 2026-11-09: Single-source 'nice' stats (Citi's prior 26,000 target, PSU bank individual moves, breadth) were dropped; check two-source coverage before drafting slides to avoid rework.
- 2026-11-09: Renderer overflow on 'split' slides when bullets exceed ~40 chars; draft split bullets short from the start. Hyphenated words (e.g. '8-month') can break awkwardly in cover/section titles - avoid them in titles.

- 2026-11-10 (evening review): Windsor insights still ~0 for all 6 posts (only Nov 9 evening shows reach 1, views 2) about 3 days after the first post; treat as a trial-plan data lag, not real zero reach. No performance conclusions possible.
- 2026-11-10: Holiday-day cycles (markets shut) are thin on fresh Indian news; a reopen-preview angle (GIFT Nifty + previously verified closes) works but overlaps earlier topics. Plan 'week-ahead'/macro (US CPI, trade deal) stories earlier in the day to avoid repeats.
- 2026-11-10: Research budget (8 searches) ran out before the 7 PM IST US CPI release; for evening cycles on CPI days, spend fewer searches on generic Indian-market queries (results were stale/noisy) and target the scheduled event directly.
- 2026-11-10: Single-source live figures (e.g. GIFT Nifty level) should be stated approximately and attributed; exact levels with mismatched bases were dropped.

- 2026-11-11 (evening review): Windsor insights remain ~0 for all 11 posts (max reach 1, views 3 on the Nov 11 afternoon post); still a trial-plan data lag, no performance conclusions possible.
- 2026-11-11: Standard searches returned mostly 2025 pages for same-day close; one 'extended' search with the exact date plus 'market close report' found the Nov 11 2026 HDFC Sky/Business Standard reports. For evening cycles, use that query pattern early.
- 2026-11-11: Same-day close figures were mostly single-source beyond index levels; sector/stock moves, FPI totals and breadth were dropped. Verified index levels were cross-checked by arithmetic against prior closes (81,879.40-772.75 = 81,106.65).
- 2026-11-11: Angle 'gains pared from early +1.5%' differentiated the close post from the afternoon opening post; avoid a third Sensex/Nifty-level post tomorrow unless a major new development.

- 2026-11-12: Two consecutive cycles (morning, afternoon) failed to find a verified fresh story; standard searches return Nov 12 2025 pages for 'Nov 12' queries. Use exact-phrase queries with '2026' plus specific events (e.g. named company + 'Q2 FY27') early, and spend at most 2 searches on generic market queries.

- 2026-11-12 (evening review): Windsor insights still ~0 for all 12 posts (max reach 3, views 5 on Nov 11 afternoon; zero likes/saves/shares/follows anywhere). Data lag or tiny audience; no performance conclusions possible.
- 2026-11-12: Evening search pattern 'Sensex Nifty closing <date> market close report' (extended) surfaced same-day HDFC Sky/Business Standard reports immediately; reuse it. A multi-day theme (FPI flows) with two older sources plus same-day close gave a verifiable non-repeat topic.
- 2026-11-12: Cover stat with unit text ('₹38,971 Cr') wraps badly in the renderer; put the unit in stat_label instead.
- 2026-11-12: Sandbox checkout may be a detached HEAD behind origin/main; use 'git fetch && git rebase origin/main && git push origin HEAD:main'. Do not run rm with a shell variable path (blocked); use "${F:?}".

- 2026-11-13: Third failed morning/afternoon cycle in 2 days. Search engine mostly returns 2025 pages for date queries; same-day pre-market pages (DSIJ, HDFC Sky, 5paisa) appear but WebFetch often errors. Next time spend the first 2 searches on site-specific queries (hdfcsky.com "gift nifty november 13 2026", kotakneo "pre-market 13 november 2026") and use allowed_domains.

- 2026-11-14: Site-specific query with allowed_domains (hdfcsky.com, kotakneo.com, upstox.com) plus 'market close report today <date>' surfaced same-day 2026 pages immediately; generic date queries returned 2025 pages. Weekly % moves can be verified by arithmetic against prior closes stored in the repo. Saturday week-ahead searches found no 2026 sources; weekly-wrap angle worked.

- 2026-11-14 (afternoon): Saturday afternoon after a weekly-wrap morning post leaves little fresh material; 8-search budget ran out. HDFC Sky allowed_domains searches work only with a single domain (multi-domain lists were rejected by the proxy). A weekend cycle should plan a non-market angle (global policy, IPO calendar) from the first search.
