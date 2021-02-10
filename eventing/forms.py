from django import forms
from eventing.models import Event


class EventSearchForm(forms.Form):
    event_title = forms.CharField(label='عنوان رویداد', max_length=200, required=False)
    event_NOT_START = forms.BooleanField(label='فقط رویدادهای شروع نشده', required=False)
    subject_choices = Event.subject_choices
    event_subject = forms.ChoiceField(label='موضوع رویداد', choices=subject_choices, required=False)
