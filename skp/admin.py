from django.contrib import admin

#model import 
from .models import DetailSasaranKinerja, RencanaHasilKerja, Perspektif

#admin Import 
from .subadmin.detailsasarankerja_admin import DetailsasarankerjaAdmin
from .subadmin.rencanahasilkerja_admin import RencanahasilkerjaAdmin
from .subadmin.perspektif_admin import PerspektifAdmin



admin.site.register(DetailSasaranKinerja, DetailsasarankerjaAdmin)
admin.site.register(RencanaHasilKerja, RencanahasilkerjaAdmin)
admin.site.register(Perspektif, PerspektifAdmin)
