from candfans_client.async_client import AsyncAnonymousCandFansClient


async def get_candfans_user_info_by_user_code(user_code: str):
    client = AsyncAnonymousCandFansClient()
    candfans_user_info = await client.get_users(user_code=user_code)
    return candfans_user_info
