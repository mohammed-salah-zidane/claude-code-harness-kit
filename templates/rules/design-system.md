---
paths:
  - "<your UI source folder>/**"
---

# Design system

This file loads only when Claude reads or edits a file that matches the paths above.

Replace each placeholder in angle brackets with your project's value: `<TOKENS-FOLDER>` holds the tokens, and `<DESIGN-SOURCE>` is the design file or board the product follows.

## Rules

- Every colour, font, spacing, radius, shadow, animation and loading state comes from a token in `<TOKENS-FOLDER>`, so one change there reaches every screen. Raw values and the platform's default styles appear only inside that folder.
- `<DESIGN-SOURCE>` is the visual truth. When the code and the design disagree, change the code to match the design, because two truths split the product into two looks.
- Never invent a value, a component or a state that `<DESIGN-SOURCE>` does not contain. Ask instead, because a guess that looks close spreads to every screen that copies it.
- Add a new value to `<TOKENS-FOLDER>` first and use it in a screen after that, so the tokens stay the full list of what the product uses.
- Build every screen and component for light and dark, and check both, because a screen tested in one theme tends to break in the other.
- Keep one component per need. Search the shared components before adding one, and extend the existing one with a variant, because two components for one need drift apart. Secondary surfaces such as widgets or extensions use the same tokens, not a parallel set, because a second set soon disagrees with the first.
- Show a skeleton while data loads and a spinner, inside the control that started it, while an action runs. Never swap them, because people read a skeleton as "content is coming" and a spinner as "your request is running".
- Text scales with the reader's text-size setting, contrast passes in both themes, every control carries a label for screen readers, colour never carries meaning alone, and a reduced-motion setting swaps movement for a short fade token, because people who change these settings rely on them.

## Tokens

| Need | Use | Never |
|---|---|---|
| Colour | `<colour token>` | A raw colour value or a named system colour |
| Screen background | `<background token>` | A background drawn by hand |
| Text style | `<type token>` | The platform's built-in text styles |
| One-off text size | `<font token call with size and weight>` | A font named by its file or a system font |
| Spacing and size | `<spacing token>` | A raw number |
| Radius | `<radius token for that element type>` | A radius literal, or one that differs from the design |
| Shadow | `<shadow token>` | An inline shadow |
| Motion | `<motion token>` | An inline duration or curve |
| Data loading | `<skeleton component>` | A spinner as a placeholder |
| Action loading | `<spinner component>` | A skeleton for an action in flight |
| Primary action | `<primary button component>` | A button built by hand |

## Check before you finish

Run each audit command over the files you changed. Each one prints nothing, so a clean run proves the change used only tokens; treat every hit outside `<TOKENS-FOLDER>` as a bug to fix, not a finding to report.

```
<search for raw colour values, excluding the tokens folder>
<search for built-in text styles and fonts named directly>
<search for raw spacing, size and radius numbers>
<search for inline shadows, animation curves and durations>
<search for a spinner used as a data placeholder>
```

Then capture every changed screen in light and dark, and compare each one side by side with `<DESIGN-SOURCE>`.
