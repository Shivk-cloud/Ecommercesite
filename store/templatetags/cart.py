from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    return str(product.id) in cart

@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    if cart:
        quantity = cart.get(str(product.id))
        if quantity:
            return quantity
    return 0

@register.filter(name='price_total')
def price_total(product, cart):
    return product.price * cart_quantity(product, cart)


@register.filter(name='total_cart_price')
def total_cart_price(products, cart):
    total = 0
    for product in products:
        total += price_total(product, cart)
    return total