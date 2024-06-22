from .SignUp_view import (
    SignUpView, SignUpTmpReceptView, ActivateUserView,
)
from .LoginLogout_view import OverlapLoginView, OverlapLogoutView
from .AccountChange_views import (
    OverlapPasswordChangeView, OverlapPasswordChangeOneStepView, OverlapPasswordChangeDoneView,
    OverlapPasswordResetView, OverlapPasswordResetDoneView, OverlapPasswordResetConfirmView,
    EmailChangeView, EmailChangeTmpReceptView, ActivateEmailView,
    UserDeleteView,
)
from .TokenDelete_view import TokenDeleteView
from .UserIdSet_view import UserIdSetView
from .send_mail.send_mail import send_token_for_change_email