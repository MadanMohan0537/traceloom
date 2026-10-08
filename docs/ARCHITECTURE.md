# Architecture and data boundaries

## Span contract

A span has a run ID, stable span ID, monotonic sequence, kind, name, start time, duration, tokens, cost, status, optional milestone, and structured input/output. TraceLoom validates sequence uniqueness, persists JSON with stable key ordering, and replays spans by sequence.

## Decisions

| Decision | Rationale | Tradeoff |
|---|---|---|
| Local SQLite store | Zero-service reproducible MVP | Not a distributed telemetry backend |
| OpenTelemetry-shaped concepts | Easier future adapter path | Not wire-compatible OTLP yet |
| Store raw recorded tool results | Deterministic replay and diagnosis | Raises privacy and retention risk |
| Explicit success label | Needed for cost per success and silent errors | Labels can be delayed or subjective |
| Six-class taxonomy | Actionable without excessive fragmentation | `unknown` remains necessary |
| Explicit milestones | Detects progress across different actions | Requires task-aware instrumentation |
| Static HTML console | Portable and credential-free | No interactive filtering or auth |

## Safe replay boundary

This MVP never re-executes tool calls. It shows stored input and output records. Any future active replay must classify tool idempotency, simulate writes by default, prevent duplicated side effects, and maintain an approval/audit path.

## Production hardening

Add OTLP ingestion, tenant isolation, field allowlists and redaction before persistence, encryption, retention enforcement, authenticated query access, clock-skew handling, sampling, backpressure, versioned classifiers, and a label-feedback loop. Benchmark taxonomy precision and watchdog thresholds on representative reviewed traces before paging operators.

