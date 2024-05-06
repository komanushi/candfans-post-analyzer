from collections import namedtuple

from submodule.sql import QueryModel
from ...domain_models import PlanStats


query = """\
with calendar as (
    select
        month as month_date,
        to_char(month, 'YYYY-MM') as month_str
    from
    (
        select
            generate_series(start_date, end_date, '1 month') as month
        from
            (
                select
                    to_date(min(month), 'YYYY-MM') as start_date,
                    to_date(max(month), 'YYYY-MM') as end_date
                from
                    analyzer_candfanspost
                where
                    user_id = %s
            ) t
    ) t2
),
plan as (
    select
        plan_id,
        plan_name,
        support_price,
        backnumber_price
    from
        analyzer_candfansplan
    where
        user_id = %s
),
post as (
    select
        plan.plan_name,
        plan.plan_id,
        plan.support_price,
        rel.backnumber_id,
        min(plan.support_price) over (partition by post_id) as min_price,
        post.*
    from
        analyzer_candfanspost post
        join
        analyzer_candfanspostplanrelation rel
        on
        post.post_id = rel.candfans_post_id
        join
        plan
        on
        rel.candfans_plan_id = plan.plan_id
    where
        post_type in (1, 3)
),
free_plan_stats as (
    select
        month,
        plan_name,
        plan_id,
        count(*) as total_post_count,
        sum((backnumber_id is null)::int) as plan_post_count,
        sum((backnumber_id is not null)::int) as backnumber_post_count,
        sum((backnumber_id is null and contents_type = 2)::int) as plan_movie_post_count,
        sum((backnumber_id is not null and contents_type = 2)::int) as backnumber_movie_post_count,
        sum((backnumber_id is null and contents_type = 1)::int) as plan_photo_post_count,
        sum((backnumber_id is not null and contents_type = 1)::int) as backnumber_photo_post_count,
        sum(
            case
                when backnumber_id is null and contents_type = 2 then post.movie_time
                else 0
            end
        ) as plan_movie_time_sec,
        sum(
            case
                when backnumber_id is not null and contents_type = 2 then post.movie_time
                else 0
            end
        ) as backnumber_movie_time_sec,
        sum(
            case
                when backnumber_id is null and contents_type = 1 then post.image_count
                else 0
            end
        ) as plan_photo_count,
        sum(
            case
                when backnumber_id is not null and contents_type = 1 then post.image_count
                else 0
            end
        ) as backnumber_photo_count
    from
        post
    where
        min_price = 0
        and
        support_price = 0
    group by
        month, plan_name, plan_id
    order by
        month, plan_name
),
paid_plan_stats as (
    select
        month,
        plan_name,
        plan_id,
        count(*) as total_post_count,
        sum((backnumber_id is null)::int) as plan_post_count,
        sum((backnumber_id is not null)::int) as backnumber_post_count,
        sum((backnumber_id is null and contents_type = 2)::int) as plan_movie_post_count,
        sum((backnumber_id is not null and contents_type = 2)::int) as backnumber_movie_post_count,
        sum((backnumber_id is null and contents_type = 1)::int) as plan_photo_post_count,
        sum((backnumber_id is not null and contents_type = 1)::int) as backnumber_photo_post_count,
        sum(
            case
                when backnumber_id is null and contents_type = 2 then post.movie_time
                else 0
            end
        ) as plan_movie_time_sec,
        sum(
            case
                when backnumber_id is not null and contents_type = 2 then post.movie_time
                else 0
            end
        ) as backnumber_movie_time_sec,
        sum(
            case
                when backnumber_id is null and contents_type = 1 then post.image_count
                else 0
            end
        ) as plan_photo_count,
        sum(
            case
                when backnumber_id is not null and contents_type = 1 then post.image_count
                else 0
            end
        ) as backnumber_photo_count
    from
        post
    where
        min_price > 0
    group by
        month, plan_name, plan_id
    order by
        month,
        min(support_price)
),
aggregate_stats as (
    select * from free_plan_stats
    union
    select * from paid_plan_stats
)
select
    calendar.month_str as month,
    plan.plan_name,
    plan.plan_id,
    plan.support_price,
    plan.backnumber_price,
    COALESCE(total_post_count, 0) as total_post_count,
    COALESCE(plan_post_count, 0) as plan_post_count,
    COALESCE(backnumber_post_count, 0) as backnumber_post_count,
    COALESCE(plan_movie_post_count, 0) as plan_movie_post_count,
    COALESCE(backnumber_movie_post_count, 0) as backnumber_movie_post_count,
    COALESCE(plan_movie_time_sec, 0) as plan_movie_time_sec,
    COALESCE(backnumber_movie_time_sec, 0) as backnumber_movie_time_sec,
    COALESCE(plan_photo_post_count, 0) as plan_photo_post_count,
    COALESCE(backnumber_photo_post_count, 0) as backnumber_photo_post_count,
    COALESCE(plan_photo_count, 0) as plan_photo_count,
    COALESCE(backnumber_photo_count, 0) as backnumber_photo_count
from
    calendar
    cross join
    plan
    left outer join
    aggregate_stats
    on
    calendar.month_str = aggregate_stats.month
    and
    plan.plan_id = aggregate_stats.plan_id
order by
    month,
    support_price desc,
    plan_name
"""

"""
-[ RECORD 1 ]-------------------------
month_str                   | 2023-10
plan_name                   | plan_1
total_post_count            | 0
plan_post_count             | 0
backnumber_post_count       | 0
plan_movie_post_count       | 0
backnumber_movie_post_count | 0
plan_movie_time_sec         | 0.0
backnumber_movie_time_sec   | 0.0
plan_photo_post_count       | 0
backnumber_photo_post_count | 0
plan_photo_count            | 0
backnumber_photo_count      | 0
-[ RECORD 2 ]-------------------------
month_str                   | 2023-10
plan_name                   | plan_2
total_post_count            | 4
plan_post_count             | 4
backnumber_post_count       | 0
plan_movie_post_count       | 0
backnumber_movie_post_count | 0
plan_movie_time_sec         | 0.0
backnumber_movie_time_sec   | 0.0
plan_photo_post_count       | 4
backnumber_photo_post_count | 0
plan_photo_count            | 16
backnumber_photo_count      | 0
-[ RECORD 3 ]-------------------------
month_str                   | 2023-10
plan_name                   | plan_3
total_post_count            | 0
plan_post_count             | 0
backnumber_post_count       | 0
plan_movie_post_count       | 0
backnumber_movie_post_count | 0
plan_movie_time_sec         | 0.0
backnumber_movie_time_sec   | 0.0
plan_photo_post_count       | 0
backnumber_photo_post_count | 0
plan_photo_count            | 0
backnumber_photo_count      | 0

"""

def row_to_model(row: namedtuple) -> PlanStats:
    return PlanStats(**row._asdict())


PlanBasedStatsQuery = QueryModel(
    query=query,
    row_to_model=row_to_model
)
