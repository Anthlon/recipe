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


EXP_GIL = ['a\n', 'b\n', 'c\n', 'd\n', 'e\n', 'f\n', 'g\n']
EASY_GIL = 'a\nb\nc\nd\ne\nf\ng\n'


class GetIterLineTest(TestCase):

    def test_gil_functionality(self, test_line=EASY_GIL, expected=EXP_GIL):
        mocked_open = mock.mock_open(read_data=test_line)
        with mock.patch('finder.open', mocked_open, create=True):
            iter_line = finder.get_iter_line()
            self.assertNotEqual(iter_line, expected)
            unpack = [x for x in iter_line]
            self.assertEqual(unpack, expected)


EXP_GIT = [['a'], ['b', 'c'], ['d', 'e', 'f'], ['g'], ['h']]
EASY_GIT = ['a\n', '\n', 'b\n', 'c\n', '\n', 'd\n', 'e\n', 'f\n', '\n', 'g\n', '\n', 'h\n', '\n']
WITHOUT_NLS_GIT = ['a', '\n', 'b', 'c', '\n', 'd', 'e', 'f', '\n', 'g', '\n', 'h', '\n']
WITHOUT_FINISH_NLS_GIT = ['a\n', '\n', 'b\n', 'c\n', '\n', 'd\n', 'e\n', 'f\n', '\n', 'g\n', '\n', 'h\n']


@ddt.ddt
class GetIterTabTest(TestCase):
    @ddt.data(
        (EASY_GIT, EXP_GIT),
        (WITHOUT_NLS_GIT, EXP_GIT),
        (WITHOUT_FINISH_NLS_GIT, EXP_GIT)
    )
    @ddt.unpack
    def test_git_functionality(self, test_list, expected):
        iter_tab = finder.get_iter_tab(test_list)
        self.assertNotEqual(iter_tab, expected)
        unpack = [x for x in iter_tab]
        self.assertEqual(unpack, expected)


EXP_GRT = '21_за_12-01-18'
EASY_GRT = [
    [
        '      Стр. NNN                                            ',
        '                   Реализация по исполнителю : 21 за 12.01.18'
    ],
    ['test_done']
]
MULTI_TAB_GRT = [
    ['test'],
    ['test'],
    [
        '      Стр. NNN                                            ',
        '                   Реализация по исполнителю : 21 за 12.01.18'
    ],
    ['test_done']
]
EMPTY_STRING_GRT =[
    [''],
    [''],
    [
        '      Стр. NNN                                            ',
        '                   Реализация по исполнителю : 21 за 12.01.18'
    ],
    ['test_done']
]
TITLE_NOT_FOUNDED = [
    [''],
    [''],
    [
        '      Стр. NNN                                            '
    ],
    ['test_done']
]


@ddt.ddt
class GetReportTitleTest(TestCase):
    @ddt.data(
        (EASY_GRT, EXP_GRT),
        (MULTI_TAB_GRT, EXP_GRT),
        (EMPTY_STRING_GRT, EXP_GRT),
    )
    @ddt.unpack
    def test_grn_functionality(self, list_tab, expected):
        self.assertEqual(finder.get_report_title(list_tab), expected)

    @ddt.data(
        (EASY_GRT, ['test_done']),
        (MULTI_TAB_GRT, ['test_done']),
        (EMPTY_STRING_GRT, ['test_done']),
    )
    @ddt.unpack
    def test_grn_state_iter_obj(self, list_tab, expected):
        iter_tab = iter(list_tab)
        finder.get_report_title(iter_tab)
        self.assertEqual(next(iter_tab), expected)


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
        pass



