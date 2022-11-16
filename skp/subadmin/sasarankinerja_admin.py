from django.contrib import admin
from skp.forms.sasarankinerja_form import SasaranKinerjaForm, SKPForm
from django.utils.safestring import mark_safe
from django.urls import resolve, path
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect

class SasaranKinerjaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pegawai', 'get_unor', 'jabatan', 'pejabat_penilai', 'periode_awal', 'periode_akhir', 'pendekatan', 'status')
    form = SasaranKinerjaForm
    list_display_links = None

    def get_unor(self, obj):
        if obj.unor:
            return obj.unor
        elif obj.unor_text:
            return obj.unor_text
        return ''
    get_unor.short_description = 'Unor'

    def get_period(self, obj):
        return str(obj.periode_awal)+" / "+str(obj.periode_akhir)
    get_period.short_description = "Periode"

    def Aksi(self, obj):
        btn = '<div class="btn-group" role="group">'
        btn += '<button id="btnGroupDrop1" type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Aksi</button>'
        btn += '<div class="dropdown-menu" aria-labelledby="btnGroupDrop1">'
        btn += '<a class="dropdown-item" href="#">Detail SKP</a>'
        btn += '<a class="dropdown-item" href="#">Matriks Peran Hasil</a>'
        btn += '<a class="dropdown-item" href="#">SKP Bawahan</a>'
        btn += '<a class="dropdown-item" href="#">Penilaian</a>'
        btn += '</div>'
        btn += '</div>'
        return mark_safe(btn)
    Aksi.short_description = "Aksi"

    def view_custom(self, request, extra_context={}):
        func_view, func_view_args, func_view_kwargs  = resolve(request.path)
        self.request = request
        if func_view.__name__ == "view_custom":
            extra_context.update({'title':"Daftar SKP","type":"skp_list"})
            self.list_display = ('get_unor','get_period','pendekatan','jabatan','status','Aksi')
            self.list_filter = ('pendekatan','status')
        return super(SasaranKinerjaAdmin, self).changelist_view(request, extra_context=extra_context)
    
    def changelist_view(self, request, extra_context={}):
        print(dir(request.user))
        print(request.user.is_staff)
        if request.user.is_admin:
            self.list_display = ('pk', 'pegawai', 'get_unor', 'jabatan', 'pejabat_penilai', 'periode_awal', 'periode_akhir', 'pendekatan', 'status','Aksi')
            self.list_filter = []
        else:
            self.list_display = ('get_unor','get_period','pendekatan','jabatan','status','Aksi')
            self.list_filter = ['pendekatan','status']
        return super(SasaranKinerjaAdmin, self).changelist_view(request, extra_context=extra_context)

    def add_skp(self, request, obj=None, **kwargs):
        form = SKPForm
        form.user = request.user
        print(form)
        extra_context = {
            'title': "Tambah SKP",
            'form' : form
        }
        url_ = ""
        template = loader.get_template("admin/skp/sasarankinerja/changeform_skp.html")
        # ec = RequestContext(request, extra_context)
        return HttpResponse(template.render(extra_context))

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = SasaranKinerjaForm
        form = super().get_form(request, obj, **kwargs)
        form.request_user = request.user
        return form

    # def get_queryset(self, request):
    #     queryset = super(SasaranKinerjaAdmin, self).get_queryset()
    #     queryset = queryset # TODO
    #     return queryset

    def get_urls(self):
        urls = super(SasaranKinerjaAdmin, self).get_urls()
        urlp = [
            path("skpdata/", self.view_custom, name="list_skp_admin"),
            path("skpdata/add/", self.add_skp, name="add_skp_admin"),
        ]
        return urlp + urls
