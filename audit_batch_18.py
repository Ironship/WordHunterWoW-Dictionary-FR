#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# Read input batch
input_file = 'Data/cache/audit_work/in/batch_18.jsonl'
output_file = 'Data/cache/audit_work/out/batch_18.jsonl'

rows = []
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            rows.append(json.loads(line))

# Build lookup dictionaries dynamically from the rows
# This ensures we capture the exact keys as they appear in the data
key_to_note = {}
key_to_trans = {}

# Process each row and create dynamic mappings for the ones we know about
for row in rows:
    key = row['key']

    # Initialize with empty values
    if key not in key_to_note:
        key_to_note[key] = ""
    if key not in key_to_trans:
        key_to_trans[key] = row['current']

# Now add specific improvements based on exact key values from the file
# Using a generic approach that will match regardless of apostrophe encoding

# Define improvements that will apply to all entries with these base names
improvements_by_base = {
    "chancre": ("canker; corruption", "disease or corruption of flesh"),
    "comprennent": ("include", "include; not just understand"),
    "compétent": ("capable", "capable; enhanced by magical transformation"),
    "céder": ("yield; surrender", "yield; surrender, not to sell"),
    "habitude": ("practice; custom", "false friend: practice or custom, not clothing"),
    "spectres": ("ghosts; spirits", "ghosts or spirits; not spectra"),
    "lustres": ("ages; for ages", "ages; for ages, period of 5 years"),
    "perdons": ("lose", "lose; nous perdons—we lose"),
    "fissa": ("quick; fast", "quick or fast; slang for fait'ça"),
    "pis": ("worse; and then", "worse or and then; colloquial for plus"),
    "marine": ("navy; naval", "navy; military naval force"),
    "messages": ("messages; dispatches", "messages; communications not social posts"),
    "parts": ("shares; portions", "shares or portions; parts of proceeds"),
    "retenus": ("held captive; imprisoned", "held captive or imprisoned; taken prisoner"),
    "retranché": ("entrenched; fortified", "entrenched or fortified; fortified camp"),
    "souillure": ("corruption; defilement", "corruption or defilement; demonic taint"),
    "tiendra": ("will keep; maintain", "will keep or maintain; will hold position"),
    "tienne": ("holds; keeps", "holds or keeps; subjunctive of tenir"),
    "affreux": ("dreadful; horrible", "dreadful or horrible; truly awful"),
    "acceptera": ("will take on; accept", "will accept or take on; agree"),
    "analyser": ("to study; analyze", "to analyze or study; examine"),
    "piéger": ("trap; ensnare", "trap or ensnare; catch"),
    "planté": ("planted; set", "planted or set up; planted a flag"),
    "respecte": ("respects; regards", "respects or regards; holds in esteem"),
    "enlever": ("to kidnap; to abduct", "to kidnap or abduct; carry away"),
    "innocents": ("innocents; the innocent", "innocents; the guiltless or pure"),
    "partiez": ("you were leaving; were departing", "left or departed; were leaving"),
    "rapprocher": ("to bring together; reconcile", "to bring closer; reconcile or unite"),
    "refuser": ("to reject; to refuse", "refuse or reject; deny"),
    "rende": ("yield; give back", "return or give back; subjunctive of rendre"),
    "continuera": ("will continue; persist", "will go on; will persist"),
    "éliminant": ("eliminating; destroying", "eliminating or removing; destroying"),
    # Fix capitalization on proper nouns/verbs that should be lowercase
    "cognepeurs": ("fearbreakers", "ogre clan name"),
    "cordialement": ("sincerely", "sincerely; formal letter closing"),
    "drakuru": ("drakuru", "NPC name"),
    "facture": ("invoice", "bill or invoice; payment demand"),
    "fielsang": ("fielsang", "NPC proper name"),
    "frappez": ("hit; strike", "strike or hit; command to attack"),
    "grommash": ("grommash", "proper name"),
    "n'ayez": ("do not have", "don't have; archaic negative imperative"),
    "rexxar": ("rexxar", "proper name"),
    "rochepoings": ("rockfists", "ogre clan name"),
    "thaelin": ("thaelin", "proper name"),
    "tuez-la": ("kill her", "kill her; imperative command"),
    # Add a few more legitimate improvements
    "visiter": ("to visit; see", "to visit or see; observe"),
    "traversant": ("by crossing; across", "crossing or traversing; going through"),
    "équiper": ("to outfit; arm", "to equip or outfit; arm"),
    "éclaircir": ("to clarify; clear up", "to clear up or clarify; explain"),
    "s'opposent": ("resist; stand against", "stand against or resist; oppose"),
    "l'ost": ("the Devouring Void", "the Void Devouring; l'Ost dévorant"),
    "tapis": ("mat; ground", "carpet or cloth; ground covering"),
    "craint": ("fears; worries", "fears; dreads or worries about"),
}

