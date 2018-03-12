# transliteration dictionaries for transformation from russian into english
one_letter = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "з": "z",
    "и": "i",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "ц": "c",
    "ъ": "\"",
    "ы": "y",
    "ь": "\'",
}
two_letter = {
    "ё": "jo",
    "ж": "zh",
    "й": "jj",
    "х": "kh",
    "ч": "ch",
    "ш": "sh",
    "э": "eh",
    "ю": "ju",
    "я": "ja",
}
three_letter = {
    "щ": "shh",
}


def dict_replacement(text, *args):
    """ Function that applies replacement rules from replacement dictionaries.

    Args:
        text (str): text for replacement application
        *args: list of dictionaries with replacement rules
            Each dictionary contains replacement rules in following way:
            {
                "old_string" : "new_string"
            }

    Returns:
        new_text (str): text after the replacement rules applied
    """
    list_of_dicts = args
    new_text = text
    for d in list_of_dicts:
        for k, v in d.items():
            new_text = new_text.replace(k.lower(), v.lower())
            new_text = new_text.replace(k.upper(), v.upper())
    return new_text


def transliterate(text, source_lang="ru"):
    """Transliteration function based on GOST http://transliteration.ru/gost/

    Supports transliteration from Russian and vice versa

    Args:
        text (str): text for transliteration
        source_lang (str): register-free marker of source language.
            "ru", "rus", "r", "russain" for Russian source language
            "eng", "en", "e", "english" for English source language

    Returns:
        eng_to_rus (str): russian text gathered from translit
            OR
        rus_to_eng (str): translitted text
    """
    if source_lang.lower() in ("eng", "en", "e", "english"):
        # switch keys and values in replacement dictionaries
        # because source dictionaries are for translit from russian into english
        three_letter_r = {v: k for k, v in three_letter.items()}
        two_letter_r = {v: k for k, v in two_letter.items()}
        one_letter_r = {v: k for k, v in one_letter.items()}
        # apply replacement rules from dictionaries
        eng_to_rus = dict_replacement(text, three_letter_r, two_letter_r, one_letter_r)
        return eng_to_rus
    elif source_lang.lower() in ("ru", "rus", "r", "russain"):
        # apply replacement rules from dictionaries
        rus_to_eng = dict_replacement(text, three_letter, two_letter, one_letter)
        return rus_to_eng
    else:
        raise ValueError("Wrong language selected")



