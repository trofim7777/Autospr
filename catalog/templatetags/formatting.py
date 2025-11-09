from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()

@register.filter
def spaced_money(value):
    """
    10299500    -> '10 299 500'
    10299500.00 -> '10 299 500'
    10299500.5  -> '10 299 500.5'
    """
    if value is None or value == "":
        return ""
    try:
        d = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return value

    # форматируем с разделителями тысяч и убираем .00
    s = f"{d:,.2f}".replace(",", " ")
    if s.endswith(".00"):
        s = s[:-3]
    return s
