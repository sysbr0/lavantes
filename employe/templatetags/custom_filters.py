# employe/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def key(d, key_name):
    """
    Custom template filter to fetch value from dictionary based on key.
    """
    try:
        return d[key_name]
    except KeyError:
        return None
    except TypeError:
        return None
