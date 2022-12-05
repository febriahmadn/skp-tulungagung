from django.contrib import admin

# admin Import
from skp.subadmin.sasarankinerja_admin import SasaranKinerjaAdmin

# model import
from .models import (DaftarLampiran, DaftarPerilakuKerja, DetailSasaranKinerja,
                     IndikatorKinerjaIndividu, Lampiran, PerilakuKerja,
                     Perspektif, RencanaHasilKerja, SasaranKinerja,
                     DaftarPerilakuKerjaPegawai, RencanaAksi)
from .subadmin.daftarlampiran_admin import DaftarlampiranAdmin
from .subadmin.daftarperilakukerja_admin import DaftarperilakukerjaAdmin
from .subadmin.detailsasarankerja_admin import DetailsasarankerjaAdmin
from .subadmin.indikator_admin import IndikatorAdmin
from .subadmin.lampiran_admin import LampiranAdmin
from .subadmin.perilakukerja_admin import PerilakukerjaAdmin
from .subadmin.perspektif_admin import PerspektifAdmin
from .subadmin.rencanahasilkerja_admin import RencanahasilkerjaAdmin
from .subadmin.daftarperilakuerjapegawai_admin import DaftarPerilakuKerjaPegawaiAdmin
from .subadmin.rencana_aksi_admin import RencanaAksiAdmin

admin.site.register(DetailSasaranKinerja, DetailsasarankerjaAdmin)
admin.site.register(RencanaHasilKerja, RencanahasilkerjaAdmin)
admin.site.register(Perspektif, PerspektifAdmin)
admin.site.register(IndikatorKinerjaIndividu, IndikatorAdmin)
admin.site.register(SasaranKinerja, SasaranKinerjaAdmin)
admin.site.register(PerilakuKerja, PerilakukerjaAdmin)
admin.site.register(DaftarPerilakuKerja, DaftarperilakukerjaAdmin)
admin.site.register(
    DaftarPerilakuKerjaPegawai,
    DaftarPerilakuKerjaPegawaiAdmin
)
admin.site.register(RencanaAksi, RencanaAksiAdmin)
admin.site.register(Lampiran, LampiranAdmin)
admin.site.register(DaftarLampiran, DaftarlampiranAdmin)
