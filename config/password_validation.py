from django.core.exceptions import ValidationError
from string import ascii_letters, ascii_uppercase, ascii_lowercase, digits

def contain_any(target, condition_list):
    return any([i in target for i in condition_list])

class CustomValidator01:
    message = "パスワードは(大小英字、数字)全てを組み合わせて設定してください。"
    def validate(self, password, user=None):
        if not all([contain_any(password, ascii_lowercase),
                    contain_any(password, ascii_uppercase),
                    contain_any(password, digits)]):
            raise ValidationError(self.message)
    def get_help_text(self):
        return self.message

class CustomValidator02:
    message = "パスワードは英数字を組み合わせて設定してください。"
    def validate(self, password, user=None):
        if not all([contain_any(password, ascii_letters),
                    contain_any(password, digits)]):
            raise ValidationError(self.message)
    def get_help_text(self):
        return self.message