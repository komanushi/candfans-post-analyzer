import factory
from modules.analyzer.models import CandfansUser


class CandfansUserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CandfansUser

    user_id = factory.Sequence(lambda n: n + 1)
    user_code = factory.Sequence(lambda n: f'user_{n}')
    user_name = factory.Sequence(lambda n: f'user_name_{n}')
    last_synced_at = None
