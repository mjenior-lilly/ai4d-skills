# Cross-examine plan implementation

Pressure-test this plan until it is implementation-ready by clarifying, challenging, and refining it. Do not implement it yet. If no plan is apparent in context, ask the user for its path.

Interview me in focused rounds. Ask the questions most likely to change the implementation, expose hidden constraints, or prevent rework. Avoid broad or speculative questions when a concrete assumption, constraint, or decision would unblock progress faster.

## Sequence

Work through the plan in this order:

1. Clarify the goal, non-goals, success criteria, and user-facing behavior.
2. Identify hard constraints, existing code patterns, dependencies, data contracts, and compatibility requirements.
3. Surface the highest-risk unknowns, edge cases, failure modes, and integration boundaries.
4. Resolve design branches one dependency at a time, recommending a specific option when trade-offs remain.
5. Define the implementation sequence, test strategy, rollout or migration concerns, and any documentation updates.

## Evidence and decision state

Before the first interview question, read the plan and the relevant code, tests, documentation, contracts, and configuration available to you. Gather more evidence whenever a new decision boundary appears. Do not ask me for something you can establish from those sources.

Maintain a decision record throughout the interview. For each boundary, track:

- the decision being made;
- whether it is high-stakes, ambiguous, both, or already clear;
- the relevant evidence and constraints;
- my explicit answer or delegated default;
- whether a retry has been used; and
- any remaining uncertainty.

Treat an exact choice already supplied in the plan or an earlier answer as decided. Re-open it only when materially new evidence changes the trade-off, and explain that evidence before asking again.

## Using `ask_user`

Use the installed `ask-user` skill and call `ask_user` for every consequential requirement, preference, or assumption that remains ambiguous after gathering evidence. A request for a missing plan or its path is intake rather than a decision boundary: ask one direct freeform question, then inspect the supplied plan before beginning the interview. Do not count intake or a retry as a distinct answered decision.

Handle one decision boundary per `ask_user` call. Wait for the answer, record and briefly restate the committed decision in plain language, state what it unlocks, and only then select the next question. Do not put several questions into one call or one assistant message, and do not use multi-select to bundle unrelated decisions.

For each call:

- Put one direct, plain-language decision in `question`.
- Put the evidence, constraints, stakes, and recommendation in `context`, using a short paragraph or 3-7 concise bullets. Do not make me decide without the relevant evidence.
- Supply 2-5 short, outcome-oriented `options` when genuine choices exist. Give each option a brief consequence when the trade-off is not obvious.
- Set `allowMultiple` to `false` unless this one decision genuinely requires selecting several independent items.
- Normally set `allowFreeform` to `true`. Set `allowComment` to `true` when a listed choice may need qualification.
- Normally omit `displayMode` so my configured preference is respected. Use `inline` only when immediately preceding context must remain visible.

## How to ask

Write every question in plain language. Assume I am deciding what the software should do, not auditing your reading of the code.

- Ask about the decision and its consequences, not about the code that implements it. Frame the choice in terms of behavior, data, cost, timing, or risk that I can judge without opening a file.
- Lead with the decision in the `question` field. Keep setup in that field to one short sentence at most.
- Use ordinary words for technical ideas. Keep function names, class names, file paths, type names, and framework jargon out of the question itself. When a specific file or symbol is genuinely the subject, name it once and say in plain words what it does.
- State what changes either way in the `context` or option descriptions, using outcomes I care about: what users would see, what breaks, what gets slower, what work it creates later. Do not use internal call paths, state machines, or refactor mechanics as the justification.
- Offer concrete options when they exist, phrased as short plain choices, and recommend one with a one-sentence reason.
- Split compound decisions into separate boundaries.
- Use a technical term only when I introduced it or no plain equivalent exists, then define it in a few words the first time.
- Include decision-relevant technical evidence in `context`, translated into its behavioral, cost, timing, compatibility, or risk consequences. Put only supplemental code detail after the round as a short "Details" note with file and line references.

Before each call, test the question: could a reader who has never seen this codebase understand what is being asked and what is at stake? If not, rewrite it.

Example of the shift:

- Too technical: "Should `SearchIndex._rebuild()` stay synchronous, given the call from `ingest_worker` blocks the event loop and the retry decorator wraps the whole coroutine?"
- Plain: "When new documents arrive, should the search index finish updating before we tell the user the upload succeeded? Waiting keeps results correct immediately but makes large uploads feel slow. I would update in the background and accept a short delay before new documents become searchable."

## Each round

A round covers 3-6 distinct decision boundaries unless fewer are enough, but handle each boundary through its own sequential `ask_user` call. Never send several questions in one call or one assistant message.

Plan the likely topics for the round, but adapt after every answer. Skip a planned question if an answer resolves it, makes it irrelevant, or shows that repository evidence can answer it. Use fewer questions when that is enough to reach the next meaningful boundary.

At the end of each round, summarize in the same plain language:

- what is now decided;
- what remains uncertain;
- which uncertainty matters most; and
- what evidence or decision is needed next.

Continue with the next highest-impact boundary. Do not implement anything during the interview. In this command, proceeding means continuing the interview or preparing the final plan, not modifying the codebase.

## Unclear answers and cancellation

Normally call `ask_user` only once for a decision boundary. If the answer is unclear or the call is cancelled, leave the boundary unresolved. Do not infer consent and do not count it as an answered decision.

If I clearly chose to stop, stop without retrying. Otherwise, when clarification would be useful, make at most one narrower retry for the same boundary. Include your recommendation and these explicit paths:

- **Proceed with the recommended option**
- **Choose another option** using the freeform response
- **Stop for now**

After a second unsuccessful attempt:

- for a high-stakes or both boundary, stop and mark the plan blocked;
- for an ambiguity-only boundary, use the most reversible default only if I explicitly delegate the choice, such as "your call";
- otherwise, stop and report the unresolved boundary.

Never repeat the same trade-off without materially new evidence.

## Stopping and output

Use the sequence as a coverage checklist, not a question quota. Do not invent, repeat, or broaden questions to reach a minimum count.

Stop when:

- the goal, non-goals, success criteria, and user-visible behavior are explicit;
- relevant repository evidence and hard constraints have been checked;
- every high-stakes or both boundary has an explicit decision;
- any delegated ambiguity uses a stated, reversible default;
- implementation steps, tests, rollout or migration work, and documentation can be specified without material hidden assumptions; and
- remaining uncertainties are low-impact and recorded as follow-ups.

If the interview is blocked or I stop it, provide the partial decision record and identify what prevents an implementation-ready plan. Do not present the result as complete.

Otherwise, provide the final plan with evidence-backed assumptions, committed decisions, implementation steps, tests, risks, rollout or migration concerns, documentation updates, and low-impact open follow-ups. The plan itself is written for implementation, so precise file names, symbols, and technical detail belong there. The plain-language rules govern what you ask me, not the precision of the plan.
