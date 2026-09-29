import argparse
from pathlib import Path
from .csv_loader import read_campaign_csv, read_search_terms_csv, read_keyword_file
from .metrics import aggregate, group_by_campaign
from .intent import load_rules, aggregate_intents
from .ngram import analyze_ngrams
from .report import render_report

def main():
    p=argparse.ArgumentParser(prog="ads-intel"); s=p.add_subparsers(dest="command",required=True)
    a=s.add_parser("analyze"); a.add_argument("--campaigns"); a.add_argument("--search-terms"); a.add_argument("--rules",default="rules/default.json")
    a.add_argument("--target-cpa",type=float); a.add_argument("--min-cost",type=float,default=0); a.add_argument("--min-clicks",type=float,default=10)
    a.add_argument("--min-distinct-terms",type=int,default=2); a.add_argument("--alpha",type=float,default=.05); a.add_argument("--protected-term",action="append",default=[])
    a.add_argument("--active-keyword-file"); a.add_argument("--out",default="reports/latest.md")
    args=p.parse_args()
    cr=read_campaign_csv(args.campaigns) if args.campaigns else []; sr=read_search_terms_csv(args.search_terms) if args.search_terms else []
    if not cr and not sr: raise SystemExit("Provide --campaigns and/or --search-terms")
    metric_rows=cr or sr; overall=aggregate(metric_rows); campaigns=group_by_campaign(metric_rows); intents={}; findings=[]
    if sr:
        intents=aggregate_intents(sr,load_rules(args.rules))
        active=read_keyword_file(args.active_keyword_file) if args.active_keyword_file else []
        findings=analyze_ngrams(sr,target_cpa=args.target_cpa,min_cost=args.min_cost,min_clicks=args.min_clicks,min_distinct_terms=args.min_distinct_terms,alpha=args.alpha,protected_terms=args.protected_term,active_keywords=active)
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(render_report(overall,campaigns,intents,findings),encoding="utf-8"); print(out)
    return 0

if __name__=="__main__": raise SystemExit(main())
