---
name: ship-design
description: "Turn a design from <DESIGN-SOURCE> into shipped, working code on every platform in <PLATFORMS>: a new screen, a redesign or a feature. Use for \"implement this design\", \"make it match the design\", a design link or frame ids, even a small visual tweak. Delivers the finished feature, not a plan."
argument-hint: "<design link or frame ids>"
---

# Ship a design

In: the frames of one design. Out: the finished feature on every platform, matching the design, on real data, reviewed and seen running. A design shows one moment; most defects come from guessing what it cannot show: the data, what writes it, other states, languages and platforms.

## Fill these in first

- `<DESIGN-SOURCE>`: the design tool or file, and how this session reads its values.
- `<DESIGN-TOKENS>`: where the design-system tokens and shared components live, per platform.
- `<PLATFORMS>`: the apps that ship together.
- `<LANGUAGES>`: the languages the product ships in, and its string files.
- `<BUILD-COMMAND>`: the debug build per platform.
- `<TEST-COMMAND>`: the tests per platform.
- `<EVIDENCE-FOLDER>`: where screenshots and comparisons go.

## Phases, in this order

1. Anchor the source
2. Read the code that exists
3. Get current
4. Extract the design
5. Diff and decide
6. Assets and strings
7. One plan, then wait for a go
8. Build completely
9. Wire what the design does not show
10. Review
11. Verify against the design

## Rules

1. Ship the whole thing: no stub, sample data, TODO or quietly dropped part. Raise a worry and ask; never skip.
2. The design source is the only authority for visuals: read every color, size, spacing, radius, duration and string from it, never from a screenshot or a guess.
3. Build no screen, state or control the design does not contain; ask about the gap.
4. One plan covers every platform; a session that builds one leaves a written handoff.
5. Edit nothing before the plan has a go; after it, build all of it without asking again.
6. Work inline: device tests go to the `tester` agent, a large change also gets a `reviewer` check, and only the owner starts a `/graph` run.

Done means: it matches the design and was seen running on each platform built, every state ships on real data, every path that touches the data has a decision, strings exist in all `<LANGUAGES>`, tests pass and review findings are fixed.

## 1. Anchor the source

Do: resolve each link or frame id to its name. Decide new or rewrite; a rewrite changes the shipped screen, view model, tests and strings, never adds a sibling. Name the platforms this session builds.
Proof: the frame list, confirmed by the user.
Why: a wrong frame or a silent sibling screen wastes everything after it.

## 2. Read the code that exists

Do: before the design, read the screens and components that already render this shape, the view model and data layer behind them, the money, date and formatting helpers they call, the states they handle, and whatever else reads or writes this data.
Proof: a written current contract.
Why: phase 5 diffs the design against it, and helpers are shared on purpose.

## 3. Get current

Do: read platform and library versions from the dependency manifests, not memory, and fetch current documentation for any non-trivial API. Take platform guidance for behaviour (touch targets, gestures, text scaling, screen readers), never for looks. Look for deprecated APIs in the area.
Proof: the APIs and versions you build against.
Why: an API written from memory is how deprecated code ships.

## 4. Extract the design

Do: read the node tree with variables and components resolved. Per frame, record layout, gap, padding, sizing, fills per theme, strokes, radii, shadows, font family, size, weight and line height, text, icons and motion. Read the design's spec notes first; use a screenshot only to check your reading.
Proof: a value table per frame.
Why: a screenshot cannot tell 12 from 13.

## 5. Diff and decide

Do: set phase 2 beside phase 4 and decide every difference.

| Difference | Decision |
|---|---|
| Matches a component | Reuse it |
| A variant of one | Extend it; never a second component with the same job |
| A value with no token | Add the token in `<DESIGN-TOKENS>` first |
| A value derived differently | Change the helper, so every caller moves |
| Nothing behind it in code | New work, in the plan |

When the product has plans or limits, decide gating even if the design shows no lock, and enforce it at the action, not only on screen.
Proof: the decision table.
Why: near-copies and inline formatting are where drift starts.

## 6. Assets and strings

Do: export every icon and illustration from the design source, never redrawn or swapped for a system icon, into every platform under matching names. Write every visible string in all `<LANGUAGES>`, each for its reader rather than word for word, with the same placeholders.
Proof: assets and string keys present on every platform.
Why: then nobody improvises an icon or a hardcoded string mid-build.

## 7. One plan, then wait for a go

Do: one plan for every platform: files in dependency order (tokens, components, screen, view model, data, wiring, tests); reused, extended or new; helper changes; APIs and versions; gating; the phase 9 rows; tests; what lands now and what is handed off. Show it and stop. Say a concern in one sentence; scaling down is the user's call.
Proof: the user's go.
Why: a plan for every platform makes a deferred half a handoff, not a hole.

## 8. Build completely

Do: tokens, then components, then screens, then wiring, one vertical slice at a time. Every visual value is a `<DESIGN-TOKENS>` token, every component reused or extended, every number from real data. Port a finished platform value for value: same order, motion, asset and string names. Write tests as you go; build often with `<BUILD-COMMAND>`.
Proof: green builds and the tests.
Why: one slice that saves real data beats five stubs.

## 9. Wire what the design does not show

Do: decide each row, even if "unchanged": every path that creates or edits this data (manual, import, automation, sync); storage, sync and backup with the same field names on every platform; the refresh signal other screens hear; active filters and scope; widgets, shortcuts, notifications, deep links, export; gating at the action; analytics in the existing naming, with no personal data.
Proof: a wiring table, a decision per row.
Why: this is where "it looks right but does not work" is caught.

## 10. Review

Do: run `/review` on the diff, once per diff: a diff that was reviewed and has not changed is not reviewed again. Check correctness (boundaries, signs, rounding, money types, time zones, missing values), concurrency, completeness, architecture, tokens and parity, strings, gating, and that replaced code is deleted. For a large change, give the `reviewer` agent the diff, value tables and plan. Fix every finding.
Proof: findings and fixes, written down.
Why: reading your diff as a suspect's catches most of what a device catches slowly.

## 11. Verify against the design

Do: build, run `<TEST-COMMAND>`, install on a device per platform, drive the real flow to the designed state, save something. Compare a screenshot beside the frame: copy, order, spacing, type, color in both themes, radius, shadow, icons, motion; fix and reshoot until they match. Give the `tester` agent the states: light, dark, right-to-left, empty, loading, error, offline, locked, long strings, large text.
Proof: side-by-side screenshots per state in `<EVIDENCE-FOLDER>`.
Why: "it compiles" is not done; seen running and matching is.

## Handoff when one platform is built

Write a handoff file in the repository: frames, files shipped (the port's source), phase 5 decisions, the wiring table, which strings and assets landed where, what is verified, open design questions. Name screens and rows; "port the rest" is not a handoff. Then report what was built, verified, not verified and left out, and why.
