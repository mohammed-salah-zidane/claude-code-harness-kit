---
name: architecture
description: Choose the architecture for a new project, or learn the one an existing project already has, write it down as a contract, and set up the checks that keep all later work inside it. Started by the user with /architecture.
argument-hint: "[new | existing] [area to focus on]"
disable-model-invocation: true
---

# Architecture contract

Request: $ARGUMENTS

The aim is that every later session builds inside one known architecture, and that code which leaves it is caught by a check and not by luck. This skill does not carry an architecture of its own. A new project gets the one that fits its product and its stack. An existing project keeps its own: you learn it from the code, write it down, and improve it only where the owner agrees.

## 1. Pick the mode

- **Existing:** the repository has real features. Learn what is there.
- **New:** the repository is empty or holds only a starter. Choose.
- **Mixed:** a rewrite is under way and two patterns live side by side. Learn both, then ask the owner which one is the target.

## 2A. Existing project: learn it before judging it

Give every finding its source as `path:line`.

1. **Map the parts.** Entry points, modules or packages and what each depends on (read the build files), and the folder conventions.
2. **Trace real features.** Take four: a simple one, the most complex one, the newest and the oldest. Follow one user action through each, from the screen to storage or the network and back. Note the type that crosses each boundary.
3. **Name the patterns in use:** layers and which direction dependencies run; where state lives and how the screen learns of a change; how dependencies are provided; navigation; data access, caching and sync; errors and what the user sees; concurrency and lifecycle; naming and file layout; how tests are built and what they replace with a fake.
4. **Count.** For each pattern, how many features follow it and which do not. The newest code usually shows the intended direction. When two patterns each cover a large share, ask; do not pick.
5. **Write two short lists:** what the code does today, and what it seems to intend.

A wide read can go to one `scout` agent with an output file, so that it does not fill your context.

## 2B. New project: choose with the owner

1. **Collect the constraints.** What the product does and what it must survive (working offline, live updates, money, private data). The platforms. Who maintains it and for how long. What the owner already knows well.
2. **Check today's guidance.** Read the platform's current recommended architecture and the current versions of the libraries you would use. Do not rely on memory for this; it changes.
3. **Offer two or three options that fit.** For each: its shape (layers, state, how dependencies are provided, navigation, data), what it costs in code and learning, what it protects against, and where it starts to hurt. Recommend one and say why for this product.
4. **Prefer** the platform's mainstream current approach, and the simplest structure that keeps the business rules testable without a screen or a network. Add a layer only for a need you can name.
5. Wait for the owner's choice.

## 3. Write the contract

Write `.claude/rules/architecture.md` with a `paths:` list that covers the source files, so that it loads whenever code is touched and costs nothing otherwise. Use `references/outline.md` in this skill's folder as the outline.

- State each rule so that it can be checked: "the domain module imports nothing from the interface or the data modules", not "keep layers clean". Give each one a short reason.
- Point at real files as the examples to copy ("the reference feature is `<path>`"). Do not paste code that will go stale.
- Include a checklist for adding a feature, and the naming and file layout.
- For an existing project, add a section "Known deviations". Each entry is marked: fix now, fix when the file is next touched, or accepted exception. The owner decides the mark.
- Keep the file near 150 lines. A longer one is skimmed.

Then add one line to the project's CLAUDE.md that points at the file, and remove any description of the architecture from CLAUDE.md itself.

## 4. Make it strict

Prose asks. A check enforces. Set up as many of these as the project supports, strongest first:

1. **The build.** Where the stack can enforce a boundary (separate modules, a dependency rule in the build system, a linter rule, an architecture test), propose that. A boundary the compiler enforces cannot be forgotten.
2. **Audit commands** in the contract: searches that print nothing when the code conforms, such as a forbidden import per layer. Run them now and record how many violations exist today, so that later work is judged on what it adds.
3. **A guard script or the CI,** if the project has one: add the audit commands to it.
4. **The review.** Add "architecture: the audit commands print nothing new" to the review sides in CLAUDE.md.
5. **A hook at edit time,** for the few mechanical patterns worth blocking outright. Offer it; do not install it without a go. Only patterns with almost no false alarms belong there, because a noisy hook gets switched off.

## 5. Improve an existing project, only with a go

Present the deviations ranked by risk and by cost. A small mechanical one can be fixed now, with the tests green before and after. A large one becomes a planned piece of work of its own. Never fold a refactor into unrelated work, and never change what the product does while moving code.

## 6. Report

In plain sentences: the architecture in ten lines; the file written; the checks added, with today's violation counts; the deviations and what you propose for each; the decisions that are still the owner's.

When a later decision changes the architecture, the contract changes in the same piece of work.
