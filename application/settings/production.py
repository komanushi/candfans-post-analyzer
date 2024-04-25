import os
from .base import *

DEBUG = False

SERVICE_HOST = f"https://candfans-analyzer.onrender.com/"


CSRF_TRUSTED_ORIGINS = [
    f"https://{os.environ['SERVICE_DOMAIN']}",
]
