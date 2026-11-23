# Audit and rebuild my Claude Code setup

I want you to audit my whole Claude Code setup on this machine, clean it, and install a kit that keeps quality high and token use low. It should work the same in every project I have.

This file comes from a rebuild that someone else did on their own machine in November 2026, on Claude Code 2.1.325. The lessons and the kit are theirs. My machine, my projects and my plugins are different, so measure here first, and show me one plan before you remove or overwrite anything.

This file sits in a kit folder. Paths such as `kit/agents/` and `templates/` are relative to the folder this file is in. `README.md` there explains the ideas, and `SKILLS.md` lists what the original setup kept.

## What I want

- The best quality for the tokens spent.
- One setup for every project. The generic parts live in `~/.claude`. A repository holds only its own facts.
- Replies in plain, complete sentences.
- Subagents allowed, but under control: a written contract, a check of the result, and a budget.

## What the original rebuild measured

Use these facts to decide what matters. The numbers are from that machine.

1. One large task, run as seven full sessions, read about 7.0 billion cached tokens. The cost was context size per turn times the number of turns, not the number of agents. Every session sat near 500k tokens per turn for thousands of turns, because auto-compact only starts near 967k on a 1M-context model. The lead session was woken 138 times by messages from the others. Two read-only helpers used 120 to 150 million tokens each to write one fact file.
2. So the large levers are a smaller compact window, short replies from helpers with the state kept in files, helpers that are small subagents with their own model and turn limit, and a sensible effort level. Trimming the start-up prompt helps less: it gave about 9% there.
3. The skill listing is capped at a share of the context window, 1% by default. Removing skills does not shrink the listing until the total is under the cap. It does give the remaining skills their full descriptions. `skillListingBudgetFraction` lowers the cap, and the least-used skills lose their descriptions first.
4. `ENABLE_TOOL_SEARCH=auto` is a trap. With few MCP servers connected it stops deferring tools and loads every tool definition up front, 118k tokens in one measured run. Leave the variable unset; deferring is the default.
5. A skill invoked in a session keeps only its first 5,000 tokens after a compaction. A long skill keeps its rules at the top and its detail in a `references/` folder.
6. Each advisor call re-reads the whole conversation, uncached. An advisor must rank at or above the main model.
7. `skillOverrides` does not affect plugin skills. A plugin whose hooks inject text into every session can only be stopped by uninstalling it. If one of its skills is worth keeping, keep it as a personal copy, and respect its licence.
8. Anthropic's own guidance now lists these as habits to drop: emphasis in capitals, "don't be lazy" lines, "think hard", using a subagent to get a better answer, describing the architecture in CLAUDE.md. A rule that can never bend belongs in a hook or a permission deny rule, not in prose.
9. There, the always-on memory index was the largest single item at start-up (about 7.7k tokens), ahead of the skill listing (5k) and MCP server instructions (3.4k).
10. Results there: 26 plugins down to 8, 86 of 120 personal skills removed, 678 permission allow rules down to 176, one 91KB skill down to 58KB.

## Ground rules for this job

- Back up before you change anything, into `~/.claude/backups/setup-<today>/`: `~/.claude/settings.json`, `~/.claude/CLAUDE.md`, `~/.claude/agents`, `~/.claude/commands`, `~/.claude/plugins/installed_plugins.json`, a listing of `~/.claude/skills` with link targets, `~/.claude.json` (owner-only permissions), `~/.claude/hooks`, any shell profile you will edit, and each project's `CLAUDE.md` and `.claude` folder (without its worktrees) before you touch them.
- A removed skill that is a symlink is unlinked, with its target recorded. A removed skill that is a real folder is moved into the backup. Write `skills-removed.tsv` (name, kind, target) and a `RESTORE.md` beside it. Files are moved into the backup, never deleted. Plugins and global command-line packages are uninstalled with their own commands, and the backup lists each one so that it can be reinstalled.
- Never print a secret. `~/.claude.json` holds sign-in data: never open it with Read or `cat`; query only the keys you need (`mcpServers`, `projects`, `disabledMcpServers`) with a script. Read `.mcp.json`, `~/.claude.json` and env files with a script that prints key names and `<set>` in place of values. Treat as secret everything under `env` or `headers`, any value whose key contains KEY, TOKEN, SECRET, PASSWORD, CREDENTIAL, AUTH or DSN, any argument that follows a flag such as `--token`, and any address with a name and password in it. If a secret does reach the log, tell me so that I can rotate it.
- No commits and nothing staged. Delete a tracked file with `rm`, not `git rm`, so that another session's commit cannot pick the change up. No destructive git.
- When a permission check refuses an action, do not route around it. Finish the rest and tell me which line to change by hand.
- Work inline. The only subagents in this job are the one-agent test near the end and, if the architecture step needs a wide read, one `scout`.
- Settings keys, agent frontmatter fields and `claude plugin` commands change between versions. Run `claude --version`. Before you rely on one you have not used, check it in the documentation linked from `https://code.claude.com/docs/llms.txt`, or with `--help`.
- The commands below are for macOS and Linux. On Windows, use the equivalent.
- Inside a file you are already changing with my go, fix what you find on the way, such as a stale path. Anything else you find goes into the plan.

