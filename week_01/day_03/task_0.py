RU_TO_ENG_DICT = {
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
    "ё": "jo",
    "ж": "zh",
    "й": "jj",
    "х": "kh",
    "ч": "ch",
    "ш": "sh",
    "э": "eh",
    "ю": "ju",
    "я": "ja",
    "щ": "shh",
}
ENG_TO_RU_DICT = {v: k for k, v in RU_TO_ENG_DICT.items()}


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
    new_text = ""
    for d in args:
        current_symbol_pos = 0
        while current_symbol_pos < len(text):
            # search group of symbols or symbol in transliterate dictionary
            is_translitable_old_letter = False
            # first check group of three symbols
            if text[current_symbol_pos: current_symbol_pos + 3].lower() in d.keys():
                old_letter = text[current_symbol_pos: current_symbol_pos + 3]
                is_translitable_old_letter = True
            # then check group of two symbols
            elif text[current_symbol_pos: current_symbol_pos + 2].lower() in d.keys():
                old_letter = text[current_symbol_pos: current_symbol_pos + 2]
                is_translitable_old_letter = True
            # finally check single symbols
            elif text[current_symbol_pos].lower() in d.keys():
                old_letter = text[current_symbol_pos]
                is_translitable_old_letter = True
            # if symbols are not in transliteration dictionary
            else:
                old_letter = text[current_symbol_pos]

            # produce new text
            # translited symbol added to new text
            if is_translitable_old_letter:
                # process uppercase translitable symbols
                if old_letter[0].isupper():
                    new_text += d[old_letter.lower()].upper()
                else:
                    new_text += d[old_letter.lower()]
            # non-translitable symbol added to new text
            else:
                new_text += old_letter

            current_symbol_pos += len(old_letter)

    return new_text


def transliterate(text, source_lang='ru'):
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

    Raises:
        ValueError: If 'source_lang' argument incorrect
            (see 'source_lang' description)

    """
    if source_lang.lower() in ('eng', 'en', 'e', 'english'):
        # apply replacement rules from dictionaries
        eng_to_rus = dict_replacement(text, ENG_TO_RU_DICT)
        return eng_to_rus
    elif source_lang.lower() in ('ru', 'rus', 'r', 'russain'):
        # apply replacement rules from dictionaries
        rus_to_eng = dict_replacement(text, RU_TO_ENG_DICT)
        return rus_to_eng
    else:
        raise ValueError("Wrong language selected")


