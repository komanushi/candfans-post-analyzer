import json

from django.http import JsonResponse
from django.views import View

from modules.analyzer import service as analyzer_sv
from usecase import stats_case


class MonthlyStatsApiView(View):

    async def get(self, request, user_id: int, *args, **kwargs):
        candfans_user = await analyzer_sv.get_candfans_user_by_user_id(user_id)
        if not candfans_user:
            return JsonResponse({'error': 'not found'}, status=404)
        monthly_stats = await analyzer_sv.get_monthly_post_stats(user=candfans_user)
        return JsonResponse(monthly_stats.model_dump(), safe=False)


class PlanBasedStatsApiView(View):

    async def get(self, request, user_id: int, *args, **kwargs):
        candfans_user = await analyzer_sv.get_candfans_user_by_user_id(user_id)
        if not candfans_user:
            return JsonResponse({'error': 'not found'}, status=404)
        plan_based_stats, _ = await analyzer_sv.get_plan_based_stats(candfans_user)
        return JsonResponse(plan_based_stats.model_dump(), safe=False)


class DailyRankingApiView(View):

    async def get(self, request, user_id: int, *args, **kwargs):
        candfans_user = await analyzer_sv.get_candfans_user_by_user_id(user_id)
        if not candfans_user:
            return JsonResponse({'error': 'not found'}, status=404)
        daily_ranks = await analyzer_sv.get_daily_ranking_list_by_user_id(user_id)
        return JsonResponse({
            'labels': [r.day.isoformat() for r in daily_ranks.ranks],
            'datasets': [{
                'label': 'デイリー順位',
                'data': daily_ranks.formated_ranks,
            }],
        })
