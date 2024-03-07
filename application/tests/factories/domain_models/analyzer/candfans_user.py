import factory

from modules.analyzer.domain_models import CandfansUserModel


class CandFansUserModelFactory(factory.Factory):
    class Meta:
        model = CandfansUserModel
    user_id = factory.Sequence(lambda n: n)
    user_code = factory.Sequence(lambda n: f"user{n}")
    username = factory.Faker('user_name')
    sync_status = None
    last_synced_at = None
    sync_requested_at = None
