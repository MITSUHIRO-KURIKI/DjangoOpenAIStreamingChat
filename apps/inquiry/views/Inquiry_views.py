from django.conf import settings
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from common.scripts import grecaptcha_request, RequestUtil
from ..models import Inquiry

class InquiryCreateView(CreateView):
    
    template_name = 'apps/inquiry/inquiry_form/form.html'
    model         = Inquiry
    fields        = ['email','inquiry_text',]
    success_url   = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY if settings.IS_USE_RECAPTCHA else None,
            'IS_USE_RECAPTCHA': settings.IS_USE_RECAPTCHA,
        })
        return context

    # reCaptcha_token の検証
    def post(self, request, *args, **kwargs):
        # reCaptcha_token の検証▽
        if settings.IS_USE_RECAPTCHA:
            recaptcha_token = self.request.POST.get('g-recaptcha-response')
            if recaptcha_token is None or recaptcha_token == '':
                messages.add_message(self.request, messages.WARNING,
                                     f'不正なPOSTです - reCaptcha ERROR',)
                # reCaptcha ERROR の場合に入力された内容を返す
                request.session['invalid_inquiry_text_data'] = self.request.POST['inquiry_text']
                reverse_url = reverse_lazy('inquiry:inquiry_form')
                return HttpResponseRedirect(reverse_url)
            else:
                res = grecaptcha_request(recaptcha_token)
                if res:  # reCaptcha SUCCESS
                    return super().post(request, *args, **kwargs)
                else:    # reCaptcha FALSE
                    messages.add_message(self.request, messages.WARNING,
                                         f'不正なPOSTです - reCaptcha ERROR',)
                    # reCaptcha ERROR の場合に入力された内容を返す
                    request.session['invalid_inquiry_text_data'] = self.request.POST['inquiry_text']
                    reverse_url = reverse_lazy('inquiry:inquiry_form')
                    return HttpResponseRedirect(reverse_url)
        else:
            return super().post(request, *args, **kwargs)
        # reCaptcha_token の検証△

    def form_valid(self, form):
        form.instance.ip_address = RequestUtil.get_ip(self)
        # 問い合わせ者
        if self.request.user.is_anonymous:
            form.instance.unique_account_id = None
        else:
            form.instance.unique_account_id = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        # invalid の場合に入力された内容を返す
        context.update({
            'invalid_inquiry_text_data': self.request.POST['inquiry_text'],
        })
        return self.render_to_response(context)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             f'お問い合わせを受け付けました',)
        return self.success_url