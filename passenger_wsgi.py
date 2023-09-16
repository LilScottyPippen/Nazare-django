import os
import sys

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass


cwd = os.getcwd() 
sys.path.append(cwd) 
sys.path.append(cwd + '/nazare') 
os.environ['DJANGO_SETTINGS_MODULE'] = "ZorkaDjango.settings" 
from django.core.wsgi import get_wsgi_application 
application = get_wsgi_application()