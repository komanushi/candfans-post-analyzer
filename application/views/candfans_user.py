import django_rq

from candfans_client.exceptions import CandFansException
from django.shortcuts import render, redirect
from django.views import View

from modules.analyzer import service as analyzer_sv
from modules.analyzer.domain_models import SyncStatus
from usecase import (
    users_case,
    plans_case,
    stats_case,
)


class CandfansRequestView(View):

    async def get(self, request, user_code: str, *args, **kwargs):
        context = {
            'user_code': user_code,
        }
        candfans_user = await analyzer_sv.get_candfans_user_by_user_code(user_code)
        if not candfans_user:
            try:
                candfans_user, candfans_plans = await users_case.create_new_candfans_user(user_code)
            except CandFansException as e:
                message = str(e)
                if 'アカウントが見つかりませんでした' in message:
                    return redirect('candfans_user_not_found', user_code=user_code)
                else:
                    return redirect('candfans_user_request', user_code=user_code)

        if candfans_user:
            context['candfans_user'] = candfans_user
            user_stats = await stats_case.generate_stats(candfans_user)
            context['monthly_stats'] = user_stats.monthly_stats
            context['summary_monthly_stats_json'] = user_stats.summary_monthly_stats_json
            context['plan_summaries'] = user_stats.plan_summaries
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
            try:
                candfans_user, candfans_plans = await users_case.create_new_candfans_user(user_code)
            except CandFansException as e:
                message = str(e)
                if 'アカウントが見つかりませんでした' in message:
                    return redirect('candfans_user_not_found', user_code=user_code)
                else:
                    return redirect('candfans_user_request', user_code=user_code)

        if candfans_user.is_necessary_to_refresh:
            if not is_new_user:
                await plans_case.resync_candfans_plan(user_code)

            await analyzer_sv.set_sync_status(candfans_user, status=SyncStatus.SYNCING)
            django_rq.enqueue(users_case.sync_user_stats, candfans_user.user_id)

        return redirect('candfans_user_request', user_code=user_code)


class CandidatesUserNotFoundView(View):
    async def get(self, request, user_code: str, *args, **kwargs):
        context = {
            'user_code': user_code,
        }
        return render(
            request,
            'user_not_found.j2',
            context=context,
        )