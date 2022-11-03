from django.contrib import admin

#model import 
from .models import DetailSasaranKinerja, RencanaHasilKerja

#admin Import 
from .subadmin.detailsasarankerja_admin import DetailsasarankerjaAdmin
from .subadmin.rencanahasilkerja_admin import RencanahasilkerjaAdmin



admin.site.register(DetailSasaranKinerja, DetailsasarankerjaAdmin)
admin.site.register(RencanaHasilKerja, RencanahasilkerjaAdmin)