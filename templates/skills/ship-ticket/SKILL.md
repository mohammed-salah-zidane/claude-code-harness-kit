---
name: ship-ticket
description: "Ship one <TRACKER> ticket end to end: check its claim, fix it test-first on every platform it touches, review and hand-test it, and open a pull request to <BASE-BRANCH>. Use for /ship-ticket, a named ticket, or the next one. Never merges. Not for releases or designs (use ship-design)."
argument-hint: "<TICKET-KEY> | next [--plan] [--go] [--resume]"
---

# Ship a ticket

One ticket goes in; one small, proven pull request per repository it changes comes out, each able to stand alone, then its related tickets. Running this skill is the go to branch, commit, push and open pull requests for this ticket and the related tickets phase 11 names, never to merge, force-push or touch another session's files.

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

## Phases, in this order

1. Ticket and gates
2. Context
3. Verdict, before any change
4. Plan
5. Workspace
6. Implement, test first
7. Verify
8. Review
9. Hand test
10. Pull request, review bot and tracker
11. Related tickets

## Rules

1. After a compaction only the start of this file is still in context, so read it again from the phase you are on.
2. Keep a log at `<EVIDENCE-FOLDER>/log.md` (layout in `references/templates.md`). After each phase, tick it, add one line of evidence and rewrite "Next step". With `--resume` or an existing log, continue at the first unticked phase.
3. Claim only what you ran in this session and read the result of; otherwise write "not run" and why. The hand test is the exception: it always runs.
4. Work inline. Device hand tests go to the `tester` agent; a risky change also gets a `reviewer` agent check. For size l, propose a `/graph` run to the owner.
5. One review per diff: a diff that was reviewed and has not changed is not reviewed again.
6. Comment on the ticket at each milestone, from the templates.
7. When a stop condition fires, stop and report.
8. Add what a run teaches to `references/traps.md` in the same session.

## 1. Ticket and gates

Do: take the given key, or with `next` the first open ticket in board order that fits your size. Read it with its labels, links and comments; comments win. Stop on a decision-needed label, an open blocker, someone else's work, or an epic. Size it, set its mode, create the log, move it to In Progress, assign it and post "Work started".
Proof: key, size and mode.
Why: a blocked, undecided or taken ticket wastes a run.

## 2. Context

Do: fetch `<BASE-BRANCH>` and read there `CLAUDE.md` and the matching rules files, the code you will change with its callers and tests, the same behaviour on the other platforms in `<PLATFORMS>`, and the `references/traps.md` notes for this area.
Proof: the files read.
Why: the rules outrank the ticket, and the platform that already behaves correctly is the contract.

## 3. Verdict, before any change

Check the ticket's claim first. Answer these in the log, for every platform:

1. Can a real person reach it? Trace the steps from launch to the broken line and what guards them; "on a new device" has to match how a new device starts.
2. Does something already prevent it? List every caller and every writer of the data first.
3. Does the ask fit the product's rules, the other platforms and itself?
4. How many users does it touch? Count the path's events in `<USAGE-DATA>`, never personal data, and write the number and source. With no source, write "not measured", name the event to count, and estimate from how often the path runs.

Reject only with proof: an unreachable path, a test that disproves the claim, or a broken rule. Never ship a ticket only because it exists.

| Verdict | Then |
|---|---|
| Confirmed | Continue |
| Code moved | Note where, continue |
| Partly true or rarer | Comment, correct text and priority, continue with what holds |
| Already fixed | Comment, In Review for the owner, stop |
| Rejected | Comment the traced path, Rejected, stop |
| Needs a decision | Comment the options, label decision-needed, To Do, stop |

Proof: for a bug, a test that fails for the reason the ticket gives, or the bug is not confirmed; for a clean-up, its measurement run again. Plan mode may confirm by reading until the go.
Why: tickets written from reading code are often wrong, and fixing a bug nobody hits still costs a review and a risk.

## 4. Plan

Do: write the commits in order, the tests, each platform's change, the shared values touched (copy, stored fields, analytics names, ids, numbers) and what is out of scope. In plan mode, post the plan and stop; on "go" or `--go`, build exactly that. A ticket too big for one reviewable pull request ships one part per run.
Proof: the plan, and in plan mode the go.
Why: the review and the owner hold the diff against the plan.

## 5. Workspace

Do: if another session owns the checkout (a recent branch switch, a live build), use a worktree. Cut `<TICKET-KEY>-<slug>` from the remote `<BASE-BRANCH>` with no upstream, in each repository the plan touches.
Proof: branches and base commits.
Why: cut after the verdict, a rejected ticket leaves no branch, and with no upstream a plain push cannot reach `<BASE-BRANCH>`.

## 6. Implement, test first

Do: write the failing test (a bug) or one that pins today's behaviour (a refactor) and log its failure line, then make the change and add the other acceptance tests. Change every platform the ticket touches the same way, inside the rules files. Fix what you meet in its own commit, or open a ticket if it is large. Commit small, one concern each, with the key, staging files by name.
Proof: the failure line and the commits.
Why: a test written after the fix tends to prove the fix, not the bug.

