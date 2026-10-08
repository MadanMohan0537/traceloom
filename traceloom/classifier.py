from .models import Run
from .watchdog import semantic_progress


FAILURES=("wrong_tool","bad_arguments","infinite_loop","timeout","refusal","silent_wrong_answer","unknown")


def classify(run: Run) -> str | None:
    if run.success:
        return None
    spans=run.spans
    if semantic_progress(spans).flagged:
        return "infinite_loop"
    if any(s.status=="timeout" for s in spans):
        return "timeout"
    if any(s.status=="refused" for s in spans):
        return "refusal"
    if any(s.status=="bad_arguments" for s in spans):
        return "bad_arguments"
    if any(s.status=="wrong_tool" for s in spans):
        return "wrong_tool"
    if spans and all(s.status=="ok" for s in spans):
        return "silent_wrong_answer"
    return "unknown"

