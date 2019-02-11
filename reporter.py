"""
This module provides outputing result of programm.

Module working with data in fallowing format:
{'title': 'oprator_date', 'body': {('name', price): {'tab_number': [], 'amount' : float}}}
"""
import sys
from datetime import datetime


def get_title(line):
    return [
     'Реализация по кассе №{0:<2}, за {1:<8}'.format(line[:2], line[-8:]),
     '-' * 80,
     '{0:^40}|{1:^8}|{2:^8}|{3:^21}'.format('Наименование ЛС', 'Цена', 'Кол-во', 'Чеки'),
     '-' * 80,
    ]


def get_border():
    return [
    '-' * 80,
    'Report date: {}, MAD, Recipe, 2019'.format(str(datetime.now())[:16])
] 


def get_content(report):
    content = []
    for key in report['body']:
        line = '{0:<40}|{1:>8}|{2:>8}|{3:>21}'.format(
             key[0], key[1], report['body'][key]['amount'], 
             ', '.join(str(x) for x in report['body'][key]['tab_number'])
        ) 
        content.append(line)
    responce = get_title(report['title']) + content + get_border()
    return '\n'.join(x for x in responce) + '\n'


def report_manager(report, output=sys.stdout):
    data = get_content(report)
    with open(output, 'w') as speach:
        speach.write(data)
    return data


def autoreport(report):
    return report_manager(report, 'result/{}.txt'.format(report['title']))

