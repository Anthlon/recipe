

import os
from finder import find_manager
from reporter import autoreport


def autorun():
    list_target = os.listdir('base')
    for each in list_target:
        autoreport(find_manager('base/{}'.format(each)))
