

config = 'config.txt'
filename = 'base/12-2.txt'

"""
{'logotype': {('name', 'price'): {'amount': float, 'position': [int, int]}}}
"""
result = {}


def get_search_set(config_module=config):
    with open(config_module) as config:
        data = config.read().lstrip().split('\n')
        result = set('{:<40}'.format(x[:40]) for x in data)
        whitespace = ' ' * 40
        if whitespace in result:
            result.remove(whitespace)
        return result


def get_logotype(opened_fail):
    """

    return: logotype(name of new file in format: operator_date)
    """
    line = opened_fail.readline()

    while 'Реализация по исполнителю' not in line:
        line = opened_fail.readline()

    i = line.find(':')
    return line[(i + 2):].rstrip().replace(' ', '_').replace('.', '_')


def detective(content, sought_for, logotype, position):
    """ Writing result on dict 'result' in following format:
    {'logotype': {('name', float(price)): {'amount': float, 'position': [int, int]}}}

    Keyword arguments:
        content - list, with strings from 1 operation
        sought_for - set, with strings(recipe required)
        logotype - string, name of report
        position - integer, number of current operation

    return -> None
    """
    for line in content:
        if line[:40] in sought_for:
            name, amount, price, t_price = line.strip().split('|')
            key = name, float(price)
            data = result.get(logotype)
            if key in data.keys():
                data[key]['amount'] += float(amount)
                data[key]['position'].append(position)
            else:
                data[key] = {}
                data[key]['amount'] = float(amount)
                data[key]['position'] = [position]


def carver(opened_file, sought_for, logotype):
    """
    Main functionality:
    * Looking for number of operation and return them

    Keyword arguments:
        opened_file
        sought_for - set, with strings(recipe required)
        logotype - string, name of report

    return -> operation number or None
    """
    position = False
    content = []

    while not position:
        line = opened_file.readline()
        if 'Общий итог' in line:
            break
        elif 'Документ :' in line:
            position = int(line[40:46])
        else:
            content.append(line)

    if position:
        detective(content, sought_for, logotype, position)
    return position


def search_manager(file_name):
    """
    Keyword arguments:
        file_name - string, name of file like 'base/12-2.txt'

    return: None
    """
    position = True
    sought_for = get_search_set()
    with open(file_name) as file:
        logotype = get_logotype(file)
        result[logotype] = {}
        while position:
            position = carver(file, sought_for, logotype)














