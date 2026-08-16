# workflows/

End-to-end operating procedures for tasks that need more than a single command invocation. A workflow defines the objective, phase gates, subagent topology, model and thinking tiers, verification requirements, and stopping conditions for a long-running loop.

Unlike the basic slash-commands in `commands/`, workflows do not just tell one agent how to perform a bounded action. They describe how a coordinator should split work across subagents, keep subagent outputs advisory until verified, sequence dependent phases, and decide when the overall objective is complete.

## `create-test-dataset.md`

Generate a corpus-grounded benchmark dataset with adversarial JSON evaluation items, including plausible negative response examples and optional domain-specific context for downstream judging of specialized or novel corpus knowledge.

Execution topology:

- **Tier 1 — Orchestrator and Analyst** (high-reasoning model): analyzes the source corpus, builds a strict distribution matrix over question types and difficulty, assigns batches, then aggregates, validates, and normalizes the final dataset. Every concept must map back to a direct citation or undeniable logical inference from the corpus — no invented information.
- **Tier 2 — Item Generation Subagents** (fast, low-thinking models, 5–10 parallel workers): each consumes a targeted item specification and emits 10–15 questions per batch against a strict JSON schema.

The resulting dataset pairs with `agents/judge.md`, which scores a target LLM's responses against each entry's canonical answers, required facts, reasoning paths, source references, and known negative responses.

## `map-repository.md`

Create or update an agent-optimized `AGENTS.md` repository map. The workflow inventories the repository, delegates evidence-gathering missions to specialized read-only subagents, reconciles contradictions, and validates the resulting navigation guidance through cold-start task rehearsals.

Key mechanics:

- **Evidence-first reconnaissance**: captures topology, runtime paths, commands, conventions, contracts, configuration, tests, history, landmines, and domain vocabulary with path, symbol, or execution evidence.
- **Scale-aware subagent topology**: selects and shards reconnaissance missions based on repository size, applies explicit budgets and ignore lists, and uses targeted follow-up agents only for unresolved high-value questions.
- **Agent-focused synthesis**: prioritizes a fast-path task index, verified commands, runtime traces, landmines, diagnostic guidance, and high-value negative space instead of general onboarding documentation.
- **Safe, idempotent output**: writes a SHA-stamped generated block without overwriting human-authored `AGENTS.md` content, splits monorepo-specific guidance by package, and records confidence, coverage gaps, and invalidation triggers.
- **Validation**: checks cited paths, command status, secret handling, and map utility through realistic feature, debugging, testing, and configuration rehearsals before writing.

## `simplification-audit-to-pr.md`

Convert a broad simplification audit into a reviewed, implemented, tested, committed, and PR-ready change. Run from the repository root; the file is the complete workflow definition, and subagent output remains advisory until the coordinator verifies it against repository evidence.

Key mechanics:

- **Evidence-gated phases**: no file modification during audit or planning; no commit, push, or PR unless the user explicitly requested the full repository workflow or confirms the final plan.
- **Finding taxonomy**: audit findings are classified as `duplication`, `conflict`, `bug`, `dead-code`, `useless-active`, or `simplification`, each with a defined evidence bar.
- **Core-functionality protection**: behavior reachable from real entry points (public APIs, CLI commands, handlers, scheduled jobs, exported surfaces, persisted schemas, tests protecting real workflows) is preserved unless the user explicitly approves a breaking change.
- **Subagent topology**: the coordinator may use bounded audit scouts, plan reviewers, implementation workers, and confirmation reviewers, while retaining responsibility for evidence checks, integration decisions, verification, and branch operations.
- **Verification**: targeted tests, type checks, lint checks, and a final change-set audit before any commit; commits include only triage-approved paths.

## `unslopify.md`

Critically explore all code in a target repository workspace and identify every element that is poorly constructed, difficult to maintain, difficult to navigate, or following a bad pattern characteristic of code written by agents over long unsupervised stretches. Strictly read-only and terminal at one ranked report — no plan, implementation, commit, or PR phase exists. Hand its report to `simplification-audit-to-pr.md` if the findings should be acted on.

Key mechanics:

- **Construction-quality taxonomy**: `slop-artifact`, `defensive-noise`, `structural-debt`, `flat-topology`, `convention-drift`, `contract-fiction`, `dependency-hygiene`, `test-theater`, `duplication`, `dead-code`, and `bug`.
- **Dual evidence bar**: reachability and behavior claims require an entry-point trace or a complete caller set; construction, maintainability, and navigability claims require a measured signal with the command behind it, plus a counterexample for convention drift and a named concern partition for flat topology. Impression-only findings are rejected.
- **Repository-relative baseline**: preflight measures the repo's own median and 90th-percentile function and file lengths, its directory fan-out and depth distribution, its catch-all and most-imported modules, and its dominant conventions — so findings are judged against local norms rather than an external ideal, and framework-imposed layout is excluded.
- **Coordinator-owned topology**: cross-directory flatness is the one category a scope-bounded scout structurally cannot see, so the coordinator owns every repo-level `flat-topology` finding while scouts report only what is visible inside their own scope and never propose a directory scheme.
- **Declared coverage**: every in-scope module is listed as `audited`, `partial`, or `not audited` with a reason; the register is complete rather than top-N, and zero findings is only valid when coverage is complete.
- **Bounded verification**: refuters attack every `critical` and `high` finding, the coordinator re-checks those plus a sample of the rest, and unverified findings ship labeled rather than silently accepted or dropped.
