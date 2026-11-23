---
description: Code review. One deep review, then one over-engineering pass, each finding reported once.
---

Review this target: $ARGUMENTS

With no target, review the current diff against the base branch.

1. Run `/code-review` on the target, at the effort level named in the target line above, or `high` when it names none. It reviews in a fresh context, so its findings do not lean on how the code was written.
2. Check once, yourself, the sides that review does not cover for this project. The project's CLAUDE.md lists them. When it lists none, check: tests present and meaningful, error handling and what the user sees, accessibility, and anything the change deletes or migrates. Read the changed files and their callers in full for these. Leave out anything step 1 already reported.
3. Run one over-engineering pass on the same target: a dedicated skill for it if one is installed, otherwise `/simplify`. It looks only for code that can be deleted or made simpler. Apply its cuts directly. Never cut validation, error handling, security, accessibility, data-loss handling or required tests.
4. Report once: the findings by severity, each with `file:line` and a concrete failure scenario; then what step 3 cut; then what was not checked.

If this exact diff was reviewed earlier in this session and has not changed since, say so and do not review it again. Creating a pull request follows the same rule: one review per diff.
