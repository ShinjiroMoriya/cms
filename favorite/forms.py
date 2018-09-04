from django import forms
from feed_app.validator import ERROR_MESSAGES


class FavoriteForm(forms.Form):
    uuid = forms.UUIDField(required=True,
                           error_messages=ERROR_MESSAGES, )
    video_id = forms.IntegerField(required=True,
                                  error_messages=ERROR_MESSAGES, )
    lang = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES, )
