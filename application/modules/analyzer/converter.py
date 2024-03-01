from .models import CandfansUser
from .domain_models import CandfansUserModel


def convert_to_candfans_user_model(user: CandfansUser) -> CandfansUserModel:
    return CandfansUserModel(
        user_id=user.user_id,
        user_code=user.user_code,
        user_name=user.user_name,
        last_synced_at=user.last_synced_at,
    )
