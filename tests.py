from unittest import TestCase, mock
import ddt

import finder


EXP_GSS = {
    'Эутирокс 75мкг тб.№100                  ',
    'Фромилид 0.5 тб.14                      ',
    'Никсар 20мг тб.30                       '
}
EXP_LL_GSS = {
    'Эутирокс 75мкг тб.№100antonantonantonant',
    'Фромилид 0.5 тб.14antonantonantonantonan',
    'Никсар 20мг тб.30antonantonantonantonant'
}
CLEAR_CONFIG_GSS = 'Эутирокс 75мкг тб.№100\nФромилид 0.5 тб.14\nНиксар 20мг тб.30'
STARTSWITH_NEWLINE_GSS = '\nЭутирокс 75мкг тб.№100\nФромилид 0.5 тб.14\nНиксар 20мг тб.30'
STARTSWITH_WHITESPACE_GSS = '   Эутирокс 75мкг тб.№100\n    Фромилид 0.5 тб.14\n         Никсар 20мг тб.30'
WHITESPACE_MULTIPLE_GSS = 'Эутирокс 75мкг тб.№100                              ' + \
                          '\nФромилид 0.5 тб.14               ' + \
                          '\nНиксар 20мг тб.30                                       \n'
NEWLINE_MULTIPLE_GSS = 'Эутирокс 75мкг тб.№100\nФромилид 0.5 тб.14\n\n\n\nНиксар 20мг тб.30\n\n\n\n\n\n\n\n\n\n\n'
LONG_LINE_GSS = 'Эутирокс 75мкг тб.№100antonantonantonantonanton' + \
                '\nФромилид 0.5 тб.14antonantonantonantonantonanton' + \
                '\nНиксар 20мг тб.30antonantonantonantonantonantonanton'


@ddt.ddt
class GetSearchSetTest(TestCase):
    @ddt.data(
        (CLEAR_CONFIG_GSS, EXP_GSS),
        (STARTSWITH_NEWLINE_GSS, EXP_GSS),
        (STARTSWITH_WHITESPACE_GSS, EXP_GSS),
        (WHITESPACE_MULTIPLE_GSS, EXP_GSS),
        (NEWLINE_MULTIPLE_GSS, EXP_GSS),
        (LONG_LINE_GSS, EXP_LL_GSS),
    )
    @ddt.unpack
    def test_gss_functionality(self, test_line, expected):
        mocked_open = mock.mock_open(read_data=test_line)
        with mock.patch('finder.open', mocked_open, create=True):
            self.assertEqual(finder.get_search_set(), expected)


EXP_GT = [['a'], ['b', 'c'], ['d', 'e', 'f'], ['g'], ['h']]
EASY_GT = ['a\n', '\n', 'b\n', 'c\n', '\n', 'd\n', 'e\n', 'f\n', '\n', 'g\n', '\n', 'h\n', '\n']
WITHOUT_NLS_GT = ['a', '\n', 'b', 'c', '\n', 'd', 'e', 'f', '\n', 'g', '\n', 'h', '\n']
WITHOUT_FINISH_NLS_GT = ['a\n', '\n', 'b\n', 'c\n', '\n', 'd\n', 'e\n', 'f\n', '\n', 'g\n', '\n', 'h\n']


@ddt.ddt
class GetTabsTest(TestCase):
    @ddt.data(
        (EASY_GT, EXP_GT),
        (WITHOUT_NLS_GT, EXP_GT),
        (WITHOUT_FINISH_NLS_GT, EXP_GT)
    )
    @ddt.unpack
    def test_get_tabs_functionality(self, test_lines, expected):
        tabs = finder.get_tabs(test_lines)
        self.assertNotEqual(tabs, expected)
        unpack = [tab for tab in tabs]
        self.assertEqual(unpack, expected)


