# Methodology

The platform supplies measurements. The advertiser supplies goals. The engine supplies transparent calculations.

## Metrics
CTR = clicks / impressions; CPC = cost / clicks; CVR = conversions / clicks; CPA = cost / conversions; ROAS = conversion value / cost.

Missing denominators return no rate rather than infinity or a fabricated value.

## Search-term evidence
Search queries are decomposed into 1/2/3-grams. A gram is counted at most once per query.

For zero-conversion grams, with baseline CVR p and N clicks:

    P(X=0) = (1-p)^N

Only statistically surprising zeroes that also pass sample thresholds become WASTE_SIGNAL.

When target CPA exists:

    required CVR = average CPC / target CPA

If the 95% Wilson upper confidence bound for observed CVR is still below required CVR, the gram becomes EFFICIENCY_RISK.

Protected phrases and active-keyword collisions cannot become automatic negative candidates.

## Limits
This does not establish causality, lead quality, incrementality, true market demand, or profitability without external evidence.