## Step 1. Measure before changing anything

Run these in a project I use often, and keep the numbers for the report.

```bash
claude --version
claude -p "Reply with the single word OK" --model haiku --output-format json   # add cache_creation_input_tokens + cache_read_input_tokens + input_tokens
claude -p "/context" --model haiku                                              # the always-on table
claude plugin list          # then: claude plugin details <name> for each, to see its always-on cost and hooks
claude mcp list
```

One headless sample moves by a few thousand tokens with which MCP servers connect in time, so take two.

Count what I use with `python3 <kit folder>/scripts/usage-count.py`. It reads `~/.claude/projects` wherever it runs, and counts both skills the model invoked and commands I typed as `/name`. It only sees the transcripts still on disk, so it prints the date of the oldest one: the counts cover that window, and a skill I use once a quarter can look unused. It also lists the personal skills with no run.

Then run `python3 <kit folder>/scripts/session-cost.py 14`. It lists my recent sessions with their turns and their median context per turn. That shows whether my cost is context size, as it was in the original rebuild.

## Step 2. Take inventory and show me one plan

Read everything, then give me a single plan and wait for my go. Look in these places:

- `~/.claude`: `settings.json`, `CLAUDE.md`, `agents/`, `commands/`, `skills/`, `hooks/`, `output-styles/`, the installed plugins and their marketplaces.
- `~/.claude.json`: user-scope MCP servers.
- Each project: `CLAUDE.md`, `AGENTS.md`, `.claude/` (settings, rules, skills, commands, agents, hooks) and `.mcp.json`. Find projects from the folder names in `~/.claude/projects` and from `.claude` folders under my code folders. A folder name there is the project's path with each `/` written as `-`; confirm each one by checking that the path exists. List the projects in the plan and let me choose which ones this job covers.
- Each project's memory folder in `~/.claude/projects/<project>/memory/`, when it exists.

Put each finding in the plan with what you would do. These are the defaults that the original rebuild used:

| What you find | Default action |
|---|---|
| A plugin whose hooks inject text into every session or every prompt (a forced "check skills first" preamble, a talking style, a standing persona) | Uninstall it. Keep one skill from it as a personal copy if I use that skill. |
| A plugin, skill, agent or command with no use in the logs and no reference from something I keep | Remove it. Before that, grep the kept skills, commands and CLAUDE.md files for its name. |
| Two plugins or skills that do the same thing, or a plugin that a built-in command now covers (`/code-review`, `/simplify`) | Keep one. |
| An agent with a "use proactively" description, or an old pack of generic agents | Remove it; the kit in step 5 replaces it. |
| An MCP server that fails to connect in every session | Remove it. Save its config in the backup first. |
| An MCP server or account connector I use in only one project | Take it out of the global setup. Switch it on in that project only, or off elsewhere through `/mcp`. |
| A permission allow rule that is a one-off (an absolute path, a line number, a process id, a long one-liner) | Drop it. |
| A permission allow rule that is risky (`bash -c`, `sudo`, `rm -rf`, `git push`, `git reset --hard`, `git stash drop`, `killall`, a bare `env`) | Drop it. |
| A secret in `.mcp.json`, in a settings file or in a tracked file | Move it to the system keychain or to an environment variable set outside the repository. Tell me to rotate it if it was ever committed or printed. |
| A CLAUDE.md rule that bans subagents outright, forces a habit with capitals, or says "don't be lazy" | Replace it with the wording in step 6. |
| A CLAUDE.md that names a path, command or tool that no longer exists | Fix it. |
| A CLAUDE.md with no test command | Add the real one. |
| A skill file longer than about 20KB | Keep its rules and steps in `SKILL.md`. Move examples, history and dated notes into `references/`, text unchanged, each under a heading. Verify with a short script that every non-empty line of the moved text is in the new file, in the same order. |
| A memory index with status lines of finished work, or lines that repeat a CLAUDE.md rule | Move those lines to an archive file in the same folder. The notes themselves stay. |
| A tool I no longer use that left files, shell profile lines or scripts behind | Remove it after I confirm I no longer use the tool. Its files, my own and its install folder alike, are moved into the backup. Tell me the size of the install folder so that I can delete that copy myself. |

