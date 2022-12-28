from django import template
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from skp.models import (BuktiDukung, DaftarLampiran,
                        DaftarPerilakuKerjaPegawai, PenilaianBawahan,
                        Realisasi, RencanaAksi, RencanaHasilKerja,
                        SasaranKinerja, UmpanBalikPegawai)
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
            aksi = """
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
            """.format(
                value.id,
                value.lampiran.lampiran.title(),
                # value.id,
                reverse_lazy("admin:skp_daftarlampiran_hapus", kwargs={"id": value.id}),
            )
            html += """
            <tr>
                <td style="width: 50px">{}</td>
                <td>
                <div id="isi-lampiran-{}">{}</div>
                {}
                </td>
            </tr>
            """.format(
                idx + 1, value.id, value.isi, "" if cetak == "ya" else aksi
            )
        return mark_safe(html)
    return ""


@register.simple_tag
def daftar_ekspetasi(perilaku_id, skp, cetak, user=None):
    isi = ""
    ol = ""
    html_isi = ""
    ekspetasi_list = []
    find_ekspetasi = None
    try:
        find_ekspetasi = DaftarPerilakuKerjaPegawai.objects.get(
            skp=skp, perilaku_kerja__id=perilaku_id
        )
    except DaftarPerilakuKerjaPegawai.DoesNotExist:
        tambah = True
    else:
        tambah = False
        isi = find_ekspetasi.isi
        if find_ekspetasi.ekspetasi_tambahan.count() > 0:
            ekspetasi_list = list(
                find_ekspetasi.ekspetasi_tambahan.all().values_list("id", flat=True)
            )
            ol = """<table class="table table-borderless">"""
            for idx, i in enumerate(find_ekspetasi.ekspetasi_tambahan.all()):
                ol += """
                    <tr>
                        <td>{}.</td>
                        <td>{}</td>
                    </tr>
                """.format(
                    idx + 1, i.ekspetasi
                )
            ol += "</table>"
    if cetak == "tidak":
        aksi = ""
        if skp.jenis_jabatan == 1 or user == skp.pejabat_penilai:
            aksi = """
                <br>
                <button type="button"
                data-id="{}" data-ekspetasi="{}" data-tambah="{}"
                data-ekspetasi_multiple="{}"
                class="mt-3 ml-3 btn btn-{} btn-sm"
                data-toggle="modal"
                data-target="#modal_tambah_ekspetasi">
                    {} Ekspektasi
                </button>
            """.format(
                perilaku_id,
                find_ekspetasi.id if find_ekspetasi else "",
                tambah,
                ekspetasi_list,
                "primary" if tambah else "warning",
                "Tambah" if tambah else "Edit",
            )
        if isi and isi != "":
            html_isi = """
            Ekspetasi Lainnya:&nbsp;
                <span id="ekspetasi-{}">{}</span>
            """.format(
                perilaku_id,
                isi,
            )
        else:
            html_isi = ""
        html = """
            <span id="ekspetasi-multile-{}">{}</span>
            {}
            {}
        """.format(
            perilaku_id, ol, html_isi, aksi
        )
    else:
        if isi and isi != "":
            html_isi = """
                Ekspetasi Lainnya:&nbsp;
                <span>{}</span>
            """.format(
                isi
            )
        html = """
            {}
            <span>{}</span>
        """.format(
            html_isi,
            ol,
        )
    return mark_safe(html)


@register.simple_tag
def daftar_rencana_aksi(counter, skp_id, rhk_id, periode, cetak="tidak"):
    rencana_list = RencanaAksi.objects.filter(skp=skp_id, rhk=rhk_id, periode=periode)
    isi = ""
    isi_luar = ""
    if cetak == "ya":
        if rencana_list.count() > 0:
            html = """<ol style="margin: unset;">"""
            for i in rencana_list:
                html += """<li style="margin: unset;">{}</li>""".format(i.rencana_aksi)
            html += "</ol>"
        else:
            html = ""
    else:
        if rencana_list.count() > 0:
            for i in rencana_list:
                aksi = """
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
                """.format(
                    i.id,
                    # value.id,
                    reverse_lazy("admin:skp_rencanaaksi_hapus", kwargs={"id": i.id}),
                )
                isi += """
                <tr>
                <td><span id="rencana-aksi-{}">{}</span>{}</td>
                </tr>
                """.format(
                    i.id, i.rencana_aksi, aksi
                )
            isi_luar = """
            <tr>
                <td>
                    <button type="button" data-rhk="{}"
                    class="btn btn-sm btn-primary btn-block"
                    data-toggle="modal" data-target="#modal_rencana_aksi">
                        <i class="fas fa-plus"></i> Tambah Rencana Aksi
                    </button>
                </td>
            </tr>
            """.format(
                rhk_id.id
            )
        else:
            isi = """
                <td>
                    <button type="button" data-rhk="{}"
                    class="btn btn-sm btn-primary btn-block"
                    data-toggle="modal" data-target="#modal_rencana_aksi">
                        <i class="fas fa-plus"></i> Tambah Rencana Aksi
                    </button>
                </td>
            """.format(
                rhk_id.id
            )
        html = """
            <tr>
                <td rowspan="{}" style="width: 20px">{}</td>
                <td rowspan="{}">{}</td>
            </tr>
            {}
            {}

        """.format(
            rencana_list.count() + 2 if rencana_list.count() > 0 else 2,
            counter,
            rencana_list.count() + 2 if rencana_list.count() > 0 else 2,
            rhk_id.rencana_kerja,
            isi,
            isi_luar,
        )
    return mark_safe(html)


