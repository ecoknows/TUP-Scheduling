from django import template

register = template.Library()

@register.filter(name='getColor')
def getColor(value, args):
    print(value[args])
    return value[args]