Also put these decisions in the plan, each with your recommendation:

1. **Main model, advisor and effort.** Ask me which models my plan includes; the `/model` picker lists them. The pairing the original used was a strong main model with the strongest model as advisor, at effort `high`. A cheaper pairing is a mid model as main with a strong advisor. `xhigh` on every model was one of the costs there; each current model's own default is `medium`.
2. **Compact window.** The original chose 300k for the main session and 200k for helpers, instead of about 967k.
3. **Subagents.** Whether to lift any existing ban and use the rule in step 6.
4. **Workflows.** The original put the `Workflow` tool on "ask", so that it never starts without a yes.
5. **Output style.** Whether to install the Concise style from step 4.
6. **The CLAUDE.md plugin.** Whether to install `claude-md-management`, which step 6 uses.
7. **Anything you are unsure about.** Say what you found and what you would do.

Then stop and wait for my go. I may strike or change items first; a go covers only the items left in the plan, and nothing outside it. Three later steps ask again, because they depend on what you find: code changes after the architecture read, which working rules to add, and the fixes the CLAUDE.md skills propose.

## Step 3. Apply the removals

After my go:

- Plugins: `claude plugin uninstall <name>@<marketplace> --scope user`, then `claude plugin marketplace remove <name>` for a marketplace with nothing left. To use a plugin in one project only, disable it at user scope and run `claude plugin enable <name>@<marketplace> --scope local` in that project.
- Skills, agents and commands: by the backup rule above.
- MCP servers: `claude mcp remove <name> -s user`, with the config saved first.
- Account connectors are switched off per project in `/mcp`. Tell me which ones, and let me do it there. Only if I ask you to do it: they are stored by display name in `~/.claude.json` under `projects["<path>"].disabledMcpServers`. Write that file through a temporary file and a rename, and read the value back at the end of the job, because a running session can rewrite it.
- Leftovers of a removed plugin: move its flag files in `~/.claude` and its config folder into the backup, and uninstall its global command-line package with the package manager that installed it, adding the package name to the backup's list. Before moving a tool's data folder, check whether another program still points at it. If one does, leave the folder and tell me its size.
- Permission rules: rewrite each allow list to the command-family patterns and the entries still in use.

A secret moved to the macOS Keychain is read at start through a small script: `scripts/start-from-keychain.sh` is the pattern. On another system use its own secret store, or an environment variable set in my shell profile. Store the value with a script that reads it from the old file, writes it with `security add-generic-password -U`, reads it back and compares, without printing it. Point the `.mcp.json` entry at the start script, and test it by piping one MCP `initialize` request into the script. Passing a value on the command line shows it for a moment to other programs on this machine. If I would rather avoid that, give me the command to run myself: `security add-generic-password -U -s <service> -a <name> -w` asks for the value without showing it.

## Step 4. Settings

In `~/.claude/settings.json`, apply `templates/settings/global-settings.json` with the values I chose in step 2. `templates/settings/README.md` gives the reason for each key.

- Merge these into the file; do not replace it.
- If `modelSettings` holds a saved effort level per model, set those to the same level, because they win over `effortLevel`.
- Set `skillListingBudgetFraction` only if I still have more than about 40 skills after the cleanup. Otherwise leave it out.
- Remove `ENABLE_TOOL_SEARCH` wherever it is set: the `env` of a settings file, or my shell profile.
- Do not set `CLAUDE_CODE_SUBAGENT_MODEL`, and remove it if it is set. It would also lower the model of `/code-review`'s reviewers. The kit's agents name their own model.
- Remove a blanket `"deny": ["Agent", "Workflow"]` from project settings if I agreed to the subagent rule.
- A smaller compact window means more compactions. That is the reason for the "Compact instructions" section in step 6 and for keeping long skills short at the top.

If I chose the Concise output style, copy `kit/output-styles/Concise.md` to `~/.claude/output-styles/`.

## Step 5. Install the kit in `~/.claude`

Copy these files. If a file of the same name exists, show me the difference and merge; do not overwrite my own rules.

