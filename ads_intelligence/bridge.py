from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .models import SearchTermRow


ESSENTIAL_TABS = {
    "campaign_performance": "01_campaign_performance",
    "ad_group_performance": "02_ad_group_performance",
    "keyword_performance": "03_keyword_performance",
    "search_terms": "04_search_terms",
    "conversion_health": "05_conversion_health",
    "change_history": "07_change_history",
    "budget_impression_share": "11_budget_impression_share",
    "pmax_channel_performance": "12_pmax_channel_performance",
    "pmax_conversion_detail": "13_pmax_conversion_detail",
    "pmax_placements": "14_pmax_placements",
    "qualified_campaign_daily": "15_qualified_campaign_daily",
    "conversion_actions": "16_conversion_actions",
    "qualified_search_terms_daily": "17_qualified_search_terms_daily",
}


@dataclass(slots=True)
class QualitySummary:
    clicks: float = 0.0
    cost: float = 0.0
    platform_conversions: float = 0.0
    qualified_leads: float = 0.0

    @property
    def platform_cpa(self) -> float | None:
        return self.cost / self.platform_conversions if self.platform_conversions else None

    @property
    def qualified_cpa(self) -> float | None:
        return self.cost / self.qualified_leads if self.qualified_leads else None

    @property
    def qualified_cvr(self) -> float | None:
        return self.qualified_leads / self.clicks if self.clicks else None

    @property
    def qualification_rate(self) -> float | None:
        return self.qualified_leads / self.platform_conversions if self.platform_conversions else None


@dataclass(slots=True)
class QualifiedCampaignRow:
    date: str
    campaign: str
    clicks: float
    cost: float
    platform_conversions: float
    qualified_leads: float


def _float(value: object) -> float:
    if value in (None, ""):
        return 0.0
    return float(value)


def _read_dicts(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_qualified_campaign_csv(path: str | Path) -> list[QualifiedCampaignRow]:
    rows: list[QualifiedCampaignRow] = []
    for raw in _read_dicts(path):
        rows.append(
            QualifiedCampaignRow(
                date=raw.get("date", ""),
                campaign=raw.get("campaign_name", ""),
                clicks=_float(raw.get("clicks")),
                cost=_float(raw.get("cost")),
                platform_conversions=_float(raw.get("conversions_all")),
                qualified_leads=_float(raw.get("qualified_lead_conversions")),
            )
        )
    return rows


def summarize_quality(
    rows: list[QualifiedCampaignRow],
) -> tuple[QualitySummary, dict[str, QualitySummary]]:
    overall = QualitySummary()
    campaigns: dict[str, QualitySummary] = {}

    for row in rows:
        campaign = campaigns.setdefault(row.campaign or "(unknown)", QualitySummary())
        for target in (overall, campaign):
            target.clicks += row.clicks
            target.cost += row.cost
            target.platform_conversions += row.platform_conversions
            target.qualified_leads += row.qualified_leads

    return overall, campaigns


def read_qualified_search_term_lookup(
    path: str | Path,
) -> dict[tuple[str, str, str, str], float]:
    lookup: dict[tuple[str, str, str, str], float] = {}
    for raw in _read_dicts(path):
        key = (
            raw.get("date", ""),
            raw.get("campaign_name", ""),
            raw.get("ad_group_name", ""),
            raw.get("search_term", "").casefold().strip(),
        )
        lookup[key] = lookup.get(key, 0.0) + _float(raw.get("qualified_lead_conversions"))
    return lookup


def overlay_qualified_conversions(
    search_rows: list[SearchTermRow],
    lookup: dict[tuple[str, str, str, str], float],
) -> list[SearchTermRow]:
    """Return search rows with platform conversions replaced by qualified-lead conversions.

    Unmatched rows intentionally receive zero qualified conversions. This lets the
    same n-gram engine evaluate all visible search traffic against the quality
    signal instead of analysing only queries that produced a qualified lead.
    """
    output: list[SearchTermRow] = []
    for row in search_rows:
        key = (
            row.date or "",
            row.campaign,
            row.ad_group,
            row.search_term.casefold().strip(),
        )
        output.append(
            SearchTermRow(
                search_term=row.search_term,
                campaign=row.campaign,
                ad_group=row.ad_group,
                keyword=row.keyword,
                impressions=row.impressions,
                clicks=row.clicks,
                cost=row.cost,
                conversions=lookup.get(key, 0.0),
                conversion_value=0.0,
                date=row.date,
            )
        )
    return output
