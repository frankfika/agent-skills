---
name: polymarket-analysis
description: Analyze Polymarket prediction-market links. Use whenever the user provides a polymarket.com event/market URL or asks which outcome is more likely to win on a Polymarket market; extract the title, resolution rules, options, prices, and timing, then evaluate the likely winner using current facts, primary sources, market evidence, and calibrated reasoning.
---

# Polymarket Analysis

Analyze Polymarket links by separating the market's exact resolution criteria from the real-world question, then compare market odds with current evidence.

## Reliability Contract

- Treat a Polymarket URL as a normal public page-reading task, not a bulk scraping task. Use a few targeted requests only.
- Do not stop just because one source fails. Follow this fallback ladder until the market is understood:
  1. Read the Polymarket page itself as the primary user-facing source.
  2. Use the Gamma API with a browser-like `User-Agent` for structured event/market data.
  3. If the API is blocked or incomplete, use the visible Polymarket page text, page snippets, and any embedded market context.
  4. If the public page is partially unavailable, use search results and authoritative external sources to reconstruct the title, rules, options, and timing.
  5. If exact odds/liquidity still cannot be retrieved, continue the analysis with `current odds unavailable` and explain what is missing.
- Minimum successful answer: title/question, relevant options, resolution rule, deadline or timing, resolution credibility, manipulation/liquidity risk, current odds when available, and an evidence-backed lean. Missing price data is not a reason to abandon the analysis.

## Required Workflow

1. Parse the Polymarket link.
   - Extract the slug from URLs like `https://polymarket.com/event/<slug>` or `https://polymarket.com/market/<slug>`.
   - Prefer the Polymarket Gamma API for structured data:

```bash
curl -sS -H "User-Agent: Mozilla/5.0" "https://gamma-api.polymarket.com/events?slug=<slug>"
curl -sS -H "User-Agent: Mozilla/5.0" "https://gamma-api.polymarket.com/markets?slug=<slug>"
```
   - If an event contains multiple markets, list the child markets and prioritize the unresolved/live ones (`closed=false`, `acceptingOrders=true`, or non-null current prices). Do not assume the first child market is the one the user cares about.
   - If the API is blocked, stale, or incomplete, fall back to the Polymarket page text and other publicly available structured data.

2. Capture the market mechanics.
   - title, description, options/outcomes, current prices or probabilities
   - end date, resolution deadline, resolution source, and exact conditions for Yes/No or each option
   - whether the market is already resolved, stale, or near deadline
   - volume/liquidity when available; mention when thin liquidity makes prices noisy
   - data retrieval status: page/API/browser/search fallback used, and any fields that could not be recovered

3. Assess resolution credibility and manipulation risk.
   - Check how the market resolves: source named in the rules, Polymarket/UMA oracle flow, official source, credible reporting consensus, price feed, or subjective judgment.
   - Polymarket commonly resolves through the UMA Optimistic Oracle: a proposed outcome can pass if undisputed after a challenge period, and disputed cases can escalate to UMA voters. See official docs when needed: `https://docs.polymarket.com/developers/resolution/UMA`.
   - Rate rule credibility: `high`, `medium`, or `low`.
     - High: objective, time-stamped, primary source or deterministic feed; clear edge cases; mutually exclusive and exhaustive outcomes.
     - Medium: credible-source consensus, multiple possible interpretations, or delayed/off-platform confirmation.
     - Low: subjective language, vague terms like "released", "major", "official", "credible", "announce", "available", or edge cases that can change the intended outcome.
   - Assess whether the market price can be distorted by low liquidity, wide bid/ask spread, concentrated holders, near-resolution squeezes, stale UI prices, or incentives to dispute/propose a favorable interpretation.
   - Distinguish two probabilities: the real-world event probability and the market-resolution probability when rules/oracle interpretation may diverge.

4. Interpret the resolution rules before predicting.
   - Quote or tightly paraphrase only the key rule text needed to avoid ambiguity.
   - Identify what evidence would settle the market and what would not count.
   - If the user's natural-language question differs from the market rule, analyze the market rule.

5. Research current evidence.
   - Browse when the event is current, unresolved, time-sensitive, or source-dependent.
   - Prefer primary and authoritative sources: company investor relations, SEC filings, official blogs, official model/API docs, exchange filings, regulator pages, court records, government releases, and reputable market-data pages.
   - Use credible reporting only when primary sources are unavailable or the market explicitly resolves by media consensus.
   - Record exact dates and time zones for deadlines and announcements.

6. Evaluate outcomes.
   - Treat the Polymarket price as useful evidence, not the answer.
   - Compare market-implied odds against fundamentals, base rates, recency, incentives, timing, and known catalysts.
   - For each plausible winning option, summarize evidence for, evidence against, and key watch items.
   - Give a calibrated call: `higher probability`, `lean`, `toss-up`, or `unlikely`; include a rough probability range only when justified.

7. Respond in Chinese unless the user asks otherwise.
   - Lead with the likely winner or current best answer.
   - Then explain why in a compact, evidence-backed way.
   - Include source links used.
   - Mention uncertainty, missing data, or rule ambiguity plainly.

## Market-Specific Research Patterns

- **Corporate purchase / filing markets**: check official press releases, investor relations, SEC 8-K/10-Q/10-K filings, Form 4 only when relevant, official X posts only as supporting evidence, and the market's specified announcement window.
- **Largest company / market cap markets**: compare live or latest-close market caps for all plausible contenders, usually NVIDIA, Apple, Microsoft, Alphabet, Amazon, Meta, and Saudi Aramco if the rule includes non-US firms. Note share-price movements needed to overtake the leader.
- **AI model release markets**: check official company announcement pages, model docs, API model lists, system cards, help-center release notes, and public availability. Rumors, leaks, closed beta access, or internal codenames do not count unless the market rules say they do.
- **Political / legal / macro markets**: use official government calendars, court dockets, bills, executive actions, election authorities, and reputable wire services; distinguish proposals from enacted or official outcomes.

## Output Shape

Use this structure for a single market:

```text
结论：<哪个选项更可能赢，概率判断>

规则要点：<市场到底如何结算>
当前赔率：<选项和价格，如可得>
数据获取：<网页/API/浏览器/搜索兜底；缺失项如有>
结算可信度：<高/中/低；是否存在 UMA/规则解释/流动性/争议风险>
事实依据：<最关键的 3-5 条事实，带日期和来源>
逻辑判断：<为什么这个选项更强；主要反例是什么>
需要盯的信号：<临近结算前最可能改变判断的事件>
```

For multiple links, use one short section per link and finish with a ranked summary.

## Guardrails

- Do not present rumors or community speculation as facts.
- Do not assume the market title is enough; always inspect the description/resolution criteria.
- Do not rely only on model memory for recent events.
- Do not guarantee outcomes or frame analysis as financial advice.
- Do not conflate "what happened in reality" with "what Polymarket/UMA is likely to resolve"; call out the gap when it matters.
- Do not ignore market microstructure: a price in a thin market may reflect liquidity, spread, or holder incentives more than true probability.
- If the market has already resolved, report the resolved outcome first, then explain whether it matched the pre-resolution evidence.
