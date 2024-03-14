from candfans_client.models.timeline import Post
from pydantic import BaseModel


class PostMap(BaseModel):
    public_item: list[Post]
    limited_access_item: list[Post]
    individual_access_item: list[Post]
    back_number_item: list[Post]

    @property
    def all_posts(self):
        return (
                self.public_item
                + self.limited_access_item
                + self.individual_access_item
                + self.back_number_item
        )


class TimelinePosts(BaseModel):
    month: str
    post_map: PostMap
