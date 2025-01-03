# your_app/templatetags/custom_filters.py
from django import template
from django.utils.formats import localize
from datetime import timedelta
register = template.Library()




@register.filter
def add_hours(value, hours):
    if value:
        return value + timedelta(hours=int(hours))
    return value
