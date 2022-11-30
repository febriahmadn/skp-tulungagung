from django import template
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from skp.models import RencanaHasilKerja, DaftarLampiran

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

@register.simple_tag
def daftar_lampiran(lampiran_id, skp_id, cetak):
    daftar_list = DaftarLampiran.objects.filter(
        skp_id=skp_id, lampiran_id=lampiran_id
    ).order_by("id")
    if daftar_list.exists():
        html = ""
        for idx, value in enumerate(daftar_list):
            aksi = '''
            <div style="display: flex" >
                <button type="button" data-jenis="ubah" data-id="{}"
                data-judul="{}" class="btn btn-icon btn-warning btn-sm"
                data-toggle="modal" data-target="#modal_tambah_lampiran">
                    <i class="flaticon2-pen"></i>
                </button>
                <a onclick="delete_action('{}')"
                    class="ml-2 btn btn-icon btn-danger btn-sm">
                        <i class="flaticon-delete-1"></i>
                </a>
            </div>
            '''.format(
                value.id,
                value.lampiran.lampiran.title(),
                # value.id,
                reverse_lazy('admin:skp_daftarlampiran_hapus', kwargs={"id": value.id})
            )
            html += '''
            <tr>
                <td style="width: 50px">{}</td>
                <td>
                <div id="isi-lampiran-{}">{}</div>
                {}
                </td>
            </tr>
            '''.format(
                    idx+1,
                    value.id,
                    value.isi,
                    "" if cetak == "ya" else aksi
            )
        return mark_safe(html)
    return ""
