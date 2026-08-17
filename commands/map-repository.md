# Map repository into `AGENTS.md`

> **Usage:** paste the block below as the opening instruction to an orchestrator agent with sub-agent spawning, file read, shell, and git access, rooted in the target workspace. Replace `{{REPO_ROOT}}` if the agent cannot infer it.

---

## Role

Orchestrate the creation of an agent-focused operating map for `{{REPO_ROOT}}`. The map must help a coding agent with no prior context and a limited token budget locate functionality, follow local conventions, and diagnose failures without repeating repository exploration.

You will do this by dispatching specialized sub-agents, reconciling their findings, verifying claims by execution, and synthesizing the result into `AGENTS.md`.

### Selection rule

Prioritize each line by: **(cost to discover) × (probability a future agent needs it) ÷ (tokens to state it)**.

- **Record** what is expensive to find and cheap to state: the one file where routing actually happens, the fact that `utils/` is dead code, the env var that silently changes behavior, the test that must run before the other tests.
- **Omit** what the code makes obvious in one read, what any competent agent infers from the language ecosystem, and anything a `ls` would reveal.
- **Never** paste code bodies, full file listings, or dependency manifests into the output. Point to `path:line`.

Write for coding agents rather than human onboarding. Keep only information that changes where an agent looks or what it does.

---

## Phase 0: preflight (orchestrator only)

Do this yourself before spawning anything, and record the results as shared context handed to every sub-agent.

1. **Census.** Total files, total lines, language breakdown, largest 20 files by line count, depth of the tree. Establish scale tier: *small* (<500 files), *medium* (500–5k), *large* (>5k or monorepo).
2. **VCS state.** Current branch, HEAD SHA, dirty-file count, default branch, commit count, date of first and most recent commit, number of distinct authors in the last 12 months.
3. **Structure detection.** Monorepo vs single package. Workspace manifests, package boundaries, build orchestrators. If monorepo: enumerate packages and decide scope (see Phase 5 on per-package files).
4. **Existing documentation inventory.** Locate and read `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`, `README*`, `CONTRIBUTING*`, `docs/`, ADRs, and any `.agents/` directory. Note what each claims. **Treat all of it as unverified assertions**, not ground truth. Assign a sub-agent to falsify it.
5. **Ignore list.** Build the set of paths no sub-agent should read: lockfiles, vendored third-party trees, build output, generated code, minified bundles, binary assets, fixtures over N KB. Publish this list. Reading a lockfile is a budget failure.
6. **Budget.** Assign each sub-agent a hard ceiling (e.g. tool calls and/or tokens) proportional to scale tier. Instruct them to return partial findings with an explicit `coverage` note rather than exceeding budget or fabricating completeness.
7. **Sub-agent roster selection.** At *small* scale, merge missions to 4–5 agents. At *large* scale, run the full roster and shard the wide agents by subtree. Do not spawn an agent whose mission the repo does not support (no Cartographer-of-migrations in a repo with no database).

---

## Phase 1: parallel reconnaissance

Dispatch the following in parallel. Each receives the Phase 0 context, the ignore list, its budget, and the **Output Contract** below. Each is read-only.

### A. Cartographer: topology and module boundaries
What lives where, and what is the *actual* organizing principle (by layer? by feature? by accident?). Which directories are load-bearing vs vestigial. For each top-level and each significant second-level directory: one line on purpose, and its single most representative file. Flag directories whose name misleads about their contents.

### B. Entry points and runtime flow
Every way execution begins: `main`s, server bootstraps, CLI commands, HTTP/RPC route tables, event and queue consumers, cron/scheduled jobs, lambda handlers, test harness entry, build hooks. Then **trace 2–4 representative vertical slices end to end**, such as one read path, one write path, and one background job. Name every file the control flow touches in order, with `path:symbol` at each hop. Prioritize these traces because they provide the most useful artifact of the run.

