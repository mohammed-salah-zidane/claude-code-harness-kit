---
name: ship-ticket
description: "Ship one <TRACKER> ticket end to end: check its claim, build the whole fix on every platform it touches, then run the tests once, one /review, one hand test, and open a pull request to <BASE-BRANCH> with at most two review-bot rounds. Use for /ship-ticket, a named ticket, or the next one. Never merges. Not for releases or designs (use ship-design)."
argument-hint: "<TICKET-KEY> | next [--plan] [--go] [--resume]"
---

# Ship a ticket

One ticket goes in; one proven pull request per repository it changes comes out, each able to stand alone. Everything found on the way is fixed inside this ticket. Running this skill is the go to branch, commit, push and open pull requests for this ticket, never to merge, force-push or touch another session's files.

## Fill these in first

- `<TRACKER>`: Jira, Linear or GitHub Issues, with access, assignee and state names.
- `<TICKET-KEY>`: the key format, such as `ABC-123`.
- `<BASE-BRANCH>`: the branch pull requests target.
- `<PLATFORMS>`: the apps that ship together, and their repositories.
- `<BUILD-COMMAND>`: the debug build per platform.
- `<TEST-COMMAND>`: module tests, full suite, lint and guard scripts, per platform.
- `<EVIDENCE-FOLDER>`: an untracked folder per ticket for log, output and screenshots.
- `<LANGUAGES>`: the languages the product ships in.
- `<USAGE-DATA>`: where usage is counted (analytics, crashes, support).
- `<REVIEW-BOT>`: the automated pull-request reviewer, or "none".
- `<SIZE-MODELS>`: the model for sizes s, m and l.

## The flow

Check the ticket, build all of it, then run each check once, in this order:

1. Verdict from reading the code (phase 3). No test runs before phase 6.
2. Build the whole change on every platform, tests written with the code, nothing run (phase 5).
3. Tests once: new, module and full suites, static checks (phase 6).
4. One `/review` of the whole diff, and its fixes (phase 7).
5. One hand test, after the review, by one `tester` (phase 8).
6. The pull request, then the review bot, two rounds at most (phase 9).

**Re-checking a fix.** A fix made at step 4, 5 or 6 gets the one check that proves it, never the whole set again:

| The fix | Its one check |
|---|---|
| Changes what a person sees | That scenario on the device |
| Changes logic only | The test classes that cover it |
| Touches sync, money, data loss, concurrency or security, or is more than a small edit | `/code-review` of that change only, plus its tests |

A fix made before the hand test needs no device check of its own: the hand test covers it. Log each re-check: the fix, the check chosen, the result. Merging, on the owner's word, adds one full suite on the merged tree.

## Rules

1. After a compaction only the start of this file is still in context, so read it again from the phase you are on.
2. Keep a log at `<EVIDENCE-FOLDER>/log.md` (layout in `references/templates.md`). After each phase, tick it, add one line of evidence and rewrite "Next step". On resume, read "Next step" and the phase list, not the whole log. Keep it short: long output goes to files beside it.
3. Claim only what you ran in this session and read the result of; otherwise write "not run" and why. The hand test is the exception: it always runs.
4. Work inline. The hand test goes to one `tester` agent. For size l, propose a `/graph` run to the owner.
5. No new tickets. A bug, a red test, dead code or a stale comment met on the way is fixed in this ticket and listed in the pull request. A product question goes to the owner.
6. Advisor: on the plan, when a fix has failed twice, and before opening the pull request.
7. Comment on the ticket at start, verdict and plan, pull request opened, and stop.
8. When a stop condition fires, stop and report.
9. Add what a run teaches to `references/traps.md`, one heading per lesson, in the same session.

## 1. Ticket and gates

Do: take the given key, or with `next` the first open ticket in board order that fits your size. Read it with its labels, links and comments; comments win. Stop on a decision-needed label, an open blocker, someone else's work, or an epic. Size it, set its mode, create the log, move it to In Progress, assign it and post "Work started".
Proof: key, size and mode.
Why: a blocked, undecided or taken ticket wastes a run.

## 2. Context

Do: fetch `<BASE-BRANCH>` and read there `CLAUDE.md` and the matching rules files, the code you will change with its callers and tests, the same behaviour on the other platforms in `<PLATFORMS>`, and the headings of `references/traps.md`, then the notes for this area.
Proof: the files read.
Why: the rules outrank the ticket, and the platform that already behaves correctly is the contract.

## 3. Verdict, before any change

Check the ticket's claim first. Answer these in the log, for every platform:

1. Can a real person reach it? Trace the steps from launch to the broken line and what guards them; "on a new device" has to match how a new device starts.
2. Does something already prevent it? List every caller and every writer of the data first.
3. Does the ask fit the product's rules, the other platforms and itself?
4. How many users does it touch? Count the path's events in `<USAGE-DATA>` only when the verdict or the priority depends on it, never personal data. Otherwise estimate from how often the path runs, and say so.

Reject only with proof: an unreachable path, a test or code that disproves the claim, or a broken rule. Never ship a ticket only because it exists.

| Verdict | Then |
|---|---|
| Confirmed | Continue |
| Code moved | Note where, continue |
| Partly true or rarer | Comment, correct text and priority, continue with what holds |
| Already fixed | Comment, In Review for the owner, stop |
| Rejected | Comment the traced path, Rejected, stop |
| Needs a decision | Comment the options, label decision-needed, To Do, stop |

Proof: the traced path with `file:line`. A bug's test is written in phase 5 and must assert the behaviour the ticket describes, so that it would fail on today's code.
Why: tickets written from reading code are often wrong, and fixing a bug nobody hits still costs a review and a risk.

