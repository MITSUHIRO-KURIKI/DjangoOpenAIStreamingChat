from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from ..models import UserProfile, UserReceptionSetting

User = get_user_model()


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    
    template_name = 'apps/user_properties/Settings/user_profile.html'
    model         = UserProfile
    fields        = ['display_name','user_icon',]
    success_url   = reverse_lazy('accounts:user_properties:user_profile')

    def get_object(self):
        return get_object_or_404(self.model, unique_account_id=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'IS_USE_SIDENAV': True,
        })
        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             f'変更完了',)
        return self.success_url

class UserReceptionSettingsUpdateView(LoginRequiredMixin, UpdateView):
    
    model         = UserReceptionSetting
    fields        = ['is_receive_all','is_receive_important_only',]
    template_name = 'apps/user_properties/Settings/user_reception_setting.html'
    success_url   = reverse_lazy('accounts:user_properties:user_reception_setting')

    def get_object(self):
        return get_object_or_404(self.model, unique_account_id=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'IS_USE_SIDENAV': True,
        })
        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             f'変更完了',)
        return self.success_url