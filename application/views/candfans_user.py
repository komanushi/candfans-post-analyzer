import django_rq

from django.shortcuts import render, redirect
from django.views import View

from modules.analyzer import service as analyzer_sv
from modules.analyzer.domain_models import SyncStatus
from modules.candfans_gateway import service as cg_sv
from usecase import users as users_usecase


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
        if not candfans_user:
            candfans_user = await users_usecase.create_new_candfans_user(user_code)
        if candfans_user.is_necessary_to_refresh:
            await analyzer_sv.set_sync_status(candfans_user, status=SyncStatus.SYNCING)
            django_rq.enqueue(users_usecase.sync_user_stats, candfans_user.user_id)

        return redirect('candfans_user_request', user_code=user_code)
