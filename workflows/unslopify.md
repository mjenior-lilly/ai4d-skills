# unslopify workflow

Critically explore all code in a target repository workspace and identify every element that is poorly constructed, difficult to maintain, difficult to navigate, or following a bad pattern characteristic of code written by agents over long unsupervised stretches. The deliverable is one ranked report, written to a markdown file on every run. Nothing else.

## hard constraints

1. **Read-only.** Do not edit, create, move, delete, or reformat any file in the target repository. Do not run formatters, linters with `--fix`, codemods, or package managers that mutate lockfiles. Do not stage, commit, branch, push, or open a PR or MR under any circumstance, including when the user later asks mid-run — that is a separate workflow (`simplification-audit-to-pr.md`), and switching to it requires a new invocation.
2. **Terminates at a written report.** There is no plan phase, no implementation phase, and no verification-by-execution phase. The run is not complete until the report artifact exists on disk. Findings carry a recommended action so a human or a later workflow can act; this workflow never acts on them.
3. **One writable artifact, always written.** Every run ends by persisting the report to a single markdown file (see [report artifact](#report-artifact)) — no exceptions for short registers, zero findings, incomplete coverage, or an early stop. That file must live outside version control or in an existing untracked reports directory, and must never be staged. It is the only file this workflow is permitted to write.
4. **Read-only commands only.** Permitted: file reads, `grep`/`rg`, `git log`/`show`/`diff`/`ls-files`, dependency and config inspection, and analysis tools invoked in report-only mode (`ruff check` without `--fix`, `mypy`, `pytest --collect-only`, `radon`, `jscpd`, `tsc --noEmit`, `npm ls`). Do not run the test suite, build the project, or execute repository entry points.

## scope input

1. The target is `{{REPO_ROOT}}`. If it is not supplied, resolve it with `git rev-parse --show-toplevel` from the current directory and state the resolved path in the report before proceeding.
2. If the user names specific packages, directories, or a subtree, that is the audit scope and the coverage ledger covers only that scope. Otherwise the scope is every first-party source file in `{{REPO_ROOT}}` after the ignore list is applied.
3. `{{REPO_ROOT}}` need not be the current working directory. Never audit files outside it, and never write outside the report artifact path.

## definitions

**Live code** is behavior reachable from a real entry point: public API, CLI command, HTTP or RPC handler, scheduled job, event listener, exported library surface, framework or plugin discovery, serialization hook, persisted schema, migration, or a test that protects a real workflow. Treat convention-reachable and dynamically-dispatched code as live until proven otherwise.

### finding categories

| category | what it captures |
| --- | --- |
| `slop-artifact` | Residue of generation rather than design: comments and docstrings that restate the line below, placeholder or TODO scaffolding never filled in, parameters and config keys accepted "for compatibility" with no consumer, unused imports and locals, invented abstractions with exactly one implementation and one caller, example or demo code left in a production module, redundant re-exports, numbered or `_v2`/`_new`/`_final` symbol names living beside their predecessors. |
| `defensive-noise` | Error handling that costs correctness: bare or blanket `except Exception` / `catch (e) {}`, handlers that swallow or log-and-continue past a real failure, guards for conditions the type system or caller set makes impossible, silent fallback defaults that mask a missing configuration, retries around non-idempotent work, `# type: ignore` / `@ts-ignore` / `# noqa` suppressions without a cited reason. |
| `structural-debt` | Construction that blocks safe change: functions or files far beyond the repository's own norm, parameter lists that should be a type, nesting or branch depth that hides the happy path, modules with no single responsibility, cyclic or upward imports, indirection layers that forward without transforming, global mutable state, business logic embedded in a CLI or handler body. |
| `flat-topology` | Layout that has accreted rather than been organized, so the tree no longer tells a reader where anything lives. Directory fan-out far beyond the repository's own norm — dozens of sibling modules at one level with no subpackage boundary; unrelated domains co-located in one directory; catch-all modules (`utils`, `helpers`, `common`, `core`, `misc`, `shared`) that grew instead of being partitioned; a package root whose module list must be read in full to find one behavior; modules that grew past the norm because appending was cheaper than splitting; non-discriminating filenames (`data`, `process`, `handler2`, `manager`, `service`) that make the tree grep-hostile; a package whose `__init__.py` exports nothing, forcing a reader to open every file to learn the surface; missing module docstrings across a flat set of siblings; one god-module that most of the repository imports from. |
| `convention-drift` | The same decision made differently across modules: naming, import style, error-raising, logging, configuration access, path handling, typing depth, async style, docstring format, or return-shape conventions that contradict the repository's dominant pattern. |
| `contract-fiction` | Model-facing or human-facing text that the code contradicts: README, docstring, type hint, schema, CLI help, agent instruction, or config comment describing behavior that does not occur; referenced files, flags, commands, or env vars that do not exist; version or dependency claims that disagree with the manifest. |
| `dependency-hygiene` | Declared-but-unused, used-but-undeclared, duplicated-purpose, unpinned-where-the-repo-pins, abandoned, or vendored-by-copy-paste dependencies; a bespoke implementation of something an already-installed dependency or the standard library provides. |
| `test-theater` | Tests that look like coverage and are not: mocking or patching the unit under test, asserting on log strings or call counts instead of behavior, `assert True` / `assert result is not None` as the only assertion, snapshot assertions over whole objects, tests whose scenario cannot occur through supported inputs, order-dependent or clock/network/filesystem-dependent tests, and duplicated setup asserting one contract many times. |
| `duplication` | Exact or near-duplicate functions, classes, blocks, literals, or rule tables; parallel implementations of one concept that have drifted apart. Name the designated source of truth and every caller that would have to move to it. |
| `dead-code` | Functions, classes, files, exports, feature-flag branches, or config keys with no live caller, proven after checking dynamic and convention-based reachability. |
| `bug` | A behavior defect found while tracing: wrong condition, broken invariant, unreachable branch that should be reachable, race, resource leak, or logic diverging from a documented contract. |

Assign exactly one primary category per finding; note secondary categories in the evidence field rather than filing duplicates.

### severity

| severity | bar |
| --- | --- |
| `critical` | Data loss, security exposure, silently wrong results, or a crash on a commonly taken path. |
| `high` | Incorrect behavior on a realistic path; dead, fictional, or theatrical code in a public interface or in the primary test suite; structure that makes a likely change unsafe to attempt; a layout in which the code owning a common behavior cannot be located without reading unrelated modules. |
| `medium` | Incorrect behavior on an edge path; internal dead code; structural debt, flat topology, or convention drift with a stated, concrete maintenance cost. |
| `low` | Localized noise with no behavioral consequence: restating comments, unused parameters, single-site inconsistency. |

Severity is impact if left alone, not effort to fix. Effort is a separate field.

### confidence

`confirmed` — traced from an entry point, a complete caller set, a framework convention, or a measured signal; enough to act on.
`likely` — strong static evidence, one reachability or intent detail unresolved; state the exact verification step.
`uncertain` — reachability, intent, or external use unclear; report it with the verification step and do not recommend removal.

Report `likely` and `uncertain` findings. Do not omit them and do not upgrade them.

### evidence rules

Two classes of claim, two different bars. Apply the bar that matches the claim, not the one that is easier to satisfy.

**Class A — reachability and behavior claims** (`dead-code`, `duplication`, `bug`, `contract-fiction`, and any `defensive-noise` or `slop-artifact` finding asserting that code never runs or that a failure is masked):

1. Cite file, symbol, and line range for every location.
2. Trace from a real entry point, or present the complete static caller set from a repo-wide search.
3. Before calling anything unreachable, check dynamic imports, plugin and entry-point registries, decorators, reflection, string-keyed dispatch, `__init__.py` and `pyproject.toml` exports, test discovery, serialization hooks, migrations, and fixtures.
4. For `contract-fiction`, quote both sides — the claim and the contradicting code.
5. Never infer deadness, duplication, or defect from a name, a file location, or intuition.

**Class B — construction, maintainability, and navigability claims** (`structural-debt`, `flat-topology`, `convention-drift`, `slop-artifact` where the claim is that code is poorly built, `dependency-hygiene`, `test-theater`):

1. Cite file, symbol, and line range for every location. For `flat-topology`, cite the directory path plus the specific modules that constitute the fan-out.
2. Name at least one **measured signal**, with the number and the command or read that produced it. Acceptable signals include: line count of the function or file against the repository's own median or 90th percentile; parameter count; maximum nesting or branch depth; caller count for an abstraction; length in lines or tokens of a duplicated span; count of sibling modules following the *other* convention; comment lines that restate the adjacent statement; mock or patch count versus assertion count in a test; import-cycle membership; declared-versus-imported dependency diff.
3. Signals specific to `flat-topology`: file count in the directory against the repository's median and maximum directory fan-out; tree depth against total file count; count of top-level modules in the package root; number of distinct, separable domain concerns co-located in one directory; symbol count and unrelated-symbol count in a catch-all module; number of first-party modules importing a single god-module; number of siblings with no module docstring; count of names in a directory that do not discriminate their contents.
4. For `convention-drift`, cite a **counterexample**: at least two locations following the dominant convention, so drift is demonstrated rather than asserted as preference. For `flat-topology`, cite the partition the code already implies — the concern groups a reader can name from the existing modules — so the finding rests on separable content, not on a directory-size preference.
5. Compare against the repository's own norms, not an external ideal. A 90-line function in a repository whose median is 80 is not a finding, and a flat package of a dozen cohesive modules is not a finding.
6. Never write "this looks AI-generated", "this feels over-engineered", "this is too flat", or any claim whose only support is impression. If no signal can be measured, the finding does not exist.

**Anti-fabrication rule, both classes.** Do not report a metric you did not measure or a line range you did not read. If a tool was unavailable, say so and fall back to a signal you can produce by reading. Findings that survive to the report must be reproducible by the reader from the cited evidence alone.

## non-goals

1. Do not recommend behavior changes, API breakage, or dependency upgrades as findings in themselves — report the defect and its blast radius; the decision is the reader's.
2. Do not report anything the repository's configured linter, formatter, or type checker already enforces and already flags; inspect those configurations in preflight and exclude their output. Error-handling and typing-suppression defects remain in scope even when a style rule touches them, because they are behavioral.
3. Do not report vendored, generated, minified, third-party, or fixture code as poorly constructed. Do report a *generated-code boundary* that is edited by hand or checked in stale, as `contract-fiction`.
4. Do not propose speculative architecture, rename-for-taste, or extraction merely because a file is long.
5. Do not recommend hierarchy for its own sake. A `flat-topology` finding must name the concern groups the existing modules already fall into and stop there; do not invent a layered directory scheme, do not recommend nesting a package that a reader can hold in one screen, and do not propose a move whose only benefit is a tidier tree. Over-nesting is its own navigability defect — report it as `flat-topology`'s inverse under `structural-debt` when a directory chain adds depth without adding a boundary.
6. Do not pad. An honest short report beats a long one, subject to the coverage rule below.

## coverage rule

"All code" is the objective, and partial coverage is permitted only when it is declared.

1. Every first-party source module in scope is either audited or explicitly listed as unaudited with a reason. There is no silent truncation and no implicit top-N cut.
2. The findings register is complete, not a top-10. Rank it, group it, collapse repeated instances of one pattern into a single finding listing every location — but do not drop findings to hit a length target.
3. A report with zero findings is acceptable **only** when the coverage ledger shows every in-scope module audited. Zero findings plus unaudited modules is a failed run: report what was covered and state that the audit is incomplete.
4. If budget runs out, stop auditing and report; do not thin the ledger to make coverage look complete.

## model tiers

Use the smallest tier that can reliably do the assigned reading. Escalate when the work turns out to involve cross-file relationships, dynamic reachability, or boundary contracts. Omitting a model override and inheriting the session model is an acceptable default; only override when the tier genuinely differs.

complex = Claude-Opus-5, GPT-5.6-Sol
standard = Claude-Sonnet-5, GPT-5.6-Terra, Gemini-3.7-Flash
quick = Claude-Haiku-4.5, GPT-5.6-Luna, Gemini-3.7-Flash

| tier | use for | thinking |
| --- | --- | --- | --- |
| quick | Mechanical inventory: censuses, line-count, depth, and directory fan-out metrics, dependency diffs, import graphs, ignore-list construction. | low |
| standard | Single-domain scout reading: one package or top-level module with clear boundaries. | medium |
| complex | Public APIs, schemas, migrations, framework discovery, security-sensitive code, dynamic dispatch, or any scope where reachability is unclear. | high |
| verifier | Adversarial refutation of a finding, and coordinator-side confirmation. | standard for `medium`/`low` findings; complex for `critical`/`high` findings and for any Class A removal claim | medium; high for `critical`/`high` |

## subagent topology and budgets

Stated once; this section is the only authority on counts and limits.

1. **Scouts.** 1 scout for a narrow or single-package scope; 2–4 for a medium repository; up to 6 only when the repository has that many genuinely independent domains and the coordinator can synthesize all of their output. Never exceed 6.
2. **Assignment.** Each scout receives a non-overlapping scope, the shared preflight context, the ignore list, its budget, and its explicit unassessed boundaries. Do not assign two scouts to the same files unless independent review is deliberately wanted.
3. **Budget.** Give each scout a hard ceiling in tool calls proportional to scale tier — roughly 40 for *small* (<500 files), 80 for *medium* (500–5k), 150 for *large* (>5k or monorepo). A scout that reaches its ceiling returns partial findings with an explicit `coverage` note. Exceeding budget or fabricating completeness is a failure; returning partial work is not.
4. **Refuters.** One refuter per `critical` or `high` finding, up to 8 total; if more than 8 qualify, refute the top 8 by severity then impact and mark the remainder `coordinator-verified only`.
5. **Coordinator verification, bounded.** The coordinator independently re-checks every `critical` and `high` finding against the cited lines, plus a sample of at least 25% or 3 (whichever is larger) of `medium` and `low` findings. Findings outside the sample ship labeled `scout-reported, coordinator-unverified` — never silently accepted, never silently dropped.
6. **Never parallelize** the synthesis, ranking, or report-writing step. There is one coordinator-owned register.
7. Do not use subagents at all when the scope is a single file or small module; direct reading costs less than coordination.

## phases

A phase advances only when its gate is satisfied.

| phase | gate |
| --- | --- |
| 0 preflight | Scope resolved, scale tier set, ignore list published, tooling configuration inspected, scout budgets assigned. |
| 1 recon | Every scout has returned findings meeting the evidence rules plus an explicit coverage note. |
| 2 synthesis | Findings deduplicated, refuted findings removed or downgraded, verification labels applied, coverage ledger complete. |
| 3 report | Every finding has location, evidence, severity, confidence, and recommended action; ledger accounts for every in-scope module; the report artifact is written to disk and its path is named in the final message. |

### 0. preflight

Do this before spawning anything, and hand the result to every scout as shared context.

1. **Census.** File count, line count, language breakdown, the 20 largest files, tree depth. Compute the repository's own median and 90th-percentile function and file length — these become the baseline for Class B signals. Set the scale tier.
2. **VCS state.** Branch, HEAD SHA, dirty-file count, first and most recent commit date, distinct authors in the last 12 months. High file count with few authors and a compressed commit history is context for interpreting slop density; it is never itself a finding.
3. **Structure.** Monorepo versus single package, workspace manifests, package boundaries, real entry points, exported surfaces.
4. **Topology baseline.** Before judging layout, measure: files per directory (median, 90th percentile, and maximum, with the directory named); tree depth distribution against total file count; module count in each package root; symbol count per module against the repository median; the catch-all modules present and their symbol counts; the most-imported first-party modules with their importer counts; and the directories whose siblings carry no module docstring. Record which directories are cohesive at their current fan-out — these are the counterexamples that keep `flat-topology` findings honest. Note where the layout is imposed by a framework or tooling convention (Django apps, Next.js routes, `tests/` mirroring, Terraform modules), because convention-imposed flatness is not a finding.
5. **Tooling configuration.** Locate and read linter, formatter, type-checker, and test configuration. Record which rules are enabled, so already-enforced style is excluded per non-goal 2. Note rules that are configured but disabled or suppressed repo-wide — that itself is a `dependency-hygiene` or `defensive-noise` candidate.
6. **Convention baseline.** Before judging drift, record the repository's dominant conventions for naming, imports, error raising, logging, configuration access, typing depth, and docstring format, each with two example locations.
7. **Reachability conventions.** List the plugin registries, dynamic dispatch sites, decorators, framework discovery rules, serialization hooks, migrations, fixtures, and generated-code boundaries that make code live without a static caller. Publish this list; scouts must check it before any `dead-code` claim.
8. **Ignore list.** Publish the set of paths no scout reads: lockfiles, vendored and third-party trees, build output, generated code, minified bundles, binary assets, `.venv`/`node_modules`, caches, and fixtures over 50 KB. Reading a lockfile is a budget failure, except for the single dependency diff in step 9.
9. **Dependency inventory.** Declared dependencies from the manifest versus imports actually present in first-party source, in both directions. This is the input to `dependency-hygiene`.
10. **Existing documentation inventory.** `README*`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING*`, `docs/`, ADRs, agent and prompt files. Treat every claim as an unverified assertion to be checked against code — this is the input to `contract-fiction`.

Steps 1 and 4 are the only whole-tree measurements in the workflow and they belong to the coordinator, because `flat-topology` is the one category a scope-bounded scout structurally cannot see: a scout given one directory has no view of fan-out across siblings. The coordinator owns every `flat-topology` finding above the single-directory level and states that ownership in the report.

### 1. recon

Scouts audit their assigned scope against all eleven categories, applying the evidence rule that matches each claim. Each scout returns only evidence-backed findings, in the finding format below, plus a coverage note naming every file it read, every file it skipped, and why.

For `flat-topology`, a scout reports only what is visible inside its own scope — fan-out within a directory it owns, catch-all modules, non-discriminating names, missing module docstrings, an empty `__init__.py` surface — and reports the concern groups it can name from the module contents. Cross-directory and repo-root flatness is the coordinator's, per the preflight note. A scout must not recommend a target layout; it names the separable concerns and stops.

Reject and return any scout output that asserts a Class B claim without a measured signal, asserts a Class A claim without a trace or complete caller set, reports a metric with no command behind it, or proposes a directory scheme.

### 2. synthesis

1. Deduplicate across scouts; merge instances of one pattern into a single finding listing every location.
2. Spawn refuters per the topology section. A refuter is instructed to *break* the finding: prove the code is reachable, prove the convention is not dominant, prove the metric was mismeasured, prove the contract claim is stale rather than false, prove a flat directory is cohesive at its current fan-out or that its layout is framework-imposed. Remove refuted findings; downgrade partially refuted ones in confidence and say so.
3. Assemble the repo-level `flat-topology` findings the coordinator owns, using the topology baseline from preflight and the concern groups the scouts named. One finding per directory or package root, not one per file.
4. Apply coordinator verification and the `coordinator-unverified` labels.
5. Rank: severity first, then confidence, then blast radius, then effort. Ties break toward the finding with more locations.
6. Build the coverage ledger from the scout coverage notes.

### 3. report

Write the full report to the report artifact first, then present it to the user. The artifact is the deliverable; the chat rendering is a copy of it. Never end a run with the report existing only in the conversation — it must survive context compaction and the session ending.

Writing the file is not conditional on register size, finding count, or coverage completeness. A run that found nothing writes a report saying so with the coverage ledger that proves it. A run that stopped early writes a report of what it covered, with the stop condition and the honest ledger. If the register is short enough to read comfortably inline, still write the file and still name its path.

When the register is very large, the user-facing message may be the executive summary, the severity counts, the top findings by rank, and the artifact path, with the complete register living in the file. State plainly that the message is abridged and the file is complete.

## report artifact

One markdown file, written on every run. Path preference order: an existing untracked or gitignored reports directory; otherwise `{{REPO_ROOT}}/unslopify-audit-<YYYYMMDD>-<short-sha>.md`. Verify the path is gitignored or state plainly that it is not. Never stage it. Name the path in the final message.

The file contains the complete report in the format below — all five sections, the full untruncated findings register, and the full coverage ledger — regardless of what the user-facing message shows.

If the preferred path cannot be written (read-only filesystem, permission denied, unresolvable `{{REPO_ROOT}}`), fall back to a temporary directory, and if that also fails, say explicitly in the final message that no artifact could be written and why, then emit the complete report inline. A silently missing artifact is a failed run.

## report format

### 1. Executive summary

Resolved `{{REPO_ROOT}}`, scale tier, and audit date. Overall assessment of construction quality, plus one sentence on whether the layout lets a reader find the code that owns a given behavior. The three to five dominant themes, each with the count of findings supporting it. Total findings by severity. Explicit statement of what was not assessed. If the audit is incomplete, say so in the first sentence.

### 2. Coverage ledger

One row per first-party module in scope. No module omitted.

| module | files | lines | status | reason if not fully audited | scout |
| --- | --- | --- | --- | --- | --- |

`status` is `audited`, `partial`, or `not audited`. Follow the table with the ignore list applied and the total in-scope files audited versus skipped.

### 3. Baseline

The measured norms from preflight that Class B findings are judged against: median and 90th-percentile function and file length; the topology baseline — files per directory (median, 90th percentile, maximum), depth distribution against file count, package-root module counts, catch-all modules with their symbol counts, most-imported first-party modules with importer counts, and the directories judged cohesive at their current fan-out; dominant conventions with their example locations; framework- or tooling-imposed layout that was excluded from judgment; and the reachability conventions that kept code alive during the audit. A reader must be able to check any Class B finding against this section.

### 4. Findings register

Grouped by category, ranked by severity within each group, with the global rank noted. Complete, not truncated.

For each finding:

```
<global rank>. <short title>
   Category:      <one of the eleven>
   Severity:      critical | high | medium | low
   Confidence:    confirmed | likely | uncertain
   Verification:  coordinator-verified | refuter-tested | scout-reported, coordinator-unverified
   Location(s):   path/to/file.py:120-168  (every occurrence; directory path for flat-topology)
   Signal:        <measured number + how it was produced — required for Class B>
   Evidence:      <trace, caller set, or quoted contradiction — required for Class A>
   Why it hurts:  <one or two sentences on maintenance, navigability, or behavioral cost, not taste>
   Blast radius:  <callers, contracts, schemas, tests, and docs that a fix would touch>
   Effort:        small | medium | large
   Action:        remove | refine | rewire | restructure | partition | normalize | add | document | defer
   Next step:     <for likely/uncertain only: the exact check that would settle it>
```

`Action` vocabulary: `remove` delete it, nothing live depends on it; `refine` keep the role, fix the defect in place; `rewire` it should exist but is reached from the wrong place or not at all; `restructure` split, merge, or flatten within a module; `partition` the content is separable and should move into subpackages or a differently-named module — name the concern groups the existing code already falls into, not an invented scheme; `normalize` bring it onto the repository's dominant convention; `add` the fix requires new code, such as a missing guard or a real assertion; `document` the code is correct and the text describing it is wrong; `defer` real but not worth acting on yet, with the reason.

A `partition` action must state the blast radius honestly: moving modules breaks import paths, and for a published package that is an API change. Say so in the blast-radius field rather than presenting a move as free.

### 5. Residual uncertainty

Every `likely` and `uncertain` finding with its next step, every finding shipped `coordinator-unverified`, tools that were unavailable and the signal used instead, and any area where the ignore list may have hidden first-party code.

## stop conditions

Stop and report what is known, rather than guessing, when:

1. `{{REPO_ROOT}}` cannot be resolved, is not a repository, or contains no first-party source after the ignore list.
2. A finding would require executing repository code to confirm — report it as `uncertain` with the execution step named, since this workflow does not run code.
3. Scout budgets are exhausted before coverage is complete — report with an honest ledger.
4. The user asks mid-run for the findings to be implemented, committed, or turned into a PR — state that this workflow is read-only and name `simplification-audit-to-pr.md` as the next invocation.

Every stop condition still terminates in a written report artifact naming the condition that triggered it, the phase reached, and the coverage achieved — except condition 1, where there is no resolvable `{{REPO_ROOT}}` to write into and the finding is stated in the message instead. Stopping early narrows the report's scope; it never cancels the artifact.

Ask a clarifying question only when the audit scope itself is ambiguous — which repository, which packages, or whether a large vendored or generated tree is first-party. Ask it once, before preflight, and proceed on a stated assumption if unanswered.
