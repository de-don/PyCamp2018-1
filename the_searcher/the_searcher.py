#!/usr/bin/env python
import re
import click
from collections import Counter
from operator import itemgetter


help_strings = {
    '-u': 'List unique matches only.',
    '-c': 'Total count of found matches.',
    '-uc': 'Total count of unique matches.',
    '-l': 'Total count of lines, where at least one match was found.',
    '-s': 'Sorting of found matches by alphabet and frequency (related to all found matches)',
    '-o': 'Sorting order can be specified (ascending, descending).',
    '-n': 'List first N matches.',
    '--stat': 'List unique matches with statistic (count or frequency in percents).',
}


def lines_generator(filename):
    """"""
    text_stream = click.get_text_stream('stdin')
    if filename:
        text_stream = click.open_file(filename, 'r')

    with text_stream as lines:
        for line in lines:
            yield line


@click.command()
@click.argument('pattern')
@click.argument('filename', type=click.Path(exists=True), required=False)
@click.option('-u', 'flag_u', is_flag=True, help=help_strings['-u'])
@click.option('-c', 'flag_c', is_flag=True, help=help_strings['-c'])
@click.option('-uc', 'flag_uc', is_flag=True, help=help_strings['-uc'])
@click.option('-l', 'flag_l', is_flag=True, help=help_strings['-l'])
@click.option('-s', 'flag_s', type=click.Choice(['freq', 'abc']), help=help_strings['-s'])
@click.option('-o', 'flag_o', type=click.Choice(['asc', 'desc']), default="asc", help=help_strings['-o'])
@click.option('-n', 'flag_n', default=None, help=help_strings['-n'], type=int)
@click.option('--stat', 'stat', type=click.Choice(['count', 'freq']), help=help_strings['--stat'])
def searcher(pattern, filename, flag_u, flag_c, flag_uc, flag_l, flag_s, flag_o, flag_n, stat):
    """
    """
    text_lines = lines_generator(filename)

    count = Counter()
    pattern_matches = 0
    lines_matches = 0

    if flag_u:
        click.echo("List of unique matches")

        for line in text_lines:
            count.update(re.findall(pattern, line))

        for k in count.keys():
            print(k)

    elif flag_c:
        click.echo("Total count of matches")

        for line in text_lines:
            pattern_matches += len(re.findall(pattern, line))
        print(pattern_matches)

    elif flag_uc:
        click.echo("Total count of unique matches")

        for line in text_lines:
            count.update(re.findall(pattern, line))

        print(len(count.items()))

    elif flag_l:
        click.echo("Total count of lines with at least one match")

        for line in text_lines:
            if re.search(pattern, line):
                lines_matches += 1
        print(lines_matches)

    elif flag_s and flag_o:
        click.echo("Sort found matches by {} in {} order".format(flag_s, flag_o))

        for line in text_lines:
            count.update(re.findall(pattern, line))

        sorted_count = sorted(count.items(), key=itemgetter(flag_s=='freq'), reverse=(flag_o=='desc'))

        for s in sorted_count:
            print('{}: {}'.format(s[0], s[1]))

    elif flag_n:
        click.echo("List first {} matches".format(flag_n))

        while pattern_matches < flag_n:
            in_line = re.findall(pattern, next(text_lines))

            if pattern_matches + len(in_line) > flag_n:
                in_line = in_line[:flag_n-pattern_matches]

            for i in in_line:
                print(i)

            pattern_matches += len(in_line)

    elif stat:
        click.echo("List unique matches with {} statistic".format(stat))

        format_string = '{}\t|\t{}'

        for line in text_lines:
            count.update(re.findall(pattern, line))

        for pair in count.items():
            if stat == 'freq':
                print(format_string.format(pair[0], pair[1] / len(count.items())))
            else:
                print(format_string.format(pair[0], pair[1]))

    else:
        click.echo("List of all found matches")

        for line in text_lines:
            in_line = re.findall(pattern, line)
            for i in in_line:
                print(i)


if __name__ == '__main__':
    searcher()