| From the kit folder | To | Note |
|---|---|---|
| `kit/global-CLAUDE.md` | `~/.claude/CLAUDE.md` | Add its four sections to mine. |
| `kit/agents/scout.md`, `builder.md`, `reviewer.md`, `tester.md` | `~/.claude/agents/` | They use the model aliases `sonnet` and `opus`. If my plan lacks one, set the nearest model I have. `scout` and `reviewer` are read-only by instruction, not by tool: they keep Bash for `git diff` and searches. |
| `kit/skills/graph/SKILL.md` | `~/.claude/skills/graph/SKILL.md` | It sets `disable-model-invocation: true`, so it costs nothing until I start it with `/graph`. |
| `kit/skills/architecture/` (the whole folder) | `~/.claude/skills/architecture/` | Also started only by me, with `/architecture`. Step 6 uses it. |
| `kit/commands/review.md` | `~/.claude/commands/review.md` | One command for every code review. Its third step uses an over-engineering skill if I have one, otherwise the built-in `/simplify`. Some versions use `/review` as another name for the built-in `/code-review`. After installing, type `/review`; if the built-in one answers, save this file as `full-review.md` and use that name in the rules. |

## Step 6. Each project

For every project I work in:

**Rules in CLAUDE.md.** Where a project has a rule of this kind, replace it. Where it has none, the global file already covers it; add nothing.

- In place of a subagent ban: **Subagents under control.** Work inline by default. One subagent is fine for a check by someone who did not write the code (`reviewer`), a device or browser hand test (`tester`) or a wide read-only search (`scout`). A task split across several subagents runs as `/graph`, started by the owner. A workflow runs only when the owner asks for one in their own words.
- In place of a review rule: **One review per diff, run as `/review`.** `/code-review` first, then these sides read in full: the project's own list, such as correctness and edge cases, concurrency and lifecycle, data loss, security and privacy, error handling and what the user sees, localization, design system, accessibility, performance, tests. Then one over-engineering pass on the same diff, applying its cuts. Findings by severity with `file:line`, each reported once.
- In place of "don't be lazy": **Deliver every requested part.** Each part of a request is built in full, or named as not done with the reason. Never drop a part because it looks derivable, covered elsewhere, risky or out of scope: explain the concern and ask. Write tests for what you build.

**Sections to add where they fit:**

```markdown
## Graph runs (`/graph`)
- Lanes: <which folder or repository each builder works in>. <How many builds may run at once.>
- Run folder: <where GRAPH.md, contracts and reports go; keep it out of git>.
- Device or browser tests go to one `tester` at a time.

## Compact instructions
When compacting, keep: the task or ticket and the current step, the paths of any log or `GRAPH.md` in use, the files changed so far, the last failing test output, and the open questions for the owner. After a compaction, read that log again, and the skill in use from the step you are on, before continuing.
```

**Architecture.** The kit carries no architecture of its own. Do this for the project this session is open in, and only with my go, because it is a long read: read `~/.claude/skills/architecture/SKILL.md` and follow it. For every other project, tell me to open a fresh session there and run `/architecture`; do not do several projects in one conversation. In an existing project you learn the architecture that is already there from the code, write it down as `.claude/rules/architecture.md`, set up the checks that keep new code inside it, and show me where the code leaves it today; you change nothing in the code without a second go. In a new or empty project you offer me two or three options that fit the product and the platform's current guidance, with a recommendation, and write the contract after I choose. If a project's CLAUDE.md describes its architecture at length, that text moves into the contract file. `templates/rules/architecture.md` is the outline.

**Working rules.** `RULES.md` in the kit folder lists the working rules of the original project, each with its reason. Compare them with this project's CLAUDE.md and tell me which ones I lack that would fit my work. Add only the ones I pick, in one line each. `templates/rules/` has templates for design system, localization and platform parity; offer one only where the project has that concern and no rule file for it.

**Check the file against the disk.** Every path, make target and script a CLAUDE.md names must exist. Add the real commands for running the tests, one test, and the linters. Keep the file short: what cannot be read from the code, decisions, gotchas, and what I had to correct twice. Move long how-to material into path-scoped files under `.claude/rules/` or into a skill.

**Project permission rules.** Add the deny rules from `templates/settings/project-settings.json` to the project's `.claude/settings.json`, plus any command the project must never run. They are:

```json
{
  "permissions": {
    "deny": [
      "Bash(git push --force:*)",
      "Bash(git push -f:*)",
      "Bash(git reset --hard:*)",
      "Bash(git clean:*)",
      "Bash(git stash drop:*)",
      "Bash(git stash clear:*)"
    ]
  }
}
```

