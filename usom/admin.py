from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

from usom.models import Account, UnitKerja
from usom.forms import AccountForm


class UnitKerjaAdmin(admin.ModelAdmin):
    list_display = ("id", "unitkerja")


admin.site.register(UnitKerja, UnitKerjaAdmin)


class AccountAdmin(UserAdmin):
    list_display = ('username', 'nama_lengkap', 'email')
    readonly_fields = ('last_login','date_joined')
    form = AccountForm
    fieldsets = (
        (None, {
            "fields": (
                'username',
                'password',
                'email',
            ),
        }),
        ("Informasi", {
            "fields": (
                ('gelar_depan','nama_lengkap','gelar_belakang'),
                'jabatan',
                'jenis_jabatan',
                'unitkerja',
                'golongan',
                'eselon',
                'jenis_pegawai',
            ),
        }),
        ("Hak Akses", {
            "fields": (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
            ),
        }),
        ("Tanggal Penting", {
            "fields": (
                "last_login",
                "date_joined"
            ),
        }),
    )

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('username', 'nama_lengkap', 'email','aksi')
        return super().get_list_display(request)
    
    def aksi(self, obj):
        str_aksi = '''
            <a onclick="$(\'#loginas-form\').attr(\'action\',\'%s\');
            $(\'#loginas-form\').submit(); return false;"
            class="btn btn-icon btn-sm btn-warning"
            title="Login sebagai %s" href="#"><i class="fa fa-user"></i></a>
        ''' % (
            reverse('loginas-user-login',
                    kwargs={'user_id': obj.id }),
            obj.nama_lengkap
            )
        return mark_safe(str_aksi)


admin.site.register(Account, AccountAdmin)
