import os, django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django_asgi_app = get_asgi_application()

# MUST BOTTOM get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from apps.chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    'http': django_asgi_app,
    
    # WebSocket chat handler
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
