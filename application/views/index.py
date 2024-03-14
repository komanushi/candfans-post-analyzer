from django.shortcuts import render, redirect
from django.views import View


class IndexView(View):
    def get(self, request):
        return render(
            request,
            'index.j2',
        )

    def post(self, request, *args, **kwargs):
        user_code = request.POST.get('user_code')
        return redirect('candfans_user_request', user_code=user_code)