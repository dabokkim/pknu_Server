import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter # 레지스터 필터로 사용할것이라 선언(어노테이션)
def sub(value, arg) : # 템플릿 필터로 사용됨
    return value - arg

@register.filter
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions)) # mark_safe : 입력한 값을 html로 변환하는 함수