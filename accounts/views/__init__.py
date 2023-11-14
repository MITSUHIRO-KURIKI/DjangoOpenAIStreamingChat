from .SignUp_view import (
    SignUpView, SignUpTmpReceptView, ActivateUserView,
)
from .LoginLogout_view import LogInView, LogoutView
from .AccountChange_views import (
    OverlapPasswordChangeView, OverlapPasswordChangeDoneView,
    OverlapPasswordResetView, OverlapPasswordResetDoneView, OverlapPasswordResetConfirmView,
    EmailChangeView, EmailChangeTmpReceptView, ActivateEmailView,
    UserDeleteView,
)
from .send_mail.send_mail import send_token_for_change_email