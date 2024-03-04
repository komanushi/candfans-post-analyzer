import factory

from modules.analyzer.domain_models import CandfansUserModel


class CandFansUserModelFactory(factory.Factory):
    class Meta:
        model = CandfansUserModel
    user_id = factory.Sequence(lambda n: n)
    user_code = factory.Sequence(lambda n: f"user{n}")
    username = factory.Faker('user_name')
    last_synced_at = None
