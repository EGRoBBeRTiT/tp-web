from django import template

register = template.Library()

@register.filter() 
def items_length(value, arg):
    return len(list(filter(lambda n: n.is_like == arg, list(value))))