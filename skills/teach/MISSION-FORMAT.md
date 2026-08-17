# MISSION.md Format

`MISSION.md` lives at the workspace root and captures why the user is learning the topic. Every decision about what to teach, which resources to surface, and which exercises to design should trace back to it.

## Template

```md
# Mission: {Topic}

## Why
{In 1-3 sentences, state the concrete real-world goal. Explain what will change in the user's life or work when they gain this skill. Avoid abstract goals such as "to understand X" and identify the underlying outcome.}

## Success looks like
- {A specific, observable thing the user will be able to do}
- {Another specific thing}
- {…}

## Constraints
- {Time, budget, prior commitments, learning preferences, anything that bounds the approach}

## Out of scope
- {Adjacent topics the user does not want to pursue now; excluding them protects the zone of proximal development}
```

## Rules

- **One mission per workspace.** If the user wants to learn two unrelated things, that is two workspaces.
- **Concrete over abstract.** "Run a half marathon by October" beats "get fitter." "Ship a Rust CLI to my team" beats "learn Rust."
- **Push back on vagueness.** If the user cannot explain why they want to learn the topic, interview them before writing `MISSION.md`; do not create a vague mission.
- **Revise when reality shifts.** When the user's goal changes, update this file so future sessions do not follow a stale mission.
- **Keep it short.** Keep `MISSION.md` to one screen so it remains a concise guide rather than becoming a plan.
