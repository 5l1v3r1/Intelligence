
__title__ = 'virustotal-api'
__version__ = 'July 4, 2017'
__author__ = 'Fatih'


try:
    import requests
except ImportError:
    pass

from .virustotal import PublicApi, ApiError