@register.simple_tag
def get_complete_periode(awal, akhir):
    if awal.month == akhir.month:
        if awal.day == akhir.day:
            return "{} {} TAHUN {}".format(
                awal.day, FULL_BULAN[awal.month].upper(), awal.year
            )
        return "{} SD {} {} TAHUN {}".format(
            awal.day, akhir.day, FULL_BULAN[awal.month].upper(), awal.year
        )
    else:
        return "{} {} SD {} {} TAHUN {}".format(
            awal.day,
            FULL_BULAN[awal.month].upper(),
            akhir.day,
            FULL_BULAN[akhir.month],
            awal.year,
        )


@register.simple_tag
def get_bukti_dukung(indikator_obj, periode):
    bukti_dukung_list = BuktiDukung.objects.filter(
        indikator=indikator_obj, periode=periode
    )
    html = ""
    if bukti_dukung_list.exists():
        html = "<ol>"
        for i in bukti_dukung_list:
            html += """<li>
                            <a href="{}"
                                target="_blank">
                                {}
                            </a>
                        </li>
                    """.format(
                i.link, i.nama_bukti_dukung
            )
        html += "</ol>"
    return mark_safe(html)


@register.simple_tag
def get_realisasi(indikator_obj, periode):
    realisasi_list = Realisasi.objects.filter(indikator=indikator_obj, periode=periode)
    if realisasi_list.exists():
        return realisasi_list.last()
    return None


@register.simple_tag
def get_umpan_balik(indikator_obj, periode):
    umpan_balik_list = UmpanBalikPegawai.objects.filter(
        indikator=indikator_obj, periode=periode
    )
    ol = ""
    if umpan_balik_list.exists():
        obj = umpan_balik_list.last()
        if obj.umpan_balik.count() > 0:
            ol = """<ol style="padding-inline-start: 15px;margin-block-start:unset">"""
            for i in obj.umpan_balik.all():
                ol += "<li>{}</li>".format(i.nama)
            ol += "</ol>"
            ol += "<span>Umpan Balik Tambahan:<br>{}</span>".format(
                obj.umpan_balik_tambahan
            )
    return mark_safe(ol)


@register.simple_tag
def get_detail_skp(pegawai, skp_obj, periode):
    list_skp_bawahan = SasaranKinerja.objects.filter(
        pegawai=pegawai,
        periode_awal__gte=skp_obj.periode_awal,
        periode_akhir__lte=skp_obj.periode_akhir,
        status=SasaranKinerja.Status.PERSETUJUAN,
    )
    if list_skp_bawahan.exists():
        obj = list_skp_bawahan.last()
        button = """
            <a href="{}" class="btn btn-sm btn-warning">
                <i class="fas fa-info-circle"></i> Detail
            </a>
        """.format(
            reverse_lazy(
                "admin:penilaian-bawahan-skp-detail",
                kwargs={"skp_id": obj.id, "periode": periode},
            )
        )
        return mark_safe(button)
    return "---"


@register.simple_tag
def get_penilaian_bawahan_status(pegawai, skp_obj, periode):
    text = "Belum Dinilai"
    list_skp_bawahan = SasaranKinerja.objects.filter(
        pegawai=pegawai,
        periode_awal__gte=skp_obj.periode_awal,
        periode_akhir__lte=skp_obj.periode_akhir,
        status=SasaranKinerja.Status.PERSETUJUAN,
    )
    if list_skp_bawahan.exists():
        obj = list_skp_bawahan.last()
        find_penilaian_bawahan = PenilaianBawahan.objects.filter(
            skp=obj, periode=periode
        )
        if find_penilaian_bawahan.exists():
            penilaian_obj = find_penilaian_bawahan.last()
            if penilaian_obj.is_dinilai:
                text = "Sudah Dinilai"
    return text
