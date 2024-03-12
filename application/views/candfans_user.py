import django_rq

from django.shortcuts import render, redirect
from django.views import View

from modules.analyzer import service as analyzer_sv
from modules.analyzer.domain_models import SyncStatus
from usecase import (
    users as users_usecase,
    plans as plans_usecase,
)


class CandfansRequestView(View):

    async def get(self, request, user_code: str, *args, **kwargs):
        context = {
            'user_code': user_code,
        }
        candfans_user = await analyzer_sv.get_candfans_user_by_user_code(user_code)
        if candfans_user:
            context['candfans_user'] = candfans_user
        return render(
            request,
            'user.j2',
            context=context,
        )


class CandfansRefreshView(View):
    async def post(self, request, user_code: str, *args, **kwargs):
        candfans_user = await analyzer_sv.get_candfans_user_by_user_code(user_code)
        is_new_user = False
        if not candfans_user:
            is_new_user = True
            candfans_user, candfans_plans = await users_usecase.create_new_candfans_user(user_code)

        if candfans_user.is_necessary_to_refresh:
            if not is_new_user:
                await plans_usecase.resync_candfans_plan(user_code)

            await analyzer_sv.set_sync_status(candfans_user, status=SyncStatus.SYNCING)
            django_rq.enqueue(users_usecase.sync_user_stats, candfans_user.user_id)

        return redirect('candfans_user_request', user_code=user_code)
