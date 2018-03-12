from unittest import TestCase
from .task_0 import transliterate


class TranslitTest(TestCase):
    """"""
    def test_ru_into_eng(self):
        print(transliterate("ЁЖ хчШ щъыыЬ ЭюЮюЯЯ"))
        print("JOZH khchSH sch\"yy\' EH juJUjuJAJA\n")
        self.assertEqual(transliterate("ЁЖ хчШ щъыыЬ ЭюЮюЯЯ"), "JOZH khchSH sch\"yy\' EHjuJUjuJAJA")

    def test_ru_into_eng_punct(self):
        print(transliterate("Ё,Ж х;ч:Ш щъыыЬ ЭюЮюЯЯ"))
        print("JO,ZH kh;ch:SH sch\"yy\' EHjuJUjuJAJA\n")
        self.assertEqual(transliterate("Ё,Ж х;ч:Ш щъыыЬ ЭюЮюЯЯ"), "JO,ZH kh;ch:SH sch\"yy\' EHjuJUjuJAJA")

