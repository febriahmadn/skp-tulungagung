import datetime

import pytz
import requests
import xlwt
from django.contrib import admin, messages
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import path, resolve, reverse_lazy
from django.contrib.admin.utils import model_ngettext
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _


from services.models import Configurations
from skp.forms.sasarankinerja_form import SasaranKinerjaForm
from skp.models import (
    DetailSasaranKinerja,
    Lampiran,
    PenilaianBawahan,
    PerilakuKerja,
    Perspektif,
    RencanaHasilKerja,
    RiwayatKeteranganSKP,
    SasaranKinerja,
)
from skp.utils import FULL_BULAN
from usom.models import Account, UnitKerja


def delete_skp(modeladmin, request, queryset):
    count = 0
    (
        deletable_objects,
        model_count,
        perms_needed,
        protected,
    ) = modeladmin.get_deleted_objects(queryset, request)
    objects_name = model_ngettext(queryset)
    title = _("Are you sure?")
    context = {
        **modeladmin.admin_site.each_context(request),
        "title": title,
        "subtitle": None,
        "objects_name": str(objects_name),
        "deletable_objects": [deletable_objects],
        "model_count": dict(model_count).items(),
        "queryset": queryset,
        "media": modeladmin.media,
    }
    if queryset.filter(~Q(status=SasaranKinerja.Status.DRAFT)).exists():
        messages.add_message(
            request,
            messages.ERROR,
            mark_safe(
                "Hanya dokumen SKP yang berstatus <b>Draft</b> yang dapat dihapus!"
            ),
        )
        return None
    else:
        count = queryset.count()
        if request.POST.get("post"):
            queryset.delete()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Berhasil Menghapus {} data Sasaran Kinerja Pegawai".format(count),
            )
            return None
    return render(
        request,
        "admin/delete_selected_confirmation.html",
        context,
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
        if not user.is_superuser and not user.groups.filter(name="Bupati"):
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

    def has_change_permission(self, request, obj=None):
        if obj and obj.status == SasaranKinerja.Status.DRAFT:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status == SasaranKinerja.Status.DRAFT:
            return True
        return False

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
        awal = obj.periode_awal
        akhir = obj.periode_akhir
        if awal.month == akhir.month:
            if awal.day == akhir.day:
                return "{} {} {}".format(
                    awal.day, FULL_BULAN[awal.month].title(), awal.year
                )
            return "{} Sd {} {} {}".format(
                awal.day, akhir.day, FULL_BULAN[awal.month].title(), awal.year
            )
        else:
            return "{} {} Sd {} {} {}".format(
                awal.day,
                FULL_BULAN[awal.month].title(),
                akhir.day,
                FULL_BULAN[akhir.month].title(),
                awal.year,
            )

    get_period.short_description = "Periode"

    def Aksi(self, obj):
        btn = '<div class="btn-group" role="group">'
        btn += """
            <button id="btnGroupDrop1" type="button"
                class="btn btn-warning btn-sm dropdown-toggle"
                data-toggle="dropdown" aria-haspopup="true"
                aria-expanded="false">Aksi</button>"""
        btn += '<div class="dropdown-menu" aria-labelledby="btnGroupDrop1">'

        if obj.pegawai.groups.filter(name="Bupati").exists():
            btn += '<a class="dropdown-item" href="{}">SKP Bawahan</a>'.format(
                reverse_lazy("admin:skp_sasarankinerja_bawahan", kwargs={"id": obj.id})
            )
        else:
            btn += '<a class="dropdown-item" href="{}">Detail SKP</a>'.format(
                reverse_lazy("admin:detail-skp", kwargs={"id": obj.id})
            )
            btn += '<a class="dropdown-item" href="{}">Matriks Peran Hasil</a>'.format(
                reverse_lazy(
                    "admin:skp_sasarankerja_matrikshasilperan",
                    kwargs={"obj_id": obj.id},
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
            status=status,
        ).filter(
            Q(periode_awal__range=(obj.periode_awal, obj.periode_akhir))
            | Q(periode_akhir__range=(obj.periode_awal, obj.periode_akhir))
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
        q = request.GET.get("q", None)
        uk = request.GET.get("unitkerja", None)
        status = request.GET.get("status", None)
        is_bupati = False
        if request.user.groups.filter(name="Bupati").exists():
            is_bupati = True
        if q:
            list_skp_bawahan = list_skp_bawahan.filter(
                Q(detailsasarankinerja__nama_pegawai__icontains=q)
                | Q(detailsasarankinerja__nip_pegawai__icontains=q)
            )
        if uk:
            list_skp_bawahan = list_skp_bawahan.filter(unor_id=uk)

        if status:
            list_skp_bawahan = list_skp_bawahan.filter(status=status)

        show_detail = [
            SasaranKinerja.Status.PENGAJUAN,
            SasaranKinerja.Status.PERSETUJUAN,
        ]
        extra_context = {
            "obj": obj,
            "is_bupati": is_bupati,
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
        is_bupati = False
        if request.user.groups.filter(name="Bupati").exists():
            is_bupati = True
        extra_context = {
            "title": "Penilaian SKP",
            "obj": obj,
            "batas_input": config.batas_input,
            "is_bupati": is_bupati,
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
        penilaian_bawahan = None
        try:
            penilaian_bawahan = PenilaianBawahan.objects.get(skp=sasaran_obj)
        except PenilaianBawahan.DoesNotExist:
            pass
        except PenilaianBawahan.MultipleObjectsReturned:
            penilaian_bawahan = PenilaianBawahan.objects.filter(
                skp=sasaran_obj
            ).order_by("-periode")
            if penilaian_bawahan.exists():
                penilaian_bawahan = penilaian_bawahan.first()

        bulan_list = []
        # if awal.month == akhir.month:
        bulan_list.append(
            {
                "bulan": "Tahunan",
                "range": "{} / {}".format(
                    awal.strftime("%Y-%m-%d"),
                    akhir.strftime("%Y-%m-%d"),
                ),
                "hasil": penilaian_bawahan.rating_hasil.nama.upper()
                if penilaian_bawahan and penilaian_bawahan.rating_hasil
                else "-",
                "perilaku": penilaian_bawahan.predikat_perilaku.nama.upper()
                if penilaian_bawahan and penilaian_bawahan.predikat_perilaku
                else "-",
                "nilai": penilaian_bawahan.get_predikat_kerja_display().upper()
                if penilaian_bawahan and penilaian_bawahan.predikat_kerja
                else "-",
                # "rencana_aksi_url": reverse_lazy(
                #     "admin:rencana-aksi-skp",
                #     kwargs={"skp_id": sasaran_obj.id},
                # ),
                "dokumen_evaluasi_url": reverse_lazy(
                    "admin:skp_sasarankinerja_evaluasi_kinerja",
                    kwargs={"skp_id": sasaran_obj.id},
                ),
                # reverse_lazy(
                #     "admin:bukti-dukung-skp",
                #     kwargs={"skp_id": sasaran_obj.id},
                # )
                # if sasaran_obj.status == 3
                # else
                "bukti_dukung_url": reverse_lazy(
                    "admin:bukti-dukung-skp",
                    kwargs={"skp_id": sasaran_obj.id},
                )
                if sasaran_obj.status == 3
                else "#",
                "penilaian_bawahan_url": reverse_lazy(
                    "admin:skp_penilaianbawahan",
                    kwargs={"skp_id": sasaran_obj.id},
                )
                if sasaran_obj.status == 3
                else "#",
                "export_penilaian_bawahan_url": reverse_lazy(
                    "admin:skp_penilaianbawahan_export",
                    kwargs={"skp_id": sasaran_obj.id},
                )
                if sasaran_obj.status == 3
                else "#",
                "kurva_penilaian_bawahan_url": reverse_lazy(
                    "admin:skp_penilaianbawahan_kurva",
                    kwargs={"skp_id": sasaran_obj.id},
                )
                if sasaran_obj.status == 3
                else "#",
                "cetak_form_penilaian_url": reverse_lazy(
                    "admin:skp_penilaianbawahan_formpenilaiancetak",
                    kwargs={
                        "skp_id": sasaran_obj.id,
                    },
                ),
            }
        )
        # else:
        #     for i in range(awal.month, akhir.month + 1):
        #         if i == awal.month:
        #             num_days = calendar.monthrange(awal.year, awal.month)[1]
        #             bulan_list.append(
        #                 {
        #                     "bulan": FULL_BULAN[i],
        #                     "range": "{} / {}-{}-{}".format(
        #                         awal.strftime("%Y-%m-%d"),
        #                         awal.year,
        #                         awal.month
        #                         if awal.month > 9
        #                         else "0{}".format(awal.month),
        #                         num_days,
        #                     ),
        #                     "rencana_aksi_url": reverse_lazy(
        #                         "admin:rencana-aksi-skp",
        #                         kwargs={"skp_id": sasaran_obj.id, "periode": i},
        #                     ),
        #                     "bukti_dukung_url": reverse_lazy(
        #                         "admin:bukti-dukung-skp",
        #                         kwargs={"skp_id": sasaran_obj.id, "periode": i},
        #                     )
        #                     if sasaran_obj.status == 3
        #                     else "#",
        #                     "penilaian_bawahan_url": reverse_lazy(
        #                         "admin:skp_penilaianbawahan",
        #                         kwargs={"skp_id": sasaran_obj.id, "periode": i},
        #                     )
        #                     if sasaran_obj.status == 3
        #                     else "#",
        #                     "export_penilaian_bawahan_url": reverse_lazy(
        #                         "admin:skp_penilaianbawahan_export",
        #                         kwargs={
        #                             "skp_id": sasaran_obj.id,
        #                             "periode": awal.month,
        #                         },
        #                     )
        #                     if sasaran_obj.status == 3
        #                     else "#",
        #                     "kurva_penilaian_bawahan_url": reverse_lazy(
        #                         "admin:skp_penilaianbawahan_kurva",
        #                         kwargs={
        #                             "skp_id": sasaran_obj.id,
        #                             "periode": awal.month,
        #                         },
        #                     )
        #                     if sasaran_obj.status == 3
        #                     else "#",
        #                     "cetak_form_penilaian_url": reverse_lazy(
        #                         "admin:skp_penilaianbawahan_formpenilaiancetak",
        #                         kwargs={
        #                             "skp_id": sasaran_obj.id,
        #                             "periode": awal.month,
        #                         },
        #                     ),
        #                 }
        #             )
        #         elif i == akhir.month:
        #             bulan_list.append(
        #                 {
        #                     "bulan": FULL_BULAN[i],
        #                     "range": "{}-{}-{} / {}".format(
        #                         akhir.year,
        #                         akhir.month
        #                         if akhir.month > 9
        #                         else "0{}".format(awal.month),
        #                         "01",
        #                         akhir.strftime("%Y-%m-%d"),
        #                     ),
        #                     "rencana_aksi_url": reverse_lazy(
        #                         "admin:rencana-aksi-skp",
        #                         kwargs={"skp_id": sasaran_obj.id, "periode": i},
        #                     ),
        #                     "bukti_dukung_url": reverse_lazy(
        #                         "admin:bukti-dukung-skp",
        #                         kwargs={"skp_id": sasaran_obj.id, "periode": i},
        #                     )
        #                     if sasaran_obj.status == 3
        #                     else "#",
        #                     "penilaian_bawahan_url": reverse_lazy(
        #                         "admin:skp_penilaianbawahan",
        #                         kwargs={"skp_id": sasaran_obj.id, "periode": i},
        #                     )
        #                     if sasaran_obj.status == 3
        #                     else "#",
        #                     "export_penilaian_bawahan_url": reverse_lazy(
        #                         "admin:skp_penilaianbawahan_export",
        #                         kwargs={
        #                             "skp_id": sasaran_obj.id,
        #                             "periode": awal.month,
        #                         },
        #                     )
        #                     if sasaran_obj.status == 3
        #                     else "#",
        #                     "kurva_penilaian_bawahan_url": reverse_lazy(
        #                         "admin:skp_penilaianbawahan_kurva",
        #                         kwargs={
        #                             "skp_id": sasaran_obj.id,
        #                             "periode": awal.month,
        #                         },
        #                     )
        #                     if sasaran_obj.status == 3
        #                     else "#",
        #                     "cetak_form_penilaian_url": reverse_lazy(
        #                         "admin:skp_penilaianbawahan_formpenilaiancetak",
        #                         kwargs={
        #                             "skp_id": sasaran_obj.id,
        #                             "periode": awal.month,
        #                         },
        #                     ),
        #                 }
        #             )
        #         else:
        #             num_days = calendar.monthrange(awal.year, awal.month)[1]
        #             bulan_list.append(
        #                 {
        #                     "bulan": FULL_BULAN[i],
        #                     "range": "{}-{}-{} / {}-{}-{}".format(
        #                         akhir.year,
        #                         i if i > 9 else "0{}".format(i),
        #                         "01",
        #                         akhir.year,
        #                         i if i > 9 else "0{}".format(i),
        #                         num_days,
        #                     ),
        #                     "rencana_aksi_url": reverse_lazy(
        #                         "admin:rencana-aksi-skp",
        #                         kwargs={"skp_id": sasaran_obj.id, "periode": i},
        #                     ),
        #                     "bukti_dukung_url": reverse_lazy(
        #                         "admin:bukti-dukung-skp",
        #                         kwargs={"skp_id": sasaran_obj.id, "periode": i},
        #                     )
        #                     if sasaran_obj.status == 3
        #                     else "#",
        #                     "penilaian_bawahan_url": reverse_lazy(
        #                         "admin:skp_penilaianbawahan",
        #                         kwargs={"skp_id": sasaran_obj.id, "periode": i},
        #                     )
        #                     if sasaran_obj.status == 3
        #                     else "#",
        #                     "export_penilaian_bawahan_url": reverse_lazy(
        #                         "admin:skp_penilaianbawahan_export",
        #                         kwargs={
        #                             "skp_id": sasaran_obj.id,
        #                             "periode": awal.month,
        #                         },
        #                     )
        #                     if sasaran_obj.status == 3
        #                     else "#",
        #                     "kurva_penilaian_bawahan_url": reverse_lazy(
        #                         "admin:skp_penilaianbawahan_kurva",
        #                         kwargs={
        #                             "skp_id": sasaran_obj.id,
        #                             "periode": awal.month,
        #                         },
        #                     )
        #                     if sasaran_obj.status == 3
        #                     else "#",
        #                     "cetak_form_penilaian_url": reverse_lazy(
        #                         "admin:skp_penilaianbawahan_formpenilaiancetak",
        #                         kwargs={
        #                             "skp_id": sasaran_obj.id,
        #                             "periode": awal.month,
        #                         },
        #                     ),
        #                 }
        #             )
        respon = {"success": True, "data": bulan_list}
        return JsonResponse(respon, safe=False)

    def view_matriks_hasil_peran(self, request, obj_id):
        obj = get_object_or_404(SasaranKinerja, pk=obj_id)
        show = request.GET.get("show", None)
        atasan = request.GET.get("atasan", None)
        cetak = request.GET.get("cetak", None)
        skp_childs = SasaranKinerja.objects.filter(induk_id=obj.id)
        extra_context = {
            "title": "Matrik Peran Hasil",
            "obj": obj,
            "rhk_list": obj.rencanahasilkerja_set.all(),
            "skp_childs": skp_childs,
            "show": True if show == "true" else False,
            "atasan": True if atasan == "true" else False,
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
                        induk_id=item.id,
                        skp=obj,
                        klasifikasi=RencanaHasilKerja.Klasifikasi.ORGANISASI,
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
        for i in RiwayatKeteranganSKP.objects.filter(skp=obj).order_by("-created"):
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

    def get_list_skp(self, unitkerja, tahun):
        list_id = []
        find_skp = SasaranKinerja.objects.filter(
            unor=unitkerja,
            status=SasaranKinerja.Status.PERSETUJUAN,
            periode_awal__year=tahun,
        )
        list_pegawai = list(find_skp.values_list("pegawai", flat=True).distinct())
        for i in list_pegawai:
            obj_skp = find_skp.filter(
                pegawai__id=i,
            )
            # print(obj_skp)
            if obj_skp.count() > 1:
                for i in obj_skp:
                    list_skp = obj_skp.filter(
                        periode_awal__lte=i.periode_awal,
                        periode_akhir__gte=i.periode_akhir,
                    )
                    if list_skp.exists():
                        list_id.append(list_skp.last().id)
            else:
                list_id.append(obj_skp.last().id)
        list_id = list(dict.fromkeys(list_id))
        return SasaranKinerja.objects.filter(pk__in=list_id)

    def rekonsiliasi_skp(self, request):
        TAHUN = []
        for i in range(2020, datetime.date.today().year + 2):
            TAHUN.append({"id": i, "text": i})
        if request.GET:
            tahun = request.GET.get("tahun", None)
            unitkerja = request.user.unitkerja
            if (
                request.user.is_superuser
                or request.user.groups.filter(name="Bupati").exists()
            ):
                unitkerja = request.GET.get("unitkerja", None)
                if unitkerja:
                    unitkerja = get_object_or_404(UnitKerja, id=unitkerja)

            list_skp_obj = self.get_list_skp(unitkerja, tahun)

            filename = "Rekonsiliasi SKP {} {}".format(unitkerja.unitkerja, tahun)
            response = HttpResponse(content_type="application/ms-excel")
            response["Content-Disposition"] = (
                'attachment; filename="' + filename + '.xls"'
            )
            wb = xlwt.Workbook(encoding="utf-8")
            ws = wb.add_sheet("sheet 1")
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = [
                "PNS_DINILAI_ID",
                "UNOR_ID",
                "TAHUN",
                "HASIL_KERJA",
                "PERILAKU_KERJA",
                "PEGAWAI_ATASAN_UNOR_NAMA",
                "PENILAI_JABATAN_NM",
                "PENILAI_GOLONGAN_ID",
                "PENILAI_NAMA",
                "NIP_NIK_PENILAI",
                "STATUS_PENILAIAN(ASN/NON_ASN)",
            ]
            rows = []
            for i in list_skp_obj:
                find_penilaian = PenilaianBawahan.objects.filter(skp=i).order_by(
                    "periode"
                )
                if find_penilaian.exists():
                    find_penilaian = find_penilaian.last()
                else:
                    find_penilaian = None

                isi = (
                    i.pejabat_penilai.id,
                    i.unor.id,
                    tahun,
                    find_penilaian.rating_hasil.keterangan
                    if find_penilaian and find_penilaian.rating_hasil
                    else "",
                    find_penilaian.predikat_perilaku.keterangan
                    if find_penilaian and find_penilaian.predikat_perilaku
                    else "",
                    i.detailsasarankinerja.unor_pejabat,
                    i.detailsasarankinerja.jabatan_pejabat,
                    i.detailsasarankinerja.get_golongan_pejabat(),
                    i.detailsasarankinerja.nama_pejabat,
                    i.detailsasarankinerja.nip_pejabat,
                    i.detailsasarankinerja.status_pejabat,
                )
                rows.append(isi)

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            font_style = xlwt.XFStyle()

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)
            return response

        extra_context = {
            "title": "Rekonsiliasi SKP",
            "tahun": TAHUN,
            "unit_kerja": UnitKerja.objects.filter(aktif=True),
        }
        return render(
            request, "admin/skp/sasarankinerja/rekonsiliasi.html", extra_context
        )

    def cetak_evaluasi_kinerja_pegawai(self, request, skp_id, extra_context={}):
        obj = get_object_or_404(SasaranKinerja, pk=skp_id)
        find_penilaian_bawahan = PenilaianBawahan.objects.filter(skp=obj).order_by(
            "-periode"
        )
        obj_penilaian = None
        if find_penilaian_bawahan.exists():
            obj_penilaian = find_penilaian_bawahan.first()
        extra_context.update(
            {
                "title": "Evaluasi Kinerja Pegawai",
                "obj": obj,
                "obj_penilaian": obj_penilaian,
            }
        )
        return render(request, "admin/skp/dokumen_evaluasi_kinerja.html", extra_context)

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
                self.admin_site.admin_view(self.list_riwayat_keterangan),
                name="skp_sasarankinerja_riwayat_keterangan",
            ),
            path(
                "<int:id>/view",
                self.admin_site.admin_view(self.view_changeform_skp),
                name="skp_sasarankinerja_view",
            ),
            path(
                "<int:skp_id>/evaluasi-kinerja",
                self.admin_site.admin_view(self.cetak_evaluasi_kinerja_pegawai),
                name="skp_sasarankinerja_evaluasi_kinerja",
            ),
            path(
                "option",
                self.admin_site.admin_view(self.load_induk_options),
                name="skp_sasarankinerja_induk_option",
            ),
            path(
                "rekonsiliasi",
                self.admin_site.admin_view(self.rekonsiliasi_skp),
                name="skp_sasarankinerja_rekonsiliasi",
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
