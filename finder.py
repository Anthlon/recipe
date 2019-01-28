

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
        sought = {'{:<40}'.format(line.strip()[:40]) for line in data if line.strip()}
        return sought


def get_iter_line(file_name='base/12-2.txt'):
    """
    Reads the contents of a file and returns a string representation generator

    :param file_name:
        string, name of file like 'base/12-2.txt'
    :return:
        iter object, each element of which is a string
    """
    with open(file_name) as file:
        data = file.readlines()
    return iter(data)


def get_iter_tab(iter_line):
    """
    At each iteration collects and returns a check view

    :param iter_line:
        iter object, each element of which is a string
    :return:
        iter object, each element of which is a list of string without '\n'
    """
    tab = []
    for line in iter_line:
        if not line.rstrip():
            yield tab
            tab = []
        else:
            tab.append(line.rstrip())
    if tab:
        yield tab


def get_report_title(iter_tab):  # ToDo: raise Exception title not found
    """
    Retrieves and returns operator and date data as a string

    When a title is found, the iterator keeps the state in place of the title founded
    :param iter_tab:
        iter object, each element of which is a list of string without '\n'
    :return:
        report name as string in format: operator_за_date
    """
    for tab in iter_tab:
        if 'Реализация по исполнителю' in tab[-1]:
            mark_point = tab[-1].find(':') + 1
            return tab[-1][mark_point:].strip().replace(' ', '_').replace('.', '-')


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


def finder(iter_line, sought):
    """
    Retrieves and returns position data

    :param iter_line:
        iter object, each element of which is a string
    :param sought:
        set with search strings(length 40)
    :return:
        tuple with 2 elements key & amount
        key is a tuple with name string & price
    """
    for line in iter_line:    # iter_lines or lines
        if line[:40] in sought:
            name, amount, price = line.split('|')[:-1]
            found = (name, float(price)), float(amount)  #: Todo: add real format for float
            yield found


def get_report_body(iter_tab, sought):
    body = {}
    for tab in iter_tab:
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
    report = {}
    sought = get_search_set(config)
    iter_line = get_iter_line(file_name)
    iter_tab = get_iter_tab(iter_line)
    report['title'] = get_report_title(iter_tab)
    report['body'] = get_report_body(iter_tab, sought)
    return report

