---
paths:
  - "<your first platform's source folder>/**"
  - "<your second platform's source folder>/**"
---

# Platform parity

This file loads only when Claude reads or edits a file that matches the paths above.

Replace each placeholder in angle brackets with your project's value: `<PLATFORM-A>` and `<PLATFORM-B>` are the two platforms of one product.

## Two platforms, one product

A person sees the same screens, in the same order, with the same behaviour on either platform, because people switch devices and both platforms read one account. Neither side is a copy of the other. A feature is done when both sides do the same thing, and a review is done when it has checked both.

## Which side is the contract

Neither platform is the source of truth by default. Decide per behaviour, because the side that got there first is not always the side that got it right.

1. When only one side has the behaviour, that side is the contract. Read it in full before writing the second one.
2. When both sides have it and agree, land every change on both, so they keep agreeing.
3. When both sides have it and disagree, one of them is wrong. Decide which, say so, and fix that side. Never copy a bug so the two match.
4. When neither side has it, design it once, set its shared values once, then build both.

When you cannot find the matching code, ask, because an invented version becomes a third behaviour.

## Shared values

Each shared value has exactly one definition per platform, and the two definitions match, because both platforms read the same data and report into the same funnel:

- copy in every one of `<LANGUAGES>`, with placeholder syntax converted to each platform's form;
- backend paths, collection names and field names;
- analytics event names and property keys;
- persisted ids, such as record ids, stored enum values and composite keys;
- numeric policy, such as thresholds, limits, debounce times and retention windows;
- remote configuration keys and their accepted values.

A change to any of these is a change to both platforms. Colours, spacing, motion, gesture thresholds and layout order come from the other side or from `<DESIGN-SOURCE>`, never from feel, because two guesses never land on the same value. Copy binary assets such as icons, logos, animations and fonts as they are; never redraw them, because a redrawn asset drifts.

## Working on one side

Before touching either platform, read the matching implementation on the other, because the contract may live there. Keep a map of where each concern lives, so the matching code is one look away:

| Concern | `<PLATFORM-A>` | `<PLATFORM-B>` |
|---|---|---|
| <concern> | <path> | <path> |

A change lands on both platforms in the same pass. When it cannot, hand the other side off in writing: what changes, the shared values involved, which side is the contract, and the test that proves it, because a change that ships on one side alone is a defect even when it compiles.

## Reviewing for parity

Check each side on its own logic first, then against the other, and sort every finding into one bucket, so nothing hides:

1. Correctness: the code is wrong on its own terms. When both sides share a bug, name it as a bug on both platforms and fix both.
2. Divergence: the two sides disagree. Give each one a verdict: fix `<PLATFORM-A>`, fix `<PLATFORM-B>`, or keep both with the reason stated, such as a platform convention or an operating-system limit. A divergence with no verdict is a finding.
3. Gaps: one side has it and the other lacks it. Say which side, and whether the gap is planned or forgotten.

The same number formatted on two platforms can differ in small ways, such as trailing zeros, rounding, grouping separators or symbol placement. Compare the outputs for the same inputs and locale, not the code, because two correct-looking formatters can still print different text.

## Check before you finish

- Build both platforms and run both test suites; a build that compiles is not parity.
- List each shared value on both sides and compare the two lists: analytics names, string keys per language, backend field names and persisted ids. Every line on one side only is a finding.
- Feed the same inputs to both platforms and compare formatted numbers, dates and amounts side by side.
- Capture every changed screen on both platforms, in light and dark, and compare them side by side.
