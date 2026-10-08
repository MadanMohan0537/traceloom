import json
import sqlite3
from pathlib import Path

from .models import Run, Span


SCHEMA = """
CREATE TABLE IF NOT EXISTS runs(run_id TEXT PRIMARY KEY, task TEXT NOT NULL, success INTEGER NOT NULL, expected_failure TEXT);
CREATE TABLE IF NOT EXISTS spans(run_id TEXT NOT NULL, span_id TEXT NOT NULL, sequence INTEGER NOT NULL,
 kind TEXT NOT NULL, name TEXT NOT NULL, started_ms INTEGER NOT NULL, duration_ms INTEGER NOT NULL,
 tokens INTEGER NOT NULL, cost_usd REAL NOT NULL, status TEXT NOT NULL, milestone TEXT,
 input_json TEXT NOT NULL, output_json TEXT NOT NULL, PRIMARY KEY(run_id,span_id));
"""


class TraceStore:
    def __init__(self, path: str | Path):
        self.path = str(path)
        with sqlite3.connect(self.path) as db:
            db.executescript(SCHEMA)

    def ingest(self, run: Run) -> None:
        sequences = [span.sequence for span in run.spans]
        if len(sequences) != len(set(sequences)):
            raise ValueError("duplicate span sequence")
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT OR REPLACE INTO runs VALUES (?,?,?,?)", (run.run_id, run.task, int(run.success), run.expected_failure))
            db.execute("DELETE FROM spans WHERE run_id=?", (run.run_id,))
            db.executemany("INSERT INTO spans VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", [
                (s.run_id,s.span_id,s.sequence,s.kind,s.name,s.started_ms,s.duration_ms,s.tokens,s.cost_usd,s.status,s.milestone,
                 json.dumps(s.input,sort_keys=True),json.dumps(s.output,sort_keys=True)) for s in run.spans])

    def runs(self) -> list[Run]:
        with sqlite3.connect(self.path) as db:
            db.row_factory = sqlite3.Row
            result=[]
            for row in db.execute("SELECT * FROM runs ORDER BY run_id"):
                spans=tuple(Span(run_id=s["run_id"],span_id=s["span_id"],sequence=s["sequence"],kind=s["kind"],name=s["name"],
                    started_ms=s["started_ms"],duration_ms=s["duration_ms"],tokens=s["tokens"],cost_usd=s["cost_usd"],status=s["status"],
                    milestone=s["milestone"],input=json.loads(s["input_json"]),output=json.loads(s["output_json"]))
                    for s in db.execute("SELECT * FROM spans WHERE run_id=? ORDER BY sequence",(row["run_id"],)))
                result.append(Run(row["run_id"],row["task"],bool(row["success"]),spans,row["expected_failure"]))
            return result

