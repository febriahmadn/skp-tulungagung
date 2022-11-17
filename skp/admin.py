from django.contrib import admin

# model import
from .models import (
    SasaranKinerja,
    DetailSasaranKinerja,
    RencanaHasilKerja,
    Perspektif,
    IndikatorKinerjaIndividu,
    PerilakuKerja,
    DaftarPerilakuKerja,
    Lampiran,
    DaftarLampiran,
)

# admin Import
from skp.subadmin.sasarankinerja_admin import SasaranKinerjaAdmin
from .subadmin.detailsasarankerja_admin import DetailsasarankerjaAdmin
from .subadmin.rencanahasilkerja_admin import RencanahasilkerjaAdmin
from .subadmin.perspektif_admin import PerspektifAdmin
from .subadmin.indikator_admin import IndikatorAdmin
from .subadmin.perilakukerja_admin import PerilakukerjaAdmin
from .subadmin.daftarperilakukerja_admin import DaftarperilakukerjaAdmin
from .subadmin.lampiran_admin import LampiranAdmin
from .subadmin.daftarlampiran_admin import DaftarlampiranAdmin


admin.site.register(DetailSasaranKinerja, DetailsasarankerjaAdmin)
admin.site.register(RencanaHasilKerja, RencanahasilkerjaAdmin)
admin.site.register(Perspektif, PerspektifAdmin)
admin.site.register(IndikatorKinerjaIndividu, IndikatorAdmin)
admin.site.register(SasaranKinerja, SasaranKinerjaAdmin)
admin.site.register(PerilakuKerja, PerilakukerjaAdmin)
admin.site.register(DaftarPerilakuKerja, DaftarperilakukerjaAdmin)
admin.site.register(Lampiran, LampiranAdmin)
admin.site.register(DaftarLampiran, DaftarlampiranAdmin)
