import factory
from django.utils import timezone

from modules.analyzer.models import CandFansPostPlanRelation

from .base import AsyncMixin
from .candfans_post import CandfansPostFactory
from .candfans_plan import CandfansPlanFactory


class CandFansPostPlanRelationFactory(AsyncMixin, factory.django.DjangoModelFactory):

    class Meta:
        model = CandFansPostPlanRelation

    candfans_plan = factory.SubFactory(CandfansPlanFactory)
    candfans_post = factory.SubFactory(CandfansPostFactory)
    backnumber_id = None

    updated_at = timezone.now()
    created_at = timezone.now()
