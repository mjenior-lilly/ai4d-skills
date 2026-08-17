# Generate agent handoff artifact

# Objective
Write a concise, structured handoff so another AI agent or agent team can resume the work in a new session. Choose one format:

1. **Single-agent handoff:** For a straightforward task that one agent can complete in a focused session.
2. **Long-running team handoff:** For complex work that spans multiple agents or sessions and needs explicit goals, responsibilities, and specifications.

# Target destination
- **File location:** Save the final document in the operating system's temporary directory. Resolve that directory with a system-independent mechanism such as Python's `tempfile`, `$TMPDIR`, or `%TEMP%`.
- **Constraint:** Never save the file inside the active workspace or project root.

# Handoff content
The handoff document must include the following distinct sections:

1.  **Current State Summary:** A high-level overview of what has been accomplished in this session and where the execution left off.
2.  **Context & Artifact References:**
    *   Do not duplicate content already captured in external project artifacts (such as PRDs, architecture plans, ADRs, active issues, or git commits/diffs).
    *   Instead, explicitly reference these existing items by their relative file paths or URLs.
3.  **Suggested Skills:** A dedicated section listing specific tools, functions, or capabilities the incoming agent should prioritize or invoke next.
4.  **Immediate Next Steps:** A tactical list of actions for the next session.

## For long-running agent teams
When the task involves complex, sustained work that requires multiple agents or extended execution, add these sections:

5.  **Project Objectives & Success Criteria:**
    *   Define the goals and what "done" looks like.
    *   Include measurable success criteria or acceptance criteria.
    *   Specify any business requirements, user stories, or outcomes to achieve.

6.  **Required Software Specifications:**
    *   Technical requirements (languages, frameworks, platforms, versions).
    *   Architecture patterns or constraints (microservices, monolith, event-driven, etc.).
    *   Performance requirements (latency, throughput, scalability targets).
    *   Security and compliance requirements.
    *   Integration points with existing systems.

7.  **Agent Team Composition & Responsibilities:**
    *   Recommended agent roles (e.g., architect, implementer, tester, reviewer).
    *   Specific responsibilities and ownership areas for each agent type.
    *   Coordination strategy and handoff points between agents.

8.  **Constraints & Assumptions:**
    *   Time constraints or milestones.
    *   Resource limitations (budget, API rate limits, compute constraints).
    *   Assumptions made about the environment, dependencies, or user needs.
    *   Known risks or blockers.

9.  **Quality & Testing Requirements:**
    *   Testing strategy (unit, integration, e2e, performance).
    *   Code quality standards (linting, formatting, review process).
    *   Documentation requirements.
    *   Deployment and rollback procedures.

# Choosing a single-agent or team handoff

Before creating the handoff document, evaluate the task complexity:

**Create a single-agent handoff when:**
*   The task is well-defined and scoped to a single deliverable.
*   Completion can reasonably happen in one session (< 2 hours of work).
*   Dependencies are minimal and clearly identified.
*   No significant architectural decisions are required.

**Create a long-running team handoff when:**
*   The task involves multiple subsystems, components, or phases.
*   Work will span multiple sessions or require sustained effort.
*   Significant design, architecture, or technology choices need to be made.
*   Multiple specialized skills are needed (design, implementation, testing, deployment).
*   The project requires coordination across different workstreams.
*   Success criteria are complex or involve multiple stakeholders.

# Security and privacy constraints
*   **Redaction:** Before saving, scan the summary and redact all sensitive information, including API keys, authentication tokens, passwords, other secrets, and personally identifiable information (PII).

# User arguments
*   If the user has provided specific arguments or runtime flags, treat them as the explicit scope and focus for the upcoming session. Tailor the "Current State Summary" and "Immediate Next Steps" sections to align directly with the intent of those arguments.
*   When arguments suggest a complex or long-running project, automatically include the enhanced sections for long-running agent teams (objectives, specs, team composition, etc.).
*   If the user explicitly mentions "agent team," "long-running," "multi-phase," or similar terms, use the team handoff format.
