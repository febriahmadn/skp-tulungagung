from django import template

register = template.Library()


@register.filter(name="range_bulan")
def range_bulan(value):
    return range(0, value)


@register.filter(name="add_row")
def add_row(value):
    return value + 4


@register.filter(name="add_satu")
def add_satu(value):
    return value + 1


@register.filter(name="format_rupiah")
def format_rupiah(value):
    nilai = str(value)
    if len(nilai) <= 3:
        return nilai
    else:
        p = nilai[-3:]
        q = nilai[:-3]
        return format_rupiah(q) + "." + p + ",00"


@register.filter(name="add_attr")
def add_attr(field, css):
    attrs = {}
    definition = css.split(",")
    for d in definition:
        c = d.split("=")
        attrs[c[0]] = c[1]

    return field.as_widget(attrs=attrs)


@register.filter(name="dir")
def dir(fild):
    return fild
