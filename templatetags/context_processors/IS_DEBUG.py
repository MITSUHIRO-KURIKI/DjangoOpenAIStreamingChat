from django.conf import settings

def IS_DEBUG(request):
    return {"DEBUG": settings.DEBUG}