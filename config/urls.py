from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls.static import static

urlpatterns = [
     # admin
     path(settings.ADMIN_PATH+'/', admin.site.urls),
     # home
     path('', TemplateView.as_view(template_name='pages/home/home_base.html', extra_context={'IS_NO_USE_CONTEINER':True}), name='home'),
     # accounts
     path('accounts/', include('accounts.urls')),
     # apps
     path('inquiry/', include('apps.inquiry.urls')),
     path('chat/',    include('apps.chat.urls')),
]
# ADD social-auth-app-django
if settings.IS_USE_SOCIAL_LOGIN:
     urlpatterns += [path('auth/', include('common.lib.social_django.urls', namespace='social')),]
# 内部から静的メディアファイルを配信するための設定
if not settings.IS_USE_GCS:
    import os
    from django.conf.urls.static import static
    from django.urls import re_path
    from django.views.static import serve
    # 内部 static を配信する
    urlpatterns += [ re_path(r'^static/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'static/')}, name='static_urlpattern') ]
    urlpatterns += [ re_path(r'^media/(?P<path>.*)$',  serve, {'document_root': os.path.join(settings.BASE_DIR, 'media/')},  name='media_urlpattern') ]
    if settings.DEBUG:
        # media を利用
        urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
        urlpatterns += [
            path('test_404/', TemplateView.as_view(template_name='404.html',)),
        ]