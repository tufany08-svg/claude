import csv, re
from pathlib import Path
from .models import CampaignRow, SearchTermRow

ALIASES = {
 "campaign": {"campaign","campaign name","kampanya","kampanya adı"},
 "ad_group": {"ad group","ad group name","reklam grubu","reklam grubu adı"},
 "search_term": {"search term","query","arama terimi","arama sorgusu"},
 "keyword": {"keyword","keyword text","anahtar kelime"},
 "impressions": {"impressions","impr","gösterimler","gösterim"},
 "clicks": {"clicks","tıklamalar","tıklama"},
 "cost": {"cost","maliyet","harcama","spend"},
 "conversions": {"conversions","conv","dönüşümler","dönüşüm"},
 "conversion_value": {"conversion value","conv value","conv. value","dönüşüm değeri","conversion_value"},
 "date": {"date","day","tarih","gün"}
}

def _h(v):
    v = (v or "").replace("\ufeff","").strip().casefold().replace("_"," ")
    return re.sub(r"\s+"," ",v)

def parse_number(value):
    text = str(value or "").strip()
    if not text or text in {"--","-","n/a","N/A"}: return 0.0
    text = re.sub(r"[^0-9,.\-]","",text)
    if "," in text and "." in text:
        text = text.replace(".","").replace(",",".") if text.rfind(",") > text.rfind(".") else text.replace(",","")
    elif "," in text:
        p = text.split(",")
        text = p[0].replace(".","")+"."+p[1] if len(p)==2 and len(p[1]) in {1,2} else text.replace(",","")
    return float(text)

def _rows(path):
    raw = Path(path).read_text(encoding="utf-8-sig")
    try: dialect = csv.Sniffer().sniff(raw[:4096], delimiters=",;\t")
    except csv.Error: dialect = csv.excel
    return [{_h(k):(v or "").strip() for k,v in r.items() if k} for r in csv.DictReader(raw.splitlines(), dialect=dialect)]

def _v(row,name):
    for a in ALIASES[name]:
        if _h(a) in row: return row[_h(a)]
    return ""

def read_campaign_csv(path):
    return [CampaignRow(_v(r,"campaign"),parse_number(_v(r,"impressions")),parse_number(_v(r,"clicks")),parse_number(_v(r,"cost")),parse_number(_v(r,"conversions")),parse_number(_v(r,"conversion_value")),_v(r,"date") or None) for r in _rows(path)]

def read_search_terms_csv(path):
    return [SearchTermRow(_v(r,"search_term"),_v(r,"campaign"),_v(r,"ad_group"),_v(r,"keyword"),parse_number(_v(r,"impressions")),parse_number(_v(r,"clicks")),parse_number(_v(r,"cost")),parse_number(_v(r,"conversions")),parse_number(_v(r,"conversion_value")),_v(r,"date") or None) for r in _rows(path)]

def read_keyword_file(path):
    return [x.strip() for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip() and not x.lstrip().startswith("#")]