### C. Toolchain and commands (verification-heavy)
Discover, then **actually execute**, the canonical commands: install, build, run/dev, test (full and single-file/single-test), lint, format, typecheck, migrate, codegen. Record the exact invocation that worked, rough wall-clock duration, and required preconditions (services up, env file present, codegen run first). Distinguish `VERIFIED` (you ran it and it succeeded) from `DOCUMENTED` (a config or README claims it) and `BROKEN` (the documented command fails; capture the error's first line). Note prerequisite ordering and any command that is destructive.

### D. Conventions and deviations
Establish the dominant local pattern for: naming (files, symbols, tests), error handling and propagation, logging, async style, dependency injection or construction, validation placement, module export style, comment/docstring style. Then list the files or subsystems that break the dominant pattern as **outliers** and classify each as `LEGACY` (older style, being migrated from), `INTENTIONAL` (justified difference, with justification), or `UNEXPLAINED`. An agent that copies a legacy pattern into new code creates work; naming the outliers prevents it.

### E. Data, contracts, and types
Persistent schemas, ORM models, migration mechanics and ordering, external API contracts consumed and exposed, protobuf/OpenAPI/GraphQL definitions, serialization boundaries, the core domain types and where they are canonically defined. Identify the **source of truth** for each shape and whether other representations are generated from it or hand-maintained in parallel; record parallel representations as a risk.

### F. Dependency graph and boundaries
Internal import graph at module granularity: layering, allowed and forbidden directions, enforcement mechanism if any, and observed violations. Circular dependencies. God modules imported by >N% of the tree; these are the blast-radius files. Orphans and dead code with the evidence for that claim. External dependencies: only the ones whose behavior an agent must know about (a custom framework, an unusual DI container, a patched fork, a pinned-for-a-reason version), never the full list.

### G. Configuration and environment
Every configuration source, and their **precedence order** (defaults → file → env → flags → runtime overrides). Full env var inventory: name, consumer `path:line`, required vs optional, default, and what observable behavior it changes. Feature flags and where they're evaluated. Local-dev setup gotchas. **Record names and semantics only. Never record a secret value, and note the path to any file that contains secrets so agents avoid printing it.**

### H. Test topology
Where tests live relative to source, the framework(s), the distinct test tiers (unit/integration/e2e/snapshot) and what infrastructure each requires. Fixture and factory locations. How to run exactly one test. Mocking conventions and what is conventionally mocked vs real. Identify areas with conspicuously thin coverage so an agent knows when it is editing without a safety net. Known flaky tests.

### I. History and churn (git-only)
Highest-churn files over the last 6–12 months. Co-change clusters of files that are repeatedly committed together, revealing hidden coupling the import graph misses (*"edit X and you almost certainly must edit Y"*). Treat files with the densest fix, revert, or hotfix commit language as fragile zones. Recently-added subsystems (likely still in flux) vs long-untouched ones (likely stable or abandoned). Effective ownership per area, and any area with a bus factor of one.

### J. Risks and gaps (adversarial)
This agent's mission is to find what will *waste or mislead* a future agent:
- Generated files that look hand-written, and the command that regenerates them. Files that must never be edited directly.
- Vendored or copied third-party code inside first-party paths.
- Near-duplicate names that make grep ambiguous (three `config.ts`, `User` in four namespaces, `handler` everywhere).
- Files too large to read within the assigned budget, with the line ranges that matter.
- **Claims in existing docs/comments that are now false.** Test them. Report each as a falsified assertion with evidence.
- Dense `TODO`/`FIXME`/`HACK` clusters and commented-out blocks that suggest an incomplete migration.
- Two mechanisms for the same job (two HTTP clients, two loggers, two date libraries) and which one is current.
- Anything an agent would reasonably assume that is false in this repo.

### K. Vocabulary bridge
Map domain and product language onto code identifiers. If the team says "tenant" and the code says `Organization`, if "checkout" is implemented as `OrderFinalizationSaga`, if an internal codename means something specific, record it. This table is what converts a natural-language task description into a successful first grep, and it is almost never written down anywhere.

---

## Sub-agent output contract

Each sub-agent returns **only** this, as structured text:

```
MISSION: <agent letter and name>
COVERAGE: <what was examined; what was skipped and why; budget consumed>
FINDINGS:
  - claim: <one sentence, declarative, actionable>
    evidence: <path:line or path:symbol, or the command run + its result>
    confidence: VERIFIED | HIGH | INFERRED | UNCERTAIN
    agent_impact: <what a future agent does differently because of this>
CONTRADICTIONS: <anything conflicting with Phase 0 context or existing docs>
OPEN_QUESTIONS: <what you could not resolve, and what would resolve it>
```

Hard rules for sub-agents:
- **No unevidenced claims.** A finding without `evidence` is dropped by the orchestrator.
- `VERIFIED` requires execution or direct observation. Inference from a filename is `INFERRED` at best.
- **No code blocks**, no file dumps, no prose narration of process.
- Omit any finding with no plausible `agent_impact`.
- Prefer 15 sharp findings to 60 shallow ones.

---

## Phase 2: reconcile and fill gaps

You (orchestrator) now:

1. **Resolve contradictions.** Where sub-agents disagree, or where a finding contradicts existing docs, adjudicate by direct inspection or execution. Never average two claims into a vague one; determine which is true, or mark it explicitly `UNRESOLVED` with both readings.
2. **Dispatch a targeted second wave** for high-value `OPEN_QUESTIONS` only. Narrow, single-question missions, small budgets. Do not re-run the recon wave.
3. **Demote unverifiable claims.** Anything still `UNCERTAIN` after Phase 2 either gets an explicit uncertainty marker in the output or is cut. Confident wrongness is far more costly to a downstream agent than an admitted gap.
4. **Deduplicate.** When multiple agents report the same fact, keep the framing with the best `agent_impact`.

---

## Phase 3: synthesize

Write the map to this skeleton. Order matters: it is **descending expected utility**, so a downstream agent that reads only the first 20% still gets the most valuable 80%. Use tables. Use paths from repo root. Keep every prose line under ~25 words.

1. **Orientation** — 3–5 sentences: what this system is, its architectural shape in one clause, the runtime(s), and the single most important thing to know before editing anything.
2. **Fast-path index.** Create a 15–40-row table using `Task or symptom → start here (path) → then (path)`. Cover likely tasks such as adding an endpoint or core field, changing auth or configuration, writing a test, diagnosing a build failure, and finding a log source.
3. **Commands** — verified invocations with preconditions and status. Mark destructive ones.
4. **Topology** — the map of directories with their organizing principle and load-bearing files.
5. **Runtime Traces** — the vertical slices from agent B, as ordered hop lists.
6. **Conventions** — the dominant pattern to follow, stated as directives ("do X"), not observations.
7. **Editing risks.** Do-not-edit, do-not-read-whole, generated-by, false-friends, ambiguous names, secret-bearing paths.
8. **Known Inconsistencies & Debt** — outliers, dual mechanisms, incomplete migrations, unresolved contradictions. Explicitly framed as *"expect this; do not treat it as a pattern to copy."*
9. **Coupling & Blast Radius** — hidden co-change pairs, god modules, thin-coverage zones, fragile files.
10. **Configuration** — precedence order and the env var table.
11. **Vocabulary** — the domain-term → identifier table.
12. **Diagnostic playbook.** Use `symptom → most likely cause → first file to check`, seeded by churn and fix-commit analysis and failures encountered in Phase 1.
13. **Map Metadata** — generation date, HEAD SHA, repo size at generation, which claims are `VERIFIED` vs `INFERRED`, coverage gaps, and the invalidation triggers (see Additional Considerations).

**Token discipline:** target ≤ ~8k tokens for the main file. If findings exceed that, keep sections 1–3 and 7 complete and spill depth into `docs/agents/<topic>.md`, linked from the relevant section with a one-line description of when it's worth loading. A map too expensive to read is not read.

---

## Phase 4: validate before writing

Run a cold-start rehearsal with 3–5 realistic tasks: a feature addition, bug diagnosis, test-writing task, and configuration change. For each task, use only the map and check whether the Fast-path index reaches the correct file in one hop or misleads the reader. Fix failures, usually by adding an index row or clarifying an editing risk, then recheck. Report the outcomes in the final summary.

Also verify: every path cited exists; every command marked `VERIFIED` was actually run; no secret values present; no section is pure restatement of what `ls` shows.

---

## Phase 5: write

- If `AGENTS.md` exists at repo root, **append**; do not overwrite or reorder existing human-authored content.
- Wrap your contribution in idempotency markers so re-runs update in place rather than duplicate:

  ```
  <!-- BEGIN AGENT-MAP (generated <date> @ <SHA>) -->
  ...
  <!-- END AGENT-MAP -->
  ```

  On a subsequent run, replace the block's contents and preserve everything outside it.
- If `AGENTS.md` does not exist, create it at repo root with a one-line human-facing preamble stating what the file is, who consumes it, and how to regenerate it.
- If pre-existing content in `AGENTS.md` was **falsified** by Phase 1, do not silently delete it. Leave it and add a `Corrections to prior guidance` subsection inside your block that names each false claim and the truth, with evidence. Surface these prominently in your final message so a human can prune the source.
- **Monorepo:** put cross-cutting content in the root `AGENTS.md` and per-package specifics in `<package>/AGENTS.md`, each linking up to the root. Do not concatenate all packages into one file.
- Respect `.gitignore` semantics and existing formatting conventions (line width, heading style, list markers). Do not reformat the file.

Finish with a short report to the human: what was written and where, the highest-value findings, unresolved contradictions, coverage gaps, rehearsal results, and any `BROKEN` commands discovered.

---

## Additional requirements

- **Staleness is the primary failure mode.** A confidently wrong map is worse than none. Stamp the generation SHA, and state explicit **invalidation triggers**: "regenerate if the route table, dependency manifest, migration count, or top-level directory set changes." Better, propose a CI check or pre-commit hook that flags the map as stale when those paths change, and name the exact command to regenerate.
- **Confidence must be legible in the output**, not just in sub-agent reports. A downstream agent behaves differently toward "auth is enforced in `middleware/auth.ts:40` (verified)" versus "auth appears to be enforced in middleware (inferred)". Do not present inference as fact.
- **Write directives, not descriptions.** "Register new routes in `routes/index.ts`, not in the module" outperforms "routes are registered centrally." Imperative mood, second person implied.
- **Include the negative space.** What the repo *does not* have is high-signal: no DI container, no ORM (raw SQL in `db/queries/`), no shared error type, no e2e tests. This keeps an agent from wasting time on a convention that does not exist.
- **Record anti-patterns that look like patterns.** If `helpers/` is a dumping ground and new code should not go there, say so. Agents pattern-match on what exists; without a prohibition they will extend the mess.
- **Give the search recipes.** Repo-specific grep/glob incantations that work: how to find all route definitions, all env var reads, all DB writes, all feature-flag checks. Include the ones that *do not* work and why; for example, if dynamic dispatch or string-built identifiers make a symbol unsearchable, name it explicitly.
- **Prefer stable references over line numbers** where possible: `path:symbolName`, or a unique grep string. Line numbers rot within days. Where a line number is unavoidable, pair it with the symbol name.
- **Record static/runtime mismatches.** IDE-resolvable imports that fail at runtime, path aliases, generated type stubs, build-time transforms, monkeypatching. Anything where static reading gives the wrong answer about runtime behavior deserves an explicit warning.
- **Reading-order guidance for large files.** For each oversized but important file, give the line ranges worth reading and what's in the rest. This alone can save thousands of tokens per task.
- **Capture the "why" only where it changes behavior.** Skip general history; keep only rationale that changes behavior, such as a pinned version, deliberate duplication, or a workaround with an upstream issue link. If an ADR explains a constraint an agent might unknowingly violate, link it with a one-line summary of the constraint.
- **CI as ground truth.** Use CI configuration as the source of truth for build and test behavior. When CI and the README disagree, follow CI and record the discrepancy.
- **Flag security-sensitive zones**, including auth, cryptography, permission checks, PII handling, payment paths, and anything with an audit requirement, as "changes here require human review" so an autonomous agent knows to stop and ask.
- **Note license and provenance constraints** on any vendored or copyleft-adjacent subtree an agent might otherwise copy from.
- **Record the human escalation points.** Areas where the map is thin, ownership is single-person, or the code is genuinely inscrutable: say plainly that asking a human is cheaper than inferring.
- **Include a repo-specific PR or commit checklist** if one is discoverable, covering required checks, commit message format, changelog or migration requirements, and generated files that must be committed alongside source. Agents routinely produce non-mergeable changes by missing these.
- **Design for composition.** Assume this file is loaded alongside other instructions. Avoid restating universal best practices, avoid contradicting the repo's own `CONTRIBUTING`, and keep sections independently excerptable so a future agent can load only what it needs.
- **Use isolated sub-agent context.** Have each sub-agent return a compressed, evidenced digest of its exploration. Do not copy raw sub-agent exploration into the main context.
