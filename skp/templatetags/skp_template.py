from django import template
from skp.models import RencanaHasilKerja

register = template.Library()


@register.simple_tag
def is_fisrt_parent(skp_id, rhk_id, rhk_parent_id):
    rhk_list = RencanaHasilKerja.objects.filter(
        skp_id=skp_id, induk_id=rhk_parent_id
    ).order_by("id", "induk")
    if rhk_list.exists():
        fisrt_data = rhk_list.first()
        if fisrt_data.id == rhk_id:
            return True
    return False
