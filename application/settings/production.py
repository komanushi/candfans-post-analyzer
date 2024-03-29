import os
from .base import *

DEBUG = False

CSRF_TRUSTED_ORIGINS = [
    f"https://{os.environ['SERVICE_DOMAIN']}",
]
