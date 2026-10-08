# Rigorous feature backlog

P1 semantic progress monitoring is implemented. The remaining items are proposals, not completed functionality.

| Priority | Feature | Concrete user problem | Intended behavior | Dependencies | Success test | Risks and tradeoffs |
|---|---|---|---|---|---|---|
| P1 shipped | Semantic progress watchdog | Changing actions can loop without triggering repeated-tool rules | Track task milestones and flag bounded action windows with no change | Milestone contract, labeled scripted traces | Higher loop recall than repeated-tool detection without higher false alerts on frozen fixtures | Useful exploration may look stagnant; support task grace periods |
| P2 | Recovery checkpoint experiment | Debuggers cannot tell which restart point is worth trying | Replay mocked responses from selected checkpoints and compare recovery cost with full restart | Safe simulated tools, idempotency metadata, cost model | Recover more identical failed tasks or reduce total cost at fixed recovery rate | Writes can duplicate effects; keep tools simulated first |
| P2 | Trace privacy firewall | Raw prompts and tool results may expose secrets | Apply allowlists, structured redaction, TTLs, and retained-field accounting before storage | Data classification policy, deletion job | Seeded secrets never reach SQLite and expired traces disappear | Over-redaction can destroy diagnostic value |
| P2 | Taxonomy calibration queue | Rules silently misclassify failures | Sample runs by uncertainty and impact for blinded reviewer labels | Reviewer workflow, versioned classifier | Improve macro precision on a held-out labeled trace set | Reviewer disagreement may make labels unstable |
| P3 | Critical-path attribution | Total latency does not reveal which parallel branch delayed completion | Reconstruct dependency graph and identify critical-path spans | Parent/link span IDs, clock normalization | Identify the seeded blocking branch in parallel fixtures | Bad clocks and missing links distort attribution |
| P3 | Spend-blast-radius alert | A failing agent can burn budget before success rate moves | Forecast remaining run cost and stop within a task-level budget policy | Streaming spans, policy engine | Halt seeded runaway traces before the declared cap with measured false stops | Early stopping may abort recoverable runs |
| P3 | Counterfactual fix recommender | Operators know the failure class but not the cheapest fix | Replay prompt, schema, or model configuration changes against frozen traces | Versioned configurations, recovery harness | Recommended fix wins on recovery cost in held-out scripted incidents | Offline replay may not transfer to live tools |
| P3 | Novel failure clustering | The fixed taxonomy hides emerging modes inside `unknown` | Cluster redacted unknown traces and require reviewer naming before taxonomy changes | Embeddings or feature vectors, privacy firewall | Seeded novel family forms a stable cluster without splitting known classes | Clusters may reflect wording rather than cause |
| P4 | SLO budget by task class | One global threshold penalizes complex tasks | Configure success, latency, and cost budgets by versioned task class | Task classifier, policy registry | Frozen tasks are judged only against their declared class | Misclassification can hide regressions |

## Next slice

Build the recovery checkpoint experiment with fully simulated tools. It tests whether the console changes an operator decision—where to restart—while avoiding duplicated real-world side effects.

