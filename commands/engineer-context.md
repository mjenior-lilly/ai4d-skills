# Re-engineer context

Rewrite the supplied source text for clarity and natural flow without changing its substantive meaning.

Use the conversation to determine the audience, purpose, and tone. If that context is unavailable, preserve the audience, purpose, formality, and level of expertise implied by the source. Do not invent them. If no single source passage can be identified, ask the user which text to rewrite.

## Priorities

Apply these priorities in order:

1. Preserve every substantive claim, qualification, commitment, constraint, action, and expression of uncertainty.
2. Preserve technical terms, names, numbers, evidence, and domain-specific language.
3. Report any facts only a single time each.
4. Improve clarity, directness, and concision. Ensure a clear scope for the output text.
5. State the most important point last since it is what the user sees first.

Do NOT add facts, claims, promises, caveats, citations, arguments, or conclusions.

## Editing rules

- Prefer active voice when the actor is known and relevant and vary sentence structure when it improves readability.
- State a conclusion directly only when the source states it or makes it logically unambiguous. Do not strengthen tentative language or confidence.
- Remove wording that merely repeats an already-preserved point or comments on the writing itself.
- Compress background, examples, caveats, and explanations only when doing so preserves their substantive content. Retain details that establish scope, evidence, causality, uncertainty, exceptions, obligations, recommendations, or next steps.
- Replace stock introductions, filler transitions, inflated wording, and repeated sentence patterns with direct prose. Examples include "The honest truth", "Load-bearing", "It's important to note that," "It's worth mentioning that," "Just to clarify," "Furthermore,", "Moreover", "The real tension", etc.
- Prefer shorter wording, but do not summarize away unique details. Preserve intentional detail while removing redundant phrasing.
- Keep headings and lists when they make distinct sections or parallel items easier to scan. Do not introduce them only to impose a template.
- Preserve punctuation required by quotations, notation, ranges, or meaning. Avoid em dashes, en dashes, ellipses, emoji, and exclamation points when they serve only as stylistic emphasis.
- Preserve the source's capitalization conventions for names and established headings. Otherwise, use sentence case for headings.

## Ambiguity

Preserve ambiguity when the text can be rewritten without resolving it. Ask focused questions before rewriting if choosing an interpretation would change a factual claim, obligation, recommendation, audience, tone, or requested action.

## Output

Return only the rewritten text unless the user asks for analysis or alternatives.
