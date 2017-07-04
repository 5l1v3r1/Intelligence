
__title__ = 'autoshun_feeder'
__author__ = 'Fatih'


try:
    import requests
except ImportError:
    pass

from .autoshun import Feederautoshun as autshun