# date_120118 = '''
#
#       Стр. NNN
#                    Реализация по исполнителю : 21 за 12.01.18
#
# --------------------------------------------------------------------------------
#           Hаименование товара           | Количество|     Цена    |     Сумма
# --------------------------------------------------------------------------------
# Пакет(уп)25х42 МАЙКА РБ                 |      1.000|         0.03|         0.03
# ------------------- Опер.: 51 Документ :     1 -------------------          0.03
#
# БАД Биолектра Магнез.Дирек.пак.20 Лимон |      1.000|        11.59|        11.59
# Элевит Пронаталь тб.100                 |      0.200|        68.10|        13.62'''
#
#
# date_100119 = '''
#
#       Стр. NNN
#                    Реализация по исполнителю : 31 за 10.01.19
#
# --------------------------------------------------------------------------------
#           Hаименование товара           | Количество|     Цена    |     Сумма
# --------------------------------------------------------------------------------
# Пакет(уп)25/6х42(13мкм)белый б/логотипа |      1.000|         0.03|         0.03
# ------------------- Опер.: 51 Документ :     1 -------------------          0.03
#
# Вольтарен 75мг/3мл амп.5 Словения       |      0.400|        21.15|         8.46
# Омепразол-ЛФ 20мг капс.30               |      1.000|         2.26|         2.26
# Магния цитрат+вит.В6 1120мг тб.30 БАД   |      2.000|         9.95|        19.90
# Пакет(уп)25/6х42(13мкм)белый б/логотипа |      1.000|         0.03|         0.03
# ------------------- Опер.: 53 Документ :     4 -------------------         30.65'''
#
#
# @ddt.ddt
# class GetLogotypeTest(TestCase):
#     @ddt.data(
#         (date_100119, '31_за_10_01_19', 'Пакет(уп)25/6х42(13мкм)белый б/логотипа |      1.000|         0.03|         0.03'),
#         (date_120118, '21_за_12_01_18', 'Пакет(уп)25х42 МАЙКА РБ                 |      1.000|         0.03|         0.03'),
#     )
#     @ddt.unpack
#     def test_main_functionality(self, test_string, expected_result, iter_status):
#         mocked_file = mock.MagicMock()
#         mocked_method = mock.MagicMock(side_effect=test_string.split('\n'))
#         mocked_file.readline = mocked_method
#         self.assertEqual(rp.get_logotype(mocked_file), expected_result)
#         mocked_file.readline(); mocked_file.readline(); mocked_file.readline(); mocked_file.readline()
#         self.assertEqual(mocked_file.readline(), iter_status)
#
#
# data_content = [
#     'Беродуал р-р д/инг 20мл                 |      1.000|        13.90|        13.90',
#     'АЦЦ Лонг 0.6 тб/ш.10                    |      1.000|         8.91|         8.91',
#     'Тобрекс 0.3% гл.к-ли 5мл                |      1.000|        10.71|        10.71',
#     'Дексаметазон@ гл.к-ли 0.1% 5мл №1       |      1.000|         2.64|         2.64',
#     'Детралекс тб.60                         |      1.000|        50.27|        50.27',
#     'Никсар 20мг тб.30                       |      1.000|        18.15|        18.15',
#     'Терафлю Лимон пор.пак.10                |      1.000|        15.40|        15.40',
#     'Фромилид 0.5 тб.14                      |      0.500|        34.40|        17.20',
#     'Фромилид 0.5 тб.14                      |      1.500|        34.40|        51.60',
#     'Оспамокс 1г тб.12                       |      2.000|         8.52|        17.04',
#     'Эутирокс 150мкг тб.100                  |      1.500|         9.40|        14.10',
#     'Валериана-БЗМП 20мг тб.50               |      1.000|         0.93|         0.93',
#     'Цитеал р-р 250мл                        |      1.000|        17.11|        17.11',
#     'Беродуал р-р д/инг 20мл                 |      1.000|        13.90|        13.90',
# ]
#
# data_search = {
#     'Беродуал р-р д/инг 20мл                 ',
#     'Никсар 20мг тб.30                       ',
#     'Фромилид 0.5 тб.14                      ',
#     'Эутирокс 150мкг тб.100                  ',
# }
#
# expected_detective = {
#     'test': {
#         ('Беродуал р-р д/инг 20мл                 ', 13.9): {'amount': 2.0, 'position': [1, 1]},
#         ('Никсар 20мг тб.30                       ', 18.15): {'amount': 1.0, 'position': [1]},
#         ('Фромилид 0.5 тб.14                      ', 34.4): {'amount': 2.0, 'position': [1, 1]},
#         ('Эутирокс 150мкг тб.100                  ', 9.40): {'amount': 1.5, 'position': [1]},
#     }
# }
#
#
# @ddt.ddt
# class DetectiveTest(TestCase):
#     @ddt.data(
#         (data_content, data_search, 'test', 1, expected_detective)
#     )
#     @ddt.unpack
#     def test_main_functionality(self, content, sought_for, logotype, position, expected):
#         rp.result[logotype] = {}
#         rp.detective(content, sought_for, logotype, position)
#         self.assertEqual(rp.result, expected)
#
#
# caver_data_1 = [
#     'БАД Биолектра Магнез.Дирек.пак.20 Лимон |      1.000|        11.59|        11.59',
#     'Элевит Пронаталь тб.100                 |      0.200|        68.10|        13.62',
#     'Пакет(уп)25х42 МАЙКА РБ                 |      1.000|         0.03|         0.03',
#     '------------------- Опер.: 53 Документ :     4 -------------------         25.24',
# ]
# caver_data_2 = [
#     'Эутирокс 75мкг тб.№100                  |      1.000|         6.97|         6.97',
#     'Оспамокс 1г тб.12                       |      2.000|         8.52|        17.04',
#     'Фромилид 0.5 тб.14                      |      0.500|        34.40|        17.20',
#     'Фромилид 0.5 тб.14                      |      1.500|        34.40|        51.60',
#     '------------------- Опер.: 53 Документ :    18 -------------------         92.81'
# ]
# caver_data_3 = [
#     '--------------------------------------------------------------------------------',
#     'Общий итог : (65 документов).......................................     1 791.02',
# ]
# caver_data_search = {
#     'Беродуал р-р д/инг 20мл                 ',
#     'Никсар 20мг тб.30                       ',
#     'Фромилид 0.5 тб.14                      ',
#     'Эутирокс 150мкг тб.100                  ',
# }
#
#
# @ddt.ddt
# class CarverTest(TestCase):
#     @ddt.data(
#         (caver_data_1, caver_data_search, 'test', 4),
#         (caver_data_2, caver_data_search, 'test', 18),
#         (caver_data_3, caver_data_search, 'test', None),
#     )
#     @ddt.unpack
#     def test_main_functionality(self, data, sought_for, logotype, expected):
#         mocked_file = mock.MagicMock()
#         mocked_method = mock.MagicMock(side_effect=data)
#         mocked_file.readline = mocked_method
#         detective = mock.MagicMock()
#         with mock.patch('rp.detective', detective):
#             self.assertEqual(rp.carver(mocked_file, sought_for, logotype), expected)
#
#     @ddt.data(
#         (caver_data_1, caver_data_search, 'test', 4),
#         (caver_data_2, caver_data_search, 'test', 18),
#     )
#     @ddt.unpack
#     def test_called_detective_control(self, data, sought_for, logotype, expected):
#         mocked_file = mock.MagicMock()
#         mocked_method = mock.MagicMock(side_effect=data)
#         mocked_file.readline = mocked_method
#         detective = mock.MagicMock()
#         with mock.patch('rp.detective', detective):
#             rp.carver(mocked_file, sought_for, logotype)
#             detective.assert_called_with(data[:-1], sought_for, logotype, expected)
#
