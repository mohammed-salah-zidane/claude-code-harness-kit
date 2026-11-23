# Skills, plugins and MCP servers in the original setup

This is what one developer kept after the cleanup, with how often each was run over seven weeks of logs. It is a record of what earned its place for one kind of work (a mobile app on iOS and Android, with its marketing, store listing and videos). It is not a list to install. Run `scripts/usage-count.py` on your own logs and let those numbers decide.

"Runs" counts the times the model invoked a skill plus the times it was typed as a command.

Third-party skills are not included in this kit. Where the source was recorded, it is given as a skills.sh reference (`owner/repository/skill`). Where it was not, search for the name.

## Written for this setup (included in the kit)

| Skill or command | What it does | Runs |
|---|---|---|
| `/review` (`kit/commands/review.md`) | One review per diff: `/code-review`, the project's own sides, one over-engineering pass | new |
| `/graph` (`kit/skills/graph/`) | A large task as a small graph of subagents with contracts, gates and budgets | new |
| `/architecture` (`kit/skills/architecture/`) | Chooses or learns a project's architecture, writes the contract, sets up the checks | new |
| `scout`, `builder`, `reviewer`, `tester` (`kit/agents/`) | The four node types | new |
| Ship a ticket (`templates/skills/ship-ticket/`) | One ticket in, one proven pull request out, in eleven phases | about 65 |
| Ship a design (`templates/skills/ship-design/`) | A design becomes shipped code on every platform | 14 |
| Release notes (`templates/skills/release-notes/`) | Release copy through a business filter, per locale | 11 |

The three templates are generalized from private skills. Adapt them to your project before use.

## Review

| Skill | What it does | Source | Runs |
|---|---|---|---|
| `/code-review` | Bug review in a fresh context | Built into Claude Code | 70 |
| `ponytail-review` | Looks only for code to delete or simplify | One file from the ponytail plugin by Dietrich Gebert (MIT) | about 100 |
| `/simplify` | Built-in alternative for the over-engineering pass | Built into Claude Code | – |

## Platform work

| Skill | What it does | Source | Runs |
|---|---|---|---|
| `rocketsim` | Reads and drives an iOS simulator through the RocketSim command-line tool | not recorded | 30 |
| `ios-architect` | iOS architecture reference | not recorded | 1 |
| `ios-dead-code-cleanup` | Finds and removes dead Swift code | not recorded | 1 |
| `android-cli` | Drives the Android command-line tools | `android/skills/android-cli` | 1 |
| `android-dead-code-cleanup` | Finds and removes dead Kotlin code | not recorded | 1 |
| `r8-analyzer` | Reads R8 shrinker configuration and output | not recorded | 1 |
| `perfetto-trace-analysis` | Reads performance traces | not recorded | 2 |
| `localization` | Store and app localization | `appeeky/aso-skills/localization` | kept because other skills call it |

## Design

| Skill | What it does | Source | Runs |
|---|---|---|---|
| `ui-ux-pro-max` | Styles, palettes, type pairings and UX rules | not recorded | 67 |
| `frontend-design` | Design direction for new interfaces | Plugin in the official marketplace | 27 |
| `apple-design` | Reviews a design against Apple's guidelines | `emilkowalski/skills/apple-design` | 20 |
| `apple-hig-designer` | Native components following Apple's guidelines | `jamesrochabrun/skills/apple-hig-designer` | 7 |
| `onboard` | Onboarding flows and empty states | not recorded | 3 |
| `emil-design-eng` | Polish and animation decisions | not recorded | 2 |
| `make-interfaces-feel-better` | Small details that make an interface feel finished | not recorded | 2 |
| `audit`, `arrange`, `teach-impeccable` | Quality checks, layout, design context setup | not recorded | 1 each |
| `archify` | Architecture diagrams | not recorded (MIT) | 1 |

## Words, market and store

| Skill | What it does | Source | Runs |
|---|---|---|---|
| `copywriting` | Marketing copy for pages | not recorded | 25 |
| `market-research` | Market and competitor research with sources | not recorded | 14 |
| `content-strategy` | What to write about | not recorded | 6 |
| `app-store-optimization` | Store listing research and tracking | not recorded | 5 |
| `stop-slop` | Removes machine-sounding patterns from prose | `github.com/hardikpandya/stop-slop` (MIT) | 4 |
| `copy-editing` | Editing passes on existing copy | not recorded | 3 |
| `ads-apple` | Apple search ads | `agricidaniel/claude-ads/ads-apple` | 1 |

## Video

| Skill | What it does | Source | Runs |
|---|---|---|---|
| `hyperframes`, with `hyperframes-cli`, `hyperframes-media`, `hyperframes-registry` | Video compositions in HTML | not recorded | 2 |
| `remotion-best-practices`, `remotion-to-hyperframes` | Video in React, and porting it | not recorded | 2 each |
| `ai-video-generation` | Generated video | `101-skills/superpowers/ai-video-generation` | 2 |

## Plugins kept

`atlassian` (the issue tracker), `firebase`, `playwright` (browser checks), `swift-lsp` (code intelligence, which saves file reads), `frontend-design`, `claude-md-management` (audits and updates CLAUDE.md files), `cloudflare`. An analytics plugin is enabled only in the one project that uses it.

## MCP servers kept

In the project: a build-and-run server for the simulator, an app store server, an analytics server. For the user: GitHub, a design-file server, one documentation server. Account connectors that were not used for coding are switched off per project.

## Removed, and why

- **Three plugins that acted through hooks on every session:** superpowers (a skill check before every reply), caveman (a compressed talking style on every prompt) and ponytail's standing mode (a minimal-code persona in every session and subagent). All three do what they promise, and many people like them. In this setup their always-on text cost more than it gave, so they went; ponytail's review skill was kept as a single file.
- **Plugins that duplicated a built-in command or another plugin:** a review toolkit, a review plugin, a simplifier, a second copy of a cloud plugin, and copies of skills that also arrive through the account.
- **86 personal skills with no run in the logs:** twenty skills for delegating to other coding tools, skills for platforms not in use, an SEO set, most of a design family.
- **Old agents with "use proactively" descriptions.** The four kit agents replaced them.
- **MCP servers that failed to connect in every session,** and four that were global but used in one project or none.
- **A test tool no longer in use,** with its flows, scripts and shell profile lines.
- **About 500 one-off or risky permission rules.**