## 4. Plan

Do: write the commits in order, the tests, each platform's change, the shared values touched (copy, stored fields, analytics names, ids, numbers), each acceptance criterion with its test and hand-test scenario, and what is out of scope. In plan mode, post the plan and stop; on "go" or `--go`, build exactly that. A ticket with several independent parts: ask the owner whether it ships as one pull request or one part per run. Cut `<TICKET-KEY>-<slug>` from the remote `<BASE-BRANCH>` with no upstream in each repository the plan touches, in a worktree if another session owns the checkout.
Proof: the plan, the branches, and in plan mode the go.
Why: the review and the owner hold the diff against the plan, and a rejected ticket leaves no branch.

## 5. Implement, all of it

Do: build the whole change on every platform the ticket touches, inside the rules files, before running anything. Write each test with the code it covers: the bug's test first. Run no tests while implementing; build only when you cannot continue without knowing the code compiles. Fix what you meet in its own commit (rule 5). Commit small, one concern each, with the key, staging files by name.
Proof: the commits.
Why: test runs after every step are where long tickets lose their days.

## 6. Tests, once

Do: when all the code is written, run once on each platform touched: the new tests first as a fast fail, then the full suite (it includes the module tests) and static checks (`<TEST-COMMAND>`), output to files. Show that a failure you did not cause is old (the same test on `<BASE-BRANCH>`), then fix it in this ticket when it is within reach. A fixed failure is re-checked by its test class, not by another full run.
Proof: each command and its counts.
Why: a count you read is evidence; "tests pass" from memory is not.

## 7. Review, once

Do: run `/review` once on the whole diff, each repository. It runs `/code-review`, the project's own review sides and the over-engineering pass, and reports each finding once. Fix each real finding or take it to the owner; apply the cuts, never cutting validation, error handling, security, accessibility or required tests. Re-check each fix once, by the table in "The flow". The diff is not reviewed again.
Proof: the findings, the fixes and their re-checks.
Why: one fresh-context review finds what the author missed; a second one on the same code finds the same things again.

## 8. Hand test, once

Do: write the scenarios and expected results first: each acceptance criterion, the broken state, the fix and the recovery, the real save path. Install a `<BUILD-COMMAND>` build per platform touched and give the list to one `tester` agent, one platform at a time. Use the simulators and emulators that exist; create one only when none can run a scenario, and record it in the log so the clean-up removes it. Each scenario runs once. The base language and another from `<LANGUAGES>` (right-to-left if any), light and dark, on the screens whose layout changed; a logic scenario runs once. Build hard states (seed data, edit storage, a debug-only switch, airplane mode) rather than skip them; ask the owner for what only the owner holds. A failed scenario is fixed, then run again alone.
Proof: a result and screenshots per scenario in `<EVIDENCE-FOLDER>`.
Why: unit tests prove the unit; only the real flow shows what a person gets.

## 9. Pull request, review bot and tracker

Do: when "Ready to open" holds, open it without asking again: a clean tree, only this ticket's commits, the body from the template, linked to its sibling pull requests. Unless `<REVIEW-BOT>` is none, run at most two rounds: request a review and wait in one blocking command for one on the head commit; fix each real comment in its own commit on every platform it holds for, re-checking each fix once; reply on every thread with the commit or proof that nothing needs to change, and resolve it; request round 2 once, fix it the same way, and request no third. A bot that could not review counts as not verified. Then post "Pull request opened", move the ticket to In Review, comment on any existing ticket this pull request also resolves, and tell the user what changed and what was and was not verified.
Proof: the links, each round in the body, the comment and the new state.
Why: the owner reads the pull request and the ticket first, so both tell the truth about every check.

## Sizes and modes

Size s names the exact lines in three files or fewer; m is an ordinary bug across four to ten files; l is sync, concurrency, money or a guessed cause. When two fit, take the bigger: a wrong pull request costs more than a strong model. A model in `<SIZE-MODELS>` takes its size and smaller, or names the right one and asks for a rerun. Raise the size when phase 3 finds more. The mode is plan with `--plan` or for a stored shape, payments, deleted data, new copy, or refactor or security work; owner when only the owner can act, which is not shipped; otherwise auto. Start each ticket in a fresh session, or clear the conversation between tickets.

## Stop conditions

Stop, log the reason, comment on the ticket and tell the user when:

- a phase 1 gate fails, the verdict ends the run, or plan mode has no go;
- the fix needs a product decision, unapproved copy or a missing design;
- it would take something from a paying user, change behaviour beyond the ticket, or alter a stored shape outside the plan;
- phase 6 is still red after two rounds of fixes, or the hand test fails with no clear fix;
- a command is destructive or touches `<BASE-BRANCH>`, a release branch or another session's files;
- the scope is unclear.

## What done means

Ready to open: phases 1 to 8 passed in order on the pushed code, with evidence; each acceptance criterion has a test and a scenario, or the owner's written decision; the platforms agree, or the body says why one needs nothing; the diff holds this ticket's change and the fixes found on the way, nothing else; new strings exist in all `<LANGUAGES>`; the body claims nothing unseen.

Done: the bot rounds are finished, the owner said to merge, the merged tree passed the full suite once, the merge is pinned to the tested commit, and the owner closed the ticket.

Clean-up, right after the merge and not before (the review and the bot fixes use these): remove the ticket's worktrees and their build folders, the merged branch, the devices the log says it created (never a shared one), and its evidence folder with its screenshots, recordings and builds. Keep the log. A run ends In Review or Done, never in between.
