from collections import namedtuple

from submodule.sql import QueryModel
from ...domain_models import PostTypeStat

query = """\
select
    sum((post_type=0)::int) as PUBLIC_ITEM,
    sum((post_type=1)::int) as LIMITED_ACCESS_ITEM,
    sum((post_type=2)::int) as INDIVIDUAL_ITEM,
    sum((post_type=3)::int) as BACK_NUMBER_ITEM
from
    analyzer_candfanspost
where
    user_id = %s
"""


def post_type_stat_factory(row: namedtuple) -> PostTypeStat:
    return PostTypeStat(**row._asdict())


TotalPostTypeStatsQuery = QueryModel(
    query=query,
    row_to_model=post_type_stat_factory
)
