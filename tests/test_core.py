import tempfile
import unittest
from pathlib import Path

from traceloom.classifier import classify
from traceloom.fixtures import sample_runs
from traceloom.metrics import summarize, watchdog_experiment
from traceloom.models import Run, Span
from traceloom.report import write_report
from traceloom.store import TraceStore
from traceloom.watchdog import repeated_tool_loop, semantic_progress


class CoreTests(unittest.TestCase):
    def test_fixture_classification(self):
        labels={r.run_id:classify(r) for r in sample_runs()}
        self.assertEqual(labels["run-002"],"infinite_loop")
        self.assertEqual(labels["run-003"],"timeout")
        self.assertEqual(labels["run-004"],"refusal")
        self.assertIsNone(labels["run-001"])
    def test_progress_finds_different_action_loop(self):
        run=sample_runs()[1]
        self.assertTrue(semantic_progress(run.spans).flagged)
        self.assertFalse(repeated_tool_loop(run.spans))
    def test_repeated_detector_finds_literal_loop(self):
        run=sample_runs()[4]
        self.assertTrue(repeated_tool_loop(run.spans))
        self.assertFalse(semantic_progress(run.spans).flagged)
    def test_invalid_window(self):
        with self.assertRaises(ValueError): semantic_progress(sample_runs()[0].spans,1)
    def test_rollup_uses_cost_per_success(self):
        result=summarize(sample_runs())
        self.assertEqual(result["runs"],5); self.assertEqual(result["successes"],2)
        self.assertGreater(result["cost_per_success_usd"],0)
    def test_experiment_improves_loop_recall_without_false_alert(self):
        result=watchdog_experiment(sample_runs())
        self.assertGreater(result["semantic_progress"]["recall"],result["repeated_tool"]["recall"])
        self.assertEqual(result["semantic_progress"]["false_alert_rate"],0)
    def test_store_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            store=TraceStore(Path(d)/"t.db"); runs=sample_runs()
            for r in runs: store.ingest(r)
            self.assertEqual(store.runs(),runs)
    def test_store_rejects_duplicate_sequence(self):
        span=Span("x","1",0,"tool","a",0,1)
        run=Run("x","task",False,(span,Span("x","2",0,"tool","b",1,1)))
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): TraceStore(Path(d)/"t.db").ingest(run)
    def test_report_writes_json_and_html(self):
        with tempfile.TemporaryDirectory() as d:
            j,h=Path(d)/"r.json",Path(d)/"r.html"
            report=write_report(sample_runs(),str(j),str(h))
            self.assertTrue(j.exists() and h.exists()); self.assertEqual(report["summary"]["runs"],5)
            self.assertIn("TraceLoom",h.read_text())

if __name__=="__main__": unittest.main()
