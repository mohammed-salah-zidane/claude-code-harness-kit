---
name: graph
description: Run one large task as a small graph of subagents, each with a written contract, a gate and a token budget. Started by the user with /graph.
disable-model-invocation: true
---

# Graph run

Task: $ARGUMENTS

A graph run splits one large task into nodes. A node is one subagent with one job, a written contract and a budget. You are the lead: you write the contracts, check each result at a gate, and keep the state in files. The aim is quality per token. Nodes work in small contexts, and nothing is accepted on a node's word alone.

## 1. Check that a graph is the right tool

One change with one check is one session's work, and a loop with a test to pass beats a graph. Use a graph when at least one of these holds:

- Two or more parts can be built separately.
- A part needs a check by someone who did not write it.
- The work needs long, noisy runs (device tests, wide searches) that would fill your context.

If none holds, say so and work inline.

## 2. Write the run file first

Create the run folder: the folder the project's CLAUDE.md names for graph runs, or `.claude/graph/<short-name>/` when it names none (keep it out of git). Write `GRAPH.md` there:

- The source of truth (ticket, spec, design) and which one wins when they differ.
- The limits of this host and project: builds at a time, lanes, devices.
- The node table: id · job · agent · needs · output file · status.
- What you read as approved, and what stays the owner's decision.

Keep `GRAPH.md` current. It is what lets you compact or clear the conversation and continue.

Then call the advisor once on the plan, before the first node starts.

## 3. Nodes

| Agent | Job | Default model | Never |
|---|---|---|---|
| `scout` | Reads, writes one fact file | Sonnet | Edits anything |
| `builder` | Builds one part test first, inside a closed file list | Opus | Commits, or leaves its list |
| `reviewer` | Checks a part against its contract | Opus | Edits, or sees your conclusions |
| `tester` | Runs a case list on a device | Opus | Fixes code |

Pass `model` on the call only when a node needs more or less than its default: Opus for a hard design read, Haiku for a file listing.

- **Size.** A node is a piece one agent finishes well inside its turn limit. Split a larger part into nodes that run one after another. Each starts fresh from files, not from the previous node's chat.
- **Width.** At most three nodes at once. One builder per repository at a time. Builders never share a file.
- **Questions.** A node cannot ask the owner. It writes the question down and stops; you ask.
- A node is a subagent. Start a separate full session only when the owner wants to watch or steer that node directly.

## 4. The contract

Every node gets all eight lines:

1. Goal, in one sentence.
2. Read first: paths and line ranges.
3. Files it may create or change, as a closed list. For a scout: its output file only.
4. Shared values, each with its one definition: names, keys, numbers, tokens.
5. Tests to write first, and the failing proof wanted (builders).
6. Exit commands, and the counts to report.
7. Stop rules: on a blocker, a file outside the list or a product question, stop and write it down.
8. Report file path, with the headings: Changed · Tests (command, counts) · Not done · Questions · Risks.

Point at files instead of pasting their content. Never put your own conclusions in a reviewer's brief.

## 5. Budgets

- A node's reply is 15 lines at most: status, report path, counts, questions. The rest goes in its report file.
- Read a node's report and its diff. Do not ask it to repeat them in chat.
- Long command output goes to a file; read the failing part.
- You do not drive devices, and you do not build a part a node could build. You write contracts, run gates, fix the small things a gate finds, and talk to the owner.
- At a part boundary, bring `GRAPH.md` up to date, then compact with it as the focus, or clear and read it again. One part's history does not ride into the next.
- Advisor: three planned calls per run. On the plan; on a node's second failed gate or a change of approach; before you say done. Each call re-reads the whole conversation, so add none for routine steps.

## 6. The gate

Run it before the next node starts:

- Read the diff in full: `git diff --stat`, then each changed file. Nothing outside the node's list.
- Re-run the exit commands yourself when the report's counts are the only proof.
- A part that touches sync, money, data loss, concurrency or security gets one `reviewer` check against its contract. Every other part relies on this gate and the one `/review` at the end.
- A change a person can see gets one `tester` run, with pictures beside the design.
- Failed gate: send the findings back to the same node as its new contract. SendMessage keeps its context. Second failure: advisor. Third: you take the node.
- Update the node's status in `GRAPH.md`.

## 7. Many items of the same shape

Twenty files to migrate or twenty-four languages to check is a fan-out, not a set of hand-run nodes. Tell the owner a workflow fits, give the agent count, and run it only when they say so.

## 8. Finish

Run the project's review once on the whole change, then the full checks. Report what was built, what was not, what was not run and why, the open questions, and the run's cost from `/usage`.
