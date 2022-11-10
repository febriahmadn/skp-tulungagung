from django.db import models
from usom.models import Account, UnitKerja


class SasaranKinerja(models.Model):
    class Pendekatan(models.IntegerChoices):
        KUANTITATIF = 1, "Kuantitatif"
        KUALITATIF = 2, "Kualitatif"

    class Status(models.IntegerChoices):
        DRAFT = 1, "Draft"
        PENGAJUAN = 2, "Pengajuan"
        PERSETUJUAN = 3, "Persetujuan"
        CLOSE = 4, "Close"

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
    periode_awal = models.DateField(null=True, verbose_name="Periode Awal")
    periode_akhir = models.DateField(null=True, verbose_name="Periode Akhir")
    pendekatan = models.IntegerField(choices=Pendekatan.choices, null=True)
    status = models.IntegerField(choices=Status.choices, null=True)
    keterangan = models.CharField("Keterangan", max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Sasaran Kinerja Pegawai"
        verbose_name_plural = "Sasaran Kinerja Pegawai"


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

    skp = models.ForeignKey(
        SasaranKinerja, on_delete=models.CASCADE, verbose_name="Sasaran Kinerja Pegawai"
    )
    rencana_kerja = models.CharField("Rencana Hasil Kerja", max_length=255, null=True)
    penugasan_dari = models.CharField(
        "Penugasan Dari", max_length=255, null=True, blank=True
    )
    jenis = models.IntegerField(
        choices=Jenis.choices, verbose_name="Jenis Rencana Hasik Kerja"
    )
    klasifikasi = models.IntegerField(
        choices=Klasifikasi.choices, verbose_name="Klasifikasi Rencana Hasil Kerja"
    )
    unor = models.ForeignKey(
        UnitKerja, null=True, blank=True, on_delete=models.SET_NULL
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Rencana Hasil Kerja"
        verbose_name_plural = "Rencana Hasil Kerja"


class Perspektif(models.Model):
    perspektif = models.CharField("Perspektif", max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Perspektif"
        verbose_name_plural = "Perspektif"


class IndikatorKinerjaIndividu(models.Model):
    rencana_kerja = models.ForeignKey(
        RencanaHasilKerja, on_delete=models.CASCADE, verbose_name="Rencana Hasil Kerja"
    )
    indikator = models.CharField("Indikator", max_length=255, null=True)
    target = models.CharField("Target", max_length=100, null=True, blank=True)
    perspektif = models.ForeignKey(
        Perspektif, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Indikator Kinerja Individu"
        verbose_name_plural = "Indikator Kinerja Individu"


class PerilakuKerja(models.Model):
    class Status(models.IntegerChoices):
        ACTIVE = 1, "Aktif"
        NONACTIVE = 2, "Non Aktif"

    perilaku_kerja = models.CharField("Perilaku Kerja", max_length=200)
    status = models.IntegerField(choices=Status.choices, null=True, default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Perilaku Kerja"
        verbose_name_plural = "Perilaku Kerja"


class DaftarPerilakuKerja(models.Model):
    class Status(models.IntegerChoices):
        ACTIVE = 1, "Aktif"
        NONACTIVE = 2, "Non Aktif"

    perilaku_kerja = models.ForeignKey(
        PerilakuKerja, on_delete=models.CASCADE, verbose_name="Perilaku Kerja"
    )
    keterangan = models.CharField("Keterangan Perilaku", max_length=255)
    status = models.IntegerField(choices=Status.choices, null=True, default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Daftar Perilaku Kerja"
        verbose_name_plural = "Daftar Perilaku Kerja"


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


class DaftarLampiran(models.Model):
    lampiran = models.ForeignKey(Lampiran, on_delete=models.CASCADE)
    isi = models.TextField("Isi Lampiran", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id))

    class Meta:
        verbose_name = "Daftar Lampiran"
        verbose_name_plural = "Daftar Lampiran"