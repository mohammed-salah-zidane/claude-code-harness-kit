# Claude Code harness kit

A small setup for Claude Code that aims to keep quality high and token use low, plus a prompt that has Claude audit your current setup, clean it up with your approval, and install the kit.

It comes from one rebuild in November 2026 by one developer who builds a mobile app for iOS and Android with Claude Code every day. The numbers behind each choice are summarised below; the logs themselves stay private. Nothing here is specific to that app.

Made by Mohamed Salah ([mohammed-salah-zidane](https://github.com/mohammed-salah-zidane) on GitHub). MIT licence.

## How it came about

Since I started coding with AI, I have changed my setup almost every week, looking for what works. Plain chat first. Then agents that edit the code. Then Spec Kit to write specs before code. Then Superpowers for planning, with UI skills on top for design. Now a small graph of agents with an advisor. Each step fixed something the one before could not.

Newer models do much of what those layers did, and every layer costs tokens. So this kit keeps only what still earns its place on my own projects: a ticket instead of a plan file, a few agents with written briefs, an advisor at the decision points, and one review per change. The daily flow below shows how they fit together.

## Before you run it

**What the setup prompt does to your machine.** It reads `~/.claude` (settings, CLAUDE.md, agents, commands, skills, hooks, plugins), the MCP server entries in `~/.claude.json`, and the `CLAUDE.md`, `.claude` folder, `.mcp.json` and memory folder of each project you choose. Then it shows you one plan and stops.

- You can strike or change items in the plan. Your go covers only what is left in it. Three later steps ask again: code changes after the architecture read, which working rules to add, and the fixes the CLAUDE.md skills propose.
- Before it changes anything, it backs up what it will touch into `~/.claude/backups/setup-<date>/`. Removed skills, agents, commands and leftover files are moved there, not deleted. Plugins are uninstalled with Claude Code's own command, and the backup lists them so that each can be reinstalled. A `RESTORE.md` in that folder says how to put each one back.
- It does not commit or stage anything, and it never prints a secret. If one does reach the log, it tells you so that you can rotate it.

**Requirements.**

- Claude Code. The kit was built on version 2.1.325. Settings keys change between versions, so the prompt tells Claude to check the documentation before relying on one.
- macOS or Linux. On Windows Claude uses the equivalent commands; that path has not been tried.
- Python 3, for the two counting scripts.
- `scripts/start-from-keychain.sh` uses the macOS Keychain. On Linux, use your own secret store or an environment variable set outside the repository.

**Privacy.** `scripts/usage-count.py` and `scripts/session-cost.py` read every transcript under `~/.claude/projects` on your machine and print counts into your Claude Code session. They send nothing anywhere else.

## Quick start

1. Clone it: `git clone https://github.com/mohammed-salah-zidane/claude-code-harness-kit`, or download the zip from this page.
2. Open Claude Code in a project you work on often.
3. Say: `Read <path to this folder>/SETUP-PROMPT.md and follow it.`

Claude measures your current setup first, so you get before and after numbers.

## Install by hand

If you would rather not hand your setup to a prompt, copy the kit yourself. `-n` leaves any file you already have untouched; compare those by hand.

```bash
cd claude-code-harness-kit
mkdir -p ~/.claude/agents ~/.claude/skills ~/.claude/commands ~/.claude/output-styles
cp -n kit/agents/*.md ~/.claude/agents/
cp -Rn kit/skills/graph kit/skills/architecture ~/.claude/skills/
cp -n kit/commands/review.md ~/.claude/commands/
cp -n kit/output-styles/Concise.md ~/.claude/output-styles/
```

Then:

1. Add the four sections of `kit/global-CLAUDE.md` to `~/.claude/CLAUDE.md`.
2. Merge the keys of `templates/settings/global-settings.json` into `~/.claude/settings.json`. Replace the two `<...>` model values with models your plan includes, for example `opus`; the advisor must rank at or above the main model. `templates/settings/README.md` explains each key.
3. Add the deny rules of `templates/settings/project-settings.json` to each project's `.claude/settings.json`.
4. Type `/review` once. If Claude Code's built-in review answers instead of the kit's, rename the file to `full-review.md`, and write `/full-review` in place of `/review` in `~/.claude/CLAUDE.md`.
5. Run `claude -p "/context"` before and after, to see what changed.

The cleanup itself, deciding which plugins and skills to remove, is the part the prompt does for you.

## Words used here

| Word | Meaning |
|---|---|
| Subagent, helper | A second Claude that Claude Code starts inside your session, with its own fresh context. It does one job and returns a short reply. |
| Contract | The written brief a subagent gets: its goal, what to read, which files it may change, the checks that prove it is done, and how long its reply may be. |
| Graph run (`/graph`) | One large task split into subagents, called nodes, each with a contract. The lead session checks each node's result (the gate) before the next node starts. |
| Advisor | A stronger model that Claude Code consults at decision points, set with `advisorModel`. |
| Compact window | The context size at which Claude Code summarises the conversation to make room. |
| Over-engineering pass | One review pass that only looks for code to delete: the built-in `/simplify`, or a dedicated skill. |

## What has been measured and what has not

| Claim | Status |
|---|---|
| Start-up prompt, headless: 65.8k down to 60.0k tokens, about 9% | Measured with headless cold prompts before and after. |
| Plugins, skills and permission rules removed (table below) | Counted. |
| About 7.0 billion cached tokens for one large task | Measured from that task's transcripts, before the rebuild. |
| Lower cost on long runs from the 300k compact window, short helper replies and `high` effort | Not measured yet. It is expected from where the cost was; the next large task will show it. |
| The four agents and the three scripts | Installed on that machine. The agents pass `claude plugin validate`, and both counting scripts run there. |
| `/graph`, `/architecture`, the three skill templates and the setup prompt | Written and validated, not yet run end to end. A fresh Claude session reviewed the setup prompt, and its findings were fixed. |

## What is in the folder

| Path | What it is |
|---|---|
| `SETUP-PROMPT.md` | The prompt for Claude: measure, propose, clean up, install the kit, fix each project, verify, report. |
| `kit/` | Files that go into `~/.claude` and work in every project: four agents, the `/graph` and `/architecture` skills, the `/review` command, four short global rules (`global-CLAUDE.md`), an output style. |
| `templates/skills/` | Three procedure skills to adapt to your own project: ship a ticket, ship a design, write release notes. |
| `templates/project-CLAUDE.md` | A model for a project's CLAUDE.md. |
| `RULES.md` | The working rules one product runs on, each with its reason, with the stack and the architecture taken out. |
| `templates/rules/` | Rule files that load only when matching files are touched: an architecture outline for Claude to fill, and templates for design system, localization and platform parity. |
| `templates/settings/` | The settings values, with the reason for each. |
| `scripts/` | Three small scripts: count which skills, agents and MCP servers you really use; measure what a session cost; start an MCP server with its key read from the macOS Keychain. |
| `SKILLS.md` | The skills, plugins and MCP servers the original setup kept, by role, with how often each was used. |

## The ideas behind it

**1. On a long run, cost is context size per turn times the number of turns.** One large task, run as seven full sessions, read about 7.0 billion cached tokens. Each session carried close to 500k tokens on every turn for thousands of turns, because auto-compact only starts near 967k on a 1M-context model. The cost came from how much each session carried, more than from how many sessions there were. So: set a smaller compact window, clear the conversation between unrelated tasks, and keep the state of long work in files.

**2. What loads in every session is a budget.** Keep CLAUDE.md to what cannot be read from the code: commands, decisions, gotchas, what you corrected twice. Put area rules in path-scoped files. Put procedures in skills, which load only when used. Trim the memory index. Check the result with `/context`.

**3. Keep the tools you use.** Let the logs decide: a plugin, skill or agent with no use goes. That machine's transcripts went back seven weeks; in them, 86 of 120 personal skills had never run, and nothing that did run needed them. A plugin that injects text into every session through hooks changes every reply, whether you wanted it that turn or not. Connect an MCP server only in the project that needs it, and prefer a command-line tool where one exists, because it adds nothing to the start-up prompt.

**4. Write judgment calls in prose, and put rules that must never bend in hooks or deny rules.** Capitals, "don't be lazy" and "think hard" no longer help: current models follow a plainly worded line, and tend to over-apply an emphasized one. If a rule keeps being missed, the file is too long or the rule belongs in a hook.

**5. Use a subagent for parallel work, to keep the main context small, or for a check by someone who did not write the code.** It will not give a better answer than the main session would. A single helper gets a short contract (goal, files to read, files it may change, exit checks, a reply of at most 15 lines), its own model and turn limit, and its result is checked before anything is built on it. Several helpers on one task run as `/graph`, where each node gets a fuller eight-line contract and the lead checks every result before the next node starts.

**6. Ask the stronger model at the decision points only.** The advisor is worth a call on the plan, when a fix has failed twice, and before saying a long task is done. Each call re-reads the whole conversation.

**7. One review per diff.** A bug review in a fresh context, then the sides your project cares about, then one pass that only looks for code to delete. Each finding is reported once. A diff that has not changed is not reviewed again.

**8. A procedure you repeat becomes a skill with phases, gates and a log.** Each phase names the proof it needs. The log is ticked after each phase, so a new session, or the same one after a compaction, continues without repeating work. Lessons from earlier runs live in a reference file with one heading per lesson, and only the matching ones are read. After a compaction a skill keeps only its first 5,000 tokens, so the rules go at the top.

**9. Claim only what you ran.** A bug is confirmed by a test that fails for the reason given. A change a person can see is hand tested on a device, with screenshots kept. Anything not run is written "not run", with the reason.

**10. No secret sits in a project file.** Keys go in the system keychain or in an environment variable set outside the repository.

**11. Match the model and the effort to the job.** The strongest model at the highest effort on every turn was one of the measured costs. The setup now runs a strong main model at `high` effort, with the strongest model as advisor.

**12. The architecture is chosen or learned, then written down and checked.** This kit ships no architecture. `/architecture` picks one with you for a new project, from the platform's current guidance and your product's needs. For an existing project it reads the code, writes down the architecture that is already there, and lists where the code leaves it. Either way the result is one contract file, plus checks that print nothing when the code conforms: the build where it can enforce a boundary, audit searches, the review, and a hook for the few patterns worth blocking.

**13. Measure before and after.** Two commands tell you most of it: `claude -p "/context"` for what loads at start-up, and `/usage` for where the tokens went.

## What the original rebuild changed

| | Before | After |
|---|---|---|
| Plugins | 26 | 8 |
| Personal skills | 120 | 34 kept, plus three written for this kit |
| Permission allow rules | 678 | 176 |
| Auto-compact window | about 967k | 300k for the main session, 200k for agents |
| Effort | `xhigh` on every model | `high` |
| Start-up prompt, headless | 65.8k tokens | 60.0k, with the subagent tools now loaded |
| Largest procedure skill | 91KB in one file | 58KB, with its lessons in a reference file |

Two traps it found on the way:

- `ENABLE_TOOL_SEARCH=auto` stops deferring tools once few MCP servers are connected, and loads every tool definition up front: 118k tokens in one run. Leave it unset.
- The skill listing is capped at 1% of the context window. Removing skills does not shrink it until the total is under the cap, although the remaining skills do get their full descriptions back. `skillListingBudgetFraction` lowers the cap.

## The daily flow

1. **A ticket, not a plan file.** Every task starts as a ticket in the tracker, and a ship-ticket skill takes it from there: check that the ticket is real before changing anything, plan, build test first, verify, review, hand test, open the pull request, update the ticket. The skill keeps a log that survives a compaction, so no separate plan document is needed.
2. **A design** goes through a ship-design skill: read the existing code, take every value from the design source, plan every platform together, build, compare on a device.
3. **A review**, in any wording, is `/review` (or `/full-review` where the built-in name is taken): bugs first, then the project's own checklist, then a pass that only looks for code to delete.
4. **A large task with separable parts** is `/graph`. The lead writes a run file and asks the advisor about the plan. Each `builder` agent gets a written contract and a closed list of files it may touch. A `reviewer` that has not seen the code being written checks each part before the next one starts. A `tester` agent runs the app on a simulator or emulator. The review runs once at the end.
5. **State lives in files**: the ship log, the evidence folder, the run file. Compacting or clearing loses nothing.
6. **A correction becomes a memory note with its reason.** A rule repeated often moves into CLAUDE.md. A rule that must never bend becomes a hook or a deny rule.

## Sources and credit

- Claude Code documentation: [best practices](https://code.claude.com/docs/en/best-practices.md), [costs](https://code.claude.com/docs/en/costs.md), [subagents](https://code.claude.com/docs/en/sub-agents.md), [skills](https://code.claude.com/docs/en/skills.md), [advisor](https://code.claude.com/docs/en/advisor.md), [workflows](https://code.claude.com/docs/en/workflows.md), [model configuration](https://code.claude.com/docs/en/model-config.md).
- The graph pattern is Anthropic's orchestrator-workers pattern under a newer name. Two readable write-ups: [Graph Engineering with Claude Code](https://www.aibuilderclub.com/blog/graph-engineering-with-claude-code) and [five composable patterns](https://www.qawolf.com/blog/how-to-implement-graph-engineering-5-composable-patterns).
- Third-party skills and plugins named in `SKILLS.md` belong to their authors and are not included here.

## Feedback and contributions

If you run it, open an issue with the "Share your results" template: your start-up numbers before and after, and anything the prompt got wrong on your machine. Real numbers from other setups are what this kit needs most.

Pull requests that fix a wrong claim, a settings key that has changed, or a step that failed on your machine are welcome. Please name the Claude Code version you used.

## Licence

MIT, see `LICENSE`. Skills and plugins named in `SKILLS.md` belong to their authors and keep their own licences.
