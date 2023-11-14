from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls.static import static

urlpatterns = [
     # admin
     path(settings.ADMIN_PATH+'/', admin.site.urls),
     # home
     path('', TemplateView.as_view(template_name='pages/home/home_base.html', extra_context={'IS_USE_NO_CONTAINER':True}), name='home'),
     # accounts
     path('accounts/', include('accounts.urls')),
     # apps
     path('inquiry/', include('apps.inquiry.urls')),
     path('chat/',    include('apps.chat.urls')),
     # ADD social-auth-app-django
     path('auth/', include('common.lib.social_django.urls', namespace='social')),
]
# 内部から静的メディアファイルを配信するための設定
if settings.DEBUG or not settings.IS_USE_GCS:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)