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


def count_lines_with_matches(pattern, text_lines):
    lines_count = 0
    for t in text_lines:
        print(re.search(pattern, t))
        if re.search(pattern, t):
            print()
            lines_count += 1
    # save total count of LINES
    return lines_count


def output_stat_with_sorting_options(
        data,
        matches,
        stat='count',
        flag_s=None,
        flag_o=None
):
    """"""
    # check if sorted output intended
    if flag_s or flag_o:
        data = sorted(
            data,
            key=itemgetter(flag_s == 'freq'),
            reverse=(flag_o == 'desc')
        )

    for st in data:
        if stat == 'freq':
            click.echo('{: >15} | {: >5}'.format(st[0], st[1] / matches))
        else:
            click.echo('{: >15} | {: >5}'.format(st[0], st[1]))


def output_data_with_sorting_options(
        data,
        flag_s=None,
        flag_o=None
):
    """"""
    sorted_data = sorted(
        data,
        key=itemgetter(flag_s == 'freq'),
        reverse=(flag_o == 'desc')
    )
    for d in sorted_data:
        click.echo(d[0])


def output_data(data):
    """
    """
    for d in data:
        click.echo(d)


@click.command()
@click.argument('pattern')
@click.argument('filename', type=click.Path(exists=True), required=False)
@click.option('-u', 'flag_u', is_flag=True, help=help_strings['-u'])
@click.option('-c', 'flag_c', is_flag=True, help=help_strings['-c'])
@click.option('-l', 'flag_l', is_flag=True, help=help_strings['-l'])
@click.option('-s', 'flag_s', type=click.Choice(['abc', 'freq']), help=help_strings['-s'])
@click.option('-o', 'flag_o', type=click.Choice(['asc', 'desc']), help=help_strings['-o'])
@click.option('-n', 'flag_n', default=None, help=help_strings['-n'], type=int)
@click.option('--stat', 'stat', type=click.Choice(['count', 'freq']), help=help_strings['--stat'])
def searcher(pattern, filename, flag_u, flag_c, flag_l, flag_s, flag_o, flag_n, stat):
    """
    """
    text_lines = click.get_text_stream('stdin')
    if filename:
        text_lines = click.open_file(filename, 'r')

    counter_of_matches = Counter()
    list_of_matches = list()
    lines_with_matches = 0

    # save all matches
    for l in text_lines:
        matches = re.findall(pattern, l)
        list_of_matches += matches
        lines_with_matches += (len(matches) > 0)
    counter_of_matches.update(list_of_matches)

    # flag -l : total count of LINES with at least one match
    if flag_l:
        click.echo(lines_with_matches)

    # flag --stats: statistics of matches
    elif stat:
        #
        output_stat_with_sorting_options(
            counter_of_matches.items(),
            len(list_of_matches),
            stat=stat,
            flag_s=flag_s,
            flag_o=flag_o,
        )

    # other flags
    else:
        # flags -u and -c: print total count of unique matches
        if flag_u and flag_c:
            click.echo(len(counter_of_matches.keys()))

        # flag -c: print total count of found matches
        elif flag_c:
            click.echo(len(list_of_matches))

        # flag -u: print unique matches only
        elif flag_u:
            out_data = counter_of_matches

            if flag_s or flag_o:
                output_data_with_sorting_options(
                    out_data.items(),
                    flag_s,
                    flag_o,
                )
            else:
                output_data(out_data)

        # flag -n: print first N matches
        elif flag_n:
            if 0 < flag_n < len(list_of_matches):
                out_data = list_of_matches[:flag_n]
            else:
                out_data = list_of_matches

            if flag_s or flag_o:
                output_data_with_sorting_options(
                    Counter(out_data).items(),
                    flag_s,
                    flag_o,
                )
            else:
                output_data(out_data)

        # no flag: print list of all matches
        else:

            if flag_s or flag_o:
                output_data_with_sorting_options(
                    counter_of_matches.items(),
                    flag_s,
                    flag_o,
                )
            else:
                output_data(list_of_matches)


if __name__ == '__main__':
    searcher()


