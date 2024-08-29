from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    old, new = arg.split(',')
    return value.replace(old, new)



@register.filter
def custom_range(value, arg):
    try:
        start, end = map(int, arg.split(','))
        return start <= value <= end
    except (ValueError, TypeError):
        return False


@register.filter
def ranges(value):
    return range(value)


@register.filter
def get_item(list, id):
    for item in list:
        if item.booth.id == id:
            return item
    return None