## 7. Verify

Do: on each platform touched, run the new tests, module tests, full suite and static checks (`<TEST-COMMAND>`), output to files. Show that a failure you did not cause is old (the same test on `<BASE-BRANCH>`); fix it if within reach, otherwise name it in the pull request.
Proof: each command and its counts.
Why: a count you read is evidence; "tests pass" from memory is not.

## 8. Review

Do: run `/review` on each repository's diff; it is the one review of this diff. Record what it finds, and what your own read of the diff and its callers finds, under six dimensions, each finding with `file:line` and a concrete failure, or "none, because <what you checked>":

1. Logic: every acceptance criterion, for empty, negative, first-run, signed-out, offline and second-device input, at the root cause.
2. Bugs: concurrency, lifecycle, data loss, sync, errors shown, money, time zones, languages, accessibility, themes.
3. Code quality: one job per type, no duplicate or dead code, tests that fail for the right reason.
4. Scalability: ten times the data, and the hot paths.
5. Maintenance: one source of truth per fact.
6. Project standards: each broken rule, quoted.

Then write three concrete ways the fix could still be wrong (an edge input, another caller, another platform, a lifecycle) and check each. Fix real findings with a test that fails first, or take them to the owner. Apply the cuts of the over-engineering pass that ends `/review`, never cutting validation, error handling, security, accessibility or required tests. For size l or a risky change (sync, money, data loss, security), give the `reviewer` agent the ticket, the diff and the criteria, not your conclusions, and settle each point. Rerun phase 7 after any change.
Proof: the dimensions, the three checks, the cuts and any reviewer report.
Why: the author is the worst judge of a fix, so the review hunts for reasons it is wrong.

## 9. Hand test

Do: write the scenarios and expected results first: the broken state, the fix and the recovery, in the base language and another from `<LANGUAGES>` (right-to-left if any), light and dark. Install a `<BUILD-COMMAND>` build of the final code per platform touched and give the list to the `tester` agent. Build hard states (seed data, edit storage, a debug-only switch, airplane mode) rather than skip them; ask the owner for what only the owner holds. A later code change reruns the scenarios it touches.
Proof: a result and screenshots per scenario in `<EVIDENCE-FOLDER>`.
Why: unit tests prove the unit; only the real flow shows what a person gets.

## 10. Pull request, review bot and tracker

Do: when "Ready to open" holds, open it without asking again: a clean tree, only this ticket's commits, the body from the template, linked to its sibling pull requests. Unless `<REVIEW-BOT>` is none, run rounds: request a review and wait in one blocking command for one on the head commit; fix each real comment in its own commit on every platform it holds for, then verify, review and rerun the scenarios it touches; reply on every thread with the commit or proof that nothing needs to change, resolve it, request again. Clean means the newest bot review is on the head commit with no new comments and no open thread. Stop after five rounds that still add comments; a bot that could not review counts as not verified. Then post "Pull request opened", move the ticket to In Review, and tell the user what changed and what was and was not verified.
Proof: the links, each round in the body, the comment and the new state.
Why: the owner reads the pull request and the ticket first, so both tell the truth about every check.

## 11. Related tickets

Do: list the tickets this one blocks, those with its root cause, and its twin on another platform. Ship each from phase 1; cut one that needs this change from this branch, its body opening with "merge after <link>". Comment on one that fails a gate.
Proof: each one shipped, or named with its reason.
Why: a fix that leaves its twin broken ships the bug again.

## Sizes and modes

Size s names the exact lines in three files or fewer; m is an ordinary bug across four to ten files; l is sync, concurrency, money or a guessed cause. When two fit, take the bigger: a wrong pull request costs more than a strong model. A model in `<SIZE-MODELS>` takes its size and smaller, or names the right one and asks for a rerun. Raise the size when phase 3 finds more. The mode is plan with `--plan` or for a stored shape, payments, deleted data, new copy, or refactor or security work; owner when only the owner can act, which is not shipped; otherwise auto.

## Stop conditions

Stop, log the reason, comment on the ticket and tell the user when:

- a phase 1 gate fails, the verdict ends the run, or plan mode has no go;
- the fix needs a product decision, unapproved copy or a missing design;
- it would take something from a paying user, change behaviour beyond the ticket, or alter a stored shape outside the plan;
- three verify passes end red, or the hand test fails with no clear fix;
- a command is destructive or touches `<BASE-BRANCH>`, a release branch or another session's files;
- the scope is unclear.

## What done means

Ready to open: phases 1 to 9 passed in order on the pushed code, with evidence; each acceptance criterion has a test and a scenario, or the owner's written decision; the platforms agree, or the body says why one needs nothing; the diff holds only this ticket; new strings exist in all `<LANGUAGES>`; the body claims nothing unseen.

Done: the bot is clean, the owner said to merge, the merged tree passed the full suite, the merge is pinned to the tested commit, related tickets are shipped or named, and the owner closed the ticket. A run ends In Review or Done, never in between.
