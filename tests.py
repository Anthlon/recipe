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
starts_with_new_line = '\nЭутирокс 75мкг тб.№100\nФромилид 0.5 тб.14\nНиксар 20мг тб.30'
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






