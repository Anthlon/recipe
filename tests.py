from unittest import TestCase, mock
import ddt

import finder
import reporter


EXP_GSL = [
    'Эутирокс 75мкг тб.№100                  ',
    'Фромилид 0.5 тб.14                      ',
    'Никсар 20мг тб.30                       '
]
EXP_LL_GSL = [
    'Эутирокс 75мкг тб.№100antonantonantonant',
    'Фромилид 0.5 тб.14antonantonantonantonan',
    'Никсар 20мг тб.30antonantonantonantonant'
]
CLEAR_CONFIG_GSL = 'Эутирокс 75мкг тб.№100\nФромилид 0.5 тб.14\nНиксар 20мг тб.30'
STARTSWITH_NEWLINE_GSL = '\nЭутирокс 75мкг тб.№100\nФромилид 0.5 тб.14\nНиксар 20мг тб.30'
STARTSWITH_WHITESPACE_GSL = '   Эутирокс 75мкг тб.№100\n    Фромилид 0.5 тб.14\n         Никсар 20мг тб.30'
WHITESPACE_MULTIPLE_GSL = 'Эутирокс 75мкг тб.№100                              ' + \
                          '\nФромилид 0.5 тб.14               ' + \
                          '\nНиксар 20мг тб.30                                       \n'
NEWLINE_MULTIPLE_GSL = 'Эутирокс 75мкг тб.№100\nФромилид 0.5 тб.14\n\n\n\nНиксар 20мг тб.30\n\n\n\n\n\n\n\n\n\n\n'
LONG_LINE_GSL = 'Эутирокс 75мкг тб.№100antonantonantonantonanton' + \
                '\nФромилид 0.5 тб.14antonantonantonantonantonanton' + \
                '\nНиксар 20мг тб.30antonantonantonantonantonantonanton'


@ddt.ddt
class GetSearchListTest(TestCase):
    @ddt.data(
        (CLEAR_CONFIG_GSL, EXP_GSL),
        (STARTSWITH_NEWLINE_GSL, EXP_GSL),
        (STARTSWITH_WHITESPACE_GSL, EXP_GSL),
        (WHITESPACE_MULTIPLE_GSL, EXP_GSL),
        (NEWLINE_MULTIPLE_GSL, EXP_GSL),
        (LONG_LINE_GSL, EXP_LL_GSL),
    )
    @ddt.unpack
    def test_gss_functionality(self, test_line, expected):
        mocked_open = mock.mock_open(read_data=test_line)
        with mock.patch('finder.open', mocked_open, create=True):
            self.assertEqual(finder.get_search_list(), expected)


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


EXP1_GHT = [
        'Реализация по кассе №21, за 11-01-18',
        '--------------------------------------------------------------------------------',
        '            Наименование ЛС             |  Цена  | Кол-во |                 Чеки',
        '--------------------------------------------------------------------------------'
    ]
CONFIG1_GHT = {
        'line': '-'*80,
        'format': '{0:^40}|{1:^8}|{2:^8}|{3:>21}'
    }
EXP2_GHT = [
        'Реализация по кассе №21, за 11-01-18',
        '----------------------------------------------------------------------------------',
        '             Наименование ЛС              |  Цена  | Кол-во |                 Чеки',
        '----------------------------------------------------------------------------------'
    ]
CONFIG2_GHT = {
        'line': '-'*82,
        'format': '{0:^42}|{1:^8}|{2:^8}|{3:>21}'
    }
EXP3_GHT = [
        'Реализация по кассе №21, за 11-01-18',
        '----------------------------------------------------------------------------------',
        '            Наименование ЛС             |   Цена   | Кол-во |                 Чеки',
        '----------------------------------------------------------------------------------'
    ]
CONFIG3_GHT = {
        'line': '-'*82,
        'format': '{0:^40}|{1:^10}|{2:^8}|{3:>21}'
    }
EXP4_GHT = [
        'Реализация по кассе №21, за 11-01-18',
        '----------------------------------------------------------------------------------',
        '            Наименование ЛС             |  Цена  |  Кол-во  |                 Чеки',
        '----------------------------------------------------------------------------------'
    ]
CONFIG4_GHT = {
        'line': '-'*82,
        'format': '{0:^40}|{1:^8}|{2:^10}|{3:>21}'
    }
EXP5_GHT = [
        'Реализация по кассе №21, за 11-01-18',
        '---------------------------------------------------------------------------------',
        '            Наименование ЛС             |  Цена  | Кол-во |                  Чеки',
        '---------------------------------------------------------------------------------'
    ]
CONFIG5_GHT = {
        'line': '-'*81,
        'format': '{0:^40}|{1:^8}|{2:^8}|{3:>22}'
    }
EXP6_GHT = [
        'Реализация по кассе №21, за 11-01-18',
        '---------------------------------------------------------------------------------------',
        '             Наименование ЛС              |   Цена   |  Кол-во  |                  Чеки',
        '---------------------------------------------------------------------------------------'
    ]
CONFIG6_GHT = {
        'line': '-'*87,
        'format': '{0:^42}|{1:^10}|{2:^10}|{3:>22}'
    }
TITLE_GHT = '21_за_11-01-18'


