import calendar
import pytz
import requests
from django.utils import timezone

from django.contrib import admin, messages
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import path, resolve, reverse_lazy
from django.utils.safestring import mark_safe

from services.models import Configurations
from skp.forms.sasarankinerja_form import SasaranKinerjaForm
from skp.models import (
    DetailSasaranKinerja,
    Lampiran,
    PerilakuKerja,
    Perspektif,
    RencanaHasilKerja,
    SasaranKinerja,
    RiwayatKeteranganSKP,
)
from skp.utils import FULL_BULAN
from usom.models import Account


def delete_skp(modeladmin, request, queryset):
    count = 0
    if queryset.filter(~Q(status=SasaranKinerja.Status.DRAFT)).exists():
        messages.add_message(
            request,
            messages.ERROR,
            mark_safe(
                "Hanya dokumen SKP yang berstatus <b>Draft</b> yang dapat dihapus!"
            ),
        )
    else:
        count = queryset.count()
        queryset.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Berhasil Menghapus {} data Sasaran Kinerja Pegawai".format(count),
        )


delete_skp.short_description = "Hapus Sasaran Kinerja Pegawai yang dipilih"


class SasaranKinerjaAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "pegawai",
        "get_unor",
        "jabatan",
        "pejabat_penilai",
        "periode_awal",
        "periode_akhir",
        "pendekatan",
        "status",
    )
    form = SasaranKinerjaForm
    # list_display_links = None
    actions = [
        delete_skp,
    ]

    def has_add_permission(self, request):
        user = request.user
        if not user.is_superuser:
            if user.unitkerja and user.jabatan and user.jenis_jabatan:
                return True
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Unit Kerja, Jabatan atau Jenis Jabatan Kosong",
                )
                return False
        else:
            return True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def get_unor(self, obj):
        if obj.unor:
            return obj.unor
        elif obj.unor_text:
            return obj.unor_text
        return ""

    get_unor.short_description = "Unor"

    def get_unit_kerja(self, obj):
        if obj.pegawai:
            if obj.pegawai.unitkerja:
                return obj.pegawai.unitkerja
        return ""

    get_unit_kerja.short_description = "Unit Kerja"

    def get_period(self, obj):
        return str(obj.periode_awal) + " / " + str(obj.periode_akhir)

    get_period.short_description = "Periode"

    def Aksi(self, obj):
        btn = '<div class="btn-group" role="group">'
        btn += """
            <button id="btnGroupDrop1" type="button"
                class="btn btn-warning btn-sm dropdown-toggle"
                data-toggle="dropdown" aria-haspopup="true"
                aria-expanded="false">Aksi</button>"""
        btn += '<div class="dropdown-menu" aria-labelledby="btnGroupDrop1">'
        btn += '<a class="dropdown-item" href="{}">Detail SKP</a>'.format(
            reverse_lazy("admin:detail-skp", kwargs={"id": obj.id})
        )
        btn += '<a class="dropdown-item" href="{}">Matriks Peran Hasil</a>'.format(
            reverse_lazy(
                "admin:skp_sasarankerja_matrikshasilperan", kwargs={"obj_id": obj.id}
            )
        )
        btn += '<a class="dropdown-item" href="{}">SKP Bawahan</a>'.format(
            reverse_lazy("admin:skp_sasarankinerja_bawahan", kwargs={"id": obj.id})
        )
        if obj.status == 3:
            btn += '<a class="dropdown-item" href="{}">Penilaian</a>'.format(
                reverse_lazy(
                    "admin:skp_sasarankinerja_penilaian", kwargs={"id": obj.id}
                )
            )
        btn += "</div>"
        btn += "</div>"
        return mark_safe(btn)

    Aksi.short_description = "Aksi"

    def view_custom(self, request, extra_context={}):
        func_view, func_view_args, func_view_kwargs = resolve(request.path)
        self.request = request
        if func_view.__name__ == "view_custom":
            extra_context.update({"title": "Daftar SKP", "type": "skp_list"})
            self.list_display = (
                "get_unor",
                "get_period",
                "pendekatan",
                "jabatan",
                "status",
                "Aksi",
            )
            self.list_filter = ("pendekatan", "status")
        return super(SasaranKinerjaAdmin, self).changelist_view(
            request, extra_context=extra_context
        )

    def changelist_view(self, request, extra_context={}):
        # print(dir(request.user))
        # print(request.user.is_staff)
        if request.user.is_superuser:
            self.list_display = (
                "get_unor",
                "get_period",
                "pendekatan",
                "jabatan",
                "status",
                "Aksi",
            )
            self.list_filter = []
        else:
            self.list_display = (
                "get_unor",
                "get_period",
                "pendekatan",
                "jabatan",
                "status",
                "Aksi",
            )
            self.list_filter = ["pendekatan", "status"]
        return super(SasaranKinerjaAdmin, self).changelist_view(
            request, extra_context=extra_context
        )

    # def add_skp(self, request, obj=None, **kwargs):
    #     form = SKPForm
    #     form.user = request.user
    #     # print(form)
    #     extra_context = {"title": "Tambah SKP", "form": form}
    #     template = loader.get_template("admin/skp/sasarankinerja/changeform_skp.html")
    #     # ec = RequestContext(request, extra_context)
    #     return HttpResponse(template.render(extra_context))

    def get_form(self, request, obj=None, **kwargs):
        kwargs["form"] = SasaranKinerjaForm
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form

    def get_queryset(self, request):
        qs = super(SasaranKinerjaAdmin, self).get_queryset(request)
        func_view, func_view_args, func_view_kwargs = resolve(request.path)
        if func_view.__name__ == self.view_detail_skp.__name__:
            qs = qs
        else:
            qs = qs.filter(pegawai=request.user)
        return qs

    def view_changeform_skp(self, request, id=None):
        respon = {"success": False}
        obj = get_object_or_404(SasaranKinerja, pk=id)
        if obj:
            data = {
                "nama": obj.detailsasarankinerja.nama_pegawai,
                "jabatan": obj.detailsasarankinerja.jabatan_pegawai,
                "unit_kerja": obj.detailsasarankinerja.unor_pegawai,
                "nama_atasan": obj.detailsasarankinerja.nama_pejabat,
                "jabatan_atasan": obj.detailsasarankinerja.jabatan_pejabat,
                "unit_kerja_atasan": obj.detailsasarankinerja.unor_pejabat,
            }
            respon = {"success": True, "data": data}
        return JsonResponse(respon, safe=False)

    def change_view(self, request, object_id, form_url="", extra_context={}):
        obj = get_object_or_404(SasaranKinerja, pk=object_id)
        extra_context.update({"obj": obj})
        self.request = request
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )

    def view_detail_skp(self, request, id=None):
        obj = get_object_or_404(SasaranKinerja, pk=id)
        perilaku_kerja_list = PerilakuKerja.objects.filter(is_active=True)
        lampiran_list = Lampiran.objects.filter(status=Lampiran.Status.ACTIVE)
        penilai = False
        view = request.GET.get("view", None)
        if view == "penilai":
            penilai = True
        extra_context = {
            "title": "Detail SKP",
            "obj": obj,
            "perilaku_kerja_list": perilaku_kerja_list,
            "perspektif_list": Perspektif.objects.all(),
            "lampiran": lampiran_list.order_by("id"),
            "penilai_view": penilai,
        }
        return render(
            request, "admin/skp/sasarankinerja/detail_skp.html", extra_context
        )

    def action_sinkron_ekinerja(self, request, obj_id):
        respon = {}
        try:
            obj = SasaranKinerja.objects.get(pk=obj_id)
        except SasaranKinerja.DoesNotExist:
            pass
        else:
            config = Configurations.get_solo()
            # print(config.ekinerja_url)
            # print(config.ekinerja_token)
            url = "{}/api/kinerja-pegawai/".format(config.ekinerja_url)
            headers = {"Authorization": "Token {}".format(config.ekinerja_token)}
            params = {"nip": obj.pegawai.username, "tahun": 2022}
            fetch_kinerja = requests.get(url, headers=headers, params=params)
            if fetch_kinerja.ok:
                respon_json = fetch_kinerja.json()
                # print(respon_json)
                results = respon_json.get("results", [])
                if len(results) > 0:
                    # create = 0
                    # update = 0
                    for item in results:
                        # print(item)
                        uraianobj = item.get("uraianaktifitas", None)
                        if uraianobj:
                            uraian_id = uraianobj.get("id", None)
                            uraian = uraianobj.get("uraian", None)
                            # satuan = uraianobj.get("satuan", None)
                            # target = uraianobj.get("target", None)

                            # indikator_list = IndikatorKinerjaIndividu.objects.filter(
                            #     skp=obj,
                            #     ekinerja_id=uraian_id,
                            # )
                            # if indikator_list.exists():
                            #     # update
                            #     print("update")
                            #     update += 1
                            # else:
                            #     print("create")
                            #     indikator_obj = IndikatorKinerjaIndividu(
                            #         ekinerja_id=uraian_id,
                            #         indikator=uraian,
                            #         aspek=satuan,
                            #         target=target,
                            #         skp=obj,
                            #     )
                            #     indikator_obj.save()
                            #     create += 1
                            rhk_list = RencanaHasilKerja.objects.filter(
                                skp=obj,
                                ekinerja_id=uraian_id,
                            )
                            if rhk_list.exists():
                                # update
                                print("update")
                                # rhk = rhk_list.last()
                                # rhk.save()
                            else:
                                RencanaHasilKerja.objects.create(
                                    skp=obj,
                                    ekinerja_id=uraian_id,
                                    jenis=1,
                                    klasifikasi=1,
                                    rencana_kerja=uraian,
                                )
                                print("create")

                            # if rhk:
                            #     indikator_obj = IndikatorKinerjaIndividu(
                            #         rencana_kerja=rhk,
                            #         indikator=satuan,
                            #         target=target
                            #     )
                            #     indikator_obj.save()
                            #     print("create")

                    respon = {
                        "success": True,
                        "message": "Berhasil mensinkronkan dengan ekinerja",
                    }
        return JsonResponse(respon)

    def find_exists_skp(self, obj, status):
        find_skp = SasaranKinerja.objects.filter(
            pegawai=obj.pegawai,
            periode_awal__gte=obj.periode_awal,
            periode_akhir__lte=obj.periode_akhir,
            status=status,
        )
        if find_skp.exists():
            return True
        return False

    def create_riwayat(self, obj, keterangan):
        if keterangan:
            RiwayatKeteranganSKP.objects.create(skp=obj, keterangan=keterangan)

    def action_change_status_skp(self, request):
        respon = {"success": False}
        skp_id = request.GET.get("skp_id", None)
        status = request.GET.get("status", None)
        keterangan = None
        if request.POST:
            skp_id = request.POST.get("skp_id", None)
            status = request.POST.get("status", None)
            keterangan = request.POST.get("keterangan", None)
            if not keterangan and keterangan == "":
                keterangan = None

        try:
            obj = SasaranKinerja.objects.get(id=skp_id)
        except SasaranKinerja.DoesNotExist:
            pass
        else:
            skp_exist = False
            if status != 1 and status != "1":
                if self.find_exists_skp(obj, status):
                    skp_exist = True

            if status and not skp_exist:
                try:
                    self.create_riwayat(obj, keterangan)
                    obj.status = status
                    obj.keterangan = keterangan
                    obj.save()
                except Exception:
                    pass
                else:
                    respon = {"success": True}
            else:
                pesan = mark_safe(
                    """
                    Mohon maaf, Sasaran Kinerja Pegawai pada periode {} - {}
                    telah digunakan.
                    <br>Silahkan menggunakan periode diluar periode {} - {}
                    """.format(
                        obj.periode_awal.strftime("%d/%m/%Y"),
                        obj.periode_akhir.strftime("%d/%m/%Y"),
                        obj.periode_awal.strftime("%d/%m/%Y"),
                        obj.periode_akhir.strftime("%d/%m/%Y"),
                    )
                )
                respon = {"success": False, "pesan": pesan}
        return JsonResponse(respon)

    def view_changelist_penilaian_skp(self, request):
        extra_context = {"title": "Penilaian SKP Pegawai"}
        return super().changelist_view(request, extra_context)

    def view_cetak_skp_pegawai(self, request, obj_id):
        obj = get_object_or_404(SasaranKinerja, pk=obj_id)
        show_ttd = True
        if obj.status in [SasaranKinerja.Status.DRAFT, SasaranKinerja.Status.PENGAJUAN]:
            show_ttd = False
        extra_context = {
            "obj": obj,
            "title": "Cetak SKP {} [{}]".format(
                obj.pegawai.username, obj.get_periode()
            ),
            "perilakukerja_list": PerilakuKerja.objects.filter(is_active=True),
            "lampiran_list": Lampiran.objects.filter(
                status=Lampiran.Status.ACTIVE
            ).order_by("id"),
            "show_ttd": show_ttd,
        }
        return render(request, "admin/skp/sasarankinerja/cetak.html", extra_context)

    def view_skp_bawahan(self, request, id):
        obj = get_object_or_404(SasaranKinerja, pk=id)
        list_skp_bawahan = SasaranKinerja.objects.filter(induk=obj)
        show_detail = [
            SasaranKinerja.Status.PENGAJUAN,
            SasaranKinerja.Status.PERSETUJUAN,
        ]
        extra_context = {
            "obj": obj,
            "list_skp_bawahan": list_skp_bawahan,
            "status_choices": SasaranKinerja.Status.choices,
            "title": "SKP Bawahan",
            "show_detail": show_detail,
        }
        return render(
            request, "admin/skp/sasarankinerja/skp_bawahan.html", extra_context
        )

    def view_penilaian(self, request, id):
        obj = get_object_or_404(SasaranKinerja, pk=id)
        config = Configurations.get_solo()
        extra_context = {
            "title": "Penilaian SKP",
            "obj": obj,
            "batas_input": config.batas_input,
        }
        return render(request, "admin/skp/sasarankinerja/penilaian.html", extra_context)

    def load_penilaian(self, request):
        sasaran_id = request.GET.get("id", None)
        respon = {"success": False, "pesan": "Terjadi Kesalahan Sistem"}
        try:
            sasaran_obj = SasaranKinerja.objects.get(pk=sasaran_id)
        except Exception as e:
            respon = {"success": False, "pesan": str(e)}
            return JsonResponse(respon, safe=False)

        awal = sasaran_obj.periode_awal
        akhir = sasaran_obj.periode_akhir
        bulan_list = []
        if awal.month == akhir.month:
            bulan_list.append(
                {
                    "bulan": FULL_BULAN[awal.month],
                    "range": "{} / {}".format(
                        awal.strftime("%Y-%m-%d"),
                        akhir.strftime("%Y-%m-%d"),
                    ),
                    "rencana_aksi_url": reverse_lazy(
                        "admin:rencana-aksi-skp",
                        kwargs={"skp_id": sasaran_obj.id, "periode": awal.month},
                    ),
                    "bukti_dukung_url": reverse_lazy(
                        "admin:bukti-dukung-skp",
                        kwargs={"skp_id": sasaran_obj.id, "periode": awal.month},
                    )
                    if sasaran_obj.status == 3
                    else "#",
                    "penilaian_bawahan_url": reverse_lazy(
                        "admin:penilaian-bawahan-skp",
                        kwargs={"skp_id": sasaran_obj.id, "periode": awal.month},
                    )
                    if sasaran_obj.status == 3
                    else "#",
                    "export_penilaian_bawahan_url": reverse_lazy(
                        "admin:penilaian-bawahan-skp-export",
                        kwargs={"skp_id": sasaran_obj.id, "periode": awal.month},
                    )
                    if sasaran_obj.status == 3
                    else "#",
                    "kurva_penilaian_bawahan_url": reverse_lazy(
                        "admin:penilaian-bawahan-skp-kurva",
                        kwargs={"skp_id": sasaran_obj.id, "periode": awal.month},
                    )
                    if sasaran_obj.status == 3
                    else "#",
                    "cetak_form_penilaian_url": reverse_lazy(
                        "admin:form-penilaian-skp-cetak",
                        kwargs={
                            "skp_id": sasaran_obj.id,
                            "periode": awal.month,
                        },
                    ),
                }
            )
        else:
            for i in range(awal.month, akhir.month + 1):
                if i == awal.month:
                    num_days = calendar.monthrange(awal.year, awal.month)[1]
                    bulan_list.append(
                        {
                            "bulan": FULL_BULAN[i],
                            "range": "{} / {}-{}-{}".format(
                                awal.strftime("%Y-%m-%d"),
                                awal.year,
                                awal.month
                                if awal.month > 9
                                else "0{}".format(awal.month),
                                num_days,
                            ),
                            "rencana_aksi_url": reverse_lazy(
                                "admin:rencana-aksi-skp",
                                kwargs={"skp_id": sasaran_obj.id, "periode": i},
                            ),
                            "bukti_dukung_url": reverse_lazy(
                                "admin:bukti-dukung-skp",
                                kwargs={"skp_id": sasaran_obj.id, "periode": i},
                            )
                            if sasaran_obj.status == 3
                            else "#",
                            "penilaian_bawahan_url": reverse_lazy(
                                "admin:penilaian-bawahan-skp",
                                kwargs={"skp_id": sasaran_obj.id, "periode": i},
                            )
                            if sasaran_obj.status == 3
                            else "#",
                            "export_penilaian_bawahan_url": reverse_lazy(
                                "admin:penilaian-bawahan-skp-export",
                                kwargs={
                                    "skp_id": sasaran_obj.id,
                                    "periode": awal.month,
                                },
                            )
                            if sasaran_obj.status == 3
                            else "#",
                            "kurva_penilaian_bawahan_url": reverse_lazy(
                                "admin:penilaian-bawahan-skp-kurva",
                                kwargs={
                                    "skp_id": sasaran_obj.id,
                                    "periode": awal.month,
                                },
                            )
                            if sasaran_obj.status == 3
                            else "#",
                            "cetak_form_penilaian_url": reverse_lazy(
                                "admin:form-penilaian-skp-cetak",
                                kwargs={
                                    "skp_id": sasaran_obj.id,
                                    "periode": awal.month,
                                },
                            ),
                        }
                    )
                elif i == akhir.month:
                    bulan_list.append(
                        {
                            "bulan": FULL_BULAN[i],
                            "range": "{}-{}-{} / {}".format(
                                akhir.year,
                                akhir.month
                                if akhir.month > 9
                                else "0{}".format(awal.month),
                                "01",
                                akhir.strftime("%Y-%m-%d"),
                            ),
                            "rencana_aksi_url": reverse_lazy(
                                "admin:rencana-aksi-skp",
                                kwargs={"skp_id": sasaran_obj.id, "periode": i},
                            ),
                            "bukti_dukung_url": reverse_lazy(
                                "admin:bukti-dukung-skp",
                                kwargs={"skp_id": sasaran_obj.id, "periode": i},
                            )
                            if sasaran_obj.status == 3
                            else "#",
                            "penilaian_bawahan_url": reverse_lazy(
                                "admin:penilaian-bawahan-skp",
                                kwargs={"skp_id": sasaran_obj.id, "periode": i},
                            )
                            if sasaran_obj.status == 3
                            else "#",
                            "export_penilaian_bawahan_url": reverse_lazy(
                                "admin:penilaian-bawahan-skp-export",
                                kwargs={
                                    "skp_id": sasaran_obj.id,
                                    "periode": awal.month,
                                },
                            )
                            if sasaran_obj.status == 3
                            else "#",
                            "kurva_penilaian_bawahan_url": reverse_lazy(
                                "admin:penilaian-bawahan-skp-kurva",
                                kwargs={
                                    "skp_id": sasaran_obj.id,
                                    "periode": awal.month,
                                },
                            )
                            if sasaran_obj.status == 3
                            else "#",
                            "cetak_form_penilaian_url": reverse_lazy(
                                "admin:form-penilaian-skp-cetak",
                                kwargs={
                                    "skp_id": sasaran_obj.id,
                                    "periode": awal.month,
                                },
                            ),
                        }
                    )
                else:
                    num_days = calendar.monthrange(awal.year, awal.month)[1]
                    bulan_list.append(
                        {
                            "bulan": FULL_BULAN[i],
                            "range": "{}-{}-{} / {}-{}-{}".format(
                                akhir.year,
                                i if i > 9 else "0{}".format(i),
                                "01",
                                akhir.year,
                                i if i > 9 else "0{}".format(i),
                                num_days,
                            ),
                            "rencana_aksi_url": reverse_lazy(
                                "admin:rencana-aksi-skp",
                                kwargs={"skp_id": sasaran_obj.id, "periode": i},
                            ),
                            "bukti_dukung_url": reverse_lazy(
                                "admin:bukti-dukung-skp",
                                kwargs={"skp_id": sasaran_obj.id, "periode": i},
                            )
                            if sasaran_obj.status == 3
                            else "#",
                            "penilaian_bawahan_url": reverse_lazy(
                                "admin:penilaian-bawahan-skp",
                                kwargs={"skp_id": sasaran_obj.id, "periode": i},
                            )
                            if sasaran_obj.status == 3
                            else "#",
                            "export_penilaian_bawahan_url": reverse_lazy(
                                "admin:penilaian-bawahan-skp-export",
                                kwargs={
                                    "skp_id": sasaran_obj.id,
                                    "periode": awal.month,
                                },
                            )
                            if sasaran_obj.status == 3
                            else "#",
                            "kurva_penilaian_bawahan_url": reverse_lazy(
                                "admin:penilaian-bawahan-skp-kurva",
                                kwargs={
                                    "skp_id": sasaran_obj.id,
                                    "periode": awal.month,
                                },
                            )
                            if sasaran_obj.status == 3
                            else "#",
                            "cetak_form_penilaian_url": reverse_lazy(
                                "admin:form-penilaian-skp-cetak",
                                kwargs={
                                    "skp_id": sasaran_obj.id,
                                    "periode": awal.month,
                                },
                            ),
                        }
                    )
        respon = {"success": True, "data": bulan_list}
        return JsonResponse(respon, safe=False)

    def view_matriks_hasil_peran(self, request, obj_id):
        obj = get_object_or_404(SasaranKinerja, pk=obj_id)
        show = request.GET.get("show", None)
        cetak = request.GET.get("cetak", None)

        skp_childs = SasaranKinerja.objects.filter(induk_id=obj.id)
        extra_context = {
            "title": "Matrik Peran Hasil",
            "obj": obj,
            "rhk_list": obj.rencanahasilkerja_set.all(),
            "skp_childs": skp_childs,
            "show": True if show == "true" else False,
        }

        if cetak:
            return render(
                request,
                "admin/skp/sasarankinerja/matriks_hasil_peran_cetak.html",
                extra_context,
            )
        return render(
            request, "admin/skp/sasarankinerja/matriks_hasil_peran.html", extra_context
        )

    def get_rhk_by_skp_parent(self, request, obj_id):
        obj = get_object_or_404(SasaranKinerja, pk=obj_id)
        respon = {"success": False}
        if obj.induk:
            rhk_parent_list = obj.induk.rencanahasilkerja_set.filter(
                klasifikasi=RencanaHasilKerja.Klasifikasi.ORGANISASI
            )
            if rhk_parent_list.exists():
                results = []
                terbesar = 0
                for item in rhk_parent_list:
                    childs = []
                    list_childs = RencanaHasilKerja.objects.filter(
                        induk_id=item.id, skp=obj
                    )
                    if list_childs.count() > terbesar:
                        terbesar = list_childs.count()
                    for child in list_childs:
                        childs.append({"text": child.rencana_kerja})

                    results.append({"id": item.id, "childs": childs})
                respon = {"success": True, "results": results, "terbesar": terbesar}
        return JsonResponse(respon)

    def list_riwayat_keterangan(self, request, id):
        obj = get_object_or_404(SasaranKinerja, pk=id)
        data = []
        for i in RiwayatKeteranganSKP.objects.filter(skp=obj):
            tanggal = timezone.localtime(i.created, pytz.timezone("Asia/Jakarta"))
            data.append(
                {
                    "waktu": tanggal.strftime("%d-%m-%Y, %H:%M:%S"),
                    "keterangan": i.keterangan,
                }
            )
        return JsonResponse(data, safe=False)

    def sinkron_data_pegawai_local(self, request, id):
        respon = {}
        # jenis => pegawai / atasan_penilai
        jenis = request.GET.get("jenis", None)
        skp = request.GET.get("skp_id", None)
        try:
            obj = Account.objects.get(pk=id)
        except Account.DoesNotExist or Exception as e:
            print(e)
            raise Http404

        find_detail_skp = DetailSasaranKinerja.objects.filter(skp__id=skp)
        if find_detail_skp.exists():
            detail_obj = find_detail_skp.last()
            if jenis == "pegawai":
                detail_obj.nama_pegawai = obj.get_complete_name()
                detail_obj.nip_pegawai = obj.username
                detail_obj.jabatan_pegawai = obj.jabatan
                detail_obj.golongan_pegawai = obj.golongan
                detail_obj.unor_pegawai = obj.unitkerja.unitkerja
            elif jenis == "atasan_penilai":
                detail_obj.nama_pejabat = obj.get_complete_name()
                detail_obj.nip_pejabat = obj.username
                detail_obj.jabatan_pejabat = obj.jabatan
                detail_obj.golongan_pejabat = obj.golongan
                detail_obj.unor_pejabat = obj.unitkerja.unitkerja
            detail_obj.save()
            data = {
                "nama": obj.get_complete_name(),
                "nip": obj.username,
                "jabatan": obj.jabatan,
                "golongan": obj.golongan,
                "unitkerja": obj.unitkerja.unitkerja,
                "jenis": jenis,
            }
            respon = {"success": True, "data": data}
        return JsonResponse(respon)

    def load_induk_options(self, request):
        atasan = request.GET.get("atasan", None)
        respon = {"success": False, "pesan": "Terjadi Kesalahan Sistem"}
        if atasan and atasan != "" and atasan.isnumeric():
            find_skp = SasaranKinerja.objects.filter(
                pegawai__id=atasan, status=SasaranKinerja.Status.PERSETUJUAN
            )
            data = []
            for i in find_skp:
                data.append(
                    {
                        "id": i.id,
                        "text": "[{}] - {}".format(
                            i.get_periode(), i.get_status_display()
                        ),
                    }
                )
            respon = {"success": True, "data": data}
        return JsonResponse(respon, safe=False)

    def get_urls(self):
        admin_url = super(SasaranKinerjaAdmin, self).get_urls()
        custom_url = [
            path(
                "penilaian",
                self.admin_site.admin_view(self.view_changelist_penilaian_skp),
                name="skp_sasarankinerja_changelist_penilaian",
            ),
            path(
                "load-penilaian",
                self.admin_site.admin_view(self.load_penilaian),
                name="skp_sasarankinerja_penilaian_load",
            ),
            path(
                "<int:obj_id>/matriks-hasil-peran",
                self.admin_site.admin_view(self.view_matriks_hasil_peran),
                name="skp_sasarankerja_matrikshasilperan",
            ),
            path(
                "<int:id>/detail",
                self.admin_site.admin_view(self.view_detail_skp),
                name="detail-skp",
            ),
            path(
                "<int:obj_id>/cetak",
                self.admin_site.admin_view(self.view_cetak_skp_pegawai),
                name="skp_sasarankinerja_cetak",
            ),
            path(
                "<int:obj_id>/sinkron",
                self.admin_site.admin_view(self.action_sinkron_ekinerja),
                name="skp_sasarankinerja_sinkron",
            ),
            path(
                "<int:id>/skp-bawahan",
                self.admin_site.admin_view(self.view_skp_bawahan),
                name="skp_sasarankinerja_bawahan",
            ),
            path(
                "<int:id>/penilaian-skp",
                self.admin_site.admin_view(self.view_penilaian),
                name="skp_sasarankinerja_penilaian",
            ),
            path(
                "<int:obj_id>/get-rhk-childs",
                self.admin_site.admin_view(self.get_rhk_by_skp_parent),
                name="skp_sasarankinerja_get_child_rhk",
            ),
            path(
                "change-status",
                self.admin_site.admin_view(self.action_change_status_skp),
                name="skp_sasarankinerja_changestatus",
            ),
            path(
                "sync-data-local/<int:id>",
                self.admin_site.admin_view(self.sinkron_data_pegawai_local),
                name="skp_sasarankinerja_sync_data_pegawai",
            ),
            path(
                "<int:id>/riwayat-keterangan",
                self.admin_site.admin_view(self.sinkron_data_pegawai_local),
                name="skp_sasarankinerja_sync_data_pegawai",
            ),
            path(
                "<int:id>/view",
                self.admin_site.admin_view(self.view_changeform_skp),
                name="skp_sasarankinerja_view",
            ),
            path(
                "option",
                self.admin_site.admin_view(self.load_induk_options),
                name="skp_sasarankinerja_induk_option",
            ),
            # path("skpdata/", self.view_custom, name="list_skp_admin"),
            # path("skpdata/add/", self.add_skp, name="add_skp_admin"),
        ]
        return custom_url + admin_url

    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.save()
    #         # Create
    #         try:
    #             detail = DetailSasaranKinerja(
    #                 skp=obj,
    #                 nama_pegawai=obj.pegawai.get_complete_name(),
    #                 nip_pegawai=obj.pegawai.username,
    #                 jabatan_pegawai=obj.pegawai.jabatan,
    #                 golongan_pegawai=obj.pegawai.golongan,
    #                 unor_pegawai=obj.pegawai.unitkerja.unitkerja,
    #                 nama_pejabat=obj.pegawai.atasan.get_complete_name(),
    #                 nip_pejabat=obj.pegawai.atasan.username,
    #                 jabatan_pejabat=obj.pegawai.atasan.jabatan,
    #                 golongan_pejabat=obj.pegawai.atasan.golongan,
    #                 unor_pejabat=obj.pegawai.atasan.unitkerja.unitkerja,
    #             )
    #             detail.save()
    #         except Exception as e:
    #             print(e)
    #     return super().save_model(request, obj, form, change)
