from collections import Counter

from .classifier import classify
from .models import Run


def summarize(runs: list[Run]) -> dict:
    success=[run for run in runs if run.success]
    total_cost=sum(s.cost_usd for run in runs for s in run.spans)
    total_tokens=sum(s.tokens for run in runs for s in run.spans)
    failures=Counter(classify(run) for run in runs if not run.success)
    known=sum(v for k,v in failures.items() if k!="unknown")
    failed=len(runs)-len(success)
    return {
        "runs":len(runs),"successes":len(success),"success_rate":len(success)/len(runs) if runs else 0.0,
        "total_cost_usd":round(total_cost,6),"total_tokens":total_tokens,
        "cost_per_success_usd":round(total_cost/len(success),6) if success else None,
        "failure_mix":dict(failures),"classification_coverage":known/failed if failed else 1.0,
    }


def watchdog_experiment(runs: list[Run]) -> dict:
    from .watchdog import repeated_tool_loop, semantic_progress
    labels=[run.expected_failure=="infinite_loop" for run in runs]
    semantic=[semantic_progress(run.spans).flagged for run in runs]
    repeated=[repeated_tool_loop(run.spans) for run in runs]
    def score(pred):
        tp=sum(p and y for p,y in zip(pred,labels)); fp=sum(p and not y for p,y in zip(pred,labels)); fn=sum((not p) and y for p,y in zip(pred,labels))
        return {"true_positives":tp,"false_positives":fp,"false_negatives":fn,
                "recall":tp/(tp+fn) if tp+fn else 1.0,"false_alert_rate":fp/max(1,sum(not y for y in labels))}
    return {"semantic_progress":score(semantic),"repeated_tool":score(repeated)}

