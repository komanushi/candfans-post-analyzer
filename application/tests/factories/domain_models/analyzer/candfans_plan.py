import factory
from modules.analyzer.domain_models import CandfansPlanModel


class CandfansPlanModelFactory(factory.Factory):
    class Meta:
        model = CandfansPlanModel

    plan_id = factory.Sequence(lambda n: n)
    support_price = factory.Faker('random_int')
    total_support_price = factory.Faker('random_int')
    plan_name = factory.Faker('sentence', nb_words=3)
    plan_detail = factory.Faker('text')

    backnumber_id = factory.Faker('random_int')
    backnumber_price = factory.Faker('random_int')
    total_backnumber_price = factory.Faker('random_int')

    can_see_backnumber_plan_pay = factory.Faker('boolean')
    can_buy_backnumber_not_entry_plan = factory.Faker('boolean')
    add_backnumber_date = None
