from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.safestring import mark_safe

from usom.forms import AccountForm
from usom.models import Account, UnitKerja


class UnitKerjaAdmin(admin.ModelAdmin):
    list_display = ("id", "unitkerja")


admin.site.register(UnitKerja, UnitKerjaAdmin)


class AccountAdmin(UserAdmin):
    list_display = ("username", "nama_lengkap", "email")
    readonly_fields = ("last_login", "date_joined")
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
                    "atasan",
                    ("gelar_depan", "nama_lengkap", "gelar_belakang"),
                    "jabatan",
                    "jenis_jabatan",
                    "unitkerja",
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
        html_ = '''
        <span>{}</span></br>
        <span class="text-muted">{}</span>
        '''.format(obj.username, obj.get_complete_name())
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

    def view_pegawai_edit_profile(self, request):
        extra_context = {
            "title": "Edit Profile ({})".format(request.user.username),
            "title_sort": "Edit Profile",
            "golongan_list": Account.GOLONGAN,
            "unor_list": UnitKerja.objects.filter(aktif=True),
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

    def get_urls(self):
        admin_url = super().get_urls()
        custom_url = [
            path(
                "profile",
                self.admin_site.admin_view(self.view_pegawai_profile),
                name="usom_account_profile",
            ),
            path(
                "profile/edit",
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
        ]
        return custom_url + admin_url


admin.site.register(Account, AccountAdmin)
