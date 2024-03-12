import factory
from modules.analyzer.domain_models import CandfansPlanModel
from .candfans_user import CandFansUserModelFactory


class CandfansPlanModelFactory(factory.Factory):
    class Meta:
        model = CandfansPlanModel

    plan_id = factory.Sequence(lambda n: n)
    user = factory.SubFactory(CandFansUserModelFactory)
    thanks_message_template_id = factory.Sequence(lambda n: n)
    plan_name = factory.Faker('word')
    support_price = factory.Faker('random_int')
    total_support_price = factory.Faker('random_int')
    plan_detail = factory.Faker('sentence')
    r18 = factory.Faker('random_int')
    status = factory.Faker('random_int')
    fans_cnt = factory.Faker('random_int')
    is_fans = factory.Faker('boolean')
    is_price_update = factory.Faker('random_int')
    change_support_price = factory.Faker('random_int')
    content_length = factory.Faker('random_int')
    delete_at = factory.Faker('future_datetime', end_date="+30d")
    backnumber_price = factory.Faker('random_int')
    limit_after_backnumber = factory.Faker('random_int')
    this_month_after_backnumber = factory.Faker('random_int')
    can_see_backnumber_plan_pay = factory.Faker('boolean')
    can_buy_backnumber_not_entry_plan = factory.Faker('boolean')
    done_transfar_backnumber = factory.Faker('boolean')
    done_transfar_limit_backnumber = factory.Faker('boolean')
    entry_disabled = factory.Faker('boolean')
    upper_limit_entry_cnt = factory.Faker('random_int')
