# Settings

Merge these into your own files. Do not replace a file with them.

## `global-settings.json` goes into `~/.claude/settings.json`

| Key | Value | Why |
|---|---|---|
| `model`, `advisorModel` | Your choice | A strong main model with a stronger one as advisor costs less than the strongest model on every turn. The advisor must rank at or above the main model. |
| `effortLevel` | `high` | `xhigh` on every model was one of the measured costs. The models' own default is `medium`. A level saved per model under `modelSettings` wins over this key, so set those too. |
| `autoCompactWindow` | `300000` | Without it a 1M-context model compacts near 967k, and every turn of a long session re-reads up to that much. The minimum is 100000. |
| `workflowSizeGuideline` | `small` | A workflow aims for fewer than 5 agents unless you ask for more. |
| `skillListingBudgetFraction` | `0.005` | Halves the skill listing. Set it only if you still have many skills; the least-used lose their descriptions first. |
| `outputStyle` | `Concise` | Optional. The style file is in `kit/output-styles/`. |
| `env.CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` | `3` | Caps how many subagents run at once. The default is 20. |
| `permissions.ask` | `Workflow` | Claude Code asks you before any workflow starts. |

Leave these out:

- `ENABLE_TOOL_SEARCH`. Set to `auto`, it stops deferring tools once few MCP servers are connected, and loads every tool definition up front.
- `CLAUDE_CODE_SUBAGENT_MODEL`. It would also lower the model of `/code-review`'s reviewers. The kit's agents name their own model.

## `project-settings.json` goes into a project's `.claude/settings.json`

Deny rules for git commands that destroy uncommitted work. Add any command your project must never run. A deny rule is enforced by Claude Code itself, so use it for the few rules that can never bend. Note that a rule written as `Bash(git reset --hard:*)` does not match `git -C <path> reset --hard`.
