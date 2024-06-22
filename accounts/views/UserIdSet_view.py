from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

User = get_user_model()


class UserIdSetView(LoginRequiredMixin, UpdateView):

    template_name = 'accounts/UserIdSet/user_id_set.html'
    model         = User
    fields        = ['unique_user_id',]
    success_url   = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.unique_user_id is None or request.user.unique_user_id == ''):
            return super().get(request, *args, **kwargs)
        raise Http404('Page not found')

    def get_object(self):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             f'設定完了',)
        return self.success_url