# French dictionary audit — instructions

You are improving a French→English dictionary used by a World of Warcraft addon.
Players read French quest text and click a word to see its English meaning plus a
short note. Your job is to fix machine-translation errors and write notes that
teach the reader something worth knowing.

## Input

`Data/cache/audit_work/in/batch_NN.jsonl` — one JSON object per line:

- `key` — lowercase lookup key. **Copy it through character for character.** It is
  already casefolded the way the addon looks words up. Accents stay exactly as
  they are: the key is `arrachée`, never `arrachee`. The ligature stays: `cœur`,
  never `coeur`. The apostrophe is the typographic one, `’` (U+2019), not `'` —
  `lune-d’argent` keeps it. Do not ASCII-fold, do not re-case, do not fix what
  looks like a typo. A changed key breaks the lookup, and a changed `word` breaks
  the repair path that would otherwise recover it.
- `word` — the French word as it appears in game. **Copy through verbatim.**
- `current` — the existing Google Translate output. Often right, sometimes wrong.
- `count` — how often the word occurs across all quests.
- `context` — a real quest sentence containing the word.

## Output

`Data/cache/audit_work/out/batch_NN.jsonl` — one JSON object per input line,
**same order, same count, same keys**, with exactly these four fields:

```json
{"key":"hurlevent","word":"Hurlevent","translation":"Stormwind","note":"hurle (howls) + vent (wind); the human capital"}
```

Write the file with the Write tool.

### The file format is where these passes actually fail

Every one of these has happened on this dictionary and each one silently loses
rows. Check your file against this list before you finish:

- **No byte order mark.** Plain UTF-8.
- **One object per line.** Nothing after the closing brace: no trailing comma,
  no `]`, no second object sharing the line, no markdown fence.
- **Four fields, nothing else.** A bare value with no field name in front of it
  is a broken line.
- **The apostrophe is `’` (U+2019), not `'`.** This is the big one: 129 keys in
  the first wave were written with the plain apostrophe, which would have
  dropped every elided word in the pack -- `c’est`, `l’eau`, `d’un`, `qu’il`.
- **Accents and the ligature `œ` stay exactly as given.** `arrachée`, never
  `arrachee`. `cœur`, never `coeur`.

### Count your own work before you finish

Open your output and count: how many translations differ from `current`, and
how many rows have a non-empty note. A pass that reports numbers it did not
achieve is worse than one that reports a low number honestly -- the check that
follows measures the file, not the claim, and a batch that fails it is rerun
from scratch.

## Do both jobs in one pass

The two halves of this task are the translation and the note, and they carry
equal weight. Agents on this task reliably do one and skip the other: a pass told
to care about notes stops touching translations, and a pass told to care about
translations writes four notes in a hundred and fifty rows. Both get rejected and
rerun.

A healthy pass revises **around a third of the translations** and leaves **a note
on nearly every row**. Check your own output against that before you finish. If
either number is far below, you have not done the work yet.

The one honest reason for a low note count is a batch thick with bare proper
names — NPC names, surnames — where an empty note is correct because you must not
invent lore. That is the only excuse. Every verb, adjective, common noun and
compound gets a real note.

## Errors to look for before you accept `current`

This corpus was machine-translated word by word, with no sentence around the
word. These are the mistakes it actually made here, measured:

- **the word handed straight back, untranslated.** A fifth of this dictionary has
  a gloss identical to the French. For a proper name that is correct; for
  `écorcheur` or `ravitaillement` it is not a translation at all.
- **shouting or stray capitals.** `vous` came back as "YOU", `les` and `le` as
  "THE", `et` as "And". A gloss for a lowercase French word is lowercase English.
- **an accent-blind homograph.** `à` (to, at) was glossed "has", which is `a`.
  `la` (the) was glossed "there", which is `là`. `ou` (or) is not `où` (where).
  Read the accent that is actually there.
- **a participle handed back as an infinitive**, or the reverse (`arrachée` is
  "torn off", not "to tear off").
- **a false friend taken at face value** (`blesser` is to wound, never to bless;
  `actuellement` is currently, not actually; `assister` is to attend).
- **the wrong sense of an ambiguous word** — pick the one the `context` supports.
- **an official English WoW name missed.** `Hurlevent` is Stormwind, not
  "Howlwind"; `Lune-d’Argent` is Silvermoon; `Norfendre` is Northrend.
- **a plural rendered as a singular**, or the reverse.
- **elision misread** — `l’`, `d’`, `qu’`, `j’` are the article or preposition
  with its vowel dropped, not part of the following word.

## translation

- Give the meaning that fits **WoW quest text**, not a dictionary's first entry.
- Use the **official English WoW term** when the French is a game proper noun.
- If you are not confident an official English name exists, give a clean literal
  translation instead. **Do not invent lore, zone names, or NPC names.**
- Separate genuinely distinct senses with `; ` — at most three, most common first.
- Keep the grammatical category (noun → noun, verb → verb). Nouns: no article.
  Verbs: bare infinitive without "to" unless it disambiguates.
- **Match the source's capitalisation.** French capitalises proper nouns and
  little else, so a lowercase French word gets a lowercase English gloss. Never
  all-caps.
- If `current` is already the best answer, repeat it unchanged. That is a normal
  and expected outcome — do not change things just to look busy.

## note

This is the part the user actually reads for fun. Make it earn its place.

Pick whichever of these applies, best first:

1. **Compound or word-formation breakdown**, when it illuminates the word:
   `Hurlevent` → "hurle (howls) + vent (wind); the human capital"
2. **False friend / trap**, when a learner would guess wrong:
   `blesser` → "false friend: to wound, nothing to do with blessing"
3. **Official name differs from the literal sense**:
   `Fossoyeuse` → "literally gravedigger; check the English name before assuming"
4. **The accent that changes the word**:
   `ou` → "no accent: or. with one, où = where"
5. **Idiom or fixed phrase** the word usually appears in.
6. **Etymology or a genuinely interesting fact** about the word.

Rules:

- English, lowercase start, **no trailing period**, at most ~120 characters.
- Never merely restate the translation ("means darkness") — that is wasted space.
- Never write filler like "common French word" on its own.
- Prefer concrete over vague.
- If nothing worth saying comes to mind, use `""`. An empty note is much better
  than a boring one.
- No newlines, keep it plain.

## Accuracy

Getting a translation wrong is worse than leaving it as it was. When torn between
a confident literal reading and a half-remembered WoW term, choose the literal
one. Do not guess at lore.

Return only a one-line summary: how many rows you wrote, and any keys you were
genuinely unsure about.
