import asyncio

from django.core.management.base import BaseCommand
from django.conf import settings

from ...service import ping_domain


class Command(BaseCommand):
    help = 'ping'

    def handle(self, *args, **options):
        asyncio.run(self._main())

    async def _main(self, *args):
        ping_domain(settings.SERVICE_HOST)

