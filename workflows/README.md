# workflows/

End-to-end operating procedures for tasks that need more than a single command invocation. A workflow defines the objective, phase gates, subagent topology, model and thinking tiers, verification requirements, and stopping conditions for a long-running loop.

Unlike the basic slash-commands in `commands/`, workflows do not just tell one agent how to perform a bounded action. They describe how a coordinator should split work across subagents, keep subagent outputs advisory until verified, sequence dependent phases, and decide when the overall objective is complete.

## `create-test-dataset.md`

Generate a corpus-grounded benchmark dataset with adversarial JSON evaluation items, including plausible negative response examples and optional domain-specific context for downstream judging of specialized or novel corpus knowledge.

Execution topology:

- **Tier 1 — Orchestrator and Analyst** (high-reasoning model): analyzes the source corpus, builds a strict distribution matrix over question types and difficulty, assigns batches, then aggregates, validates, and normalizes the final dataset. Every concept must map back to a direct citation or undeniable logical inference from the corpus — no invented information.
- **Tier 2 — Item Generation Subagents** (fast, low-thinking models, 5–10 parallel workers): each consumes a targeted item specification and emits 10–15 questions per batch against a strict JSON schema.

The resulting dataset pairs with `agents/judge.md`, which scores a target LLM's responses against each entry's canonical answers, required facts, reasoning paths, source references, and known negative responses.

## `unvibe-code-repo.md`

Convert a broad simplification audit into a reviewed, implemented, tested, committed, and PR-ready change. Run from the repository root; the file is the complete workflow definition, and subagent output remains advisory until the coordinator verifies it against repository evidence.

Key mechanics:

- **Evidence-gated phases**: no file modification during audit or planning; no commit, push, or PR unless the user explicitly requested the full repository workflow or confirms the final plan.
- **Finding taxonomy**: audit findings are classified as `duplication`, `conflict`, `bug`, `dead-code`, `useless-active`, or `simplification`, each with a defined evidence bar.
- **Core-functionality protection**: behavior reachable from real entry points (public APIs, CLI commands, handlers, scheduled jobs, exported surfaces, persisted schemas, tests protecting real workflows) is preserved unless the user explicitly approves a breaking change.
- **Subagent topology**: the coordinator may use bounded audit scouts, plan reviewers, implementation workers, and confirmation reviewers, while retaining responsibility for evidence checks, integration decisions, verification, and branch operations.
- **Verification**: targeted tests, type checks, lint checks, and a final change-set audit before any commit; commits include only triage-approved paths.
