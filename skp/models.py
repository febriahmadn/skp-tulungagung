from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from skp.utils import FULL_BULAN
from usom.models import Account, Golongan, UnitKerja


class SasaranKinerja(models.Model):
    class Pendekatan(models.IntegerChoices):
        KUANTITATIF = 1, "Kuantitatif"
        KUALITATIF = 2, "Kualitatif"

    class Status(models.IntegerChoices):
        DRAFT = 1, "Draft"
        PENGAJUAN = 2, "Pengajuan"
        PERSETUJUAN = 3, "Persetujuan"
        CLOSE = 4, "Close"
        ARCHIVE = 5, "Archive"

    class JenisJabatan(models.IntegerChoices):
        JPT = 1, "Jabatan Pimpinan Tinggi"
        JF = 2, "Jabatan Fungsional"
        JA = 3, "Jabatan Administrator"

    induk = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    pegawai = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    unor = models.ForeignKey(UnitKerja, null=True, on_delete=models.SET_NULL)
    unor_text = models.CharField("Unor Text", max_length=255, null=True, blank=True)
    jabatan = models.CharField("Jabatan", max_length=255, null=True, blank=True)
    pejabat_penilai = models.ForeignKey(
        Account,
        null=True,
        on_delete=models.SET_NULL,
        related_name="pejabat_penilai_set",
    )
    jenis_jabatan = models.IntegerField(
        choices=JenisJabatan.choices,
        verbose_name="Jenis Jabatan",
        null=True,
        blank=True,
    )
    periode_awal = models.DateField(null=True, verbose_name="Periode Awal")
    periode_akhir = models.DateField(null=True, verbose_name="Periode Akhir")
    pendekatan = models.IntegerField(choices=Pendekatan.choices, null=True)
    status = models.IntegerField(
        choices=Status.choices, null=True, default=Status.DRAFT
    )
    keterangan = models.CharField("Keterangan", max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    def get_periode(self):
        return "{} - {}".format(
            self.periode_awal.strftime("%d/%m/%Y"),
            self.periode_akhir.strftime("%d/%m/%Y"),
        )

    def get_rencanakerja_utama(self):
        return self.rencanahasilkerja_set.filter(jenis=1).order_by("id", "induk")

    def get_rencanakerja_tambahan(self):
        return self.rencanahasilkerja_set.filter(jenis=2).order_by("id", "induk")

    class Meta:
        verbose_name = "Sasaran Kinerja Pegawai"
        verbose_name_plural = "Sasaran Kinerja Pegawai"


class RiwayatKeteranganSKP(models.Model):
    skp = models.ForeignKey(
        SasaranKinerja,
        on_delete=models.CASCADE,
        verbose_name="Sasaran Kinerja Pegawai",
    )
    keterangan = models.CharField("Keterangan", max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Riwayat Keterangan Sasaran Kinerja Pegawai"
        verbose_name_plural = "Riwayat Keterangan Sasaran Kinerja Pegawai"


class DetailSasaranKinerja(models.Model):
    skp = models.OneToOneField(SasaranKinerja, on_delete=models.CASCADE)
    # data pegawai
    nama_pegawai = models.CharField(
        "Nama Pegawai", max_length=200, null=True, blank=True
    )
    nip_pegawai = models.CharField("NIP Pegawai", max_length=200, null=True, blank=True)
    golongan_pegawai = models.CharField(
        "Pangkat Golongan Pegawai", max_length=10, null=True, blank=True
    )
    jabatan_pegawai = models.CharField(
        "Jabatan Pegawai", max_length=200, null=True, blank=True
    )
    unor_pegawai = models.CharField(
        "Unor Pegawai", max_length=200, null=True, blank=True
    )
    status_pegawai = models.CharField(
        "Status Pegawai", max_length=200, null=True, blank=True
    )
    # data pejabat penilai
    nama_pejabat = models.CharField(
        "Nama Pejabat", max_length=200, null=True, blank=True
    )
    nip_pejabat = models.CharField("NIP Pejabat", max_length=200, null=True, blank=True)
    golongan_pejabat = models.CharField(
        "Pangkat Golongan Pejabat", max_length=10, null=True, blank=True
    )
    jabatan_pejabat = models.CharField(
        "Jabatan Pejabat", max_length=200, null=True, blank=True
    )
    unor_pejabat = models.CharField(
        "Unor Pejabat", max_length=200, null=True, blank=True
    )
    status_pejabat = models.CharField(
        "Status Pejabat", max_length=200, null=True, blank=True
    )

    def get_golongan_pejabat(self):
        find_penilai_golongan = Golongan.objects.filter(
            kode=self.golongan_pejabat
        )
        if find_penilai_golongan.exists():
            return find_penilai_golongan.last().kode_angka
        else:
            return ""

    def get_golongan_pegawai(self):
        find_golongan = Golongan.objects.filter(
            kode=self.golongan_pegawai
        )
        if find_golongan.exists():
            return find_golongan.last().kode_angka
        else:
            return ""

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Detail Sasaran Kinerja"
        verbose_name_plural = "Detail Sasaran Kinerja"


class RencanaHasilKerja(models.Model):
    class Jenis(models.IntegerChoices):
        UTAMA = 1, "Utama"
        TAMBAHAN = 2, "Tambahan"

    class Klasifikasi(models.IntegerChoices):
        ORGANISASI = 1, "Organisasi"
        INDIVIDU = 2, "Individu"

    induk = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    skp = models.ForeignKey(
        SasaranKinerja,
        on_delete=models.CASCADE,
        verbose_name="Sasaran Kinerja Pegawai",
    )
    rencana_kerja = models.CharField("Rencana Hasil Kerja", max_length=255, null=True)
    penugasan_dari = models.CharField(
        "Penugasan Dari", max_length=255, null=True, blank=True
    )
    jenis = models.IntegerField(
        choices=Jenis.choices, verbose_name="Jenis Rencana Hasil Kerja"
    )
    klasifikasi = models.IntegerField(
        choices=Klasifikasi.choices,
        verbose_name="Klasifikasi Rencana Hasil Kerja",
    )
    unor = models.ForeignKey(
        UnitKerja, null=True, blank=True, on_delete=models.SET_NULL
    )
    ekinerja_id = models.IntegerField("Ekinerja ID", null=True, blank=True)
    aspek = models.CharField("Aspek", null=True, blank=True, max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.rencana_kerja))

    class Meta:
        verbose_name = "Rencana Hasil Kerja"
        verbose_name_plural = "Rencana Hasil Kerja"


class Perspektif(models.Model):
    perspektif = models.CharField("Perspektif", max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.perspektif))

    class Meta:
        verbose_name = "Perspektif"
        verbose_name_plural = "Perspektif"


