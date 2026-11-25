# Templates

Fill every field. Write "not run" or "not applicable" with the reason; never leave a field out and never write a result you did not see. The hand-test row is never "not run": a ticket without a passed hand test does not reach In Review.

## Contents

1. Ship log (`<EVIDENCE-FOLDER>/log.md`)
2. Status comments: work started, paused, resumed
3. Verdict comment (phase 3)
4. Plan comment (phase 4, plan mode)
5. Commit message
6. Pull request body
7. "Pull request opened" comment (phase 9)
8. "Stopped" comment

## 1. Ship log

Create it in phase 1. After each phase, tick the line, add one line of evidence (a command and its result, a file path, a comment link) and rewrite "Next step", so another session, or this one after a compaction, can continue from the first unticked phase.

```
# <TICKET-KEY> ship log

Ticket: <title>
Size: <s | m | l>   Mode: <auto | plan | owner>   Model: <model id>
Branches: <repository>: <branch>, cut from <base commit>

Next step: <the exact next action, written so a fresh session can start from it>

## Phases
- [ ] 1. Ticket and gates: <evidence>
- [ ] 2. Context: <evidence>
- [ ] 3. Verdict (from reading): <evidence>
- [ ] 4. Plan and branches: <evidence>
- [ ] 5. Implemented in full (tests written, nothing run): <evidence>
- [ ] 6. Tests, once: <evidence>
- [ ] 7. One /review, fixes re-checked: <evidence>
- [ ] 8. One hand test: <evidence>
- [ ] 9. Pull request, review bot (two rounds at most) and tracker: <evidence>

## Verdict
Reach: <steps from launch to the broken line, or "no path: <why>">
Already prevented: <what was checked, callers and writers listed>
Fits the rules: <yes, or the rule it breaks>
Users touched: <number, source, date range>, or <not measured: the event to count, and the estimate from the path>
Verdict: <one of the six>, evidence `<path>:<line>`
Failing test: `<test name>` failed with "<message>"

## Plan
<commits in order, tests, change per platform, shared values touched, out of scope>

## Commands
| Command | Output file | Result |
|---|---|---|

## Review
| Dimension | Finding with `file:line` and failure, or "none, because ..." | What was done |
|---|---|---|
| Logic | | |
| Bugs | | |
| Code quality | | |
| Scalability | | |
| Maintenance | | |
| Project standards | | |

Three ways it could still be wrong:
1. <way>: checked by <test or reading>, result <...>
2. ...
3. ...

Over-engineering cuts: <what was cut, or "none">
Reviewer agent: <report path>, <each point and what was done>

## Hand test
| Scenario | Platform, language, theme | Expected | Seen | Screenshot |
|---|---|---|---|---|

## Review-bot rounds
| Round | Head commit | Comments | Fix commits | Threads resolved |
|---|---|---|---|---|

## Re-checks
| Fix | The one check chosen | Result |
|---|---|---|
```

## 2. Status comments

Post "Work started" right after the move to In Progress and the assignment. Post "Paused" and "Resumed" whenever the work stops or starts again. Keep each to a few lines.

```
**Work started, <date>**

Status: In Progress, assigned to <assignee>.
Now: <what is being read or checked first>
Next updates on this ticket: <verdict, plan, pull request link>
```

```
**Paused, <date>**

Status: In Progress, paused. <why: the owner reordered, waiting on X>
Reached: phase <n> (<name>). <what exists: branch, commits, nothing committed>
```

```
**Resumed, <date>**

Continuing at phase <n> (<name>) on `<branch>`.
```

## 3. Verdict comment (phase 3)

Post it only when the verdict is not Confirmed; a confirmed ticket just continues.

```
**Ticket check, <date>: <Already fixed | Partly true | Rarer than stated | Rejected | Code moved | Needs a decision>**

What the ticket says: <one sentence>
What the code does today: <one or two sentences>
How a person reaches it: <the steps from launch, or "no path: <why>">
How many users: <number, source, date range>, or <not measured: the event that would count it, and the estimate from the path>
What is a real bug and what is not: <one line each>
Evidence:
- `<path>:<line>` <what is there>
- `<command>`: <result>
Other platforms: <same | different | not checked, and why>

Proposed next step: <close | narrow the ticket to X | owner decides between A and B>
```

