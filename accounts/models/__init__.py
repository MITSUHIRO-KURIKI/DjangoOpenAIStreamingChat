from .CustomUser_models import CustomUser
from .ActivateToken_models import ActivateToken
from .receivers.CustomUserModel_receivers import (
    create_related_model_for_custom_user_model, send_token_for_activate_user,
)