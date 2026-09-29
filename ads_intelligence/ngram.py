import math, re
from collections import defaultdict
from .models import NgramFinding

STOPWORDS={"a","an","and","the","of","to","for","in","on","ve","veya","ile","bir","bu","şu","da","de","için"}

def normalize_text(text):
    return re.sub(r"\s+"," ",re.sub(r"[^\w]+"," ",text.casefold())).strip()

def _ngrams(term,max_n=3):
    tokens=normalize_text(term).split(); out=set()
    for n in range(1,max_n+1):
        for i in range(len(tokens)-n+1):
            g=tokens[i:i+n]
            if n==1 and (g[0] in STOPWORDS or g[0].isdigit()): continue
            out.add((" ".join(g),n))
    return out

def wilson_upper(successes,trials,z=1.959963984540054):
    if trials<=0:return 1.0
    p=max(0,min(successes,trials))/trials; z2=z*z; d=1+z2/trials
    c=(p+z2/(2*trials))/d
    m=z*math.sqrt((p*(1-p)+z2/(4*trials))/trials)/d
    return min(1,c+m)

def _contains(phrase,texts):
    needle=f" {normalize_text(phrase)} "
    return any(needle in f" {normalize_text(t)} " for t in texts)

def analyze_ngrams(rows, target_cpa=None, min_cost=0, min_clicks=10, min_distinct_terms=2, alpha=.05, max_n=3, protected_terms=(), active_keywords=()):
    buckets={}
    total_clicks=sum(r.clicks for r in rows); total_conv=sum(r.conversions for r in rows)
    baseline=min(1,total_conv/total_clicks) if total_clicks else 0
    for row in rows:
        for gram,n in _ngrams(row.search_term,max_n):
            b=buckets.setdefault(gram,{"n":n,"terms":set(),"clicks":0.0,"cost":0.0,"conv":0.0})
            b["terms"].add(normalize_text(row.search_term)); b["clicks"]+=row.clicks; b["cost"]+=row.cost; b["conv"]+=row.conversions
    findings=[]
    for gram,b in buckets.items():
        protected=_contains(gram,protected_terms); collision=_contains(gram,active_keywords)
        enough=b["cost"]>=min_cost and b["clicks"]>=min_clicks and len(b["terms"])>=min_distinct_terms
        verdict="INSUFFICIENT_DATA"; action="NONE"; rationale="Below one or more configured evidence thresholds."; p0=None; upper=None
        if enough and b["conv"]<=0:
            p0=(1-baseline)**b["clicks"] if baseline>0 else 1.0
            if p0<alpha:
                verdict="WASTE_SIGNAL"
                if protected or collision:
                    action="REVIEW"; rationale="Statistically surprising zero conversions, but phrase is protected or collides with an active keyword."
                else:
                    action="NEGATIVE_CANDIDATE"; rationale="Zero conversions are statistically surprising at the observed baseline CVR."
            else:
                rationale="Zero conversions remain plausible by chance at the observed baseline CVR."
        elif enough and b["conv"]>0:
            if target_cpa and target_cpa>0:
                required=(b["cost"]/b["clicks"])/target_cpa if b["clicks"] else 1
                upper=wilson_upper(b["conv"],b["clicks"])
                if upper<required:
                    verdict="EFFICIENCY_RISK"; action="REVIEW"; rationale="95% Wilson upper bound is below CVR required by target CPA."
                else:
                    verdict="OK"; rationale="Observed uncertainty still includes a CVR compatible with target CPA."
            else:
                verdict="OK"; rationale="Converts and no target-CPA contradiction was established."
        findings.append(NgramFinding(gram,b["n"],len(b["terms"]),b["clicks"],b["cost"],b["conv"],verdict,action,rationale,p0,upper,protected,collision))
    return sorted(findings,key=lambda x:(x.action!="NEGATIVE_CANDIDATE",-x.cost,x.ngram))
