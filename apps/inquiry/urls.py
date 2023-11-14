from django.urls import path
from .views import InquiryCreateView

app_name = 'inquiry'

urlpatterns = [
    path('', InquiryCreateView.as_view(), name='inquiry_form'),
]