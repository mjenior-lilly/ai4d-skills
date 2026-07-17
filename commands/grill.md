# grill

Critically pressure-test this plan until it is implementation-ready. Your job is to clarify, challenge, and refine the plan through progressive rounds of questioning — not to implement it yet.

Run the interview in batches. Each batch targets one specific topic, and you move through topics roughly in this order as your understanding of the project deepens:

1. Goal, non-goals, success criteria, and user-facing behavior.
2. Hard constraints, existing code patterns, dependencies, data contracts, and compatibility requirements.
3. Highest-risk unknowns, edge cases, failure modes, and integration boundaries.
4. Design branches — resolved one dependency at a time, with a specific recommendation where trade-offs remain.
5. Implementation sequence, test strategy, rollout or migration concerns, and documentation updates.

Within each batch:

1. Keep every question focused on the single topic for that batch.
2. Ask questions one at a time, sequentially. Ask a question, wait for my answer, then ask the next. Do not put multiple questions in one message.
3. Include enough questions to meaningfully improve clarity on that topic — keep going until the topic is genuinely well understood, not just touched. Prioritize the questions most likely to change the implementation, expose hidden constraints, or prevent rework. Avoid broad or speculative questions when a concrete assumption, constraint, or decision would unblock progress faster.
4. Let each answer shape the next question. If an answer opens a new uncertainty within the topic, follow it before moving on.

After each batch:

1. Refine the plan using everything learned so far. Update the assumptions, decisions, and open questions.
2. Briefly summarize what is now decided, what remains uncertain, and which uncertainty matters most.
3. Start the next batch on the next-highest-impact topic, carrying the improved understanding forward.

Each subsequent round follows the same objective: clarify, challenge, refine, and improve the plan as your understanding changes.

Continue running batches until you are satisfied that the plan is robust, aligned, and complete enough to implement without significant rework. Do not stop while a topic remains materially unclear. When you reach that point, present the final plan with assumptions, key decisions, implementation steps, tests, risks, and open follow-ups.