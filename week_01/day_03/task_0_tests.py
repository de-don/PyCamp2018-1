from unittest import TestCase
from .task_0 import transliterate


class TranslitTest(TestCase):
    """"""
    def test_ru_into_eng(self):
        """
        Test different Russian letters
        """
        input_data = "абвЁЖ хчШ щъыыь ЭюЮюЯЯ"
        expected = "abvJOZH khchSH shh\"yy\' EHjuJUjuJAJA"
        self.assertEqual(transliterate(input_data), expected)

    def test_ru_into_eng_punct(self):
        """
        Test punctuation marks
        """
        input_data = "Ё,Ж х;ч:Ш щъыыь ЭюЮюЯЯ"
        expected = "JO,ZH kh;ch:SH shh\"yy\' EHjuJUjuJAJA"
        self.assertEqual(transliterate(input_data), expected)

    def test_ru_into_eng_spaces(self):
        """
        Test space symbols
        """
        input_data = "   Ё ,Ж\t\nх;ч:Ш щъыыь\nЭюЮюЯЯ"
        expected = "   JO ,ZH\t\nkh;ch:SH shh\"yy\'\nEHjuJUjuJAJA"
        self.assertEqual(transliterate(input_data), expected)

    def test_eng_into_ru(self):
        """
        Test from translit into Russian
        """
        input_data = "JOZH khchSH shh\"yy\' EHjuJUjuJAJA"
        expected = "ЁЖ хчШ щъыыь ЭюЮюЯЯ"
        self.assertEqual(transliterate(input_data, source_lang="eng"), expected)

    def test_eng_rus(self):
        """
        Test backward compatibility
        """
        a = "   Ё ,Ж\t\tх;ч:Ш щъыы ь\tЭюЮюЯЯ"
        b = transliterate(a)  # en
        c = transliterate(b, source_lang='en')  # ru
        self.assertEqual(a, c)
        self.assertEqual(transliterate(a), b)
        self.assertEqual(b, transliterate(c))

    def test_eng_to_eng(self):
        """
        Test no changes if selected Russian language for English text
        """
        a = "qaSDGVD  ergs SDEGbsd"
        self.assertEqual(a, transliterate(a, source_lang='ru'))

    def test_rus_to_rus(self):
        """
        Test no changes if selected English language for Russian text
        """
        a = "Ё ,Ж\t\tх;ч:Ш щъыы ь\tЭюЮюЯЯ"
        self.assertEqual(a, transliterate(a, source_lang='english'))

    def test_wrong_language(self):
        """
        Test correct exception if wrong language selected
        """
        with self.assertRaises(ValueError):
            transliterate('abcd', source_lang='British')