## 4. Plan comment (phase 4, plan mode)

```
**Plan for <TICKET-KEY>, <date>. Waiting for the owner's go.**

Verdict: confirmed. <one line of evidence>
Why plan mode: <stored shape | payments | deleted data | new copy | refactor | security>

Change, in order (one commit per line):
1. <test that reproduces the bug or pins today's behaviour>: `<test file>`
2. <change>: `<files>`
3. ...

Each platform: <platform>: <what changes>, or "unaffected because <fact read in the code>".
Shared values touched (copy, stored fields, analytics names, persisted ids, numbers): <list, or none>
What a person will see differently: <screens and states, or "nothing visible">
New or changed copy, in the base language for approval before the other languages are written:
- `<key>`: "<text>"
Data and migration: <none, or what changes, how old data is read, and the sync and backup impact>
Risks and how each is checked: <list>
Not in this pull request: <list, with ticket keys>
Verification: <tests, suites, hand-test scenarios>

Reply "go", or run `/ship-ticket <TICKET-KEY> --go`, to build exactly this.
```

## 5. Commit message

Conventional commits in the style `git log` already shows, one concern per commit, the ticket key at the end of the subject.

```
fix(checkout): keep the discount when the cart is edited (<TICKET-KEY>)

<optional body: why, not what; wrap at 72>
```

Types: `fix`, `feat`, `refactor`, `test`, `chore`, `perf`, `docs`. A clean-up found on the way is its own commit.

## 6. Pull request body

Title: `<TICKET-KEY>: <what changes for the person or the code, in plain words>`

```
## Ticket
<TICKET-KEY>: <link to the ticket>
Sibling pull requests: <links | none: only <platform> changes | not needed because <fact>>

## What was wrong
<two or three sentences, with the file where it lived>

## What changed
- <change> (`<path>`)

## Found and fixed on the way
- <item> (`<path>`), or "nothing"

## How it was verified
| Check | Command | Result |
|---|---|---|
| New and changed tests | `<command>` | <n> passed |
| Module tests | `<command>` | <n> passed, <n> failed |
| Full suite and static checks | `<command>` | <n> passed, <n> failed, or "not run: <reason>" |
| Hand test (required) | <device, build, languages, themes> | <what was seen per scenario>, screenshots in `<path>` |
| Review | `/review`: six dimensions, three ways it could be wrong, over-engineering cuts | per dimension: <n> fixed, or "none, because ..."; <n> lines cut |
| Independent check | `reviewer` agent | <n> points, each fixed or decided by the owner; or "not needed: size s or m, no risky area" |
| Review bot | `<REVIEW-BOT>` | round <n>: <comments>, fixed in <commits>; or "none configured" |

## Not verified
- <item and why>, or "nothing"

## Acceptance criteria from the ticket
- [x] <criterion>: <test name or check>
- [ ] <criterion>: not done, <reason>

## Review notes
<where to look first; any decision the reviewer should confirm>
```

## 7. "Pull request opened" comment (phase 10)

```
**Pull request opened, <date>**
- <platform>: <link, or "no change">

Summary: <two sentences>
Verified: <tests and counts; hand test: devices, scenarios, result>
Not verified: <list, or "nothing">
Found on the way: <fixed here: list | tickets opened: keys | nothing>
Run: model <model id>, size <s | m | l>, mode <auto | plan>, verify passes <1 to 3>
Waiting for: owner review and merge. Nothing was merged.
```

## 8. "Stopped" comment

```
**Work stopped, <date>: <reason in five words>**

Reached: phase <n> (<name>)
Blocker: <what failed, with the command and the decisive output line>
Tried: <one line per attempt>
State: branch `<branch>`, <pushed | local only>, <n> commits
Needs: <a decision between A and B | a fix in X first | access to Y>
```
