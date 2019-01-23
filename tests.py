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




