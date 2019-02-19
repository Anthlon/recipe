"""
The module provides output result of the program.

Module working with data(named 'found') in fallowing format:
{'title': 'operator_date', 'body': {('name', price): {'tabs': [], 'amount' : float}}}
"""
import sys
from datetime import datetime

from finder import get_search_list


NAME_WIDTH = 40
PRICE_WIDTH = 8
AMOUNT_WIDTH = 8
TABS_WIDTH = 40
WIDTH = NAME_WIDTH + PRICE_WIDTH + AMOUNT_WIDTH + TABS_WIDTH + 3
LINE = '-' * WIDTH
FORMAT = '{0:^' + str(NAME_WIDTH) + '}|{1:^' + str(PRICE_WIDTH) + '}|{2:^' \
         + str(AMOUNT_WIDTH) + '}|{3:>' + str(TABS_WIDTH) + '}'


def get_header(title):
    """
    Creating & formatting header for report

    :param title:
        line consist of operator & date
        format: 'operator_за_date'
    :return:
        list of lines assumed header for report
    """
    return [
     'Реализация по кассе №{0:<2}, за {1:<8}'.format(title[:2], title[-8:]),
     LINE,
     FORMAT.format('Наименование ЛС', 'Цена', 'Кол-во', 'Чеки'),
     LINE,
    ]


def get_footer():
    """
    Creating & formatting footer for report

    :return:
        list of lines assumed footer for report
    """
    return [
        LINE,
        'Report date: {}, MAD, Recipe, 2019'.format(str(datetime.now())[:16])
    ]


def sorter(name):
    data = get_search_list()
    return data.index(name[0])


def get_content(found):
    """
    Creating & formatting content of report

    :param found:
        dict in following format:
        {'title': 'operator_date', 'body': {('name', price): {'tabs': [], 'amount' : float}}}
    :return:
        multi lines string consist of header & content & footer
    """
    content = []
    for key in sorted(found['body'].keys(), key=sorter):
        line = FORMAT.format(
             key[0], key[1], found['body'][key]['amount'],
             ', '.join(str(x) for x in found['body'][key]['tabs'])
        )
        content.append(line)
    report = get_header(found['title']) + content + get_footer()
    return '\n'.join(x for x in report) + '\n'


def get_report(found, output=sys.stdout):
    """
    Displays report to output system

    :param found:
        dict in following format:
        {'title': 'operator_date', 'body': {('name', price): {'tabs': [], 'amount' : float}}}
    :param output:
        opened file for writing
        by default writing to stdout
    :return:
        None
    """
    output.write(get_content(found))


def report_manager(found, name=None, auto=False):
    """
    Displays all reports to stdout or to output text files in result package

    :param found:
        dict in following format:
        {'title': 'operator_date', 'body': {('name', price): {'tabs': [], 'amount' : float}}}
    :param name:
        string, named file or path/named_file from result directory
        file name will add extension .txt
    :param auto:
        bool True or False
    :return:
        None
    """
    if auto or name:
        with open('result/{}.txt'.format(name or found['title']), 'w') as file:
            get_report(found, file)
    else:
        get_report(found)

