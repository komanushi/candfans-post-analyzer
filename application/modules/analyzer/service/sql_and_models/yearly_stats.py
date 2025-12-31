from collections import namedtuple

from submodule.sql import QueryModel
from ...domain_models import YearlyPostStats


query = """\
with aggregate_stats as (
    select
        EXTRACT(YEAR FROM to_date(month, 'YYYY-MM'))::text as year,
        sum((post_type=0)::int) as public_item,
        sum((post_type in (1, 3))::int) as plan_item,
        sum((post_type=2)::int) as individuai_item,
        sum((contents_type=1)::int) as photo_item,
        sum((contents_type=2)::int) as movie_item,
        sum(
            case
                when post_type in (1, 3) and is_free then 1
                else 0
            end
        ) as free_plan_item,
        sum(
            case
                when post_type in (1, 3) and (not is_free) then 1
                else 0
            end
        ) as paid_plan_item,
        sum(
            case
                when post_type = 2 then 0
                when contents_type = 2 and is_free then post.movie_time
                else 0
            end
        ) as free_movie_time_sec,
        sum(
            case
                when post_type = 2 then 0
                when contents_type = 2 and (not is_free) then post.movie_time
                else 0
            end
        ) as paid_movie_time_sec,
        sum(
            case
                when post_type = 2 then 0
                when contents_type = 1 and is_free then post.image_count
                else 0
            end
        ) as free_photo_count,
        sum(
            case
                when post_type = 2 then 0
                when contents_type = 1 and (not is_free) then post.image_count
                else 0
            end
        ) as paid_photo_count
    from (
        select
            post.*,
            string_agg(plan.plan_name, '|') as plan_names,
            case
                when post.post_type = 2 then false -- 単品販売
                when count(plan.plan_id) = 0 then true -- 公開投稿
                when sum((plan.support_price = 0)::int) > 0 then true -- 無料プランに紐づく
                else false
            end is_free
        from
            analyzer_candfanspost post
            left outer join
            analyzer_candfanspostplanrelation rel
            on
            post.post_id = rel.candfans_post_id
            left outer join
            analyzer_candfansplan plan
            on
            rel.candfans_plan_id = plan.plan_id
        where
            post.user_id = %s
        group by
            post.post_id
    ) post
    group by year
)
select
    year,
    COALESCE(public_item, 0) as public_item,
    COALESCE(plan_item, 0) as plan_item,
    COALESCE(individuai_item, 0) as individual_item,
    COALESCE(photo_item, 0) as photo_item,
    COALESCE(movie_item, 0) as movie_item,
    COALESCE(free_plan_item, 0) as free_plan_item,
    COALESCE(paid_plan_item, 0) as paid_plan_item,
    COALESCE(free_movie_time_sec, 0) as free_movie_time_sec,
    COALESCE(paid_movie_time_sec, 0) as paid_movie_time_sec,
    COALESCE(free_photo_count, 0) as free_photo_count,
    COALESCE(paid_photo_count, 0) as paid_photo_count
from
    aggregate_stats
order by
    year
"""


def row_to_model(row: namedtuple) -> YearlyPostStats:
    return YearlyPostStats(**row._asdict())


YearlyStatsQuery = QueryModel(
    query=query,
    row_to_model=row_to_model
)
