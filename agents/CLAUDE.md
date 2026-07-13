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

## Sub-agent delegation

Whenever you delegate work to a sub-agent (Agent tool, Workflow, or Codex CLI), follow the `sub-agents` skill (`skills/sub-agents.md`) for model selection, thinking level, and prompt structure. Do not default to your own model or to whatever another skill suggests without checking that file first.

Quick reference (the skill is authoritative if these diverge):

| Model | Cost | Intelligence | Taste | Speed |
| --- | --- | --- | --- | --- |
| gpt-5.5 | 6 | 8 | 5 | 6 |
| sonnet-5 | 5 | 5 | 7 | 7 |
| opus-4.8 | 4 | 7 | 8 | 5 |
| haiku-4.5 | 10 | 3 | 3 | 10 |

Selection rules (first match wins):

1. **Quick classification or text evaluation** (no code generation) → **haiku-4.5**
2. **Bulk/mechanical work** → **gpt-5.5**
3. **User-facing output** (taste ≥ 7 required) → **opus-4.8**
4. **Review of plans or implementations** → **opus-4.8**
5. **Everything else** → cheapest model clearing the intelligence bar

Hard constraints:
- Haiku is classification-only — never for code generation, implementation, or review.
- Never downgrade below what the rules prescribe to save cost.
- Always escalate freely if output misses the bar.

Default thinking level: **medium** for all sub-agents. Use low only for haiku classification; escalate to high only when medium demonstrably fails.

## Knowledge-base project-fact capture

Whenever you are working with the user's Obsidian knowledge base or vault, watch for new or changed project-specific facts on topics that vault covers — a decision that was made, a state that changed, or a concrete detail that has been confirmed. This applies in every session and does not depend on the `knowledge-graph` skill having been explicitly invoked first.

When such a fact arises:

- Invoke the `knowledge-graph` skill if it is not already active, and log the fact as a timestamped, append-only note under the vault's `40_Project/` folder following the skill's `PROJECT-FACT-FORMAT.md`.
- Record only confirmed ground truth. Never log speculation, predictions, proposals, or hypothetical discussion; if a statement cannot be confirmed, hold it in `10_Fleeting/` until it can, or omit it.
- Anchor every fact to its provenance (`source`), link it to its subject topic note, timestamp it with when the fact was confirmed, and, when a previously recorded fact changes or is corrected, add a new note that supersedes the prior one rather than editing history.
- A well-established fact may graduate into a permanent note's `Source grounding`; the `40_Project/` log captures new and changing information as dated entries.

This directive is the persistent, cross-session complement to the `knowledge-graph` skill, whose own project-fact capture only runs while it is active on a vault task.
