

config = 'config.txt'
filename = 'base/12-2.txt'


def get_search_set(config_module=config):
    with open(config_module) as config:
        data = config.read().lstrip().split('\n')
        result = set('{:<40}'.format(x[:40]) for x in data)
        whitespace = ' ' * 40
        if whitespace in result:
            result.remove(whitespace)
        return result


def pre_cogwheel(filename=filename):
    for s in open(filename):
        l = s.rstrip().split('|')
        yield l


def get_logotype(opened_fail):
    """

    return: logotype(name of new file)
    """
    pass


def get_check_number(opened_fail):
    """

    return: check number or None
    """
    pass


def cogwheel(opened_faile):
    """

    return: check number or None
    """
    pass


def parad_searcher(a):
    """

    return: dict result
    """
    pass











