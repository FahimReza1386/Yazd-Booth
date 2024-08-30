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



@register.filter
def get_booth_image(booth_id, images):
    for img in images:
        if img.booth.id == booth_id:
            return img.image.url
    return None  # مسیر تصویر پیش‌فرض

@register.filter
def get_product_image(product, images):
    for img in images:
        if img.product and img.product.id == product.id:
            return img.image.url
    return None  # مسیر تصویر پیش‌فرض