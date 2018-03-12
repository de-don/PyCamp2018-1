import re


translit_dict = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "jo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "j",
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
    "х": "kh",
    "ц": "c",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ъ": "\"",
    "ы": "y",
    "ь": "\'",
    "э": "eh",
    "ю": "ju",
    "я": "ja",
}
ru_special_consonants = 'йъь'
ru_iotated_vovels = 'еёюя'



def transliterate(text, dictionary=translit_dict):
    """"""
    # split words with any space symbol
    words = re.split(r'\s+', text)
    # replace words with '{}' to save spacing format of text
    space_template = re.sub(r'\S*', '{}', text)
    trans_words = list()
    # check language
    for word in words:
        # do transliteration following dictionary
        # if language of text is russian

        # procedure each word symbol by symbol checking if it uppercase
        # if symbol not in transliteration dict, it stays unchanged
        trans_letters = [dictionary[l.lower()] if l.islower()
                         else dictionary[l.lower()].upper() if l.isupper()
                         else l
                         for l in word]
        trans_words.append("".join(trans_letters))
        # if language of text is english
        # PLACE FOR CODE
    return space_template.format(*trans_words)


print(transliterate("Ё,Ж х;ч:Ш щъыыЬ ЭюЮюЯЯ"))
