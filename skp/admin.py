from django.contrib import admin

#model import 
from .models import DetailSasaranKinerja, RencanaHasilKerja, Perspektif, IndikatorKinerjaIndividu

#admin Import 
from .subadmin.detailsasarankerja_admin import DetailsasarankerjaAdmin
from .subadmin.rencanahasilkerja_admin import RencanahasilkerjaAdmin
from .subadmin.perspektif_admin import PerspektifAdmin
from .subadmin.indikator_admin import IndikatorAdmin



admin.site.register(DetailSasaranKinerja, DetailsasarankerjaAdmin)
admin.site.register(RencanaHasilKerja, RencanahasilkerjaAdmin)
admin.site.register(Perspektif, PerspektifAdmin)
admin.site.register(IndikatorKinerjaIndividu, IndikatorAdmin)
