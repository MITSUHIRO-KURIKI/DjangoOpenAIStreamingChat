from django.conf import settings

def FRONTEND_URL(request):
    return {"FRONTEND_URL": settings.FRONTEND_URL}