**Project skills, commands and agents.** Remove the project's own review agents and the commands that only call them; carry their checklist into the review rule's list of sides. Update any skill that repeats an old rule. Fix pointers to files that no longer exist.

**Memory.** Rewrite a "no subagents" note to the new rule, keeping its history as the reason for the control. Trim the index as the table in step 2 says. Add one reference note that says where the kit lives, what was removed, where the backup is, and the traps from "What the original rebuild measured".

**Rewrite the instructions with the CLAUDE.md skills.** If I agreed to it in the plan and it is missing, install the plugin: `claude plugin install claude-md-management@claude-plugins-official`. Then, in each project:

1. Run `/claude-md-management:claude-md-improver`. It finds every CLAUDE.md, scores each one on commands, architecture clarity, gotchas, conciseness, currency and actionability, and proposes targeted fixes. Show me its report, and apply the fixes I accept.
2. Run `/claude-md-management:revise-claude-md` at the end of this job. It turns what this session learned about the project into one-line additions.

`templates/project-CLAUDE.md` is a model of the result: commands, numbered hard rules, pointers to path-scoped rule files, where things are, graph lanes, compact instructions, gotchas. The files in `templates/rules/` show rule files that load only for matching paths. Move long material out of CLAUDE.md into files of that kind.

**Workflow skills.** `templates/skills/` holds three procedure skills generalized from the original setup: `ship-ticket`, `ship-design` and `release-notes`. Do not install them as they are. For each procedure I repeat, ask me how I do it today, fill the template's placeholders from this project (tracker, branches, test and build commands, platforms, evidence folder), remove the phases that do not apply, and save the result as `.claude/skills/<name>/` in the project. If I already have a skill for that procedure, compare it with the template and tell me what mine is missing: a log that survives a compaction, a gate with its proof for each phase, "claim only what you ran", stop conditions, lessons kept in a reference file.

## Step 7. Verify

- Every edited JSON file parses.
- `claude plugin list` and the contents of `~/.claude/skills` and `~/.claude/agents` match the plan.
- Take the two cold-prompt samples and the `/context` table again, and compare with step 1. If "MCP tools" or "System tools" has jumped by tens of thousands and the "(deferred)" rows are gone, tool search is off: look for `ENABLE_TOOL_SEARCH`.
- Ask a fresh headless session whether its context still holds anything from a plugin I removed: a forced skill check before every reply, a talking style injected by a hook, or a persona. The answer must be no. The kit's own writing rule and the Concise style are expected.
- Run one real agent in a project: `claude -p "Spawn exactly one subagent of type scout with this contract. Goal: report the path and line in CLAUDE.md that names how to run the tests. Read first: CLAUDE.md. Files it may change: none. Reply: 3 lines at most. Print its reply." --model haiku --allowedTools "Agent Read Grep Glob" --output-format json`. The result's `modelUsage` must show the scout's own model.
- If a secret was moved, the server that needs it starts.
- `git diff --cached --name-only` is empty in every repository you touched.

## Step 8. Compare my setup with the original

`README.md` in this folder describes the daily flow of the original setup, and `SKILLS.md` lists what it kept, by role, with how often each was used. After the cleanup:

- For each role in `SKILLS.md` that matches the work I do, tell me which of my own skills fills it, and which roles I have nothing for. Do not install third-party skills for me; name them and let me choose.
- If I have plugins that act through hooks on every session, show me their always-on cost and what their hooks inject, and let me decide.
- Tell me which of my repeated procedures has no skill yet.

## Step 9. Report to me

In plain sentences, short:

1. Before and after: the cold-prompt numbers and the `/context` rows. Say plainly if the change is small.
2. What was removed, kept and added, as a table.
3. What you left alone and why.
4. What a permission check refused, with the exact line for me to change by hand.
5. Uncommitted changes per repository, with a path list saved in the backup folder, so that I can commit them apart from other work.
6. What I must do myself, such as rotating a key or restarting open sessions.
7. The comparison from step 8, as a short list.
8. The backup path and how to restore.

## How I work with this setup afterwards

- A code review, in any wording, is `/review`, once per diff.
- A large task with separable parts is a `/graph` run that I start: a run file first, the advisor on the plan, each node with the eight-line contract, a gate after every node, the review once at the end.
- One helper is fine without a graph: a `reviewer` for a second opinion, a `tester` for a device, a `scout` for a wide search.
- The advisor is called on the plan, on a second failed attempt, and before saying done. Not on routine steps.
- I clear the conversation between unrelated tasks, and compact with a focus at a part boundary.
- After a long run I read `/usage` to see what the agents cost, and `/context` after any change to the setup.
