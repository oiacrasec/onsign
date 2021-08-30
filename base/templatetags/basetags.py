# -*- coding: utf-8 -*-
from django import template
from django.forms.widgets import CheckboxInput

register = template.Library()


@register.filter(name='addcss')
def addcss(field, css):
    return field if isinstance(field.field.widget, CheckboxInput) else field.as_widget(attrs={"class": css})


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, CheckboxInput)
