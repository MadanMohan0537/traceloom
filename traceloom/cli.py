import argparse
import json

from .fixtures import sample_runs
from .report import write_report
from .store import TraceStore


def demo(db_path:str,json_path:str,html_path:str)->dict:
    store=TraceStore(db_path)
    for run in sample_runs(): store.ingest(run)
    return write_report(store.runs(),json_path,html_path)


def main(argv=None)->int:
    parser=argparse.ArgumentParser(prog="traceloom")
    sub=parser.add_subparsers(dest="command",required=True)
    command=sub.add_parser("demo",help="ingest scripted traces and create reports")
    command.add_argument("--db",default="traceloom.db"); command.add_argument("--json",default="report.json"); command.add_argument("--html",default="report.html")
    args=parser.parse_args(argv)
    print(json.dumps(demo(args.db,args.json,args.html)["summary"],indent=2))
    return 0


if __name__=="__main__": raise SystemExit(main())
