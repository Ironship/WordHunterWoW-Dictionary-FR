PACK_NAME = "WordHunterWoW-Dictionary-FR"

LOCALES = {
    "frFR": {
        "api": "fr_FR",
        "source": "fr",
        "variable": "WordHunterWoW_Dictionary_FR",
        "output": "DictionaryFR.lua",
        "curated": "CuratedFR.jsonl",
        # Function words. A quest field thick with the English ones and thin
        # on these is an untranslated row sitting in the locale file, and its
        # words are not French words.
        "stopwords": ("le", "la", "les", "un", "une", "des", "de", "du", "que", "qui",
                      "pour", "avec", "ne", "pas", "est", "sont", "ce", "cette",
                      "dans", "au", "aux", "par", "vous", "sur"),
        "single_char_words": "àayô",
    },
}

ENGLISH_STOPWORDS = ("the", "and", "you", "your", "with", "from", "that",
                     "this", "have", "will", "they", "them", "been", "must",
                     "into", "there", "their", "what", "when", "would")
