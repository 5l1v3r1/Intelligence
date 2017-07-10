import pkgutil
import os
from ..feeds import autoshun

__path__=os.getcwd()
__path__=__path__+'/feeds'
__path__ = pkgutil.extend_path(__path__, __name__)
for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__+'.'):
      __import__(modname)