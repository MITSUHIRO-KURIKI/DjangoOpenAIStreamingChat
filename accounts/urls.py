from django.urls import include, path
from .views import (
    SignUpView, SignUpTmpReceptView, ActivateUserView,
    LogInView, LogoutView,
    OverlapPasswordChangeView, OverlapPasswordChangeDoneView,
    OverlapPasswordResetView, OverlapPasswordResetDoneView, OverlapPasswordResetConfirmView,
    EmailChangeView, EmailChangeTmpReceptView, ActivateEmailView,
    UserDeleteView,
)

app_name = 'accounts'

urlpatterns = [
    # サインアップ
    path('signup/',                    SignUpView.as_view(),          name='signup'),
    path('signup/tmp_recept/',         SignUpTmpReceptView.as_view(), name='signup_tmp_recept'),
    path('activate_user/<str:token>/', ActivateUserView,              name='activate_user'),
    # ログイン/ログアウト処理
    path('login/',  LogInView.as_view(),  name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # パスワード変更
    path('password_change/',      OverlapPasswordChangeView.as_view(),     name='password_change'),
    path('password_change/done/', OverlapPasswordChangeDoneView.as_view(), name='password_change_done'),
    # パスワード再設定
    path('password_reset/',         OverlapPasswordResetView.as_view(),        name='password_reset'),
    path('password_reset/done/',    OverlapPasswordResetDoneView.as_view(),    name='password_reset_done'),
    path('reset/<uidb64>/<token>/', OverlapPasswordResetConfirmView.as_view(), name='password_reset_confilm'),
    # メールアドレスの変更
    path('email_change/',               EmailChangeView.as_view(),          name='email_change'),
    path('email_change/tmp_recept/',    EmailChangeTmpReceptView.as_view(), name='email_change_tmp_recept'),
    path('activate_email/<str:token>/', ActivateEmailView,                  name='email_change_confilm'),
    # アカウントの削除
    path('delete/', UserDeleteView.as_view(), name='delete'),
    # 外部 urls.py 参照
    path('', include('apps.user_properties.urls', namespace='user_properties')),
]