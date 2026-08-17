---
name: teach
description: Teach the user a new skill or concept, within this workspace.
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
---

Treat this as a stateful teaching request that may continue across multiple sessions.

## Teaching workspace

Treat the current directory as a teaching workspace. The state of their learning is captured in this directory in several files:

- `MISSION.md`: The user's reason for learning the topic. Use it to ground all teaching and follow [MISSION-FORMAT.md](./MISSION-FORMAT.md).
- `./reference/*.html`: Clean, printable reference materials distilled from lessons, such as cheat sheets, algorithms, syntax guides, yoga poses, and glossaries.
- `RESOURCES.md`: Sources that ground teaching in knowledge and wisdom. Follow [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md).
- `./learning-records/*.md`: Records of non-obvious lessons and insights, comparable to architectural decision records, that inform the zone of proximal development and may later be revised. Name them `0001-<dash-case-name>.md`, incrementing the number for each record, and follow [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md).
- `./lessons/*.html`: A directory of lessons. A **lesson** is a single, self-contained HTML output that teaches one tightly-scoped thing tied to the mission. This is the primary unit of teaching in this workspace.
- `./assets/*`: Reusable **components** shared across lessons. See [Assets](#assets).
- `NOTES.md`: A scratchpad for you to jot down user preferences, or working notes.

## Philosophy

To learn at a deep level, the user needs three things:

- **Knowledge**, captured from high-quality, high-trust resources
- **Skills**, acquired through highly-relevant interactive lessons devised by you, based on the knowledge
- **Wisdom**, which comes from interacting with other learners and practitioners

Until `RESOURCES.md` is well populated, prioritize finding high-quality resources that support the user's learning. Do not rely on parametric knowledge.

Balance knowledge and skill development to suit the topic. Theoretical physics may emphasize knowledge, while yoga may emphasize skills.

### Fluency vs storage strength

Distinguish between two types of learning:

- **Fluency strength**: in-the-moment retrieval of knowledge
- **Storage strength**: long-term retention of knowledge

Fluency can give the user an illusory sense of mastery, but storage strength is the real goal. Try to design lessons which build long-term retention by desirable difficulty:

- Using retrieval practice (recall from memory)
- Spacing (distributing practice over time)
- Interleaving (mixing up different but related topics in practice - for skills practice only)

## Lessons

Each lesson is a self-contained HTML file saved to `./lessons/` and named `0001-<dash-case-name>.html`, with the number incremented for each lesson.

Use clean, readable typography and layout, with Tufte as the design reference.

Keep each lesson quick to complete. Because working memory is limited, focus on one tangible win tied to the mission and suited to the user's zone of proximal development.

If possible, open the lesson file for the user by running a CLI command.

Each lesson should:

- link to other lessons and reference documents through HTML anchors;
- recommend the strongest available primary source for the user to read or watch;
- remind the user that the agent can answer follow-up questions.

## Assets

Build lessons from reusable **components** in `./assets/`, including stylesheets, quiz widgets, simulators, and diagram helpers.

Reuse components by default. Before authoring a lesson, inspect `./assets/`. If the lesson needs a reusable element that does not exist, add it there and link to it rather than inlining code that a later lesson would duplicate.

Create a shared stylesheet as the workspace's first component and link every lesson to it for a consistent course design. Expand the component library as the workspace grows.

## The mission

Tie every lesson to the mission: the reason the user wants to learn the topic.

If the mission is unclear or `MISSION.md` is missing, first ask why the user wants to learn it.

When the mission changes, update `MISSION.md` and add a learning record that captures the change. Confirm the change with the user first.

## Zone of proximal development

Each lesson should feel challenging but manageable.

If the user does not request a specific topic, determine their zone of proximal development by:

- reading their `learning-records`;
- identifying what best advances their mission;
- teaching the most relevant concept or skill within that zone.

## Knowledge

Design each lesson around one skill. Include only the knowledge needed for that skill, then have the user practice it through an interactive feedback loop.

Ground that knowledge in trusted sources tracked in `RESOURCES.md`. Cite external sources for all claims made in the lesson.

During knowledge acquisition, minimize difficulty so working memory remains available for understanding.

## Skills

Skill practice should make knowledge durable and flexible.

Use effortful retrieval and desirable difficulty to build storage strength. Teach skills through one of these interactive formats:

- Interactive lessons, using quizzes and light in-browser tasks
- Lessons which guide the user through a list of real-world steps to take (for instance, yoga poses)

Build each activity around a tight feedback loop that responds immediately, preferably automatically.

Keep quiz answer choices at the same word count and, where possible, the same character count so formatting does not reveal the answer.

## Acquiring wisdom

Real-world interaction builds wisdom by testing skills outside the learning environment.

For questions that require wisdom, answer what you can, then direct the user to an appropriate **community**.

Recommend reputable online or offline communities. If the user opts out, respect that preference.

## Reference documents

Create reference documents alongside lessons to preserve reusable knowledge, and link lessons to them.

Users will revisit reference documents more often than lessons, so keep them concise and optimized for quick lookup.

Some learning topics lend themselves to reference:

- Syntax and code snippets for programming
- Algorithms and flowcharts for processes
- Yoga poses and sequences for yoga
- Exercises and routines for fitness
- Glossaries for any topic with its own nomenclature

Glossaries are essential reference documents. Once created, use their terminology in every lesson.

## `NOTES.md`

Record the user's teaching preferences and other standing considerations in `NOTES.md`, then consult it when designing lessons or working with the user.
