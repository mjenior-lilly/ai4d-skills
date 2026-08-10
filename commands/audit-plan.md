# audit-plan-implementation

Audit the current state of the codebase in the workspace against the provided plan to verify that every change the plan specifies has been completely and correctly implemented.

If no plan is identifiable in the conversation or linked context, ask the user to supply one (e.g., a plan file, PR description, or named feature spec) before proceeding — do not guess.

## Scope

1. Establish the expected change set by reading the plan, then compare it against the actual workspace state using `git status` + `git diff` against the merge base, plus the files named in the plan. State the scope in one sentence before auditing.
2. For each change the plan prescribes, verify in the codebase that:
   - the corresponding symbol (function, class, type, constant, config key, route, schema field) exists at its **definition site** and is complete and consistent with both the plan's intent and how it is used elsewhere,
   - its **direct call sites and importers** (one hop) correctly reference the new or updated symbol, and
   - any **boundary contracts** it crosses (public API, serialized payload, persisted schema, env/config, CLI/MCP surface) have been updated to match.
3. Additionally, identify any plan-specified changes that are **absent** from the workspace (not yet implemented or partially implemented).
4. Stop at one hop unless a contract change at the boundary forces deeper tracing. Note any deeper traces and why.

## Sub-agent strategy

Scale sub-agent use dynamically based on change-set size and complexity. All sub-agent findings must be verified against the diff, relevant callers, diagnostics, or command results before fixing or reporting.

### Tier 1 — Symbol tracing (fan-out by file)

**When:** Change set spans 4+ files with distinct changed symbols.
**Skip when:** 1–3 files or all changes are in a single module.

| Parameter | Value |
|-----------|-------|
| Agents | 1 per changed file, cap at 8 |
| Model | sonnet |
| Effort | low |
| Agent type | Explore (read-only) |

Each agent traces symbols in its assigned file: definition site, direct callers/importers (one hop), and boundary contracts crossed. Return structured findings as JSON with keys: `file`, `symbol`, `definition_site`, `callers`, `contracts`.

### Tier 2 — Boundary-contract review

**When:** Tier 1 (or manual tracing) identifies symbols crossing boundary contracts.

| Parameter | Value |
|-----------|-------|
| Agents | 1 per contract type identified (API, schema, config, etc.), cap at 3 |
| Model | opus |
| Effort | medium |

Each agent verifies that every caller/consumer/test/doc has been updated to match the new signature or shape for its contract type. Classify gaps as Interface Drift or Missing/Insufficient.

### Tier 3 — Adversarial verification

**When:** Tiers 1–2 produce high-severity findings (broken contracts or behavioral regressions) before fixes are applied.

| Parameter | Value |
|-----------|-------|
| Agents | 1 per high-severity finding, cap at 3; batch all low-severity into 1 agent |
| Model | opus for high-severity; sonnet for low-severity batch |
| Effort | high |

Each agent attempts to REFUTE the finding by checking: (1) whether the diff actually introduces the claimed issue, (2) whether an existing test already covers it, (3) whether the "missing" piece is intentionally deferred. Return verdict: confirmed or refuted with one-sentence evidence.

### Dedup and merge

After Tier 1 completes (or after manual tracing for small diffs), deduplicate findings where the same symbol appears in multiple files' traces before proceeding to Tier 2. This is a main-agent step, not a sub-agent.

### Agent budget by change-set size

| Change set | Max total agents | Typical breakdown |
|------------|-----------------|-------------------|
| Small (1–3 files, no contracts) | 0 | Main agent only |
| Medium (4–8 files, 1–2 contract types) | 6–8 | 4–6 Tier 1 + 1–2 Tier 2 |
| Large (8+ files, 3+ contract types) | 14 | 8 Tier 1 + 3 Tier 2 + 3 Tier 3 |

## What to look for

Classify each finding into exactly one bucket:

- **Unimplemented**: a change specified in the plan has no corresponding implementation in the current workspace — the code, config, schema, or test is entirely absent.
- **Incomplete/insufficient**: a plan-specified change is partially implemented but missing branches, error paths, migrations, or other elements the plan requires.
- **Interface drift**: a signature, return shape, exception type, schema, or config key changed but at least one caller/consumer/test/doc was not updated to match.
- **Behavioral regression**: a code path that previously produced behavior X now produces behavior Y, where Y is not explicitly intended by the plan. Include test failures, type/lint errors, and removed validations.
- **Incorrect implementation**: the code exists but its logic, structure, or behavior diverges from what the plan specifies.

For each finding, record: file:line (or plan section if unimplemented), bucket, one-sentence evidence, and proposed action.

## Action policy

- **Fix directly** only when the correct change is mechanical and unambiguous (e.g., update a caller to a renamed argument, restore a removed import, re-add a deleted test that still passes). Preserve existing behavior when intent is unclear.
- **Flag and do not fix** when the resolution requires a product or design decision, when the original change itself appears to be the defect, or when fixing would expand scope beyond the audited change set. Note the open question.
- Never invent an implementation for a missing component whose intended behavior is not specified by the plan, existing code, or tests.

## Verification

After applying fixes, run the project's test, type, and lint commands relevant to the touched files in parallel and report results. If any command is unavailable or out of scope, say so explicitly rather than skipping silently.

As a final step, assess whether any symbols or contract types were not covered by the fan-out. If gaps exist, note them explicitly in the output rather than silently omitting them.

## Output

Produce a todo list with one item per finding, grouped by bucket and ordered by severity (unimplemented > incorrect > broken contracts > regressions > incomplete > cleanup). Mark each item as `fixed`, `needs-decision`, or `flagged`. End with a plan-coverage summary (what percentage of plan items are fully, partially, or not implemented), the verification results, and any unresolved questions.
