---
paths:
  - "<your UI source folder>/**"
  - "**/<STRINGS-FILE>"
---

# Localization

This file loads only when Claude reads or edits a file that matches the paths above.

Replace each placeholder in angle brackets with your project's value: `<LANGUAGES>` is every language the product ships, and `<STRINGS-FILE>` is the file that holds a module's strings.

## Rules

- No user-visible string lives in code. Labels, titles, buttons, placeholders, errors, accessibility labels, notifications and text in exported documents all come from `<STRINGS-FILE>`, so every reader sees their own language. Machine-readable text, such as data keys, headers meant for other tools and log lines, stays in code.
- A new string exists in every one of `<LANGUAGES>` before the work counts as done, because a missing language shows its readers the raw key or the source language. When the strings format records a review state, set each entry to the finished state, because an unfinished entry can fall back to the source language.
- When unsure of a language, write the idiomatic line from a reliable source or ask. Never leave a note that a translation is missing, because the note ships and the gap stays.

## Adding a string

1. Search for an existing key with the same meaning, and reuse it when one exists.
2. Add the key to the module's `<STRINGS-FILE>`.
3. Write the source copy, then transcreate it into every one of `<LANGUAGES>`, following the register table below.
4. Keep placeholders and plural forms in step with the source, and escape the characters the format reserves.
5. Add direction marks where a right-to-left string needs them.
6. Replace the text in code with a lookup of the key.
7. Run the checks at the end of this file.

## Transcreated, not translated

Copy is transcreated, not translated: written fresh for each language's reader, keeping the intent rather than the source's word order, so it reads as if that language came first. Record each language's register once, so every string speaks in one voice.

| Language | Form of address | Tone | Notes |
|---|---|---|---|
| <language> | <formal or informal "you"> | <register> | <button verb form, quotation marks, percent spacing, brand name in that script> |

In a language with grammatical case, a name, month or date dropped into a sentence cannot take the ending the grammar wants. Build the sentence around it with a colon, a head noun in the right case, or parentheses, so the sentence stays correct for every value.

## Placeholders and plurals

Every language carries the same placeholders as the source, with the same types and count, because a missing or mistyped placeholder crashes the screen or prints the wrong value. A string with more than one placeholder uses positional placeholders, so each language can reorder them. Counts use the format's plural forms with every form the language needs, because a single "1 item / n items" rule fits only some languages.

## Right-to-left and numerals

A right-to-left string that starts with a left-to-right word or a placeholder takes its direction from that first character and lays out backwards. Start such a string with the right-to-left mark (U+200F), so it reads in the right order. For each language that has its own digit set, decide once which digits numbers use and apply that choice everywhere, so amounts read the same on every screen.

## Deleting unused strings

After a sweep that deletes strings it believes unused, run a full compile and compare every strings file with the last commit. Keys the code builds at runtime from a prefix and a value never appear in a search for the literal key, so a sweep deletes them by mistake. Restore every deletion the comparison cannot explain.

## Check before you finish

```
<command that lists keys missing a language, or not in the finished state>
<command that lists keys the code uses but no strings file defines>
<command that compares placeholder sets between the source and each language>
<command that lists right-to-left strings that start with a left-to-right character and no mark>
<search for user-visible string literals in the changed code>
```

Each command prints nothing. Then open each changed screen in a right-to-left language and in the language with the longest copy, and confirm that nothing clips, overlaps or reads in the wrong order.
