from unittest import TestCase
from .task_0 import transliterate


class TranslitTest(TestCase):
    def setUp(self):
        self.simple_ru_string = "абвёж хчш щъыыь эюююяя"
        self.simple_eng_string = "abvjozh khchsh shh\"yy\' ehjujujujaja"
        self.uppercase_ru_string = "аБвЁж хЧш Щъыыь эюЮюяя"
        self.uppercase_eng_string = "aBvJOzh khCHsh SHH\"yy\' ehjuJUjujaja"
        self.uppercase_eng_string2 = "aBvJozh khChsh Shh\"yy\' ehjuJujujaja"
        self.punctuation_ru_string = "Ё,Ж х;ч:Ш щъыыь ЭюЮюЯЯ"
        self.punctuation_eng_string = "JO,ZH kh;ch:SH shh\"yy\' EHjuJUjuJAJA"
        self.space_ru_string = "   Ё ,Ж\t\nх;ч:Ш щъыыь\nЭюЮюЯЯ"
        self.space_eng_string = "   JO ,ZH\t\nkh;ch:SH shh\"yy\'\nEHjuJUjuJAJA"

    def test_simple_ru_into_eng(self):
        self.assertEqual(
            transliterate(self.simple_ru_string),
            self.simple_eng_string,
        )

    def test_uppercase_ru_into_eng(self):
        self.assertEqual(
            transliterate(self.uppercase_ru_string),
            self.uppercase_eng_string,
        )
        self.assertNotEqual(
            transliterate(self.uppercase_ru_string),
            self.simple_eng_string,
        )
        self.assertNotEqual(
            transliterate(self.uppercase_ru_string),
            self.uppercase_eng_string2,
        )

    def test_punctuation_ru_into_eng(self):
        self.assertEqual(
            transliterate(self.punctuation_ru_string),
            self.punctuation_eng_string,
        )

    def test_space_symbols_ru_into_eng(self):
        self.assertEqual(
            transliterate(self.space_ru_string),
            self.space_eng_string,
        )

    def test_simple_eng_into_ru(self):
        self.assertEqual(
            transliterate(self.simple_eng_string, source_lang="eng"),
            self.simple_ru_string,
        )

    def test_uppercase_eng_into_ru(self):
        self.assertEqual(
            transliterate(self.uppercase_eng_string, source_lang="eng"),
            self.uppercase_ru_string,
        )
        self.assertEqual(
            transliterate(self.uppercase_eng_string2, source_lang="eng"),
            self.uppercase_ru_string,
        )

    def test_backward_compatability_rut_eng_rus(self):
        a = self.space_ru_string
        b = transliterate(a)  # ru to en
        c = transliterate(b, source_lang='en')  # en to ru
        self.assertEqual(a, c)
        self.assertEqual(transliterate(a), b)
        self.assertEqual(b, transliterate(c))

    def test_no_changes_eng_text_ru_lang(self):
        self.assertEqual(
            self.simple_eng_string,
            transliterate(self.simple_eng_string, source_lang='ru')
        )

    def test_no_changes_ru_text_eng_lang(self):
        self.assertEqual(
            self.space_ru_string,
            transliterate(self.space_ru_string, source_lang='english')
        )

    def test_wrong_source_language(self):
        with self.assertRaises(ValueError):
            transliterate('abcd', source_lang='British')


