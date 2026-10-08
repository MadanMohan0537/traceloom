from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class Span:
    run_id: str
    span_id: str
    sequence: int
    kind: str
    name: str
    started_ms: int
    duration_ms: int
    tokens: int = 0
    cost_usd: float = 0.0
    status: str = "ok"
    milestone: str | None = None
    input: dict = field(default_factory=dict)
    output: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Run:
    run_id: str
    task: str
    success: bool
    spans: tuple[Span, ...]
    expected_failure: str | None = None

