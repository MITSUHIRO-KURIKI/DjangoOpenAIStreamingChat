from django.urls import path
from .views import UserProfileUpdateView, UserReceptionSettingsUpdateView
# accounts.urls 逆参照
app_name = 'user_properties'

urlpatterns = [
    path('',                        UserProfileUpdateView.as_view(),           name='user_profile'),
    path('user_reception_setting/', UserReceptionSettingsUpdateView.as_view(), name='user_reception_setting'),
]