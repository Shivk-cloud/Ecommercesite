from django import template

register = template.Library()

# @register.filter(name='currency')
# def currency(number):
#     return "₹"+str(number)


@register.filter(name='currency')
def currency(value):
    return f"₹{value:.2f}"