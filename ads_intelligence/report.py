def _n(v,d=2): return "—" if v is None else f"{v:,.{d}f}"
def _p(v): return "—" if v is None else f"{v*100:.2f}%"

def render_report(overall,campaigns,intents,findings):
    L=["# Ads Intelligence Report","","> Raw-metric analysis. Google Optimization Score and Google Recommendations are not used.","",
       "## Overall","",
       "| Impr. | Clicks | Cost | Conv. | CTR | CPC | CVR | CPA | ROAS |",
       "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
       f"| {_n(overall.impressions,0)} | {_n(overall.clicks,0)} | {_n(overall.cost)} | {_n(overall.conversions)} | {_p(overall.ctr)} | {_n(overall.cpc)} | {_p(overall.cvr)} | {_n(overall.cpa)} | {_n(overall.roas)} |",
       "","## Campaigns","",
       "| Campaign | Clicks | Cost | Conv. | CVR | CPA | ROAS |","|---|---:|---:|---:|---:|---:|---:|"]
    for name,m in sorted(campaigns.items(),key=lambda x:x[1].cost,reverse=True):
        L.append(f"| {name} | {_n(m.clicks,0)} | {_n(m.cost)} | {_n(m.conversions)} | {_p(m.cvr)} | {_n(m.cpa)} | {_n(m.roas)} |")
    if intents:
        L+=["","## Search intent mix","","| Intent | Clicks | Cost | Conv. | CVR | CPA |","|---|---:|---:|---:|---:|---:|"]
        for name,m in sorted(intents.items(),key=lambda x:x[1].cost,reverse=True):
            L.append(f"| {name} | {_n(m.clicks,0)} | {_n(m.cost)} | {_n(m.conversions)} | {_p(m.cvr)} | {_n(m.cpa)} |")
    L+=["","## N-gram evidence","","| N-gram | n | Terms | Clicks | Cost | Conv. | Verdict | Action | Evidence |","|---|---:|---:|---:|---:|---:|---|---|---|"]
    for f in findings[:50]:
        ev=f.rationale + (f" p0={f.p_zero:.4f}" if f.p_zero is not None else "") + (f" wilson95_upper={f.wilson_upper:.4f}" if f.wilson_upper is not None else "")
        L.append(f"| {f.ngram} | {f.n} | {f.distinct_terms} | {_n(f.clicks,0)} | {_n(f.cost)} | {_n(f.conversions)} | {f.verdict} | {f.action} | {ev} |")
    L+=["","## Guardrails","","- Platform conversion is not automatically a qualified lead or sale.","- Search Impression Share is not market demand.","- Negative candidates require human review.","- Sparse samples remain INSUFFICIENT_DATA.",""]
    return "\n".join(L)
