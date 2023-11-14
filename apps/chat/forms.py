
from django import forms
from .models import RoomSettings

class RoomSettingsChangeForm(forms.ModelForm):

    class Meta:
        model  = RoomSettings
        fields = ('ai_icon',
                  'system_sentence',
                  'assistant_sentence',
                  'history_len',
                  'max_tokens',
                  'temperature',
                  'top_p',
                  'presence_penalty',
                  'frequency_penalty',
                  'comment',)