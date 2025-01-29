# store/templatetags/custom_filters.py

from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return value  # In case the values are not numbers


@register.filter
def apply_discount(price, discount_percentage):
    """Apply a discount percentage to the price."""
    try:
        discount_value = price * (discount_percentage / 100)
        final_price = price - discount_value
        return final_price
    except (TypeError, ValueError):
        return price  # In case of invalid values, return the original price
