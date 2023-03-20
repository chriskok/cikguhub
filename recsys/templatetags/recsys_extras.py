from django import template

register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def get_question(obj):
    return obj.question

@register.filter()
def to_int(value):
    return int(value) 