# your_app/templatetags/custom_filters.py
from django import template
from django.utils.formats import localize
register = template.Library()



@register.filter
def format_currency(value, currency_symbol):
    return f"{value:,.2f} {currency_symbol}"