import json, re
from dataclasses import dataclass
from pathlib import Path
from .models import MetricSet

@dataclass(slots=True)
class IntentRules:
    priority: list[str]
    patterns: dict[str,list[str]]
    fallback: str = "other"

def load_rules(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return IntentRules(list(data.get("priority",[])), {k:list(v) for k,v in data.get("patterns",{}).items()}, str(data.get("fallback","other")))

def classify_intent(term, rules):
    for label in rules.priority:
        for pattern in rules.patterns.get(label,[]):
            if re.search(pattern, term, flags=re.I):
                return label
    return rules.fallback

def aggregate_intents(rows, rules):
    out = {}
    for row in rows:
        label = classify_intent(row.search_term, rules)
        m = out.setdefault(label, MetricSet())
        m.impressions += row.impressions; m.clicks += row.clicks; m.cost += row.cost
        m.conversions += row.conversions; m.conversion_value += row.conversion_value
    return out
