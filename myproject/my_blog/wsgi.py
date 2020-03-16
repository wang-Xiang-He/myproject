import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling # <- 加入

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
application = Cling(get_wsgi_application()) # <- 修改