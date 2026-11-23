---
name: release-notes
description: "Write a version's release notes: audit what changed since the last release, keep only what a person would notice or the business depends on, and write it for every locale. Use when a release is prepared, a version is bumped, or someone asks what is new in a version."
argument-hint: "<version>"
---

# Release notes

In: the changes since the last release. Out: short, true notes in every locale, read as if written for that reader: one file per locale under `<STORE-METADATA-PATH>` for each app store, plus the in-app notes in `<IN-APP-NOTES>`.

## Fill these in first

- `<STORE-METADATA-PATH>`: the per-locale release-notes files, and each store's length limit.
- `<IN-APP-NOTES>`: where in-app notes and their strings live, or "none".
- `<LANGUAGES>`: the languages the product ships in.
- `<LAST-RELEASE-TAG>`: the tag of the previous release.
- `<VOICE-GUIDE>`: the product's voice and each language's register and regional words.

## Phases, in this order

1. Already done?
2. Audit
3. Business filter
4. Base-language text
5. Every locale
6. Check and hand over

## Rules

1. Never invent a feature, a number or a promise. A short true note beats a padded one.
2. Write each locale for its reader, never word for word.
3. Nothing machine-sounding: no emojis, no em or en dashes, no three-adjective lists, no "whether you are X or Y", no "not just X but Y", no filler opener.
4. The owner's choice beats the filter: when a platform is to get only "bug fixes and improvements", write that in every language and keep the shared files in step.
5. The owner or the release command commits.

## 1. Already done?

Do: check whether every output already names this version with new text. If so, skip and say so; if partly, resume; if asked to regenerate, say what gets overwritten.
Proof: the version found in each output.
Why: a rerun must never overwrite approved copy.

## 2. Audit

Do: list the commits since `<LAST-RELEASE-TAG>`, drop internal types (docs, chore, ci, build, test, refactor, style), and read the bodies and diffs of the rest, not just titles.
Proof: a keep or drop line, with its reason, per change.
Why: titles undersell some changes and oversell others.

## 3. Business filter

Do: keep a change only when a person using the app would notice it or the business depends on it: something new to do; something that works very differently; a change to what a plan includes, or a billing problem a person can hit, said plainly; a fix for lost or wrong data, sync, backup or a crash; a new language, device or integration. Drop internal work, fixes to what never shipped, polish nobody would name, what only a new install sees (people who update read these), and team words. Merge changes about one thing. When one or two pass, the release is small and says so.
Proof: the surviving list.
Why: every extra line buries the one a person needed.

## 4. Base-language text

Do: open with one plain sentence naming the headline change, then two to four short sections on what each change means for the person. Fixes get one line naming the one or two a person would have felt, never a count. Keep the previous notes' closing (how to reach support, the thanks). Stay within each limit.
Proof: the text and its length.
Why: people read the first line and skim the rest.

## 5. Every locale

Do: write it for every locale folder that exists (list the folder, never a remembered list) and every language in `<LANGUAGES>` the in-app notes need. Follow `<VOICE-GUIDE>` for register and regional words, reuse the app's own words for its screens from the existing strings, keep trademarks as their owners write them, and swap each idiom for the local idea. In a right-to-left language, keep Latin script to what must stay Latin (trademarks, numbers, addresses) and start each line with a word in that language's script, so the line keeps its direction. Read each as its reader would; a stiff line usually needs a different verb.
Proof: every locale file updated, within its limit.
Why: a missed locale ships the last release's text, and a literal translation sounds like nobody.

## 6. Check and hand over

Do: confirm every output names this version, every locale has new text within its limit, the in-app files match on every platform, and their tests pass. Watch the in-app notes on a device as someone updating from an older version, in light and dark, and in a right-to-left language when there is one. If the release command rebuilds notes from the commit log, tell the owner how to keep these.
Proof: each check and its result.
Why: release tools overwrite hand-written notes unless told not to.
