# Smell Baseline

A fixed set of Fowler code smells (_Refactoring_, ch. 3) that applies to every review, even when a repo documents nothing else. Two rules bind it:

1. **The repo overrides.** A documented repo standard always wins. Where it endorses something the baseline would flag, suppress the smell.
2. **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Skip anything tooling already enforces, including linters, formatters, and type checks.

---

Each entry defines a smell and suggests a fix. Match the smell against the diff:

- **Mysterious Name**: a function, variable, or type whose name does not reveal what it does or holds. → Rename it; if no honest name comes, the design is murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → Extract the shared shape and call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → Move the method onto the data it envies.
- **Data Clumps**: the same few fields or parameters keep travelling together, suggesting that they should form a type. → Bundle them into one type and pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → Give the concept its own small type.
- **Repeated Switches**: the same `switch` or `if` cascade on the same type recurs across the change. → Replace it with polymorphism or a map shared by both sites.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → Gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → Split it so each module changes for one reason.
- **Speculative Generality**: abstractions, parameters, or hooks added for needs the spec does not have. → Delete them and inline the code until a real need arises.
- **Message Chains**: long `a.b().c().d()` navigation that the caller should not depend on. → Hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly delegates onward. → Remove it and call the real target directly.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → Drop the inheritance and use composition.

---

## Usage in the Standards sub-agent

Paste this entire file into the Standards sub-agent prompt because the sub-agent cannot access it directly.
