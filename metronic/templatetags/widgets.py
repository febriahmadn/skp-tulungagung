from django import forms
from django import template
# from django.utils.html import format_html
# from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name='addcls')
def addcls(field, css):
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={"class": css})
    else:
        return None


@register.filter(name='atribut')
def atribut(field_, attr_):
    if hasattr(field_, 'as_widget'):
        attrs = {}
        attrs_from_str = attr_.split("|")
        for attr in attrs_from_str:
            k_, v_ = attr.split(":")
            attrs.update({k_: v_})
        return field_.as_widget(attrs=attrs)
    else:
        return None


@register.filter('is_select')
def is_select(field):
    if isinstance(field.field.widget, forms.RadioSelect) or isinstance(field.field.widget, forms.widgets.CheckboxSelectMultiple):
        return False
    return isinstance(field.field.widget, forms.Select) or str(field.field.widget.__class__.__name__) == 'RelatedFieldWidgetWrapper'


@register.filter('is_date')
def is_date(field):
    return isinstance(field.field.widget, forms.DateInput)


@register.filter('is_datetime')
def is_datetime(field):
    return isinstance(field.field.widget, forms.SplitDateTimeWidget)


@register.filter('is_time')
def is_time(field):
    return isinstance(field.field.widget, forms.TimeInput)


@register.filter('is_file')
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter('is_readonlypassword')
def is_readonlypassword(field):
    from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
    return isinstance(field.field.widget, ReadOnlyPasswordHashWidget)


@register.filter(name='get_filter_choices')
def get_filter_choices(spec, cl):
    if spec:
        return list(spec.choices(cl))
    else:
        return ()


@register.filter(name='total_dispen')
def total_dispen(unitkerja):
    return 0


@register.filter(name='get_uk')
def get_uk(value):
    if value:
        try:
            uk_obj = UnitKerja.objects.get(pk=value)
            value = uk_obj.nama_unit_kerja
        except UnitKerja.DoesNotExist:
            value = "-"
    return value


@register.filter(name='get_unor')
def get_unor(value):
    if value:
        try:
            unor_obj = Unor.objects.get(pk=value)
            value = unor_obj.nama_unor
        except Unor.DoesNotExist:
            value = "-"
    return value


@register.filter(name='get_jenis_jabatan')
def get_jenis_jabatan(value):
    if value:
        try:
            jj_obj = JenisJabatan.objects.get(pk=value)
            value = jj_obj.jenis_jabatan
        except JenisJabatan.DoesNotExist:
            value = "-"
    return value


@register.filter(name='get_jab')
def get_jab(value):
    if value:
        try:
            j_obj = Jabatan.objects.get(pk=value)
            value = j_obj.nama_jabatan
        except Jabatan.DoesNotExist:
            value = "-"
    return value


@register.filter(name='get_gol')
def get_gol(value1, value2):
    if value1:
        try:
            gol_obj = Golongan.objects.get(pk=value1)
            if value2 == "PPPk":
                value = gol_obj.get_golongan_pppk()
            else:
                value = gol_obj.get_golongan()
        except Golongan.DoesNotExist:
            value = "-"
    return value


@register.filter(name='get_eselon')
def get_eselon(value):
    if value:
        try:
            es_obj = Eselon.objects.get(pk=value)
            value = es_obj.get_eselon()
        except Eselon.DoesNotExist:
            value = "-"
    return value


@register.filter(name='get_pendidikan')
def get_pendidikan(value):
    if value:
        try:
            p_obj = JenjangPendidikan.objects.get(pk=value)
            value = p_obj.singkatan
        except JenjangPendidikan.DoesNotExist:
            value = "-"
    return value


@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

