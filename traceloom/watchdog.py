"""Semantic progress and repeated-tool loop detectors."""

from dataclasses import dataclass

from .models import Span


@dataclass(frozen=True)
class WatchdogResult:
    flagged: bool
    stagnant_windows: tuple[tuple[int, int], ...]


def semantic_progress(spans: tuple[Span, ...], window: int = 3, grace_actions: int = 1) -> WatchdogResult:
    actions=[s for s in spans if s.kind in {"tool","model"}]
    if window < 2:
        raise ValueError("window must be at least 2")
    stagnant=[]
    for start in range(grace_actions, max(grace_actions, len(actions)-window+1)):
        group=actions[start:start+window]
        if len(group)==window and not any(s.milestone for s in group):
            stagnant.append((group[0].sequence,group[-1].sequence))
    return WatchdogResult(bool(stagnant),tuple(stagnant))


def repeated_tool_loop(spans: tuple[Span, ...], repeats: int = 3) -> bool:
    names=[s.name for s in spans if s.kind=="tool"]
    return any(len(set(names[i:i+repeats]))==1 for i in range(len(names)-repeats+1))

