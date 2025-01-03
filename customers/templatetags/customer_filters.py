# your_app/templatetags/custom_filters.py
from django import template
from django.utils.formats import localize
register = template.Library()

@register.filter
def add_class(value, css_class):
    return value.as_widget(attrs={'class': css_class})



@register.filter
def format_currency(value, currency_symbol):
    return f"{value:,.2f} {currency_symbol}"


@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})

