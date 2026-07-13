# Agent Prompt Skeleton

> **Canonical reference:** The authoritative prompt structure and model selection guide lives in `skills/sub-agents.md`. This file provides supplementary guidance on prompt design patterns beyond what the skill covers.

---

## Prompt structure (summary)

Include these blocks in order when writing a sub-agent prompt. Omit any block that adds no signal.

1. **Role** — one sentence: who the agent is and what standard it operates at
2. **Goal** — the single deliverable; define what "done" looks like
3. **Constraints** — ranked rules (always X, never Y); most important first
4. **Method** — 3–5 ordered steps including a verification step
5. **Context** — facts the agent cannot infer (file paths, schemas, prior decisions)
6. **Format** — exact output structure (sections, keys, length limits)

---

## Hybrid prompt styles

Choose a combination based on what the task needs:

| Need | Style |
|------|-------|
| Crisp deliverable (specs, plan, email) | Functional + Role |
| Ideas and synthesis | Exploratory + Role |
| Model critiques/refines its own work | Functional + Meta |
| Big, multi-stage artifact | Full hybrid (Functional + Meta + Exploratory + Role) |

- **Functional + Meta** → "Do the task, then self-improve it."
- **Meta + Exploratory** → "Refine the brainstorm, widen/sharpen ideas."
- **Exploratory + Role** → "Creative ideation with expert guardrails."
- **Functional + Role** → "Precise task, expert tone/standards."

---

## Drift control (multi-turn agents only)

For agents that run across many turns, add a reinforcement block:

- Re-read role/goal/constraints before each major output section.
- Every 3–4 turns, confirm adherence to format and constraints.
- If style or claims drift, re-ground and revise before outputting.

Not needed for single-turn sub-agents (which is most Agent tool usage).

---

## Pitfalls

| Pitfall | How to avoid |
|---------|-------------|
| Identity collisions | Don't mix conflicting personas; specify tone separately from technical constraints |
| Contradictions | Use ranked rules so the agent knows which wins |
| Overlong examples | One small example beats three large ones; examples eat context budget |
| CoT overhead | Step-by-step helps quality but costs tokens — use only for genuinely hard tasks |

---

## Agentic eagerness knobs

- **Less eagerness**: set search/tool budgets; add early-stop criteria
- **More eagerness**: add a persistence instruction — "keep going until fully solved"
- **Tool preamble pattern**: plan → act → narrate → summarize
