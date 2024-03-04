import factory
from django.utils import timezone

from modules.analyzer.models import CandfansUser

from .base import AsyncMixin


class CandfansUserFactory(AsyncMixin, factory.django.DjangoModelFactory):

    class Meta:
        model = CandfansUser

    user_id = factory.Sequence(lambda n: n + 1)
    user_code = factory.Sequence(lambda n: f'user_{n}')
    user_name = factory.Sequence(lambda n: f'user_name_{n}')
    last_synced_at = None

    updated_at = timezone.now()
    created_at = timezone.now()
