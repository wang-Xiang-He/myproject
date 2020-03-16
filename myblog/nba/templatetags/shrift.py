from django import template
register = template.Library()

from zhconv import convert

# 獲取相對時間
@register.filter(name='shrift')
def shrift(value):
    values = convert(value, 'zh-tw')
    return values


