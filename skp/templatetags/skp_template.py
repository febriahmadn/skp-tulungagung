from django import template
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from skp.models import (
    RencanaHasilKerja,
    DaftarLampiran,
    DaftarPerilakuKerjaPegawai,
    RencanaAksi
)
from skp.utils import FULL_BULAN

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

@register.filter
def get_bulan(int_bulan):
    return FULL_BULAN[int_bulan]

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

@register.simple_tag
def daftar_ekspetasi(perilaku_id, skp_id, cetak):
    isi = ""
    find_ekspetasi = None
    try:
        find_ekspetasi = DaftarPerilakuKerjaPegawai.objects.get(
            skp__id=skp_id,
            perilaku_kerja__id=perilaku_id
        )
    except DaftarPerilakuKerjaPegawai.DoesNotExist:
        tambah = True
    else:
        tambah = False
        isi = find_ekspetasi.isi
    if cetak == "tidak":
        html = '''
            <span id="ekspetasi-{}">{}</span>
            <br>
            <button type="button"
            data-id="{}" data-ekspetasi="{}" data-tambah="{}"
            class="mt-3 ml-3 btn btn-{} btn-sm"
            data-toggle="modal"
            data-target="#modal_tambah_ekspetasi">
                {} Ekspektasi
            </button>
        '''.format(
            perilaku_id,
            isi,
            perilaku_id,
            find_ekspetasi.id if find_ekspetasi else "",
            tambah,
            "primary" if tambah else "warning",
            "Tambah" if tambah else "Edit"
        )
    else:
        html = '<span>{}</span>'.format(
            isi,
        )
    return mark_safe(html)

@register.simple_tag
def daftar_rencana_aksi(counter, skp_id, rhk_id, periode, cetak="tidak"):
    rencana_list = RencanaAksi.objects.filter(
        skp=skp_id,
        rhk=rhk_id,
        periode=periode
    )
    isi = ""
    isi_luar = ""
    if cetak == "ya":
        if rencana_list.count() > 0:
            html = '''<ol style="margin: unset;">'''
            for i in rencana_list:
                html += '''<li style="margin: unset;">{}</li>'''.format(i.rencana_aksi)
            html += "</ol>"
        else:
            html = ""
    else:
        if rencana_list.count() > 0:
            for i in rencana_list:
                
                aksi = '''
                <div style="display: flex" >
                    <button type="button" data-jenis="ubah" data-id="{}"
                    class="btn btn-icon btn-warning btn-sm"
                    data-toggle="modal" data-target="#modal_rencana_aksi">
                        <i class="flaticon2-pen"></i>
                    </button>
                    <a onclick="delete_action('{}')"
                        class="ml-2 btn btn-icon btn-danger btn-sm">
                            <i class="flaticon-delete-1"></i>
                    </a>
                </div>
                '''.format(
                    i.id,
                    # value.id,
                    reverse_lazy('admin:skp_rencanaaksi_hapus', kwargs={"id": i.id})
                )
                isi += '''
                <tr>
                <td><span id="rencana-aksi-{}">{}</span>{}</td>
                </tr>
                '''.format(i.id, i.rencana_aksi, aksi)
            isi_luar = '''
            <tr>
                <td>
                    <button type="button" data-rhk="{}"
                    class="btn btn-sm btn-primary btn-block"
                    data-toggle="modal" data-target="#modal_rencana_aksi">
                        <i class="fas fa-plus"></i> Tambah Rencana Aksi
                    </button>
                </td>
            </tr>
            '''.format(
                rhk_id.id
            )
        else:
            isi = '''
                <td>
                    <button type="button" data-rhk="{}"
                    class="btn btn-sm btn-primary btn-block"
                    data-toggle="modal" data-target="#modal_rencana_aksi">
                        <i class="fas fa-plus"></i> Tambah Rencana Aksi
                    </button>
                </td>
            '''.format(
                rhk_id.id
            )
        html = '''
            <tr>
                <td rowspan="{}" style="width: 20px">{}</td>
                <td rowspan="{}">{}</td>
            </tr>
            {}
            {}

        '''.format(
            rencana_list.count()+2 if rencana_list.count() > 0 else 2,
            counter,

            rencana_list.count()+2 if rencana_list.count() > 0 else 2,
            rhk_id.rencana_kerja,

            isi,

            isi_luar
        )
    return mark_safe(html)

@register.simple_tag
def get_complete_periode(awal, akhir):
    if awal.month == akhir.month:
        if awal.day == akhir.day:
            return "{} {} TAHUN {}".format(awal.day, FULL_BULAN[awal.month].upper(), awal.year)
        return "{} SD {} {} TAHUN {}".format(awal.day, akhir.day, FULL_BULAN[awal.month].upper(), awal.year)
    else:
        return "{} {} SD {} {} TAHUN {}".format(awal.day, FULL_BULAN[awal.month].upper(), akhir.day, FULL_BULAN[akhir.month], awal.year)
    # {{obj.periode_awal|date:"j"}} {{obj.periode_awal|date:"n"|add:0|get_bulan}} SD {{obj.periode_akhir|date:"j"}} {{obj.periode_akhir|date:"n"|add:0|get_bulan}}
    return ""
