from candfans_client.models.timeline import Post

from ..models import CandfansPost, CandFansPostPlanRelation, CandfansPlan
from ..converter import convert_from_post_to_candfans_post


async def update_or_create_candfans_post(
        posts: list[Post]
) -> int:
    plan_ids = []
    for post in posts:
        plan_ids.extend([plan.plan_id for plan in post.plans])
    # to uniq
    plan_ids = list(set(plan_ids))
    related_plan_map = {p.plan_id: p for p in await CandfansPlan.get_list_by_plan_ids(plan_ids)}
    target_candfans_posts = [
        convert_from_post_to_candfans_post(p)
        for p in posts
    ]
    new_post_map = {
        new_post.post_id: new_post
        for new_post in await CandfansPost.bulk_update_or_create(
            target_candfans_posts,
        )
    }
    rels = []
    for post in posts:
        for plan in post.plans:
            rels.append(CandFansPostPlanRelation(
                candfans_plan=related_plan_map[plan.plan_id],
                candfans_post=new_post_map[post.post_id],
                backnumber_id=plan.backnumber_id
            ))
    rels = list(set(rels))
    await CandFansPostPlanRelation.bulk_create(rels)

    return len(new_post_map.items())
