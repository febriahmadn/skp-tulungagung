import requests
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import resolve, path, reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from services.models import Configurations
from skp.forms.sasarankinerja_form import SasaranKinerjaForm
from skp.models import (
    SasaranKinerja,
    RencanaHasilKerja,
    DetailSasaranKinerja,
    PerilakuKerja,
    Perspektif,
)


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
    list_display_links = None

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
                class="btn btn-warning dropdown-toggle"
                data-toggle="dropdown" aria-haspopup="true"
                aria-expanded="false">Aksi</button>"""
        btn += '<div class="dropdown-menu" aria-labelledby="btnGroupDrop1">'
        btn += '<a class="dropdown-item" href="{}">Detail SKP</a>'.format(
            reverse_lazy("admin:detail-skp", kwargs={"id": obj.id})
        )
        btn += '<a class="dropdown-item" href="#">Matriks Peran Hasil</a>'
        btn += '<a class="dropdown-item" href="#">SKP Bawahan</a>'
        btn += '<a class="dropdown-item" href="#">Penilaian</a>'
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
            print(qs)
        else:
            qs = qs.filter(pegawai=request.user)
        return qs

    def view_detail_skp(self, request, id=None):
        obj = get_object_or_404(SasaranKinerja, pk=id)
        perilaku_kerja_list = PerilakuKerja.objects.filter(is_active=True)
        extra_context = {
            "title": "Detail SKP",
            "obj": obj,
            "pegawai": obj.pegawai,
            "penilai": obj.pejabat_penilai,
            "perilaku_kerja_list": perilaku_kerja_list,
            "perspektif_list": Perspektif.objects.all(),
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

    def action_change_status_skp(self, request):
        respon = {"success": False}
        skp_id = request.GET.get("skp_id", None)
        status = request.GET.get("status", None)
        try:
            obj = SasaranKinerja.objects.get(id=skp_id)
        except SasaranKinerja.DoesNotExist:
            pass
        else:
            if status:
                try:
                    obj.status = status
                    obj.save()
                except Exception:
                    pass
                else:
                    respon = {"success": True}
        return JsonResponse(respon)

    def view_changelist_penilaian_skp(self, request):
        extra_context = {"title": "Penilaian SKP Pegawai"}
        return super().changelist_view(request, extra_context)

    def view_cetak_skp_pegawai(self, request, obj_id):
        obj = get_object_or_404(SasaranKinerja, pk=obj_id)
        extra_context = {
            "obj": obj,
            "title": "Cetak SKP {} [{}]".format(
                obj.pegawai.username, obj.get_periode()
            ),
            "perilakukerja_list": PerilakuKerja.objects.filter(is_active=True),
        }
        return render(request, "admin/skp/sasarankinerja/cetak.html", extra_context)

    def get_urls(self):
        admin_url = super(SasaranKinerjaAdmin, self).get_urls()
        custom_url = [
            path(
                "penilaian",
                self.admin_site.admin_view(self.view_changelist_penilaian_skp),
                name="skp_sasarankinerja_changelist_penilaian",
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
                "change-status",
                self.admin_site.admin_view(self.action_change_status_skp),
                name="skp_sasarankinerja_changestatus",
            ),
            # path("skpdata/", self.view_custom, name="list_skp_admin"),
            # path("skpdata/add/", self.add_skp, name="add_skp_admin"),
        ]
        return custom_url + admin_url

    def save_model(self, request, obj, form, change):
        if not change:
            obj.save()
            # Create
            try:
                detail = DetailSasaranKinerja(
                    skp=obj,
                    nama_pegawai=obj.pegawai.get_complete_name(),
                    nip_pegawai=obj.pegawai.username,
                    jabatan_pegawai=obj.pegawai.jabatan,
                    golongan_pegawai=obj.pegawai.golongan,
                    unor_pegawai=obj.pegawai.unitkerja.unitkerja,
                    nama_pejabat=obj.pegawai.atasan.get_complete_name(),
                    nip_pejabat=obj.pegawai.atasan.username,
                    jabatan_pejabat=obj.pegawai.atasan.jabatan,
                    golongan_pejabat=obj.pegawai.atasan.golongan,
                    unor_pejabat=obj.pegawai.atasan.unitkerja.unitkerja,
                )
                detail.save()
            except Exception as e:
                print(e)
        return super().save_model(request, obj, form, change)
