import asyncio

from django.core.management.base import BaseCommand

from modules.analyzer import service as analyzer_sv


class Command(BaseCommand):
    help = 'save_ranking'

    def handle(self, *args, **options):
        asyncio.run(self._main())

    async def _main(self, *args):
        await analyzer_sv.save_ranking()

