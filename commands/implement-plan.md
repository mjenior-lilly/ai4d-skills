# implement-plan

Review the provided plan file, understand its purpose and fit within the existing codebase, then implement the plan's to-do items in order.

## Method

1. Identify the exact plan file or plan text to implement. If no plan is provided or the plan source is ambiguous, ask for the plan before making changes.

2. **Context Fan-Out** — Read the relevant code, tests, configuration, and documentation needed to understand how the plan fits the current repository. Spawn parallel read-only sub-agents (one per distinct subsystem or layer touched by the plan) to gather context concurrently. Each sub-agent reads its assigned area and returns a structured summary of relevant patterns, contracts, and constraints. Prefer existing patterns and direct contract changes over new abstractions or compatibility layers unless the plan explicitly requires them.

   Sub-agent parameters:
   - Agents: 2–4 (one per distinct subsystem/layer in the plan)
   - Model: haiku or sonnet (read-only context gathering)
   - Effort: low
   - Isolation: none (read-only)
   - Agent type: Explore

3. **Plan Re-Sequencing** — Before implementation, classify each to-do item by complexity and file scope:
   - `trivial`: rename, import fix, config change
   - `moderate`: new function, test update, single-file logic
   - `complex`: new module, cross-cutting refactor, contract change

   Build a dependency graph from the plan's file references. Identify clusters of items that touch completely disjoint file sets (no shared imports, no shared contracts). Re-order items to group parallelizable clusters together while preserving necessary ordering constraints. Output a dependency DAG when beneficial; retain the original flat order for simple plans where all items are tightly coupled.

   Sub-agent parameters:
   - Agents: 1
   - Model: sonnet
   - Effort: medium
   - Isolation: none

4. **Implementation** — Work through the plan's to-do items respecting the dependency graph from step 3. Apply complexity-based routing:

   - **Trivial items** sharing no files may be batched into a single low-effort sub-agent with worktree isolation.
   - **Moderate items** run in the primary agent or a sonnet-tier sub-agent.
   - **Complex items** remain with the orchestrating agent (opus-tier reasoning).
   - **File-disjoint clusters** identified in step 3 may be implemented in parallel via worktree-isolated sub-agents when their file sets have no overlap.

   Keep each edit scoped to the current item, but update later items if earlier implementation evidence makes the original sequence stale or incorrect. When a to-do is unclear, inspect the code first and choose the smallest implementation that satisfies the plan. Ask a focused question only when the ambiguity could materially change behavior, data contracts, or user-facing results.

   Sub-agent parameters for trivial batches:
   - Agents: 1–3
   - Model: haiku
   - Effort: low
   - Isolation: worktree

   Sub-agent parameters for file-disjoint parallel:
   - Agents: 2–4 (capped by disjoint clusters)
   - Model: sonnet
   - Effort: medium
   - Isolation: worktree (mandatory for parallel writes)

5. **Parallel Verification** — After each meaningful change or logically cohesive group of items, run verification concurrently by spawning parallel sub-agents for independent checks (tests, type checks, lint). Fix issues you introduced before moving on.

   Sub-agent parameters:
   - Agents: 2–3 per verification pass
   - Model: haiku
   - Effort: low
   - Isolation: none (read-only verification)

6. **Post-Implementation Audit** — After all items are implemented, spawn a single review-focused sub-agent to verify contract consistency, import completeness, and test coverage against the plan. This agent operates with fresh context and checks for interface drift, missing pieces, and behavioral regressions that the implementing agent may miss due to context saturation.

   Sub-agent parameters:
   - Agents: 1
   - Model: sonnet or opus (for complex plans)
   - Effort: high
   - Isolation: none (read-only)

7. Do not stop with partially completed to-dos unless blocked by missing information, failing external dependencies, or an explicit user instruction. If blocked, explain the blocker, the evidence gathered, and the smallest next action needed to continue.

## Speculative Lookahead (Optional)

When implementing tightly sequenced items where item N+1's preconditions are very likely stable regardless of item N's outcome, a speculative sub-agent may begin item N+1 in a worktree while the main agent completes item N. If item N's completion invalidates the speculative work, discard it; otherwise, merge it. Use this only when the discard probability is low (items are mostly independent).

Sub-agent parameters:

- Agents: 1 (speculative lookahead)
- Model: sonnet
- Effort: medium
- Isolation: worktree (mandatory for speculative writes)

## Output

When implementation is complete, report:

1. **Implemented**: the plan items completed and the main behavior changed.
2. **Verification**: the checks run and their results.
3. **Blocked Or Deferred**: any plan items not completed, with the reason and next action.
