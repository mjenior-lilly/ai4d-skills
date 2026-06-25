# Task Analysis Formats

Use these formats for generated artifacts. Keep the section headings stable so later analyses can consume earlier outputs reliably. Add frontmatter when writing into an Obsidian vault or when the existing task workspace already uses frontmatter.

## Daily execution analysis

Filename default: `daily/YYYY-MM-DD.triaged.md`.
Existing TaskTriage convention: `daily/DD_MM_YYYY.triaged.txt`.

```md
# Daily Execution Analysis - {weekday, month day, year}

## Source

- Source note: `{path}`
- Analysis date: `{date}`
- Context used: `{project summaries, Obsidian notes, or none}`
- Re-analysis reason: `{new source | source modified | forced | not applicable}`

## A. Completion Summary

**Completed Tasks ({n} total):**

1. **{task name}** [Theme: {theme}] [Energy: {High|Medium|Low}] [Est: {minutes}min]
   - Evidence: `{marker or source line}`
   - Why it succeeded: {brief evidence-based analysis}

**Abandoned Tasks ({n} total):**

1. **{task name}** [Theme: {theme}] [Energy: {High|Medium|Low}] [Est: {minutes}min]
   - Evidence: `{marker or source line}`
   - Why it was abandoned: {brief evidence-based analysis}

**Incomplete Tasks ({n} total):**

1. **{task name}** [Theme: {theme}] [Energy: {High|Medium|Low}] [Est: {minutes}min]
   - Evidence: `{source line}`
   - Why it was not completed: {barrier, likely deferral reason, or unknown}

**Vague or Unanalyzable Tasks ({n} total):**

1. **{source wording}**
   - Issue: {why the task is too ambiguous}
   - Clearer alternatives: {1-2 concrete rewrites}

## B. Execution Patterns

- {3-5 concrete observations across status, theme, urgency, energy, clarity, scope, and subtasks}

## C. Task Categorization by Trend

| Theme | Total | Completed | Abandoned | Incomplete | Completion rate | Energy pattern | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| {theme} | {n} | {n} | {n} | {n} | {percent} | {High/Medium/Low mix} | {pattern} |

## D. Priority Alignment Assessment

{2-3 paragraphs assessing urgent markers, actual completion, implicit priorities, theme-level priority mismatches, and energy alignment. Use specific task examples.}

## E. Workload Realism Evaluation

- Estimated planned focused time: {minutes/hours}
- Estimated completed focused time: {minutes/hours}
- Healthy focused-work guardrail: 6-7 hours
- Completion rate: {percent by tasks, optionally by estimated time}

{2-3 paragraphs assessing overcommitment, time-estimate realism, and what was sacrificed.}

## F. Task Design Quality

{3-4 sentences evaluating clarity, specificity, actionability, scope, and endpoint definition. Include examples of well-designed and poorly designed tasks.}

## G. Tomorrow's Priority Queue

**High Priority (Start First):**

1. {task} - [Why: {deadline, dependency, impact, achievable size, or energy fit}]

**Medium Priority (Core Work):**

1. {task} - [Why: {rationale}]

**Lower Priority (If Time Permits):**

1. {task} - [Why: {rationale}]

## H. Key Takeaways for Future Planning

1. {specific planning recommendation grounded in the day's evidence}
2. {specific planning recommendation}
3. {specific planning recommendation}
```

## Weekly execution analysis

Filename default: `weekly/YYYY-Www.triaged.md`.
Existing TaskTriage convention: `weekly/weekN_MM_YYYY.triaged.txt`.

```md
# Weekly Execution Analysis: {week date range}

## Source

- Daily analyses included: {paths or date list}
- Context used: {project summaries, Obsidian notes, or none}

## A. Key Behavioral Findings

- {3-5 pattern-level findings about thematic success, repeated deferrals, true priorities, removed tasks, priority queue accuracy, wins, and improvements}

## B. Mis-Prioritization Insights

{2-3 paragraphs with specific dates, task names, themes, urgent markers, and priority-queue evidence. Treat repeated behavior as stronger evidence than labels.}

## C. Corrected Priority Model

### Theme-based prioritization

- {theme}: {priority level and why}

### Urgency rules

- {rule for what earns `*` next week}

### Promotion rules

- {which themes or task types deserve earlier scheduling or more capacity}

### Demotion rules

- {which recurring deferrals should be split, redesigned, moved to a project list, or deleted}

### Gravity task limits

- {caps for administrative, meetings, communication, or other time-absorbing themes}

### Daily priority queue refinement

- {how next week's High/Medium/Lower queues should change based on this week's accuracy}

## D. Next-Week Planning Strategy

- Capacity assumptions: {realistic daily hours and weekly total}
- High-energy task limits: {count or time cap by theme}
- Keystone tasks: {2-3 high-impact tasks or themes}
- Day typing: {heavy, medium, light recommendations}
- Admission criteria: {what belongs on the daily list vs. project list}
- Pre-splitting guidance: {known oversized tasks to split}
- Theme balance: {recommended allocation}

## E. System Improvement Recommendations

1. {specific change with expected effect}
2. {specific change}
3. {specific change}
```

