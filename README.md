# QuestWordHunter — French Dictionary

An optional French→English vocabulary pack for [QuestWordHunter](https://github.com/Ironship/WordHunterWoW), built from actual World of Warcraft quest text.

Click a French word in QuestWordHunter and an English gloss is ready. Entries stay in the pack rather than being copied into SavedVariables; player edits still override the pack and **Reset to dictionary** restores its wording.

## What you need

- Retail 12.1 (`Interface 120100`)
- QuestWordHunter / WordHunterWoW
- Target language set to **French**

## Rebuild (maintainers)

1. Blizzard API keys in `Tools/keys.env`.
2. Wago QuestV2 CSV in `Data/QuestV2.csv`.
3. Run `Tools/build_all.ps1`.

Never commit `Tools/keys.env`, `Data/cache/`, or `Data/QuestV2.csv`. Commit generated `Data/DictionaryFR.lua`.

All rights reserved.
