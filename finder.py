"""
A module organising and realising finding.

Main function of module is a finder_manager()
How to use - read docstring.

{'title': 'oprator_date', 'body': {('name    ', price): {'tab_number': [], 'amount' : float}}}
"""


CONFIG = 'config.txt'


def get_search_set(config_module=CONFIG):
    """
    Create and return search set. Search set created based on the data from the config_module.

    :param config_module:
        a string name of the file with the search names
    :return:
        a set with search strings(length 40)
    """
    with open(config_module) as config:
        data = config.readlines()
        return {'{:<40}'.format(line.strip()[:40]) for line in data if line.strip()}


def get_tabs(lines):
    """
    At each iteration collects and returns a check view

    :param lines:
        a iter object, each element of which is a string
    :return:
        a iter object, each element of which is a list of string without '\n'
    """
    tab = []
    for line in lines:
        sline = line.rstrip()
        if not sline:
            yield tab
            tab = []
        else:
            tab.append(sline)
    if tab:
        yield tab


def get_title(lines):  # ToDo: raise Exception title not found
    """
    Retrieves and returns operator and date data as a string

    :param lines:
        a iter object, each element of which is a string without '\n'
    :return:
        a report name as string in format: operator_за_date
    """
    for line in lines:
        if 'Реализация по исполнителю' in line:
            mark_point = line.find(':') + 1
            return line[mark_point:].strip().replace(' ', '_').replace('.', '-')


def get_tab_number(line):
    """
    Retrieves and returns tab number as a integer

    :param line:
        one string line
    :return:
        integer, tab number
    """
    if 'Документ :' in line:
        return int(line[40:46])


def finder(lines, sought):
    """
    Retrieves and returns position data

    :param lines:
        a iter object, each element of which is a string
    :param sought:
        set with search strings(length 40)
    :return:
        tuple with 2 elements key & amount
        key is a tuple with name string & price
    """
    for line in lines:  # iter_lines or lines
        if line[:40] in sought:
            name, amount, price = line.split('|')[:-1]
            found = (name, float(price)), float(amount)  #: Todo: add real format for float
            yield found


def get_body(tabs, sought):
    """
    :param tabs:
        a iter object each element is a list of lines
    :param sought:
        a set with search strings(length 40)
    :return:
        a dict, format {'body': {('name', price): {'tab_number': [], 'amount' : float}}}
    """
    body = {}
    for tab in tabs:
        tab_number = get_tab_number(tab.pop())
        found = finder(tab, sought)
        for key, amount in found:
            if key in body.keys():
                body[key]['amount'] += amount
                body[key]['tab_number'].append(tab_number)
            else:
                body[key] = {}
                body[key]['amount'] = amount
                body[key]['tab_number'] = [tab_number]
    return body


def find_manager(file_name='base/12-2.txt', config=CONFIG):
    """
    Main function, organise finding.

    :param file_name:
        a string, name of file like 'base/12-2.txt'
    :param config_module:
        a string name of the file with the search names
    :return:
        a dict, format
    {'title': 'oprator_date', 'body': {('name    ', price): {'tab_number': [], 'amount' : float}}}
    """
    report = {}
    with open(file_name) as opened:
        lines = opened.readlines()
    sought = get_search_set(config)
    tabs = get_tabs(lines)
    report['title'] = get_title(lines)
    report['body'] = get_body(tabs, sought)
    return report