## Monthly execution report

Filename default: `monthly/YYYY-MM.triaged.md`.
Existing TaskTriage convention: `monthly/MM_YYYY.triaged.txt`.

```md
# Monthly Execution Report: {month year}

## Source

- Weekly analyses included: {paths or week list}

## A. Monthly Achievements Summary

### Work/Professional

- {completed outcome, shipped deliverable, project progress, collaboration, or skill developed}

### Personal/Home

- {completed outcome}

### System/Meta

- {planning system improvement, habit, tool, or process change}

## B. Strategic Patterns and Trends

- {3-5 month-level patterns with evidence across multiple weeks}

## C. System Evolution Assessment

{Evaluate which weekly recommendations were implemented, which improved outcomes, which failed, and whether planned-vs-actual execution improved.}

## D. Persistent Challenges

| Challenge | Type | Evidence | Likely response |
| --- | --- | --- | --- |
| {challenge} | {tactical | systemic | external constraint} | {multi-week evidence} | {fix, negotiate, delegate, accept, or redesign} |

## E. Monthly Performance Metrics

- Planned tasks completed: {approximate percent or unknown}
- Theme completion leaders: {themes}
- Theme completion laggards: {themes}
- Average focused work time: {estimate or unknown}
- Priority alignment: {assessment}
- Priority queue accuracy: {assessment}
- Energy management: {assessment}
- Planning quality trend: {improving, stable, declining, mixed}

## F. Strategic Guidance for Next Month

- Strategic priorities: {3-5 keystone objectives with success criteria}
- Capacity planning: {realistic weekly capacity and buffers}
- Theme focus and balance: {recommended allocation}
- Rhythm and pacing: {heavy/light weeks, recovery periods, timing of deep work}
- Pre-emptive splitting: {large tasks/projects to decompose}
- System priorities: {2-3 planning metrics or process changes}

## G. Long-Term System Refinements

1. {structural, process, habit, tool, or boundary change with success criteria}
2. {refinement}
3. {refinement}
```

## Annual execution review

Filename default: `annual/YYYY.triaged.md`.
Existing TaskTriage convention: `annual/YYYY.triaged.txt`.

```md
# Annual Execution Review: {year}

## Source

- Monthly reports included: {paths or month list}

## A. Year in Accomplishments

### Work/Professional

- {major completed project, shipped work, milestone, skill, contribution, or outcome}

### Personal/Home

- {major outcome}

### System/Meta

- {planning system improvement or durable habit}

## B. Learning & Skill Development

- {skill or learning}: {evidence from monthly reports and theme performance}

## C. Highest-Impact Opportunities

### 1. {opportunity title}

- Issue: {concrete pattern, ideally theme-specific}
- Why it matters: {ROI and cascading benefits}
- Root cause: {task structure, energy alignment, priority model, capacity, or external constraint}
- Intervention: {specific measurable change}
- Success criteria: {how to evaluate next year}

## D. Year-Ahead Strategic Direction

### Q1-Q2 focus

- {keystone objectives, capacity allocation, early wins, obstacles}

### Q3-Q4 focus

- {strategic priorities and consolidation}

### Monthly rhythm

- {heavy/light month pattern, seasonal constraints, theme rotation}

### Resource allocation

- {time/energy allocation by theme or domain}
```

## Project context summary

Filename default: `context/{label}.context.md`.

```md
# Project Context: {label}

## Purpose and Overview

{What the project does, who it is for, and what problem it solves.}

## Technology Stack

- {languages, frameworks, runtime versions, key libraries}

## Architecture Overview

- {major components, data flow, deployment model, integration points}

## Key Patterns and Conventions

- {coding style, naming, organization, testing, domain patterns}

## Important Files and Entry Points

- `{path}`: {why it matters}

## External Dependencies and Integrations

- {service, API, database, third-party integration}

## Current State and Notable Concerns

- {technical debt, incomplete areas, risks, confusing conventions}

## Matching Metadata

- Primary keywords: {terms}
- Technologies: {terms}
- Common task terms: {terms}
- Related concepts: {terms}
```
