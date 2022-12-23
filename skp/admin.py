from django.contrib import admin

# admin Import
from skp.subadmin.sasarankinerja_admin import SasaranKinerjaAdmin

# model import
from .models import (BuktiDukung, DaftarEkspetasi, DaftarLampiran,
                     DaftarPerilakuKerja, DaftarPerilakuKerjaPegawai,
                     DetailSasaranKinerja, Hasil, IndikatorKinerjaIndividu,
                     Lampiran, PenilaianBawahan, PerilakuKerja, Perspektif,
                     Realisasi, RencanaAksi, RencanaHasilKerja, SasaranKinerja,
                     UmpanBalik, UmpanBalikPegawai)
from .subadmin.bukti_dukung_admin import BuktiDukungAdmin
from .subadmin.daftarekspetasi_admin import DaftarEkspetasiAdmin
from .subadmin.daftarlampiran_admin import DaftarlampiranAdmin
from .subadmin.daftarperilakuerjapegawai_admin import \
    DaftarPerilakuKerjaPegawaiAdmin
from .subadmin.daftarperilakukerja_admin import DaftarperilakukerjaAdmin
from .subadmin.detailsasarankerja_admin import DetailsasarankerjaAdmin
from .subadmin.indikator_admin import IndikatorAdmin
from .subadmin.lampiran_admin import LampiranAdmin
from .subadmin.penilaian_bawahan_admin import PenilaianBawahanAdmin
from .subadmin.perilakukerja_admin import PerilakukerjaAdmin
from .subadmin.perspektif_admin import PerspektifAdmin
from .subadmin.realisasi_admin import RealisasiAdmin
from .subadmin.rencana_aksi_admin import RencanaAksiAdmin
from .subadmin.rencanahasilkerja_admin import RencanahasilkerjaAdmin
from .subadmin.umpanbalik_admin import UmpanBalikAdmin
from .subadmin.umpanbalikpegawai_admin import UmpanBalikPegawaiAdmin

admin.site.register(DetailSasaranKinerja, DetailsasarankerjaAdmin)
admin.site.register(RencanaHasilKerja, RencanahasilkerjaAdmin)
admin.site.register(Perspektif, PerspektifAdmin)
admin.site.register(IndikatorKinerjaIndividu, IndikatorAdmin)
admin.site.register(SasaranKinerja, SasaranKinerjaAdmin)
admin.site.register(PerilakuKerja, PerilakukerjaAdmin)
admin.site.register(DaftarPerilakuKerja, DaftarperilakukerjaAdmin)
admin.site.register(DaftarPerilakuKerjaPegawai, DaftarPerilakuKerjaPegawaiAdmin)
admin.site.register(BuktiDukung, BuktiDukungAdmin)
admin.site.register(RencanaAksi, RencanaAksiAdmin)
admin.site.register(Realisasi, RealisasiAdmin)
admin.site.register(Lampiran, LampiranAdmin)
admin.site.register(DaftarLampiran, DaftarlampiranAdmin)

admin.site.register(Hasil)
admin.site.register(UmpanBalik, UmpanBalikAdmin)
admin.site.register(UmpanBalikPegawai, UmpanBalikPegawaiAdmin)
admin.site.register(DaftarEkspetasi, DaftarEkspetasiAdmin)
admin.site.register(PenilaianBawahan, PenilaianBawahanAdmin)
