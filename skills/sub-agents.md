---
name: sub-agents
description: Select the right model and write effective prompts when delegating work to sub-agents via the Agent tool, Workflow tool, or Codex CLI. Use this skill whenever a task requires spawning one or more sub-agents.
allowed-tools: Agent(*) Workflow(*) Bash(codex *)
---

Use this skill whenever you delegate work to a sub-agent. It governs model selection and prompt structure for every Agent tool call, Workflow agent() invocation, or Codex CLI execution.

## Model ratings

Higher = better. **Cost** reflects actual spend (higher = cheaper). **Intelligence** is unsupervised problem-solving ceiling. **Taste** is quality of user-facing output (UI, code style, API design, prose). **Speed** is latency to first useful output.

| Model | Cost | Intelligence | Taste | Speed |
| --- | --- | --- | --- | --- |
| gpt-5.5 | 6 | 8 | 5 | 6 |
| sonnet-5 | 5 | 5 | 7 | 7 |
| opus-4.8 | 4 | 7 | 8 | 5 |
| haiku-4.5 | 10 | 3 | 3 | 10 |

## Selection rules

Apply the first matching rule:

1. **Quick classification or text evaluation** (sentiment, labeling, yes/no judgments, format validation, triage — no code generation) → **haiku-4.5**
2. **Bulk/mechanical work** (implementation against a clear spec, data transforms, migrations, deterministic refactors) → **gpt-5.5**
3. **User-facing output** (UI, copy, API surface — anything a human reads or calls; requires taste ≥ 7) → **opus-4.8**; sonnet-5 only if the task is also simple
4. **Review of plans or implementations** → **opus-4.8**; gpt-5.5 may supplement as a second reviewer but never sole reviewer
5. **Everything else** → cheapest model whose intelligence clears the task difficulty bar

Tie-break order for shipping work: intelligence > taste > cost.

## Hard constraints

- **Haiku is classification-only** — never use it for code generation, implementation, review, or any task requiring intelligence > 3 or taste > 3.
- **Never downgrade** below what the rules prescribe to save cost.
- **Always escalate freely**: if a model's output misses the bar, rerun with a smarter model without asking. Escalating costs less than shipping mediocre work.

## Thinking level

Default to **medium** effort for all sub-agents. Only deviate when the task clearly demands it:

| Effort | When to use |
| --- | --- |
| low | Haiku classification tasks; trivial reformatting |
| medium | **Default for all other work** — implementation, review, analysis, generation |
| high | Reserved for tasks that fail at medium: multi-step reasoning with tight correctness requirements, novel architecture decisions, or adversarial verification |

Do not pre-emptively escalate to high. Start at medium; escalate only if the output quality is insufficient.

## Invocation mechanics

| Model | How to invoke |
| --- | --- |
| gpt-5.5 | Codex CLI only: `codex exec`, `codex review`, or the codex-implementation / codex-review / codex-computer-use skills. For investigation or data analysis: `codex exec -s read-only` with a self-contained prompt. |
| haiku-4.5, sonnet-5, opus-4.8 | `model` parameter on the Agent or Workflow `agent()` call. Set `effort` parameter to control thinking level. |

## Prompt structure for sub-agents

When writing a sub-agent prompt, include these blocks in order. Omit any block that adds no signal for the specific task.

1. **Role** — one sentence: who the agent is and what standard it operates at
2. **Goal** — the single deliverable; define what "done" looks like
3. **Constraints** — ranked rules (always X, never Y); most important first
4. **Method** — 3–5 ordered steps including a verification step
5. **Context** — facts the agent cannot infer (file paths, schemas, prior decisions)
6. **Format** — exact output structure (sections, keys, length limits)

Keep prompts concise. Every sentence should constrain the prediction space or supply a fact the agent lacks. Remove anything the agent can infer from its tools or the codebase.

### Pitfalls to avoid

- **Contradictory instructions** — rank constraints so the agent knows which wins
- **Overlong examples** — one small example beats three large ones; examples consume context budget
- **Unnecessary chain-of-thought** — only request step-by-step reasoning for genuinely hard tasks; mechanical work doesn't benefit and wastes tokens
- **Identity collisions** — don't mix conflicting personas; separate tone from technical constraints
