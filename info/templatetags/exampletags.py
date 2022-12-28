from django import template
from django.contrib.auth.models import User
from math import ceil, floor

register = template.Library()


@register.simple_tag
def mylength(value):
    return len(value)

@register.filter
def capt(value):
    return value.capitalize()


@register.inclusion_tag('includes/authors.html')
def author_list():
    authors = User.objects.filter(is_staff=False)
    return {'authors': authors}
    
    
@register.inclusion_tag('includes/stars.html')
def stars(value):
    value = float(value)
    full = floor(value)
    half = ceil(value - full)
    empty = 5 - (full + half)
    return {
        'full': range(full),
        'half': range(half),
        'empty': range(empty)
    }