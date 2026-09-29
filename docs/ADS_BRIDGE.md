# Ads Bridge integration

Ads Bridge is the live data source for account analysis. The source spreadsheet remains read-only and real account data is never committed to this public repository.

## Relevant tabs

| Logical source | Ads Bridge tab | Purpose |
|---|---|---|
| Campaign daily | 01_campaign_performance | Daily campaign metrics and channel type |
| Ad group daily | 02_ad_group_performance | Ad-group performance |
| Keyword daily | 03_keyword_performance | Keyword and match-type performance |
| Search terms | 04_search_terms | Query-level traffic and matched keyword |
| Conversion health | 05_conversion_health | Conversion-action health |
| Change history | 07_change_history | Account changes for before/after context |
| Geo | 08_geo_performance | Location performance |
| Device | 09_device_performance | Device performance |
| Time | 10_time_performance | Day/hour performance |
| Budget / IS | 11_budget_impression_share | Budget, eligible impression share and loss components |
| PMax channel | 12_pmax_channel_performance | Asset-group performance by network |
| PMax conversion detail | 13_pmax_conversion_detail | Conversion action by PMax network |
| PMax placements | 14_pmax_placements | Placement exposure |
| Qualified campaign daily | 15_qualified_campaign_daily | Qualified-lead CPA/CVR at campaign level |
| Conversion actions | 16_conversion_actions | Which conversion actions count as qualified |
| Qualified search terms | 17_qualified_search_terms_daily | Qualified leads attributable to visible queries |

## Analytical priority

The engine keeps two layers separate:

1. Platform conversion performance.
2. Qualified-lead performance.

Qualified-lead metrics are preferred for business-quality conclusions whenever the quality tabs are available. Platform conversions remain useful as a funnel/tracking signal, not as a substitute for qualified leads.

## Search-term quality join

The qualified-search-term tab is sparse by design. It should not be analysed on its own because doing so would discard zero-qualified-lead traffic.

Instead:

1. read the full search-term traffic from `04_search_terms`;
2. aggregate qualified leads from `17_qualified_search_terms_daily`;
3. join on date + campaign + ad group + normalized search term;
4. assign zero qualified leads to unmatched visible queries;
5. run intent and n-gram analysis on the full traffic set using qualified leads as the conversion signal.

This prevents selection bias.

## Impression share

`11_budget_impression_share` is useful for diagnosing eligible-impression opportunity and whether loss is budget- or rank-associated. It is not treated as a direct measurement of total market demand.

## Change history

A nearby account change is context, not proof of causality. The future attribution layer should report temporal association and require stronger evidence before describing a change as causal.

## Data handling

- No customer IDs, user emails, real queries, credentials, or raw Ads Bridge rows belong in git.
- Tests use synthetic fixtures only.
- Live reads happen through the connected Drive surface in Chat.
