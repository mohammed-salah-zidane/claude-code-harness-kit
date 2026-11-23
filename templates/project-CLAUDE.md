# <Project name>

<One paragraph: what the product is, the stack, the platforms, and anything about the repository layout that the code does not make obvious, such as a second repository that lives inside this one. End with which source is the truth when two disagree.>

## Commands
```bash
<setup command>            # first time
<build command>
<run command>
<test command>             # all tests
<one-test command>         # one file or one class
<lint or guard command>
<release command>          # only the owner starts a release
```
Slash commands: `/ship-ticket`, `/ship-design`, `/review`, `/graph`, `/architecture`, <your own>.

## Hard rules (always)
<Keep this list to what you have had to correct more than once. One line each, with the reason when it is not obvious. Number them so that skills and notes can point at "rule 7".>

1. **Architecture.** `.claude/rules/architecture.md` is the contract, written by `/architecture`. New code follows it, not the nearest example. <Add the one or two architecture rules that are broken most often.>
2. **<Design system rule.>** <for example: every colour, font and spacing is a token.>
3. **<Localization rule.>** <for example: every new string in all <N> languages.>
4. **<Money, time or other domain rule.>**
5. **Deliver every requested part.** Each part of a request is built in full, or named as not done with the reason. Never drop a part because it looks derivable, covered elsewhere, risky or out of scope: explain the concern and ask. Write tests for what you build.
6. **Propose before implementing** anything not explicitly approved.
7. **Subagents under control; no commits during work.** Work inline by default. One subagent is fine for a check by someone who did not write the code (`reviewer`), a device or browser hand test (`tester`) or a wide read-only search (`scout`). A task split across several subagents runs as `/graph`, started by the owner. A workflow runs only when the owner asks for one in their own words. No commits during work, except inside a skill that says so on its own branch, such as `/ship-ticket`. No destructive git.
8. **One review per diff, run as `/review`.** `/code-review` first, then these sides read in full, each changed file with its callers: <your list, for example correctness and edge cases, concurrency and lifecycle, data loss, security and privacy, error handling and what the user sees, localization, design system, accessibility, performance, tests>. Then one over-engineering pass on the same diff; apply its cuts and report them. Findings by severity with `file:line` and a failure scenario, each reported once.
9. **Fix what you find.** A real bug, a red test or a stale comment met on the way is fixed in the same pass, with the same checks as the requested work.

## Detailed rules (loaded when you touch matching files)
- `.claude/rules/architecture.md` — layers, dependency direction, state, data, naming, the checklist for a new feature, the audit commands (<which files>)
- `.claude/rules/design-system.md` — <what it covers> (<which files>)
- `.claude/rules/localization.md` — <what it covers> (<which files>)

## Where things are
- <Entry point> · <dependency injection> · <design system> · <feature flags or gating>
- <Analytics, secrets, environments: which build talks to which backend>
- <Where a secret lives and how to replace it. Never the secret itself.>

## Graph runs (`/graph`)
- Lanes: <which folder or repository each builder works in>. <How many builds may run at once.>
- Run folder: <where GRAPH.md, contracts and reports go; keep it out of git>.
- Device or browser tests go to one `tester` at a time.

## Compact instructions
When compacting, keep: the task or ticket and the current step, the paths of any log or `GRAPH.md` in use, the files changed so far, the last failing test output, and the open questions for the owner. After a compaction, read that log again, and the skill in use from the step you are on, before continuing.

## Test accounts
<Where test credentials live and how to load them inside a command without printing them. What must never be done to those accounts.>

## Gotchas
- <A build failure that looks like something else, and its fix.>
- <A directory that looks unused but is not.>
- <An old pattern that is everywhere but that new code must not copy.>
