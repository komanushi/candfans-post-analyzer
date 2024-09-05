import os
import sentry_sdk

from .base import *

DEBUG = False

SERVICE_HOST = f"https://candfans-analyzer.onrender.com/"


CSRF_TRUSTED_ORIGINS = [
    f"https://{os.environ['SERVICE_DOMAIN']}",
]

sentry_sdk.init(
    dsn="https://34d8a62fba5b0f9900fe8d50ad581ea9@o4507900831399936.ingest.us.sentry.io/4507900832841728",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
