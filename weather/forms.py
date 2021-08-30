# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from onsign.constants import NOT_ALLOWED_CARACTERS_GOOGLE

from .models import Tracker


class TrackerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TrackerForm, self).__init__(*args, **kwargs)
        self.fields['location'] = forms.CharField(
            label='Location',
            help_text='You can enter any type of content, such as name of the city or zipcode',
            max_length=30,
            widget=forms.TextInput()
        )

    def clean_location(self):
        data = self.cleaned_data['location']
        if all(element in list(data) for element in NOT_ALLOWED_CARACTERS_GOOGLE):
            raise ValidationError(_('Invalid input: %(value)s'), code='invalid', params={'value': data})
        return data

    class Meta:
        model = Tracker
        fields = '__all__'
