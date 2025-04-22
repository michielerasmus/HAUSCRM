# documents/templatetags/custom_filters.py

from django import template
import os

register = template.Library()

@register.filter(name='filename')
def filename(value):
    """
    Custom filter to return the filename from a file path.
    """
    return os.path.basename(value)
