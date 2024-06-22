from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from ..models import ActivateToken

# TokenDeleteView
def TokenDeleteView(request, token):
    logout(request)
    res, msg = ActivateToken.objects.token_delete(token)
    if res:
        messages.add_message(request, messages.INFO, msg)
        return redirect('accounts:token_delete_success')
    else:
        messages.add_message(request, messages.WARNING, msg)
        return redirect('accounts:token_delete_failure')