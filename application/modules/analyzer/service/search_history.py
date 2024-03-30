from ..models import SearchHistory


async def create_search_history(user_code: str):
    await SearchHistory.create(
        user_code=user_code
    )
