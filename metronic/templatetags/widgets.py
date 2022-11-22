from django import forms
from django import template

# from django.utils.html import format_html
# from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name="addcls")
def addcls(field, css):
    if hasattr(field, "as_widget"):
        return field.as_widget(attrs={"class": css})
    else:
        return None


@register.filter(name="atribut")
def atribut(field_, attr_):
    if hasattr(field_, "as_widget"):
        attrs = {}
        attrs_from_str = attr_.split("|")
        for attr in attrs_from_str:
            k_, v_ = attr.split(":")
            attrs.update({k_: v_})
        return field_.as_widget(attrs=attrs)
    else:
        return None


@register.filter("is_select")
def is_select(field):
    if isinstance(field.field.widget, forms.RadioSelect) or isinstance(
        field.field.widget, forms.widgets.CheckboxSelectMultiple
    ):
        return False
    name = str(field.field.widget.__class__.__name__)
    isinstance_ = isinstance(field.field.widget, forms.Select)
    return (
        isinstance_ or name == "RelatedFieldWidgetWrapper"
    )


@register.filter("is_date")
def is_date(field):
    return isinstance(field.field.widget, forms.DateInput)


@register.filter("is_datetime")
def is_datetime(field):
    return isinstance(field.field.widget, forms.SplitDateTimeWidget)


@register.filter("is_time")
def is_time(field):
    return isinstance(field.field.widget, forms.TimeInput)


@register.filter("is_file")
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter("is_bool")
def is_bool(field):
    # if "file" in field:
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter("is_readonlypassword")
def is_readonlypassword(field):
    from django.contrib.auth.forms import ReadOnlyPasswordHashWidget

    return isinstance(field.field.widget, ReadOnlyPasswordHashWidget)


@register.filter(name="get_filter_choices")
def get_filter_choices(spec, cl):
    if spec:
        return list(spec.choices(cl))
    else:
        return ()


@register.filter(name="lookup")
def lookup(value, arg):
    return value[arg]
