# The working rules

These are the rules one product has run on, with the stack and the architecture taken out. Each one was added after something went wrong without it. Take the ones that fit your work, put them in your own words in your project's CLAUDE.md, and leave the rest.

There is no architecture here on purpose. `/architecture` (in `kit/skills/architecture/`) chooses one for a new project or learns the one your project already has, writes it down, and sets up the checks that keep work inside it.

## How work is done

| Rule | Why |
|---|---|
| Propose before implementing anything that was not explicitly approved. Wait for a go. | A wrong direction is cheapest to stop before the first edit. |
| Deliver every requested part, or name it as not done with the reason. Never drop a part because it looks derivable, covered elsewhere, risky or out of scope: explain the concern and ask. | The person who asked decides the scope. A silently dropped part is found late. |
| Check a ticket's premise before working on it: can a real person reach it, does something already prevent it, does the ask fit the product. A ticket with no user path is rejected with the traced proof, and costs no code. | Tickets written from reading code are often wrong about the running app. |
| For a bug a customer reported: prove the cause, look at how comparable products behave, and judge by what users expect. | The reported symptom is rarely the cause. |
| Claim only what you ran in this session and read the result of. Otherwise write "not run" and why. | A summary that sounds finished is not evidence. |
| A change a person can see is hand tested on every platform it touches before it is merged or called done. | Unit tests do not show a clipped label or a dead button. |
| A review comment ends in a code change or in the owner's decision. It is not answered and left. | A reply leaves the code as it was, so the problem the reviewer found is still there. |
| Fix what you find. A real bug, a red test, a stale comment or dead code met on the way is fixed in the same pass, with the same checks as the requested work. Anything that cannot be fixed safely is named out loud. | "Not in this diff" leaves things broken for the next person. |
| One review per diff: a bug review in a fresh context, then the project's own sides, then one pass that only looks for code to delete. Never a skim. | Two overlapping reviews cost twice and report the same finding twice. |
| Write the tests with the code and run them once, at the end of the task. A fix made after the review gets the one check that proves it: its scenario on a device, its tests, or a code review of that change when it touches sync, money, data loss, concurrency or security. | Re-running the whole suite or the whole review after every small change is where long tickets lose their days. |
| In a long session, keep a handoff file current: what is done, what is next, what is decided. | It is what a new session, or this one after a compaction, continues from. |
| No commits during work unless asked. A commit holds only this session's files, never another session's. No destructive git. | Uncommitted work is often the only copy, and several sessions may share one tree. |
| Work inline by default. Subagents only under a contract, with the result checked before building on it. | A helper costs tokens and starts with no context. |

## Code

| Rule | Why |
|---|---|
| One architecture, written down and checked. New code follows the contract, not the nearest example. | The nearest example is sometimes the old pattern. |
| Search before adding. If a helper, a component or a type already exists, use or extend it. One component per file. | Re-implementing what sits a few files away is the most common waste. |
| One module owns each external service: its address, wire format, authentication, timeouts and error translation. Everything else hands it typed requests and gets typed results. Every caller is tested against a fake of it; the module itself is tested on the wire. | A change in the service then touches one place, and nothing else can drift. |
| Money is never held in a floating-point type. | Rounding errors in money are bugs users see. |
| The system's own error text never appears on a screen. Log it, and show the product's own sentence. | Raw error text is unreadable, untranslated, and sometimes private. |
| A feature that stores data is covered by sync, backup and export from its first version, where the product has those. | Adding it later means some users have already lost data. |
| No comments that restate the code or narrate the change. No compatibility shims and no "deprecated" markers in code you own: move the callers and delete. | Dead paths are read, maintained and broken for nothing. |
| New measurement never costs the user speed, and every important journey stays traceable. | Instrumentation that slows the first screen costs more than it tells. |
| The live product stays stable. No change in what it does for existing users without a go. Never take something away from a paying user. | Users who lose something they relied on are slow to trust the product again. |
| Use the current stable version of a dependency, and check its present documentation before using an interface from memory. | Interfaces change between versions, and what a model remembers of them is often out of date. |

## Interface and words

| Rule | Why |
|---|---|
| Every colour, font, spacing, radius, shadow, animation and loading state is a design-system token. | One raw value is the start of a second visual language. |
| The design source is the visual truth. The code changes to match it. | Otherwise the two drift and nobody knows which is right. |
| Never invent a screen, a state, a control, copy, a colour, an asset or a threshold. If the design lacks it, ask. | Invented interface is the most repeated failure, and the hardest to notice. |
| Never add a field whose value is unknown or not needed. | Every field is a question the user has to answer. |
| Light and dark, always. Accessibility basics, always. | They are cheap at build time and expensive afterwards. |
| A skeleton for data that is loading. A spinner for an action in progress. | The two tell the user different things. |
| "Improve" means redesign what is there, not add another card. | Additions pile up; the screen gets worse. |
| A design exploration is one concept, built from the product's own behaviour, playable, with real layout and assets, and checked before it is shown. | A board full of text cannot be judged. |
| No hardcoded user-visible string. Every new string exists in every supported language before the work counts as done. | A missing language is found by a user, not by a test. |
| Copy is transcreated, not translated: written fresh for each language's reader, in the register chosen for that language. | Word-for-word copy reads as foreign. |
| Copy should not read as machine-written, and it claims only what the user's own data supports. | People stop reading text that sounds generated, and stop trusting text that guesses. |
| Release notes say only what a person would notice, or the business depends on. | Nobody wants the plumbing. |

## More than one platform

| Rule | Why |
|---|---|
| The platforms are built in step, not one after the other. One plan covers both. | A port done later is done from memory. |
| Neither platform is the source of truth by default. Whichever side already has the behaviour is the contract. Where both have it and disagree, one is wrong: decide which, and fix that side. | "Follow the other platform" copies its bugs. |
| Copy, backend field names, analytics names, stored identifiers and numeric policy are shared values with exactly one definition per platform, and they match. | A renamed field on one side breaks sync silently. |
| Read the matching implementation on the other side before touching either. | The same feature often hides a decision made once. |

## Secrets, accounts and environments

| Rule | Why |
|---|---|
| No secret in a project file. Keys live in the system keychain or in an environment variable set outside the repository. | A file gets read, printed, copied and committed. |
| Test credentials live in one ignored file and are loaded inside the command that uses them. They are never printed, and never copied into code, tests, notes or a service other than the product's own sign-in. | A password that appears once in a log is no longer a secret. |
| Never change a test account's password or delete it. Create a throwaway account for a destructive test. | The next test run depends on that account. |
| A development build talks to a development backend. It fails on purpose when that backend is not configured. | The alternative is test data in production. |
| Never clean up a device, an emulator or its data after a test unless asked. | The state left behind is often the evidence. |

## Where each rule should live

| Kind of rule | Put it in | Because |
|---|---|---|
| Applies to every task in the project, and you have corrected it more than once | `CLAUDE.md`, one line, numbered | It loads in every session, so it must be short. |
| Applies to one area of the code | A file in `.claude/rules/` with a `paths:` list | It loads only when that area is touched. |
| A procedure with steps | A skill | It loads only when it is used. |
| Can never bend | A hook, a permission deny rule, a linter rule or the build | Claude Code or the compiler enforces it, whatever the model decides. |
| A correction or a decision with a story behind it | A memory note with "why" and "how to apply" | The reason is what lets the next session judge an edge case. |

A rule that keeps being missed is in the wrong place. Either the file it sits in has grown too long, or it belongs one row further down this table.
