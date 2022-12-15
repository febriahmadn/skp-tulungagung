from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.safestring import mark_safe

from services.functions.sinkron_sipo import ServiceSipo
from usom.forms import AccountForm, EditProfilPegawai
from usom.models import Account, UnitKerja


class UnitKerjaAdmin(admin.ModelAdmin):
    list_display = ("id", "unitkerja", "id_sipo", "aktif")
    search_fields = ("unitkerja",)
    list_filter = ("aktif",)

    def load_data_json(self, request):
        respon = []
        unitkerja_list = UnitKerja.objects.filter(aktif=True)
        if unitkerja_list.exists():
            for item in unitkerja_list:
                respon.append(
                    {
                        "id": item.id,
                        "text": item.unitkerja,
                    }
                )
        return JsonResponse(respon, safe=False)

    def get_urls(self):
        admin_url = super().get_urls()
        custom_url = [
            path(
                "load-data",
                self.admin_site.admin_view(self.load_data_json),
                name="usom_unitkerja_loaddata",
            ),
        ]
        return custom_url + admin_url


admin.site.register(UnitKerja, UnitKerjaAdmin)


class AccountAdmin(UserAdmin):
    list_display = ("username", "nama_lengkap", "email")
    readonly_fields = ("last_login", "date_joined")
    search_fields = ("username", "nama_lengkap", "jabatan")
    ordering = ("-id",)
    form = AccountForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                    "email",
                ),
            },
        ),
        (
            "Informasi",
            {
                "fields": (
                    "unitkerja",
                    "atasan",
                    ("gelar_depan", "nama_lengkap", "gelar_belakang"),
                    "jabatan",
                    "jenis_jabatan",
                    "golongan",
                    "eselon",
                    "jenis_pegawai",
                ),
            },
        ),
        (
            "Hak Akses",
            {
                "fields": (
                    "tangggal_nonaktif",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (
            "Tanggal Penting",
            {
                "fields": ("last_login", "date_joined"),
            },
        ),
    )

    def get_list_display(self, request):
        if request.user.is_superuser:
            return (
                "get_name_and_username",
                "unitkerja",
                "jabatan",
                "jenis_jabatan",
                "get_akses",
                "aksi",
            )
        return super().get_list_display(request)

    def get_name_and_username(self, obj):
        html_ = """
        <span>{}</span></br>
        <span class="text-muted">{}</span>
        """.format(
            obj.username, obj.get_complete_name()
        )
        return mark_safe(html_)

    get_name_and_username.short_description = "Pegawai"

    def get_akses(self, obj):
        groups = obj.groups.all()
        if groups.exists():
            return ["".join(item.name) for item in groups]
        return "-"

    get_akses.short_description = "Akses"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form

    def aksi(self, obj):
        str_aksi = """
            <a onclick="$(\'#loginas-form\').attr(\'action\',\'%s\');
            $(\'#loginas-form\').submit(); return false;"
            class="btn btn-icon btn-sm btn-warning"
            title="Login sebagai %s" href="#"><i class="fa fa-user"></i></a>
        """ % (
            reverse("loginas-user-login", kwargs={"user_id": obj.id}),
            obj.nama_lengkap,
        )
        return mark_safe(str_aksi)

    def view_pegawai_profile(self, request):
        extra_context = {
            "title": "Profile ({})".format(request.user.username),
            "title_sort": "Profile",
            "unor_list": UnitKerja.objects.filter(aktif=True),
            "atasan": request.user.atasan if request.user.atasan else None,
        }
        # if request.user.atasan is None:
        #     extra_context.update({
        #         'unor_list': UnitKerja.objects.filter(aktif=True)
        #     })
        return render(request, "admin/usom/account/profile.html", extra_context)

    def view_pegawai_edit_profile(self, request, id):
        try:
            obj = Account.objects.get(pk=id)
        except Account.DoesNotExist or Exception as e:
            print(e)
            raise Http404

        form = EditProfilPegawai(instance=obj)
        if request.POST:
            form = EditProfilPegawai(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Berhasil merubah {}".format(obj.get_complete_name())
                )
            else:
                print(form.errors)
                messages.error(request, form.errors)

        extra_context = {
            "title": "Edit Profile ({})".format(request.user.username),
            "title_sort": "Edit Profile",
            # "golongan_list": Account.GOLONGAN,
            # "unor_list": UnitKerja.objects.filter(aktif=True),
            "obj": obj,
            "form": form,
        }
        return render(request, "admin/usom/account/profile_edit.html", extra_context)

    def view_pegawai_json(self, request):
        results = []
        search = request.GET.get("search", None)
        unor_id = request.GET.get("unor_id", None)
        pegawai_list = Account.objects.filter(is_active=True)
        if unor_id:
            pegawai_list = pegawai_list.filter(unitkerja_id=unor_id)

        if search:
            pegawai_list = pegawai_list.filter(
                Q(nama_lengkap__icontains=search) | Q(username__icontains=search)
            )
        pegawai_list = pegawai_list.exclude(id=request.user.id)
        for item in pegawai_list:
            obj = {
                "id": item.id,
                "text": "[{}] {}".format(item.username, item.get_complete_name()),
            }
            results.append(obj)
        respon = {"success": True, "results": results}
        return JsonResponse(respon)

    def action_set_pegawai_atasan(self, request):
        respon = {"success": False, "message": "Terjadi kesalahan"}
        user = request.user
        atasan_id = request.GET.get("atasan_id", None)
        if atasan_id:
            try:
                obj = Account.objects.get(id=atasan_id)
            except Account.DoesNotExist:
                respon = {"success": False, "message": "Akun atasan tidak ditemukan"}
            else:
                user.atasan = obj
                user.save()
                respon = {"success": True}
        return JsonResponse(respon)

    def sinkron_data_pegawai(self, request):
        respon = {}
        nip = request.GET.get("nip", None)
        if nip:
            sync = ServiceSipo().sinkron_pegawai_by_nip(nip)
            if sync:
                try:
                    pegawai = Account.objects.get(username=nip)
                except Account.DoesNotExist:
                    pass
                else:
                    data = {
                        "nip": pegawai.username,
                        "nama_lengkap": pegawai.get_complete_name(),
                        "unor": pegawai.unitkerja.unitkerja
                        if pegawai.unitkerja
                        else "-",
                        "jabatan": pegawai.jabatan,
                        "jenis_jabatan": pegawai.jenis_jabatan,
                        "golongan": pegawai.golongan,
                        "eselon": pegawai.eselon,
                    }
                    respon = {"success": True, "data": data}
        return JsonResponse(respon)

    def get_urls(self):
        admin_url = super().get_urls()
        custom_url = [
            path(
                "profile",
                self.admin_site.admin_view(self.view_pegawai_profile),
                name="usom_account_profile",
            ),
            path(
                "profile/<int:id>/edit",
                self.admin_site.admin_view(self.view_pegawai_edit_profile),
                name="usom_account_profile_edit",
            ),
            path(
                "json",
                self.admin_site.admin_view(self.view_pegawai_json),
                name="usom_account_as_json",
            ),
            path(
                "set-atasan",
                self.admin_site.admin_view(self.action_set_pegawai_atasan),
                name="usom_account_set_atasan",
            ),
            path(
                "sync-data",
                self.admin_site.admin_view(self.sinkron_data_pegawai),
                name="usom_account_sync_data",
            ),
        ]
        return custom_url + admin_url


admin.site.register(Account, AccountAdmin)