class IndikatorKinerjaIndividu(models.Model):
    rencana_kerja = models.ForeignKey(
        RencanaHasilKerja,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Rencana Hasil Kerja",
    )
    skp = models.ForeignKey(
        SasaranKinerja,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sasaran Kinerja Pegawai",
    )
    ekinerja_id = models.IntegerField("Ekinerja ID", null=True, blank=True)
    indikator = models.CharField("Indikator", max_length=255, null=True)
    target = models.CharField("Target", max_length=100, null=True, blank=True)
    aspek = models.CharField("Aspek", null=True, blank=True, max_length=50)
    perspektif = models.ForeignKey(
        Perspektif, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Indikator Kinerja Individu"
        verbose_name_plural = "Indikator Kinerja Individu"


class PerilakuKerja(models.Model):
    # class Status(models.IntegerChoices):
    #     ACTIVE = 1, "Aktif"
    #     NONACTIVE = 2, "Non Aktif"

    perilaku_kerja = models.CharField("Perilaku Kerja", max_length=200)
    # status = models.IntegerField(choices=Status.choices, null=True, default=1)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.perilaku_kerja:
            return self.perilaku_kerja
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Perilaku Kerja"
        verbose_name_plural = "Perilaku Kerja"


class DaftarPerilakuKerja(models.Model):
    # class Status(models.IntegerChoices):
    #     ACTIVE = 1, "Aktif"
    #     NONACTIVE = 2, "Non Aktif"

    perilaku_kerja = models.ForeignKey(
        PerilakuKerja, on_delete=models.CASCADE, verbose_name="Perilaku Kerja"
    )
    keterangan = models.CharField("Keterangan Perilaku", max_length=255)
    # status = models.IntegerField(choices=Status.choices, null=True, default=1)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.keterangan:
            return self.keterangan
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Daftar Perilaku Kerja"
        verbose_name_plural = "Daftar Perilaku Kerja"


class DaftarEkspetasi(models.Model):
    perilaku_kerja = models.ForeignKey(
        PerilakuKerja, on_delete=models.CASCADE, verbose_name="Perilaku Kerja"
    )
    ekspetasi = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(
            self.perilaku_kerja.perilaku_kerja, self.ekspetasi[:20] + "..."
        )

    class Meta:
        verbose_name = "Daftar Ekspetasi"
        verbose_name_plural = "Daftar Ekspetasi"


class DaftarPerilakuKerjaPegawai(models.Model):
    # class Status(models.IntegerChoices):
    #     ACTIVE = 1, "Aktif"
    #     NONACTIVE = 2, "Non Aktif"

    perilaku_kerja = models.ForeignKey(
        PerilakuKerja, on_delete=models.CASCADE, verbose_name="Perilaku Kerja"
    )
    skp = models.ForeignKey(
        SasaranKinerja,
        on_delete=models.CASCADE,
        verbose_name="Sasaran Kinerja Pegawai",
        null=True,
    )
    isi = models.TextField("Isi Ekspetasi", null=True, blank=True)
    ekspetasi_tambahan = models.ManyToManyField(DaftarEkspetasi, blank=True)
    # status = models.IntegerField(choices=Status.choices, null=True, default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.isi:
            return self.isi
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Daftar Perilaku Kerja Pegawai"
        verbose_name_plural = "Daftar Perilaku Kerja Pegawai"


class Lampiran(models.Model):
    class Status(models.IntegerChoices):
        ACTIVE = 1, "Aktif"
        NONACTIVE = 2, "Non Aktif"

    lampiran = models.CharField("Lampiran", max_length=200)
    status = models.IntegerField(choices=Status.choices, null=True, default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Lampiran"
        verbose_name_plural = "Lampiran"


class UmpanBalik(models.Model):
    class Status(models.IntegerChoices):
        ACTIVE = 1, "Aktif"
        NONACTIVE = 2, "Non Aktif"

    nama = models.TextField("Nama Umpan Balik", null=True)
    status = models.IntegerField(choices=Status.choices, null=True, default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Umpan Balik"
        verbose_name_plural = "Umpan Balik"


class DaftarLampiran(models.Model):
    lampiran = models.ForeignKey(Lampiran, on_delete=models.CASCADE)
    skp = models.ForeignKey(
        SasaranKinerja,
        on_delete=models.CASCADE,
        verbose_name="Sasaran Kinerja Pegawai",
        null=True,
    )
    isi = models.TextField("Isi Lampiran", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Daftar Lampiran"
        verbose_name_plural = "Daftar Lampiran"


@receiver(post_save, sender=SasaranKinerja)
def handler_sasarankinerja_save(instance, created, **kwargs):
    if created:
        if "bupati" in instance.pegawai.jabatan.lower():
            detail = DetailSasaranKinerja(
                skp=instance,
                nama_pegawai=instance.pegawai.get_complete_name(),
                nip_pegawai=instance.pegawai.username,
                jabatan_pegawai=instance.pegawai.jabatan,
                golongan_pegawai=instance.pegawai.golongan.__str__(),
                unor_pegawai=instance.pegawai.unitkerja.unitkerja,
                status_pegawai=instance.pegawai.get_status_pegawai_display(),
            )
        else:
            golongan = instance.pejabat_penilai.golongan.__str__()
            nip = instance.pejabat_penilai.username
            if instance.pejabat_penilai.groups.filter(name="Bupati").exists():
                golongan = ""
                nip = ""
            detail = DetailSasaranKinerja(
                skp=instance,
                nama_pegawai=instance.pegawai.get_complete_name(),
                nip_pegawai=instance.pegawai.username,
                jabatan_pegawai=instance.pegawai.jabatan,
                golongan_pegawai=instance.pegawai.golongan.__str__(),
                unor_pegawai=instance.pegawai.unitkerja.unitkerja,
                nama_pejabat=instance.pejabat_penilai.get_complete_name(),
                nip_pejabat=nip,
                jabatan_pejabat=instance.pejabat_penilai.jabatan,
                golongan_pejabat=golongan,
                unor_pejabat=instance.pejabat_penilai.unitkerja.unitkerja,
                status_pejabat=instance.pejabat_penilai.get_status_pegawai_display(),
            )
        detail.save()
        if instance.jenis_jabatan != SasaranKinerja.JenisJabatan.JPT:
            for i in range(
                instance.periode_awal.month, instance.periode_akhir.month + 1
            ):
                PenilaianBawahan.objects.create(skp=instance, periode=i)

        # if "bupati" in instance.pegawai.jabatan.lower():
        #     pass
        # else:
        #     skp_atasan = instance.pejabat_penilai.sasarankinerja_set.last() # ?
        #     if skp_atasan:
        #         instance.induk = skp_atasan
        #         instance.save()


class RencanaAksi(models.Model):
    skp = models.ForeignKey(
        SasaranKinerja,
        on_delete=models.CASCADE,
        verbose_name="Sasaran Kinerja Pegawai",
        null=True,
    )
    rhk = models.ForeignKey(
        RencanaHasilKerja,
        on_delete=models.CASCADE,
        verbose_name="Rencana Hasil Kerja Pegawai",
        null=True,
    )
    periode = models.IntegerField(
        choices=[(k, v) for k, v in FULL_BULAN.items()], null=True
    )
    rencana_aksi = models.TextField("Rencana Aksi", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Rencana Aksi"
        verbose_name_plural = "Rencana Aksi"


class BuktiDukung(models.Model):
    indikator = models.OneToOneField(
        IndikatorKinerjaIndividu,
        on_delete=models.CASCADE,
        verbose_name="Indikator Kerja Individu",
        null=True,
    )
    periode = models.IntegerField(
        choices=[(k, v) for k, v in FULL_BULAN.items()], null=True
    )
    nama_bukti_dukung = models.TextField("Nama Bukti Dukung", null=True, blank=True)
    link = models.URLField("Link", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Bukti Dukung"
        verbose_name_plural = "Bukti Dukung"


class Realisasi(models.Model):
    indikator = models.OneToOneField(
        IndikatorKinerjaIndividu,
        on_delete=models.CASCADE,
        verbose_name="Indikator Kerja Individu",
        null=True,
    )
    periode = models.IntegerField(
        choices=[(k, v) for k, v in FULL_BULAN.items()], null=True
    )
    realisasi = models.CharField("Realisasi", max_length=255, null=True, blank=True)
    sumber = models.CharField("Sumber Data", max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Realisasi"
        verbose_name_plural = "Realisasi"


class UmpanBalikPegawai(models.Model):
    indikator = models.OneToOneField(
        IndikatorKinerjaIndividu,
        on_delete=models.CASCADE,
        verbose_name="Indikator Kerja Individu",
        null=True,
    )
    periode = models.IntegerField(
        choices=[(k, v) for k, v in FULL_BULAN.items()], null=True
    )
    umpan_balik = models.ManyToManyField(UmpanBalik, blank=True)
    umpan_balik_tambahan = models.CharField(
        "Umpan Balik Tambahan", max_length=255, null=True, blank=True
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Umpan Balik Tambahan"
        verbose_name_plural = "Umpan Balik Tambahan"


class Hasil(models.Model):
    nama = models.CharField("Nama Hasil", null=True, max_length=255)
    is_active = models.BooleanField(default=True)
    keterangan = models.CharField("Keterangan", max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Hasil"
        verbose_name_plural = "Hasil"


class PenilaianBawahan(models.Model):
    class PredikatKerja(models.IntegerChoices):
        SANGAT_KURANG = 1, "Sangat Kurang"
        BUTUH_PERBAIKAN = 2, "Butuh Perbaikan"
        KURANG = 3, "Kurang"
        BAIK = 4, "Baik"
        SANGAT_BAIK = 5, "Sangat Baik"

    skp = models.ForeignKey(
        SasaranKinerja,
        on_delete=models.CASCADE,
        verbose_name="Sasaran Kinerja Pegawai",
    )
    periode = models.IntegerField(
        choices=[(k, v) for k, v in FULL_BULAN.items()], null=True
    )
    is_dinilai = models.BooleanField(default=False)
    rating_hasil = models.ForeignKey(
        Hasil,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Rating Hasil Kinerja",
        related_name="hasil_rating_kinerja",
    )
    predikat_perilaku = models.ForeignKey(
        Hasil,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Predikat Perilaku Kinerja",
        related_name="hasil_predikat_perilaku_kerja",
    )
    predikat_kerja = models.IntegerField(
        choices=PredikatKerja.choices, verbose_name="Predikat Kerja", null=True
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Penilaian Bawahan"
        verbose_name_plural = "Penilaian Bawahan"
