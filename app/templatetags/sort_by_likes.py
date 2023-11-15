from django import template

register = template.Library()

@register.filter() 
def sort_by_likes(value):
    return list(value).sort(key=lambda question: len(list(filter(lambda n: n.is_like == True, list(question.question_likes))))) 