from unittest import TestCase, mock
import ddt

import rp

expected_config = {'Эутирокс 75мкг тб.№100                  ', 'Фромилид 0.5 тб.14                      ',
                   'Никсар 20мг тб.30                       '}

expected_config_longline = {'Эутирокс 75мкг тб.№100antonantonantonant', 'Фромилид 0.5 тб.14antonantonantonantonan',
                            'Никсар 20мг тб.30antonantonantonantonant'}

without_mistake_config = 'Эутирокс 75мкг тб.№100\nФромилид 0.5 тб.14\nНиксар 20мг тб.30'
new_line_multiple = 'Эутирокс 75мкг тб.№100\nФромилид 0.5 тб.14\n\n\n\nНиксар 20мг тб.30\n\n\n\n\n\n\n\n\n\n\n'
whitespace_multiple = 'Эутирокс 75мкг тб.№100                              \nФромилид 0.5 тб.14               ' + \
                      '                    \nНиксар 20мг тб.30                                       \n'
starts_with_new_line = '\n     Эутирокс 75мкг тб.№100\nФромилид 0.5 тб.14\nНиксар 20мг тб.30'
very_long_string = 'Эутирокс 75мкг тб.№100antonantonantonantonanton\nФромилид 0.5 тб.14antonantonantonantonanton' + \
                   'anton\nНиксар 20мг тб.30antonantonantonantonantonantonanton'


@ddt.ddt
class GetSearchSetTest(TestCase):
    @ddt.data(
        (without_mistake_config, expected_config),
        (new_line_multiple, expected_config),
        (whitespace_multiple, expected_config),
        (starts_with_new_line, expected_config),
        (very_long_string, expected_config_longline),
    )
    @ddt.unpack
    def test_main_functionality(self, test_file, expected):
        mocked_open = mock.mock_open(read_data=test_file)
        with mock.patch('rp.open', mocked_open, create=True):
            self.assertEqual(rp.get_search_set(), expected)


date_120118 = '''

      Стр. NNN                                            
                   Реализация по исполнителю : 21 за 12.01.18

--------------------------------------------------------------------------------
          Hаименование товара           | Количество|     Цена    |     Сумма
--------------------------------------------------------------------------------
Пакет(уп)25х42 МАЙКА РБ                 |      1.000|         0.03|         0.03
------------------- Опер.: 51 Документ :     1 -------------------          0.03

БАД Биолектра Магнез.Дирек.пак.20 Лимон |      1.000|        11.59|        11.59
Элевит Пронаталь тб.100                 |      0.200|        68.10|        13.62'''


date_100119 = '''

      Стр. NNN                                            
                   Реализация по исполнителю : 31 за 10.01.19

--------------------------------------------------------------------------------
          Hаименование товара           | Количество|     Цена    |     Сумма
--------------------------------------------------------------------------------
Пакет(уп)25/6х42(13мкм)белый б/логотипа |      1.000|         0.03|         0.03
------------------- Опер.: 51 Документ :     1 -------------------          0.03

Вольтарен 75мг/3мл амп.5 Словения       |      0.400|        21.15|         8.46
Омепразол-ЛФ 20мг капс.30               |      1.000|         2.26|         2.26
Магния цитрат+вит.В6 1120мг тб.30 БАД   |      2.000|         9.95|        19.90
Пакет(уп)25/6х42(13мкм)белый б/логотипа |      1.000|         0.03|         0.03
------------------- Опер.: 53 Документ :     4 -------------------         30.65'''


@ddt.ddt
class GetLogotypeTest(TestCase):
    @ddt.data(
        (date_100119, '31_за_10_01_19', 'Пакет(уп)25/6х42(13мкм)белый б/логотипа |      1.000|         0.03|         0.03'),
        (date_120118, '21_за_12_01_18', 'Пакет(уп)25х42 МАЙКА РБ                 |      1.000|         0.03|         0.03'),
    )
    @ddt.unpack
    def test_main_functionality(self, test_string, expected_result, iter_status):
        mocked_file = mock.MagicMock()
        mocked_method = mock.MagicMock(side_effect=test_string.split('\n'))
        mocked_file.readline = mocked_method
        self.assertEqual(rp.get_logotype(mocked_file), expected_result)
        mocked_file.readline(); mocked_file.readline(); mocked_file.readline(); mocked_file.readline()
        self.assertEqual(mocked_file.readline(), iter_status) 


