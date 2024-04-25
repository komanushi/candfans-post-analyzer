from .base import *

DEBUG = False

SERVICE_HOST = f"http://{os.environ['SERVICE_DOMAIN']}"


CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8001',
    SERVICE_HOST,
]