@ddt.ddt
class GetHeaderTest(TestCase):
    @ddt.data(
        (TITLE_GHT, EXP1_GHT, CONFIG1_GHT),
        (TITLE_GHT, EXP2_GHT, CONFIG2_GHT),
        (TITLE_GHT, EXP3_GHT, CONFIG3_GHT),
        (TITLE_GHT, EXP4_GHT, CONFIG4_GHT),
        (TITLE_GHT, EXP5_GHT, CONFIG5_GHT),
        (TITLE_GHT, EXP6_GHT, CONFIG6_GHT),
    )
    @ddt.unpack
    def test_getheader_standard(self, title, expected, config):
        with mock.patch.multiple(reporter,
                                 FORMAT=config['format'],
                                 LINE=config['line']):
            result = reporter.get_header(title)
            self.assertEqual(result, expected)


@ddt.ddt
class SorterTest(TestCase):
    @ddt.data(
        (['0', '1', '2', '3', '4'], '1', 1),
        (['0', '1', '2', '3', '4'], '0', 0),
        (['0', '1', '2', '3', '4'], '2', 2),
        (['0', '1', '2', '3', '4'], '4', 4),
    )
    @ddt.unpack
    def test_sorter_functionality(self, data, arg, expected):
        mocked_func = mock.MagicMock(return_value=data)
        with mock.patch('reporter.get_search_list', mocked_func):
            self.assertEqual(reporter.sorter(arg), expected)


FOUND1_GCT = {'title': 'header',
              'body': {
                  ('1', 1): {'tabs': [1], 'amount': 1.334},
                  ('3', 3): {'tabs': [3], 'amount': 3.334},
              }}
EXP1_GCT = 'header\n1|1|1.334|1\n3|3|3.334|3\nfooter\n'
FOUND2_GCT = {'title': 'test',
              'body': {
                  ('0', 1): {'tabs': [1], 'amount': 0.334},
                  ('4', 4): {'tabs': [4], 'amount': 4.334},
              }}
EXP2_GCT = 'header\n0|1|0.334|1\n4|4|4.334|4\nfooter\n'


@ddt.ddt
class GetContentTest(TestCase):
    @ddt.data(
        (['0', '1', '2', '3', '4'], FOUND1_GCT, EXP1_GCT),
        (['0', '1', '2', '3', '4'], FOUND2_GCT, EXP2_GCT),
    )
    @ddt.unpack
    def test_get_content_functionality(self, data, found, expected):
        mocked_header = mock.MagicMock(return_value=['header'])
        mocked_footer = mock.MagicMock(return_value=['footer'])
        mocked_get_search_list = mock.MagicMock(return_value=data)
        mocked_format = '{0:<1}|{1:<1}|{2:<5}|{3:<1}'
        with mock.patch.multiple(reporter, get_header=mocked_header, get_footer=mocked_footer,
                                 get_search_list=mocked_get_search_list, FORMAT=mocked_format):
            self.assertEqual(reporter.get_content(found), expected)
            mocked_header.assert_called_with(found['title'])


@ddt.ddt
class ReportManagerTest(TestCase):
    @ddt.data(
        ({'title': 'test'}, ('result/test.txt', 'w')),
        ({'title': 'hello/test'}, ('result/hello/test.txt', 'w')),
    )
    @ddt.unpack
    def test_report_manager_auto(self, found, expected):
        mocked_open = mock.mock_open()
        mocked_reporter = mock.MagicMock()
        with mock.patch.multiple(reporter, open=mocked_open, get_report=mocked_reporter):
            reporter.report_manager(found, auto=True)
            mocked_open.assert_called_with(expected[0], expected[1])
            mocked_reporter.assert_called_with(found, mocked_open(expected[0], expected[1]))

    @ddt.data(
        ({'title': 'test'}, 'hello', ('result/hello.txt', 'w')),
        ({'title': 'test'}, 'hello/world', ('result/hello/world.txt', 'w')),
    )
    @ddt.unpack
    def test_report_manager_name(self, found, name, expected):
        mocked_open = mock.mock_open()
        mocked_reporter = mock.MagicMock()
        with mock.patch.multiple(reporter, open=mocked_open, get_report=mocked_reporter):
            reporter.report_manager(found, name=name)
            mocked_open.assert_called_with(expected[0], expected[1])
            mocked_reporter.assert_called_with(found, mocked_open(expected[0], expected[1]))

    @ddt.data(
        ({'title': 'test'}, 'hello', ('result/hello.txt', 'w')),
        ({'title': 'test'}, 'hello/world', ('result/hello/world.txt', 'w')),
    )
    @ddt.unpack
    def test_report_manager_both(self, found, name, expected):
        mocked_open = mock.mock_open()
        mocked_reporter = mock.MagicMock()
        with mock.patch.multiple(reporter, open=mocked_open, get_report=mocked_reporter):
            reporter.report_manager(found, name=name, auto=True)
            mocked_open.assert_called_with(expected[0], expected[1])
            mocked_reporter.assert_called_with(found, mocked_open(expected[0], expected[1]))

    @ddt.data(
        ({'title': 'test'},),
        ({'title': 'hello/world'},),
    )
    @ddt.unpack
    def test_report_manager_default(self, found):
        mocked_reporter = mock.MagicMock()
        with mock.patch('reporter.get_report', mocked_reporter):
            reporter.report_manager(found)
            mocked_reporter.assert_called_with(found)

