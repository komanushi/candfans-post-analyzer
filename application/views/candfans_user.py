from django.shortcuts import render
from django.views import View

from modules.analyzer import service as analyzer_sv


class CandfansRequestView(View):
    # メソッドの先頭にasyncを付ける
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
