# QuestWordHunter — French Dictionary

An optional French→English vocabulary pack for [QuestWordHunter](https://github.com/Ironship/WordHunterWoW), built from actual World of Warcraft quest text.

Click a French word in QuestWordHunter and an English gloss is ready. Entries stay in the pack rather than being copied into SavedVariables; player edits still override the pack and **Reset to dictionary** restores its wording.

58,653 entries.

## Quality

This pack is raw machine translation. Unlike the [German dictionary](https://github.com/Ironship/WordHunterWoW-Dictionary-DE), where a large share of entries has been reviewed by hand against the quest sentence it appears in, nothing here has been through that review. Expect the usual machine-translation failures: false friends, the wrong sense of an ambiguous word, official WoW names translated literally. Treat a gloss as a starting point, and edit it when it is wrong — your edit wins over the pack.

The exception is a short hand-written list in `Data/CuratedFR.jsonl` covering the one-letter words `à`, `a`, `y` and `ô`. Those are among the most frequent words in the language and a machine translator has no context to get them right: asked in isolation, Google renders `à` as "has", confusing the preposition with the verb `a`. These four are glossed by hand and override the machine output.

## What you need

- Retail 12.1 (`Interface 120100`)
- [QuestWordHunter](https://github.com/Ironship/WordHunterWoW) **1.6.0 or newer**
- Target language set to **French**

1.6.0 is a hard requirement, not a suggestion: earlier versions lowercase only ASCII, so every word starting with an accented capital — `À`, `Ça`, `Écoutez`, `Êtes-vous` — missed the dictionary and opened a second entry in the word list. That affected 5,317 occurrences across 516 distinct words in this corpus.

## Rebuild (maintainers)

1. Blizzard API keys in `Tools/keys.env`.
2. Wago QuestV2 CSV in `Data/QuestV2.csv`.
3. Run `Tools/build_all.ps1`.

Never commit `Tools/keys.env`, `Data/cache/`, or `Data/QuestV2.csv`. Commit generated `Data/DictionaryFR.lua`.

All rights reserved.
