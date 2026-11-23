# Global rules

## Writing
Reply in plain, complete sentences. Short is good. Clipped fragments, arrows and invented abbreviations are not.

## Code review
A review request in any wording (review, `/review`, QA, pre-commit review) and every pull request get one review per diff, run as `/review`: `/code-review` for bugs and broken rules, then the project's own review sides, then one over-engineering pass for code to delete (`/simplify`, or a dedicated skill if you keep one). Report each finding once, by severity, with `file:line` and a failure scenario. Apply that pass's cuts directly; never cut validation, error handling, security, accessibility, data-loss handling or required tests. That pass runs only there, never as a standing mode. A diff that was reviewed and has not changed is not reviewed again.

## Subagents
Work inline by default. One subagent is fine where it pays: a check by someone who did not write the code (`reviewer`), a device hand test (`tester`), a wide read-only search (`scout`). Give it a contract (goal, files to read, files it may change, exit checks, a reply of 15 lines at most) and check its result before building on it. A task split across several subagents runs as `/graph`, which the user starts, by typing it or by asking for a graph run in words; then read `~/.claude/skills/graph/SKILL.md` and follow it. A workflow runs only when the user asks for one.

## Advisor
Call it before committing to a plan for multi-step work, when a fix has failed twice, and before saying a long task is done. Not for routine steps: each call re-reads the whole conversation.
