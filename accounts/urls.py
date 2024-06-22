from django.urls import include, path
from django.views.generic import TemplateView
from .views import (
    SignUpView, SignUpTmpReceptView, ActivateUserView,
    OverlapLoginView, OverlapLogoutView, TokenDeleteView,
    OverlapPasswordChangeView, OverlapPasswordChangeOneStepView, OverlapPasswordChangeDoneView,
    OverlapPasswordResetView, OverlapPasswordResetDoneView, OverlapPasswordResetConfirmView,
    EmailChangeView, EmailChangeTmpReceptView, ActivateEmailView,
    UserDeleteView, UserIdSetView,
)

app_name = 'accounts'

urlpatterns = [
    # サインアップ
    path('signup/',                    SignUpView.as_view(),          name='signup'),
    path('signup/tmp_recept/',         SignUpTmpReceptView.as_view(), name='signup_tmp_recept'),
    path('activate_user/<str:token>/', ActivateUserView,              name='activate_user'),
    # ユーザIDの設定
    path('signup/set_user_id', UserIdSetView.as_view(), name='uset_ser_id'),
    # ログイン/ログアウト処理
    path('login/',  OverlapLoginView.as_view(),  name='login'),
    path('logout/', OverlapLogoutView.as_view(), name='logout'),
    # パスワード変更
    path('password_change/',      OverlapPasswordChangeView.as_view(),        name='password_change'),
    path('password_change_/',     OverlapPasswordChangeOneStepView.as_view(), name='password_change_one_step'),
    path('password_change/done/', OverlapPasswordChangeDoneView.as_view(),    name='password_change_done'),
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
    # # トークンの破棄(見の覚えのないメールが届いた方用)
    path('token_delete/<str:token>/', TokenDeleteView,                                                                name='token_delete'),
    path('token_delete_s/',           TemplateView.as_view(template_name='accounts/TokenDelete/delete_success.html'), name='token_delete_success'),
    path('token_delete_f/',           TemplateView.as_view(template_name='accounts/TokenDelete/delete_failure.html'), name='token_delete_failure'),
    # 外部 urls.py 参照
    path('', include('apps.user_properties.urls', namespace='user_properties')),
]