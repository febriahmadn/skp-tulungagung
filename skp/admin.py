from django.contrib import admin

from skp.models import SasaranKinerja
from skp.subadmin.sasarankinerja_admin import SasaranKinerjaAdmin


admin.site.register(SasaranKinerja, SasaranKinerjaAdmin)
