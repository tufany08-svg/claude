# Agent operating rules

Goal: build an advertiser-first Google Ads intelligence engine whose conclusions are explainable from raw data, statistics, and explicit business rules.

## Analytical guardrails
1. Never use Google Optimization Score or Google Recommendations as evidence.
2. Never interpret Search Impression Share as market demand. At most, describe it as estimated eligible-impression opportunity.
3. Never equate a Google Ads conversion with a qualified lead or sale without an external quality signal.
4. Keep Search, Performance Max, Display, Video, and other campaign types distinct unless a comparison is explicitly justified.
5. Prefer period comparisons and uncertainty over single-period verdicts.
6. Account for conversion lag before declaring recent traffic non-converting.
7. Do not infer causation from a coincident settings change.
8. Do not auto-apply negatives, budget moves, bids, or status changes.
9. Recommendations must expose the input metrics, thresholds, and rule that produced them.
10. Low-sample findings must be marked insufficient-data.

## Engineering
- Python 3.11+
- Keep analysis deterministic and unit-testable.
- Separate ingestion from analysis.
- Never commit credentials or real customer exports.
- Synthetic fixtures only.
- All work through branches and PRs.
- CI must pass before merge.