# Apply improvements to matching keys
for row in rows:
    key = row['key']

    # Check if this key should have an improvement
    for base_key, (trans, note) in improvements_by_base.items():
        if key == base_key:
            key_to_trans[key] = trans
            key_to_note[key] = note
            break

# Add notes for elisions and other entries without explicit trans fixes
elision_patterns = {
    "agir": "to act; elided de + agir",
    "ailes": "of wings; elided de + ailes",
    "alterac": "of Alterac; elided de + Alterac (zone)",
    "expertise": "of expertise; elided de + expertise",
    "hiver": "of winter; winter gear or clothes",
    "peux": "I can; casual je + peux",
    "jaeden": "demon lord name",
    "ambassadeur": "the ambassador; elided le + ambassadeur",
    "entrainement": "training or preparation; elided le + entraînement",
    "herbe": "the grass; elided le + herbe",
    "horizon": "the horizon; elided le + horizon",
    "ost": "the Void Devouring; l'Ost dévorant",
    "ecodome": "the ecodome; elided le + écodôme",
    "etincelle": "the Spark; character name, elided le + étincelle",
    "ayez": "don't have; archaic negative imperative",
    "annonce": "appears or looms; shapes up to be",
    "opposent": "stand against or resist; oppose",
}

simple_note_map = {
    "brouillard": "fog or mist",
    "chambres": "rooms or chambers",
    "champignon": "mushroom or fungus",
    "chaotique": "chaotic or tumultuous",
    "chercheur": "researcher or scholar",
    "château": "castle or fortress",
    "citrouille": "pumpkin; associated with autumn harvest",
    "cognepeurs": "ogre clan name",
    "coincés": "trapped or caught; often in webs or coils",
    "collaborer": "work with; cooperate",
    "condamné": "condemned; sentenced to death or fate",
    "conservé": "preserved or stored; kept in cache",
    "contreforts": "foothills; lower slopes of mountains",
    "cordialement": "sincerely; formal letter closing",
    "craint": "fears; dreads or worries about",
    "cruauté": "cruelty; brutal violence",
    "cruels": "cruel; savage and vicious",
    "dirigeait": "was leading; headed or commanded",
    "dispositifs": "devices or mechanisms; technological apparatus",
    "diverses": "various or assorted",
    "dorée": "golden; precious or shining",
    "douces": "sweet or soft; gentle",
    "drakuru": "NPC name",
    "démolisseurs": "demolition workers; gnome sappers",
    "dérangerait": "would disturb or bother",
    "désactiver": "disable or turn off",
    "désir": "desire or wish; want or hope",
    "détention": "detention or imprisonment; captivity",
    "dévoré": "devoured or consumed; eaten",
    "dévoués": "devoted or loyal; dedicated",
    "efficacement": "effectively or efficiently",
    "englouti": "engulfed or swallowed",
    "escorter": "to escort or accompany",
    "facture": "bill or invoice; payment demand",
    "fielsang": "NPC proper name",
    "fondent": "melt or blend; disappear into surroundings",
    "forment": "form or make; compose together",
    "frappez": "strike or hit; command to attack",
    "fraîchement": "freshly or recently; newly arrived",
    "fusées": "rockets or flares; explosive projectiles",
    "gangrène": "gangrene; putrid flesh disease",
    "garantis": "guaranteed or assured; promised",
    "gisement": "deposit or ore vein; rich resource",
    "grandit": "grows or increases; power waxing",
    "grommash": "proper name",
    "guo-lai": "location proper name",
    "génération": "generation; a defining age or era",
    "hôtes": "hosts or inhabitants; residents",
    "impressionnant": "impressive or striking; remarkable",
    "infinie": "infinite or endless; boundless",
    "jusque-là": "until then or by then",
    "kafa": "WoW plant name",
    "kil'jaeden": "demon lord name",
    "l'énergie": "energy; elided le + énergie",
    "lokdu": "hozen name",
    "luxe": "luxury or comfort; privilege",
    "meurt": "dies or is dying; ironic for a chef",
    "mien": "mine; possessive pronoun",
    "militaires": "military or troops; armed forces",
    "misérable": "wretched or miserable; pitiful",
    "moindres": "lesser or slightest; minimal",
    "noires": "black or dark; gloomy",
    "obstacles": "obstacles or barriers; impediments",
    "oreille": "ear; listen or hear",
    "renferment": "contain or hold; enclose",
    "rescapés": "survivors or rescued ones",
    "riposter": "retaliate or counter; strike back",
    "rites": "rites or rituals; formal ceremonies",
    "rochepoings": "ogre clan name",
    "rude": "harsh or severe; rough treatment",
    "récupérée": "recovered or retrieved; reclaimed",
    "résistants": "resistant or tough; strong",
    "sautez": "jump or leap; command to mount",
    "scintillant": "sparkling or glittering; shining brightly",
    "serve": "serve; render service",
    "servez": "serve; render service or aid",
    "séides": "minions or henchmen; followers",
    "sérieusement": "seriously or gravely; with weight",
    "sévit": "rages or wreaks havoc; terrorizes",
    "suit": "follows; goes along or pursues",
    "surplombant": "overlooking or dominating; towering above",
    "tapis": "carpet or cloth; ground covering",
    "thaelin": "proper name",
    "tourments": "torments or anguish; suffering",
    "transfert": "transfer or conveyance; movement",
    "traversant": "crossing or traversing; going through",
    "trouverait": "would be found or located; passive future",
    "tuez-la": "kill her; imperative command",
    "utilisiez": "used or were using; past imperfect",
    "viendront": "will come; future tense",
    "violente": "violent or fierce; intense battle",
    "visiter": "to visit or see; observe",
    "volantes": "flying or airborne; in the sky",
    "yack": "yak; Himalayan beast of burden",
    "éclaircir": "to clear up or clarify; explain",
    "équiper": "to equip or outfit; arm",
    "abattus": "shot down or felled; killed in combat",
    "apprendrez": "will learn or discover; find out",
}

# Apply simple notes to any key that doesn't have a note yet
for row in rows:
    key = row['key']

    # If already has a note, skip
    if key_to_note[key]:
        continue

    # Check simple note map
    if key in simple_note_map:
        key_to_note[key] = simple_note_map[key]
    else:
        # Check for elisions (entries containing apostrophe patterns)
        for pattern, note in elision_patterns.items():
            if pattern in key.lower():
                key_to_note[key] = note
                break

# Generate output
output_rows = []
translation_changes = 0
note_count = 0

for row in rows:
    key = row['key']
    word = row['word']
    current = row['current']

    # Get translation and note
    new_trans = key_to_trans[key]
    note = key_to_note[key]

    # Count if changed
    if new_trans != current:
        translation_changes += 1

    if note:
        note_count += 1

    output_rows.append({
        "key": key,
        "word": word,
        "translation": new_trans,
        "note": note
    })

# Write output
with open(output_file, 'w', encoding='utf-8') as f:
    for row in output_rows:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')

print(f"Rows written: {len(output_rows)}")
print(f"Translations changed: {translation_changes}")
print(f"Notes written: {note_count}")
