import django_rq

from candfans_client.exceptions import CandFansException
from django.shortcuts import render, redirect
from django.views import View

from modules.analyzer import service as analyzer_sv
from modules.analyzer.domain_models import SyncStatus
from modules.exceptions import NotFoundUser
from usecase import (
    users_case,
    plans_case,
    stats_case,
)


class CandfansRequestView(View):

    async def get(self, request, user_code: str, *args, **kwargs):
        user_code = user_code.split('#')[0]
        context = {
            'user_code': user_code,
        }
        # create_history
        await analyzer_sv.create_search_history(user_code=user_code)
        candfans_user = await analyzer_sv.get_candfans_user_by_user_code(user_code)
        is_new_user = False
        if not candfans_user:
            try:
                candfans_user, candfans_plans = await users_case.create_new_candfans_user(user_code)
                is_new_user = True
            except NotFoundUser:
                return redirect('candfans_user_not_found', user_code=user_code)
            except CandFansException:
                return redirect('candfans_user_request', user_code=user_code)

        if candfans_user.is_necessary_to_refresh:
            if not is_new_user:
                await plans_case.resync_candfans_plan(user_code)

            # SyncStatusの最新化
            await analyzer_sv.set_sync_status(candfans_user, status=SyncStatus.SYNCING)
            django_rq.enqueue(users_case.sync_user_stats, candfans_user.user_id)

        candfans_user = await analyzer_sv.get_candfans_user_by_user_id(candfans_user.user_id)
        if candfans_user:
            daily_ranks = await analyzer_sv.get_daily_ranking_list_by_user_id(candfans_user.user_id)
            context['candfans_user'] = candfans_user
            user_stats = await stats_case.generate_stats(candfans_user)
            context['monthly_stats'] = user_stats.monthly_stats
            context['summary_monthly_stats_json'] = user_stats.summary_monthly_stats_json
            context['plan_based_stats_json'] = user_stats.plan_based_stats_json
            context['plan_summaries'] = user_stats.plan_summaries
            context['plan_post_summary_map'] = user_stats.plan_post_summary_map
            context['daily_ranking_json'] = daily_ranks.rank_json
            # Get available years for year summary navigation
            all_years = await analyzer_sv.get_all_years_with_posts(candfans_user)
            context['all_years'] = all_years

        return render(
            request,
            'user.j2',
            context=context,
        )


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


class CandfansUserYearSummaryView(View):
    async def get(self, request, user_code: str, year: int, *args, **kwargs):
        user_code = user_code.split('#')[0]
        context = {
            'user_code': user_code,
            'year': year,
        }

        # Get user
        candfans_user = await analyzer_sv.get_candfans_user_by_user_code(user_code)
        if not candfans_user:
            return redirect('candfans_user_not_found', user_code=user_code)

        # Get yearly stats
        yearly_stats = await analyzer_sv.get_yearly_post_stats(candfans_user, year)

        # Get all available years for navigation
        all_years = await analyzer_sv.get_all_years_with_posts(candfans_user)

        context['candfans_user'] = candfans_user
        context['yearly_stats'] = yearly_stats
        context['all_years'] = all_years

        return render(
            request,
            'user_year_summary.j2',
            context=context,
        )