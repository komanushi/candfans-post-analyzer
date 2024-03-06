from candfans_client.models.timeline import Post
from pydantic import BaseModel


class PostMap(BaseModel):
    public_item: list[Post]
    limited_access_item: list[Post]
    individual_access_item: list[Post]


class TimelinePosts(BaseModel):
    month: str
    post_map: PostMap
