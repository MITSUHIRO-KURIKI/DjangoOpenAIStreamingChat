# from django.conf import settings

# # 登録できるメールアドレスを特定ドメインだけ許可する場合
# def custom_email_validater(email:str):
#     email_domain = email.split('@')[-1] if email else ''
#     if email_domain in settings.ALLOW_EMAIL_DOMAINS_LIST:
#         return True
#     else:
#         return False