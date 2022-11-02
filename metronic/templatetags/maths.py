from django import template
from datetime import timedelta

register = template.Library()


@register.filter(name="timedelta_jam")
def timedelta_jam(timedelta_):
    tjk = timedelta_.total_seconds() / 3600
    return str(tjk)


@register.simple_tag
def zero_timedelta():
    return timedelta(0)


@register.simple_tag
def adding(a_, b_):
    t = a_ + b_
    return t


@register.simple_tag
def adding_number(a_, b_):
    try:
        a_ = int(a_)
    except ValueError:
        a_ = 0
    t = int(a_) + int(b_)
    return t


@register.simple_tag
def mod(a_, b_):
    t = a_ % b_
    return t


@register.simple_tag
def sub(a_, b_):
    t = a_ - b_
    return t


@register.simple_tag
def mul(a_, b_):
    t = a_ * b_
    return t


@register.filter(name="get_range")
def get_range(a_):
    return range(a_)


@register.filter(name="range")
def filter_range(start, end):
    print(start)
    return range(start, end)