EXP_GETTITLE = '21_за_12-01-18'
EASY_GETTITLE = [
    '      Стр. NNN                                            ',
    '                   Реализация по исполнителю : 21 за 12.01.18',
]
MULTI_LINES_GETTITLE = [
    'test',
    'test',
    '      Стр. NNN                                            ',
    '                   Реализация по исполнителю : 21 за 12.01.18',
    'test_done',
]
EMPTY_STRING_GETTITLE = [
    '',
    '',
    '      Стр. NNN                                            ',
    '                   Реализация по исполнителю : 21 за 12.01.18',
    'test_done',
]
TITLE_NOT_FOUNDED = [
    '',
    '',
    '      Стр. NNN                                            ',
    '                   Реализация по исполнителю : 21 за 12.01.18',
    'test_done',
]

@ddt.ddt
class GetTitleTest(TestCase):
    @ddt.data(
        (EASY_GETTITLE, EXP_GETTITLE),
        (MULTI_LINES_GETTITLE, EXP_GETTITLE),
        (EMPTY_STRING_GETTITLE, EXP_GETTITLE),
    )
    @ddt.unpack
    def test_get_title_functionality(self, tabs, expected):
        self.assertEqual(finder.get_title(tabs), expected)


EASY_GTN = '------------------- Опер.: 53 Документ :    10 -------------------         19.21'
EMPTY_GTN = 'Общий итог : (65 документов).......................................     1 791.02'


@ddt.ddt
class GetTabNumber(TestCase):
    @ddt.data(
        (EASY_GTN, 10),
        (EMPTY_GTN, )
    )
    def test_gtn_functionality(self, line, expected=None):
        self.assertEqual(finder.get_tab_number(line), expected)


EXP_F = [
    (('Беродуал р-р д/инг 20мл                 ', 13.9), 1.0),
    (('Никсар 20мг тб.30                       ', 18.15), 1.0),
    (('Фромилид 0.5 тб.14                      ', 34.4), 0.5),
    (('Фромилид 0.5 тб.14                      ', 34.4), 1.5),
    (('Эутирокс 150мкг тб.100                  ', 9.40), 1.5),
    (('Беродуал р-р д/инг 20мл                 ', 13.9), 1.0),
]
SOUGHT_F = {
    'Беродуал р-р д/инг 20мл                 ',
    'Никсар 20мг тб.30                       ',
    'Фромилид 0.5 тб.14                      ',
    'Эутирокс 150мкг тб.100                  ',
}
EASY_F = [
    'Беродуал р-р д/инг 20мл                 |      1.000|        13.90|        13.90',
    'АЦЦ Лонг 0.6 тб/ш.10                    |      1.000|         8.91|         8.91',
    'Тобрекс 0.3% гл.к-ли 5мл                |      1.000|        10.71|        10.71',
    'Дексаметазон@ гл.к-ли 0.1% 5мл №1       |      1.000|         2.64|         2.64',
    'Детралекс тб.60                         |      1.000|        50.27|        50.27',
    'Никсар 20мг тб.30                       |      1.000|        18.15|        18.15',
    'Терафлю Лимон пор.пак.10                |      1.000|        15.40|        15.40',
    'Фромилид 0.5 тб.14                      |      0.500|        34.40|        17.20',
    'Фромилид 0.5 тб.14                      |      1.500|        34.40|        51.60',
    'Оспамокс 1г тб.12                       |      2.000|         8.52|        17.04',
    'Эутирокс 150мкг тб.100                  |      1.500|         9.40|        14.10',
    'Валериана-БЗМП 20мг тб.50               |      1.000|         0.93|         0.93',
    'Цитеал р-р 250мл                        |      1.000|        17.11|        17.11',
    'Беродуал р-р д/инг 20мл                 |      1.000|        13.90|        13.90',
]


@ddt.ddt
class FinderTest(TestCase):
    @ddt.data(
        (EASY_F, SOUGHT_F, EXP_F)
    )
    @ddt.unpack
    def test_finder_functionality(self, list_line, sought, expected):
        self.assertNotEqual(finder.finder(list_line, sought), expected)
        unpack = [found for found in finder.finder(list_line, sought)] 
        self.assertEqual(unpack, expected)



