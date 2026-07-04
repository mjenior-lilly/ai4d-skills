# Summary Quality Evaluation

Two sub-stages: (A) score one summary against its source with a weighted
rubric; (B) consolidate multiple score reports into one. Use (B) only when 2+
independent assessments exist.

## A. Scoring rubric

Read the original source fully to establish the baseline for accuracy and key
information, then score the summary 1–10 on each criterion:

**Accuracy (40%)** — facts, data, findings, conclusions, and methodologies are
correctly reflected; nothing misrepresented, distorted, fabricated, or added.
1–3: multiple blatant errors or significant invented content. 4–6: minor
inaccuracies that don't alter the core message. 7–8: largely accurate,
negligible issues. 9–10: flawless.

**Completeness of key information (30%)** — captures all central themes,
objectives, significant results, and major conclusions; sufficient for an
informed reader to grasp the essence.
1–3: major omissions of core content. 4–6: most key information present, some
significant aspects missing. 7–8: all essentials covered. 9–10: comprehensive.

**Conciseness & efficiency (15%)** — maximum essential information in minimum
words; free of redundancy, avoidable jargon, and detail that belongs in the
full document.
1–3: verbose/redundant. 4–6: generally concise with minor bloat. 7–8: very
efficient. 9–10: exceptional economy without sacrificing clarity.

**Clarity, flow & readability (10%)** — logical presentation, smooth
transitions, precise language, free of grammatical errors and awkward phrasing.
1–3: hard to comprehend. 4–6: readable but inconsistent. 7–8: well written.
9–10: flawless.

**Neutrality & objectivity (5%)** — impartial, no opinions, bias, emotional
language, or unsupported interpretation.
1–3: heavily biased. 4–6: minor subjectivity. 7–8: generally neutral.
9–10: strictly objective.

Overall = (Accuracy × 0.40) + (Completeness × 0.30) + (Conciseness × 0.15) +
(Clarity × 0.10) + (Neutrality × 0.05), rounded to the nearest whole number
(X.5 rounds up).

### Output format

```
Summary Quality Score: [N]/10

Justification:
[One concise paragraph explaining the score, referencing the specific criteria
where the summary performed well or poorly.]
```

## B. Consolidating multiple reports

Given several reports in the format above:

1. Extract each numeric score and justification.
2. Average the scores; round to the nearest whole number (X.5 rounds up).
3. Thematically analyze the justifications: recurring strengths, recurring
   weaknesses, and unique but insightful single observations.
4. Write one cohesive analytical paragraph (two at most) — a unified narrative,
   not a concatenation. No redundant repetition of near-identical points, but
   no distinct observation omitted. Professional, objective tone.

### Output format

```
Consolidated Summary Quality Report

Average Overall Score: [N]/10

Consolidated Justification:
[The synthesized paragraph(s).]
```
