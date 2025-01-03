# your_app/templatetags/custom_filters.py
from django import template
from django.utils.formats import localize
from datetime import timedelta
register = template.Library()

@register.filter
def add_class(value, css_class):
    return value.as_widget(attrs={'class': css_class})



@register.filter
def format_currency(value, currency_symbol):
    return f"{value:,.2f} {currency_symbol}"





@register.filter
def add_hours(value, hours):
    if value:
        return value + timedelta(hours=int(hours))
    return value
