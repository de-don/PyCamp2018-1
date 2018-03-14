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
    new_text = []
    for d in args:
        # find length of the longest key in dict
        longest_substring = max(map(len, d.keys()))

        current_pos = 0
        while current_pos < len(text):

            # process symbols
            for substring_len in range(longest_substring, 0, -1):

                old_letter = text[current_pos: current_pos + substring_len]

                if old_letter.lower() in d.keys():

                    # process uppercase symbols
                    if old_letter[0].isupper():
                        new_letter = d[old_letter.lower()].upper()
                    else:
                        new_letter = d[old_letter.lower()]

                    # skip other symbols of combination
                    current_pos += substring_len
                    break

            else:
                new_letter = text[current_pos]
                current_pos += 1

            new_text.append(new_letter)

    return ''.join(new_text)


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


