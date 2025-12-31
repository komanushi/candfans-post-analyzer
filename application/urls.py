from django.urls import path
from .views import candfans_user, index


urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('django-rq/', include('django_rq.urls')),
    path(
        '', index.IndexView.as_view(),
        name='index',
    ),
    path(
        'user/<str:user_code>', candfans_user.CandfansRequestView.as_view(),
        name='candfans_user_request',
    ),
    path(
        'user/<str:user_code>/not_found', candfans_user.CandidatesUserNotFoundView.as_view(),
        name='candfans_user_not_found',
    ),
    path(
        'user/<str:user_code>/years/', candfans_user.CandfansUserLatestYearView.as_view(),
        name='candfans_user_latest_year',
    ),
    path(
        'user/<str:user_code>/years/<int:year>', candfans_user.CandfansUserYearSummaryView.as_view(),
        name='candfans_user_year_summary',
    ),
]
