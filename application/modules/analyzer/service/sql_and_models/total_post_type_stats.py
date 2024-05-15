from collections import namedtuple

from submodule.sql import QueryModel
from ...domain_models import PostTypeStat

query = """\
select
    coalesce(sum((post_type=0)::int), 0) as PUBLIC_ITEM,
    coalesce(sum((post_type=1)::int), 0) as LIMITED_ACCESS_ITEM,
    coalesce(sum((post_type=2)::int), 0) as INDIVIDUAL_ITEM,
    coalesce(sum((post_type=3)::int), 0) as BACK_NUMBER_ITEM
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
