from collections import defaultdict
from .models import MetricSet

def aggregate(rows):
    result = MetricSet()
    for row in rows:
        result.impressions += row.impressions
        result.clicks += row.clicks
        result.cost += row.cost
        result.conversions += row.conversions
        result.conversion_value += row.conversion_value
    return result

def group_by_campaign(rows):
    groups = defaultdict(MetricSet)
    for row in rows:
        g = groups[row.campaign or "(unknown)"]
        g.impressions += row.impressions
        g.clicks += row.clicks
        g.cost += row.cost
        g.conversions += row.conversions
        g.conversion_value += row.conversion_value
    return dict(groups)

def relative_delta(current, previous):
    if current is None or previous in (None, 0):
        return None
    return (current - previous) / previous
