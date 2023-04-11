from django import template

register = template.Library()

@register.filter
def by_user(qset, user):
    return qset.filter(user=user)

@register.filter
def get_first_answer(qset):
    first = qset.first()
    if (first): return first.answer
    else: return "No Answer"