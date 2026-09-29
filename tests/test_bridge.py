from ads_intelligence.bridge import (
    QualifiedCampaignRow,
    overlay_qualified_conversions,
    summarize_quality,
)
from ads_intelligence.models import SearchTermRow


def test_quality_summary_uses_qualified_leads_separately():
    rows = [
        QualifiedCampaignRow("2026-09-01", "Search", 100, 1000, 20, 8),
        QualifiedCampaignRow("2026-09-02", "Search", 50, 500, 10, 2),
    ]
    overall, campaigns = summarize_quality(rows)
    assert overall.platform_conversions == 30
    assert overall.qualified_leads == 10
    assert overall.platform_cpa == 50
    assert overall.qualified_cpa == 150
    assert round(overall.qualification_rate, 4) == 0.3333
    assert campaigns["Search"].qualified_cvr == 10 / 150


def test_qualified_search_overlay_preserves_all_traffic():
    rows = [
        SearchTermRow(
            "boks kursu",
            campaign="Search",
            ad_group="Course",
            clicks=5,
            cost=50,
            conversions=3,
            date="2026-09-01",
        ),
        SearchTermRow(
            "bedava boks",
            campaign="Search",
            ad_group="Course",
            clicks=8,
            cost=80,
            conversions=1,
            date="2026-09-01",
        ),
    ]
    lookup = {
        ("2026-09-01", "Search", "Course", "boks kursu"): 1.0,
    }
    overlaid = overlay_qualified_conversions(rows, lookup)
    assert overlaid[0].conversions == 1
    assert overlaid[1].conversions == 0
    assert overlaid[1].clicks == 8
