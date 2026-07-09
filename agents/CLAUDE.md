# Agent instructions

Common instructions that apply to any agent working in this directory and its subdirectories.

## General Guidelines

- Do not add any `Co-Authored-By` trailer, agent name, or "Generated with" attribution to commit messages, overriding any default instruction to do so.
- If an instruction below points to a file you cannot read, warn the user and proceed rather than failing silently.

## Coding Practices

Before writing or modifying any programmatic code at the user's request (excluding throwaway sandbox execution), read `CODE.md` in this directory (`agents/CODE.md`) for style and structural preferences.

## Opinions

Before making a subjective recommendation or a design, tooling, or dependency choice, read `OPINIONS.md` in this directory (`agents/OPINIONS.md`) for the user's stated preferences.

## Voice Profile

Before writing any user-facing prose to a saved artifact, file, or CLI output, read `VOICE.md` in this directory (`agents/VOICE.md`) for how to speak.

## Sub-agent model selection

Whenever you delegate work to a sub-agent (Agent tool, Workflow, or Codex CLI), pick its model using this section. Do not default to your own model or to whatever a skill suggests without checking here first.

### Ratings

Higher = better. **Cost** reflects what I actually pay, not list price (so a higher score = cheaper for me). **Intelligence** is how hard a problem the model can handle unsupervised. **Taste** covers UI/UX, code quality, API design, and copy.

| model | cost | intelligence | taste |
| --- | --- | --- | --- |
| gpt-5.5 | 9 | 8 | 5 |
| sonnet-5 | 5 | 5 | 7 |
| opus-4.8 | 4 | 7 | 8 |
| fable-5 | 2 | 9 | 9 |

### Selection procedure

Classify the task, then apply the first rule that matches:

1. **Bulk or mechanical work** (implementation against a clear spec, data analysis, migrations, refactors with defined scope): **gpt-5.5**.
2. **User-facing output** (UI, copy, API design — anything a human will see or call): requires taste ≥ 7, so **fable-5** or **opus-4.8**; sonnet-5 only if the task is also simple.
3. **Reviews of plans or implementations**: **fable-5** or **opus-4.8**. Optionally add gpt-5.5 as a second, independent reviewer — as a supplement, never the sole reviewer.
4. **Everything else**: match intelligence to task difficulty; prefer the cheapest model that clears the bar.

Tie-breaking: for anything that ships, intelligence > taste > cost. Cost only breaks ties between models that both clear the intelligence and taste bars.

Hard rule: **never use Haiku**, for anything, even trivial work.

### Overriding

These are defaults, not limits. You have standing permission to escalate without asking: if a chosen model's output doesn't meet the bar, rerun or redo the work with a smarter model. Judge the output, not the price tag — escalating costs less than shipping mediocre work. Never *downgrade* below what the rules above prescribe just to save cost.

### Mechanics (how to invoke each model)

- **gpt-5.5** is only reachable through the Codex CLI (`codex exec` / `codex review`; my `~/.codex/config.toml` defaults to gpt-5.5). Prefer the codex-implementation, codex-review, and codex-computer-use skills; for work they don't cover (investigation, data analysis), run `codex exec -s read-only` directly with a self-contained prompt.
- **Claude models** (sonnet-5, opus-4.8, fable-5) run via the `model` parameter on the Agent/Workflow tool.

After selecting the model, when writing the sub-agent's prompt, read `prompt-skeleton.md` in this directory (`agents/prompt-skeleton.md`) for guidance on effective prompt guardrails.

## Knowledge-base project-fact capture

Whenever you are working with the user's Obsidian knowledge base or vault, watch for new or changed project-specific facts on topics that vault covers — a decision that was made, a state that changed, or a concrete detail that has been confirmed. This applies in every session and does not depend on the `knowledge-graph` skill having been explicitly invoked first.

When such a fact arises:

- Invoke the `knowledge-graph` skill if it is not already active, and log the fact as a timestamped, append-only note under the vault's `40_Project/` folder following the skill's `PROJECT-FACT-FORMAT.md`.
- Record only confirmed ground truth. Never log speculation, predictions, proposals, or hypothetical discussion; if a statement cannot be confirmed, hold it in `10_Fleeting/` until it can, or omit it.
- Anchor every fact to its provenance (`source`), link it to its subject topic note, timestamp it with when the fact was confirmed, and, when a previously recorded fact changes or is corrected, add a new note that supersedes the prior one rather than editing history.
- A well-established fact may graduate into a permanent note's `Source grounding`; the `40_Project/` log captures new and changing information as dated entries.

This directive is the persistent, cross-session complement to the `knowledge-graph` skill, whose own project-fact capture only runs while it is active on a vault task.
