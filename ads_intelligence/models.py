from dataclasses import dataclass, asdict
from typing import Any

@dataclass(slots=True)
class CampaignRow:
    campaign: str
    impressions: float = 0
    clicks: float = 0
    cost: float = 0
    conversions: float = 0
    conversion_value: float = 0
    date: str | None = None

@dataclass(slots=True)
class SearchTermRow:
    search_term: str
    campaign: str = ""
    ad_group: str = ""
    keyword: str = ""
    impressions: float = 0
    clicks: float = 0
    cost: float = 0
    conversions: float = 0
    conversion_value: float = 0
    date: str | None = None

@dataclass(slots=True)
class MetricSet:
    impressions: float = 0
    clicks: float = 0
    cost: float = 0
    conversions: float = 0
    conversion_value: float = 0

    @property
    def ctr(self): return self.clicks / self.impressions if self.impressions else None
    @property
    def cpc(self): return self.cost / self.clicks if self.clicks else None
    @property
    def cvr(self): return self.conversions / self.clicks if self.clicks else None
    @property
    def cpa(self): return self.cost / self.conversions if self.conversions else None
    @property
    def roas(self): return self.conversion_value / self.cost if self.cost else None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d.update(ctr=self.ctr, cpc=self.cpc, cvr=self.cvr, cpa=self.cpa, roas=self.roas)
        return d

@dataclass(slots=True)
class NgramFinding:
    ngram: str
    n: int
    distinct_terms: int
    clicks: float
    cost: float
    conversions: float
    verdict: str
    action: str
    rationale: str
    p_zero: float | None = None
    wilson_upper: float | None = None
    protected: bool = False
    keyword_collision: bool = False
