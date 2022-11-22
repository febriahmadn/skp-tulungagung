from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.urls import resolve, path, reverse_lazy, reverse
from django.template import loader
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from skp.forms.sasarankinerja_form import SasaranKinerjaForm, SKPForm
from skp.forms.rhk_form import RHKJFJAForm, RHKJPTForm
from skp.forms.indikator_kinerja_form import IndikatorForm
from skp.models import SasaranKinerja, RencanaHasilKerja


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

    def add_skp(self, request, obj=None, **kwargs):
        form = SKPForm
        form.user = request.user
        # print(form)
        extra_context = {"title": "Tambah SKP", "form": form}
        template = loader.get_template("admin/skp/sasarankinerja/changeform_skp.html")
        # ec = RequestContext(request, extra_context)
        return HttpResponse(template.render(extra_context))

    def get_form(self, request, obj=None, **kwargs):
        kwargs["form"] = SasaranKinerjaForm
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form

    def get_queryset(self, request):
        qs = super(SasaranKinerjaAdmin, self).get_queryset(request)
        qs = qs.filter(pegawai=request.user)
        return qs

    def detail_skp(self, request, extra_context={}, id=None):
        try:
            obj = SasaranKinerja.objects.get(pk=id)
        except SasaranKinerja.DoesNotExist:
            raise Http404()
        except Exception as e:
            print(e)
            raise Http404()
        else:
            if obj.jenis_jabatan == SasaranKinerja.JenisJabatan.JPT:
                if request.POST:
                    jenis_post = request.POST.get("jenis_post", None)
                    if jenis_post == "rhk":
                        form = RHKJPTForm(request.POST)
                    elif jenis_post == "indikator":
                        form = IndikatorForm(request.POST)

                    if form.is_valid():
                        form.save()
                        messages.success(request, "Data Telah Berhasil Tersimpan")
                        return redirect(
                            reverse("admin:detail-skp", kwargs={"id": obj.id})
                        )
                    else:
                        messages.error(request, form.errors.as_text())
                else:
                    form = RHKJPTForm(initial={"skp": obj.id})
                    indikator_form = IndikatorForm
            else:
                form = RHKJFJAForm
                indikator_form = IndikatorForm
            hasil_kerja_list = RencanaHasilKerja.objects.filter(skp=obj).order_by(
                "-created"
            )
            extra_context.update(
                {
                    "title": "Detail SKP",
                    "obj": obj,
                    "pegawai": obj.pegawai,
                    "penilai": obj.pejabat_penilai,
                    "RHK_Form": form,
                    "hasil_kerja": hasil_kerja_list,
                    "indikator_form": indikator_form,
                }
            )
        return render(
            request, "admin/skp/sasarankinerja/detail_skp.html", extra_context
        )

    def get_urls(self):
        urls = super(SasaranKinerjaAdmin, self).get_urls()
        urlp = [
            path("<int:id>/detail", self.detail_skp, name="detail-skp"),
            # path("skpdata/", self.view_custom, name="list_skp_admin"),
            # path("skpdata/add/", self.add_skp, name="add_skp_admin"),
        ]
        return urlp + urls
