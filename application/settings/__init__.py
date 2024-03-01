import os

if os.environ['DJANGO_ENV'] == 'production':
    from .production import *


if os.environ['DJANGO_ENV'] == 'local':
    from .local import *

