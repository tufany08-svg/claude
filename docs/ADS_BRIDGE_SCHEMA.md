# Ads Bridge integration schema

The connected Google Sheet **Ads Bridge** is the canonical business-data source for this project.

## Important tabs

### 01_campaign_performance
Daily campaign metrics:
- date
- campaign_id / campaign_name
- status / channel_type
- impressions / clicks / cost
- conversions / conversion_value
- ctr / avg_cpc / conversion_rate / cost_per_conversion
- search_impression_share

### 04_search_terms
Daily search-term grain:
- campaign / ad group
- search_term
- matched_keyword
- match_type / status
- impressions / clicks / cost
- conversions / conversion_value

### 05_conversion_health
Conversion action by campaign/day.

### 07_change_history
Change events with:
- timestamp
- resource_type
- operation
- campaign / ad_group
- changed_fields

This is used only for temporal association. A nearby change does not prove causality.

### 11_budget_impression_share
Daily campaign:
- budget_amount
- cost
- search_impression_share
- search_budget_lost_is
- search_rank_lost_is

Guardrail: Search IS is **not market demand**. Lost IS may help describe eligible-impression opportunity constraints.

### 12_pmax_channel_performance
Performance Max by asset group and network:
SEARCH / YOUTUBE / MAPS etc.

PMax must not be analyzed as one opaque conversion bucket when channel-level detail is available.

### 13_pmax_conversion_detail
PMax conversion action + network detail.

This is critical because local actions such as directions/engagements may inflate all-conversions without representing the same business value as WhatsApp or phone contact.

### 15_qualified_campaign_daily
This is the primary campaign outcome table.

Fields include:
- conversions_all
- qualified_lead_conversions
- qualified_lead_cpa
- qualified_lead_cvr

**Qualified leads outrank raw platform conversions for optimization decisions.**

### 16_conversion_actions
Maps conversion actions to `is_qualified` and exposes qualified contribution.

### 17_qualified_search_terms_daily
Qualified-lead outcomes at search-term grain.

This should be preferred over raw search-term conversions whenever a matching qualified row exists.

## Analytical hierarchy

1. Qualified lead / business-quality outcome
2. Raw conversion by conversion action
3. Click / cost / traffic efficiency
4. Impression-share opportunity diagnostics
5. Platform-provided metrics

Platform recommendations and Optimization Score are excluded entirely.
