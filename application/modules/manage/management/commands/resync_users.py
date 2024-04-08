import asyncio

import django_rq
from django.core.management.base import BaseCommand

from modules.analyzer import service as analyzer_sv
from usecase.users_case import sync_user_stats


class Command(BaseCommand):
    help = 'resync_users'

    def handle(self, *args, **options):
        asyncio.run(self._main())

    async def _main(self, *args):
        target_users = await analyzer_sv.get_candfans_user_list_order_by_last_synced_at_asc(100)
        for user in target_users:
            print(f'request resync user: {user.user_id=} {user.user_code=} {user.username=}')
            django_rq.enqueue(sync_user_stats, user.user_id)