data_content = [
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

data_search = {
    'Беродуал р-р д/инг 20мл                 ',
    'Никсар 20мг тб.30                       ',
    'Фромилид 0.5 тб.14                      ',
    'Эутирокс 150мкг тб.100                  ',
}

expected_detective = {
    'test': {
        ('Беродуал р-р д/инг 20мл                 ', 13.9): {'amount': 2.0, 'position': [1, 1]},
        ('Никсар 20мг тб.30                       ', 18.15): {'amount': 1.0, 'position': [1]},
        ('Фромилид 0.5 тб.14                      ', 34.4): {'amount': 2.0, 'position': [1, 1]},
        ('Эутирокс 150мкг тб.100                  ', 9.40): {'amount': 1.5, 'position': [1]},
    }
}


@ddt.ddt
class DetectiveTest(TestCase):
    @ddt.data(
        (data_content, data_search, 'test', 1, expected_detective)
    )
    @ddt.unpack
    def test_main_functionality(self, content, sought_for, logotype, position, expected):
        rp.result[logotype] = {}
        rp.detective(content, sought_for, logotype, position)
        self.assertEqual(rp.result, expected)


caver_data_1 = [
    'БАД Биолектра Магнез.Дирек.пак.20 Лимон |      1.000|        11.59|        11.59',
    'Элевит Пронаталь тб.100                 |      0.200|        68.10|        13.62',
    'Пакет(уп)25х42 МАЙКА РБ                 |      1.000|         0.03|         0.03',
    '------------------- Опер.: 53 Документ :     4 -------------------         25.24',
]
caver_data_2 = [
    'Эутирокс 75мкг тб.№100                  |      1.000|         6.97|         6.97',
    'Оспамокс 1г тб.12                       |      2.000|         8.52|        17.04',
    'Фромилид 0.5 тб.14                      |      0.500|        34.40|        17.20',
    'Фромилид 0.5 тб.14                      |      1.500|        34.40|        51.60',
    '------------------- Опер.: 53 Документ :    18 -------------------         92.81'
]
caver_data_3 = [
    '--------------------------------------------------------------------------------',
    'Общий итог : (65 документов).......................................     1 791.02',
]
caver_data_search = {
    'Беродуал р-р д/инг 20мл                 ',
    'Никсар 20мг тб.30                       ',
    'Фромилид 0.5 тб.14                      ',
    'Эутирокс 150мкг тб.100                  ',
}


@ddt.ddt
class CarverTest(TestCase):
    @ddt.data(
        (caver_data_1, caver_data_search, 'test', 4),
        (caver_data_2, caver_data_search, 'test', 18),
        (caver_data_3, caver_data_search, 'test', None),
    )
    @ddt.unpack
    def test_main_functionality(self, data, sought_for, logotype, expected):
        mocked_file = mock.MagicMock()
        mocked_method = mock.MagicMock(side_effect=data)
        mocked_file.readline = mocked_method
        detective = mock.MagicMock()
        with mock.patch('rp.detective', detective):
            self.assertEqual(rp.carver(mocked_file, sought_for, logotype), expected)

    @ddt.data(
        (caver_data_1, caver_data_search, 'test', 4),
        (caver_data_2, caver_data_search, 'test', 18),
    )
    @ddt.unpack
    def test_called_detective_control(self, data, sought_for, logotype, expected):
        mocked_file = mock.MagicMock()
        mocked_method = mock.MagicMock(side_effect=data)
        mocked_file.readline = mocked_method
        detective = mock.MagicMock()
        with mock.patch('rp.detective', detective):
            rp.carver(mocked_file, sought_for, logotype)
            detective.assert_called_with(data[:-1], sought_for, logotype, expected)

