import re
import click


@click.command()
@click.argument('pattern')
@click.argument('filename', type=click.Path(exists=True), required=False)
@click.option('-u', 'flag_u', is_flag=True, help='List unique matches only.')
@click.option('-c', 'flag_c', is_flag=True, help='Total count of found matches.')
@click.option('-l', 'flag_l', is_flag=True, help='Total count of lines, where at least one match was found.')
@click.option('-s', 'opt_s', type=click.Choice(['freq', 'abc']),
              help='Sorting of found matches by alphabet and frequency (related to all found matches).')
@click.option('-o', 'opt_o', type=click.Choice(['asc', 'desc']), default="asc",
              help="Sorting order can be specified (ascending, descending).")
@click.option('-n', 'opt_n', default=None, help="List first N matches.", type=int)
@click.option('--stat', 'stat', type=click.Choice(['count', 'freq']),
              help="List unique matches with statistic (count or frequency in percents).")
def the_searcher(pattern, filename, flag_u, flag_c, flag_l, opt_s, opt_o, opt_n, stat):
    """
    """
    total_matches = 0
    unique_matches = 0


    # pattern = re.compile(pattern)
    with open(filename, 'r') as lines:
        for line in lines:
            line_matches = re.findall(pattern, line)
            # line_iter = re.finditer(pattern, line)




