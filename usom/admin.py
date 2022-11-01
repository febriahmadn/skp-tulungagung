from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from usom.models import Account, UnitKerja


class UnitKerjaAdmin(admin.ModelAdmin):
    list_display = ('id', 'unitkerja')

admin.site.register(UnitKerja, UnitKerjaAdmin)

class AccountAdmin(UserAdmin):
    pass

admin.site.register(Account, AccountAdmin)
