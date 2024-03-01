from django.contrib import admin
from django.urls import path

from .views import candfans_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/<str:user_code>', candfans_user.CandfansRequestView.as_view())
]
