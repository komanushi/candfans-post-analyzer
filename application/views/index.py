from django.shortcuts import render, redirect
from django.views import View

from modules.analyzer import service as analyzer_sv


class IndexView(View):
    async def get(self, request):
        # レコメンド
        user_list = await analyzer_sv.get_recently_synced_candfans_user_list_order_by_last_synced_at(10)
        return render(
            request,
            'index.j2',
            {'user_list': user_list},
        )

    async def post(self, request, *args, **kwargs):
        user_code = request.POST.get('user_code')
        if not user_code:
            return redirect('index')
        return redirect('candfans_user_request', user_code=user_code)
