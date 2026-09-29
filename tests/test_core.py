from ads_intelligence.csv_loader import parse_number
from ads_intelligence.metrics import aggregate, group_by_campaign
from ads_intelligence.models import CampaignRow, SearchTermRow
from ads_intelligence.ngram import analyze_ngrams, wilson_upper
from ads_intelligence.intent import IntentRules, classify_intent, load_rules

def test_number_locales():
    assert parse_number("1,234.50")==1234.5
    assert parse_number("1.234,50")==1234.5
    assert parse_number("125,50")==125.5

def test_metrics():
    rows=[CampaignRow("Search",1000,100,500,10,1000),CampaignRow("Search",500,50,250,5,500)]
    m=aggregate(rows)
    assert m.clicks==150 and m.cpa==50
    assert group_by_campaign(rows)["Search"].cost==750

def test_intent():
    rules=IntentRules(
        ["transactional","research"],
        {"transactional":["fiyat"],"research":["nasıl"]},
    )
    assert classify_intent("boks kursu fiyat",rules)=="transactional"
    assert classify_intent("boks nasıl yapılır",rules)=="research"

def test_default_rules_file():
    rules=load_rules("rules/default.json")
    assert classify_intent("boks kursu fiyat",rules)=="transactional"
    assert classify_intent("boks nasıl yapılır",rules)=="research"

def test_statistical_zero_and_collision():
    rows=[
        SearchTermRow("free boxing class one",clicks=20,cost=200,conversions=0),
        SearchTermRow("free boxing class two",clicks=20,cost=200,conversions=0),
        SearchTermRow("boxing course paid",clicks=100,cost=500,conversions=20),
    ]
    f=analyze_ngrams(rows,min_clicks=10,min_cost=100,min_distinct_terms=2)
    free=next(x for x in f if x.ngram=="free")
    assert free.verdict=="WASTE_SIGNAL" and free.action=="NEGATIVE_CANDIDATE"
    f2=analyze_ngrams(rows,min_clicks=10,min_cost=100,min_distinct_terms=2,active_keywords=["free boxing"])
    free2=next(x for x in f2 if x.ngram=="free")
    assert free2.action=="REVIEW" and free2.keyword_collision

def test_wilson():
    assert 0 < wilson_upper(2,20) < 1
