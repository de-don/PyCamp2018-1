from click.testing import CliRunner

from the_searcher import searcher


TEST_TEXT = 'acts of civil disobedience,\n' \
            'National Police\n' \
            'Alexandria\n' \
            'in other cities of Egypt.[12]\n' \
            'in other cities of Egypt.[12]\n'

TEST_RESULTS = {
    '-u': 'National\n'
          'Police\n'
          'Alexandria\n'
          'Egypt\n',

    '-s abc': 'Alexandria\n'
              'Egypt\n'
              'National\n'
              'Police\n',

    ' ': 'National\n'
         'Police\n'
         'Alexandria\n'
         'Egypt\n'
         'Egypt\n',

    '-c': '5',

    '-u -c': '4',

    '-c -u': '4',

    '-l': '4',

    '--stat count': '       National |     1\n'
                    '         Police |     1\n'
                    '     Alexandria |     1\n'
                    '          Egypt |     2\n',

    '--stat freq': '       National |   0.2\n'
                   '         Police |   0.2\n'
                   '     Alexandria |   0.2\n'
                   '          Egypt |   0.4\n',

    '-n 2': 'National\n'
            'Police\n',

    '--stat count -s abc': '     Alexandria |     1\n'
                           '          Egypt |     2\n'
                           '       National |     1\n'
                           '         Police |     1\n',

    '--stat freq -s freq': '       National |   0.2\n'
                           '         Police |   0.2\n'
                           '     Alexandria |   0.2\n'
                           '          Egypt |   0.4\n',

    '--stat freq -o asc': '     Alexandria |   0.2\n'
                          '          Egypt |   0.4\n'
                          '       National |   0.2\n'
                          '         Police |   0.2\n',

    '--stat freq -s freq -o desc': '          Egypt |   0.4\n'
                                   '       National |   0.2\n'
                                   '         Police |   0.2\n'
                                   '     Alexandria |   0.2\n',
}


def output_chech(result, expected):
    """"""
    return result.output.splitlines() == expected.splitlines()


# global runner
runner = CliRunner()

pattern = "[A-Z].[a-z]+"
file = "fortest.txt"
text_for_test = TEST_TEXT

def test_unique_matches():
    key = '-u'
    result1 = runner.invoke(
        searcher,
        [key, pattern],
        input=text_for_test,
    )

    result2 = runner.invoke(
        searcher,
        [key, pattern, file],
    )
    print(result1.output)
    assert output_chech(result1, TEST_RESULTS[key])
    assert output_chech(result2, TEST_RESULTS[key])
    assert result1.exit_code == 0
    assert result2.exit_code == 0


def test_count_of_matches():
    key = '-c'
    result = runner.invoke(searcher, [key, pattern, file])
    assert output_chech(result, TEST_RESULTS[key])


def test_count_of_unique_matches():
    key1 = '-u'
    key2 = '-c'
    result1 = runner.invoke(searcher, [key1, key2, pattern, file])
    result2 = runner.invoke(searcher, [key2, key1, pattern, file])
    assert output_chech(result1, TEST_RESULTS[f'{key1} {key2}'])
    assert output_chech(result2, TEST_RESULTS[f'{key2} {key1}'])
    assert output_chech(result1, TEST_RESULTS[f'{key2} {key1}'])
    assert output_chech(result2, TEST_RESULTS[f'{key1} {key2}'])


def test_list_of_matches():
    result = runner.invoke(searcher, [pattern, file])
    assert output_chech(result, TEST_RESULTS[' '])


def test_lines_with_matches():
    key = '-l'
    result = runner.invoke(searcher, [key, pattern, file])
    assert output_chech(result, TEST_RESULTS[key])


def test_stat_no_sorting():
    key = '--stat'
    opt1 = 'count'
    opt2 = 'freq'
    result1 = runner.invoke(searcher, [key, opt1, pattern, file])
    result2 = runner.invoke(searcher, [key, opt2, pattern, file])
    assert output_chech(result1, TEST_RESULTS[f'{key} {opt1}'])
    assert output_chech(result2, TEST_RESULTS[f'{key} {opt2}'])


def test_list_of_n_matches():
    key = '-n'
    opt = '2'
    result = runner.invoke(searcher, [key, opt, pattern, file])
    assert output_chech(result, TEST_RESULTS[f'{key} {opt}'])


def test_stat_sorting():
    key1 = '--stat'
    opt1 = 'count'
    opt2 = 'freq'

    key2 = '-s'
    opt3 = 'abc'
    opt4 = 'freq'

    key3 = '-o'
    opt5 = 'asc'
    opt6 = 'desc'

    result1 = runner.invoke(searcher, [key1, opt1, key2, opt3, pattern, file])
    result2 = runner.invoke(searcher, [key1, opt2, key2, opt4, pattern, file])
    result3 = runner.invoke(searcher, [key1, opt2, key3, opt5, pattern, file])
    result4 = runner.invoke(searcher, [key1, opt2, key2, opt4, key3, opt6, pattern, file])

    assert output_chech(result1, TEST_RESULTS[f'{key1} {opt1} {key2} {opt3}'])
    assert output_chech(result2, TEST_RESULTS[f'{key1} {opt2} {key2} {opt4}'])
    assert output_chech(result3, TEST_RESULTS[f'{key1} {opt2} {key3} {opt5}'])
    assert output_chech(result4, TEST_RESULTS[f'{key1} {opt2} {key2} {opt4} {key3} {opt6}'])


def list_of_matches_sorting():
    key1 = '-s'
    opt1 = 'abc'
    opt2 = 'freq'

    key2 = '-o'
    opt3 = 'asc'
    opt4 = 'desc'

    result1 = runner.invoke(searcher, [key1, opt2, pattern, file])
    result2 = runner.invoke(searcher, [key1, opt2, key2, opt3, pattern, file])
    assert result2.output == result1.output

    result1 = runner.invoke(searcher, [key1, opt1, key2, opt4, pattern, file])
    result2 = runner.invoke(searcher, [key2, opt4, pattern, file])
    assert result2.output == result1.output

    result1 = runner.invoke(searcher, ['-u', key2, opt4, pattern, file])
    result2 = runner.invoke(searcher, [key2, opt4, pattern, file])
    assert result2.output == result1.output


if __name__ == '__main__':
    test_unique_matches()

    test_count_of_matches()
    test_count_of_unique_matches()

    test_lines_with_matches()

    test_list_of_matches()
    test_list_of_n_matches()
    list_of_matches_sorting()

    test_stat_no_sorting()
    test_stat_sorting()


