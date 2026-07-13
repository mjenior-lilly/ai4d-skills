# agents/

System prompt text and layered policy files that define baseline agent behavior. Unlike the task-scoped content in `commands/` and `skills/`, these files shape how an agent operates across every task in a session.

## Layered policy files

`CLAUDE.md` is the entry point: it holds the common instructions that apply to any agent working in a directory, and it delegates the details to three companion files that are read on demand rather than loaded up front. This keeps the always-loaded instruction surface small while still giving the agent deep guidance at the moment each kind of decision arises.

- `CLAUDE.md` - common cross-cutting instructions: commit-message hygiene (no attribution trailers), graceful handling of missing referenced files, pointers to the three policy files below, a sub-agent delegation section (quick-reference table and selection rules that defer to `skills/sub-agents.md` as the authoritative source), and an always-on directive to capture confirmed project facts into an Obsidian vault's `40_Project/` folder via the `obsidian` skill.
- `CODE.md` - coding style and structural preferences, consulted before writing or modifying programmatic code. Covers contract-first changes (update schemas, interfaces, and all callers together; no compatibility shims), minimal surface area, dead-code removal, refactoring guardrails against speculative abstraction, matching existing conventions, minimal diffs, verification over assumption (never "should work"), and how to handle ambiguity by risk level.
- `OPINIONS.md` - the user's stated preferences on subjective design, tooling, and dependency choices, consulted before making a recommendation where more than one reasonable option exists. Structured as a scaffold (languages, libraries, architecture, testing, tradeoffs) that gets filled in as preferences are established; empty sections carry no opinion.
- `VOICE.md` - how to write user-facing prose to saved artifacts, files, or CLI output. Defines verbosity guardrails (what to cut, what never to cut), a list of assistant artifacts to avoid (throat-clearing, filler transitions, forced symmetry, stylistic dashes), rules for preserving useful structure, and output posture.

## Standalone prompts

- `SYSTEM.md` - a complete CLI-focused coding-agent system prompt emphasizing directness, minimal diffs, contract-first changes, deterministic verification, realistic testing, and cautious handling of destructive operations. Use it as a base policy when the agent has shell access, repository read/edit tools, a need to run tests or validations, and responsibility for narrowly scoped engineering changes.

- `judge.md` - a corpus-grounded benchmark response-evaluation policy that scores a target LLM response against a `create-test-dataset` entry (see `workflows/`), including canonical answers, required facts, reasoning paths, source references, known negative responses, and optional domain-specific context for specialized or novel corpus knowledge.

- `classifier.md` - an example single-label classifier prompt that emits one routing label and nothing else. It illustrates a broadly useful pattern: a cheap, fast, small-model call placed in front of a pipeline to decide the downstream handoff, rather than burning a large model on triage. The prompt is deliberately constrained — strict label set, explicit precedence and tie-break rules, few-shot anchors, prompt-injection resistance over the classified content, and a single-token-style output contract — so the result is reliable enough to branch on. The specific labels (document subject areas) are placeholder domain knowledge; the reusable idea is the shape of a constrained classifier that gates routing, escalation, or which specialized agent or skill runs next.

- `prompt-skeleton.md` - a supplementary reference for designing effective sub-agent prompts, covering hybrid prompt styles, drift control for multi-turn agents, pitfalls, and eagerness knobs. Defers to `skills/sub-agents.md` for the authoritative prompt structure, model selection, and thinking-level guidance.

## How to use

Drop `CLAUDE.md` and its companion files into a directory an agent works in (or merge their content into your harness's equivalent instruction file), and the agent will pick up the layered policies automatically. Use `SYSTEM.md` as a full system prompt for a coding agent, and `judge.md`, `classifier.md`, and `prompt_skeleton.md` as standalone building blocks for evaluation pipelines, routing layers, and new prompt authoring respectively.
