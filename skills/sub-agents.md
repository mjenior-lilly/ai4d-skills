---
name: sub-agents
description: Select the right model and write effective prompts when delegating work to sub-agents via the Agent tool, Workflow tool, or Codex CLI. Use this skill whenever a task requires spawning one or more sub-agents.
allowed-tools: Agent(*) Workflow(*) Bash(codex *)
---

These rules govern model selection and prompt structure for every Agent tool call, Workflow `agent()` invocation, and Codex CLI execution.

## Model ratings

Higher scores are better. **Cost** rates affordability, so a higher score means a cheaper model. **Intelligence** rates the model's unsupervised problem-solving ceiling. **Taste** rates the quality of user-facing output, including UI, code style, API design, and prose. **Speed** rates latency to the first useful output.

| Model | Cost | Intelligence | Taste | Speed |
| --- | --- | --- | --- | --- |
| gpt-5.5 | 6 | 8 | 5 | 6 |
| sonnet-5 | 5 | 5 | 7 | 7 |
| opus-4.8 | 4 | 7 | 8 | 5 |
| haiku-4.5 | 10 | 3 | 3 | 10 |

## Selection rules

Apply the first matching rule:

1. **Quick classification or text evaluation** (sentiment, labeling, yes/no judgments, format validation, or triage; no code generation) → **haiku-4.5**
2. **Bulk/mechanical work** (implementation against a clear spec, data transforms, migrations, deterministic refactors) → **gpt-5.5**
3. **User-facing output** (UI, copy, API surfaces, or anything else a human reads or calls; requires taste ≥ 7) → **opus-4.8**; sonnet-5 only if the task is also simple
4. **Review of plans or implementations** → **opus-4.8**; gpt-5.5 may supplement as a second reviewer but never sole reviewer
5. **Everything else** → cheapest model whose intelligence clears the task difficulty bar

Tie-break order for shipping work: intelligence > taste > cost.

## Hard constraints

- **Haiku is classification-only**: never use it for code generation, implementation, review, or any task requiring intelligence > 3 or taste > 3.
- **Never downgrade** below what the rules prescribe to save cost.
- **Escalate when needed**: if a model's output misses the bar, rerun with a smarter model without asking. Escalating is cheaper than shipping mediocre work.

## Thinking level

Default to **medium** effort for all sub-agents. Only deviate when the task clearly demands it:

| Effort | When to use |
| --- | --- |
| low | Haiku classification tasks; trivial reformatting |
| medium | **Default for all other work**: implementation, review, analysis, generation |
| high | Reserved for tasks that fail at medium: multi-step reasoning with tight correctness requirements, novel architecture decisions, or adversarial verification |

Do not pre-emptively escalate to high. Start at medium; escalate only if the output quality is insufficient.

## Invocation mechanics

| Model | How to invoke |
| --- | --- |
| gpt-5.5 | Codex CLI only: `codex exec`, `codex review`, or the codex-implementation / codex-review / codex-computer-use skills. For investigation or data analysis: `codex exec -s read-only` with a self-contained prompt. |
| haiku-4.5, sonnet-5, opus-4.8 | `model` parameter on the Agent or Workflow `agent()` call. Set `effort` parameter to control thinking level. |

## Prompt structure for sub-agents

When writing a sub-agent prompt, include these blocks in order. Omit any block that adds no signal for the specific task.

1. **Role**: who the agent is and what standard it follows, in one sentence
2. **Goal**: the single deliverable and what “done” means
3. **Constraints**: rules ranked by priority, with the most important first
4. **Method**: three to five ordered steps, including verification
5. **Context**: facts the agent cannot infer, such as file paths, schemas, and prior decisions
6. **Format**: the exact output structure, including sections, keys, and length limits

Keep prompts concise. Include only instructions that constrain the task or facts the agent cannot infer from its tools or the codebase.

### Pitfalls to avoid

- **Contradictory instructions**: rank constraints so the agent knows which one wins.
- **Overlong examples**: use one small example when needed; examples consume context.
- **Unnecessary chain-of-thought**: request step-by-step reasoning only for genuinely difficult tasks; it wastes tokens on mechanical work.
- **Identity collisions**: do not mix conflicting personas; keep tone separate from technical constraints.
