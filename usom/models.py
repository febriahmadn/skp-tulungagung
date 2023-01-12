from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from usom.utils import PathForFileModel


class UnitKerja(models.Model):
    id_sipo = models.CharField("ID SIPO", null=True, blank=True, max_length=50)
    unitkerja = models.CharField(
        max_length=200, null=True, verbose_name="Nama Unit Kerja"
    )
    aktif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.unitkerja)

    class Meta:
        verbose_name = "Unit Kerja"
        verbose_name_plural = "Unit Kerja"


class Golongan(models.Model):
    kode = models.CharField("Kode", max_length=100, null=True)
    kode_angka = models.CharField("Kode Angka", max_length=100, null=True)
    angka = models.PositiveSmallIntegerField(
        "Angka", choices=[(x, x) for x in range(1, 5)], db_index=True
    )
    huruf = models.CharField(
        "Huruf",
        choices=[("a", "a"), ("b", "b"), ("c", "c"), ("d", "d"), ("e", "e")],
        max_length=2,
        db_index=True,
    )
    keterangan = models.CharField("Keterangan", blank=True, null=True, max_length=255)

    def save(self, *args, **kwargs):
        if self.get_golongan():
            self.kode = self.get_golongan()
        return super().save(*args, **kwargs)

    def get_golongan(self):
        return self.get_romawi() + "/" + self.huruf

    def get_romawi(self):
        from usom.utils import int_to_roman

        return int_to_roman(self.angka)

    def as_option(self):
        option = '<option value="{}">{}/{}</option>'.format(
            str(self.id), str(self.get_romawi()), str(self.huruf)
        )
        return option

    def __str__(self):
        return self.get_golongan()

    class Meta:
        ordering = ["angka", "huruf"]
        verbose_name = "Golongan"
        verbose_name_plural = "Golongan"


class AccountManager(BaseUserManager):
    def create_user(self, username, nama_lengkap, password=None):
        """
        Creates and saves a User with the given username, nama_lengkap and password.
        """
        if not username:
            raise ValueError("Users must have an username")
        user = self.model(
            username=username,
            nama_lengkap=nama_lengkap,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, nama_lengkap, password):
        """
        Creates and saves a superuser with the given identity number,
        nama_lengkap and password.
        """
        user = self.create_user(username, password=password, nama_lengkap=nama_lengkap)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Account(AbstractUser):
    JENIS_PEGAWAI_CHOICES = [
        ("PI", "Pimpinan"),
        ("PA", "Atasan"),
        ("PE", "Pegawai"),
    ]
    STATUS_PEGAWAI = [
        ('ASN', 'ASN'),
        ('NON', 'NON ASN'),
    ]
    ESELON = [
        # (1, 'I-A'),
        # (2, 'I-B'),
        ("II-A", "II-A"),
        ("II-B", "II-B"),
        ("III-A", "III-A"),
        ("III-B", "III-B"),
        ("IV-A", "IV-A"),
        ("IV-B", "IV-B"),
        ("V-C", "V-C"),
    ]

    JENIS_JABATAN_CHOICES = [
        ("JPT", "Jabatan Pimpinan Tinggi"),
        ("JF", "Jabatan Fungsional"),
        ("JA", "Jabatan Administrator"),
    ]

    # JPT (Jabatan Pimpinan Tinggi) (beda pengisian),
    # JF (Jabatan Fungsional),
    # JA (Jabatan Administrator)
    atasan = models.ForeignKey(
        "self",
        related_name="pegawai_atasan",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    nama_lengkap = models.CharField("Nama Lengkap", max_length=150)
    gelar_depan = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Gelar Depan"
    )
    gelar_belakang = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Gelar Belakang"
    )
    jabatan = models.CharField(
        max_length=250, null=True, blank=True, verbose_name="Jabatan"
    )
    jenis_jabatan = models.CharField(
        choices=JENIS_JABATAN_CHOICES,
        null=True,
        blank=True,
        max_length=5,
        verbose_name="Jenis Jabatan",
    )
    unitkerja = models.ForeignKey(
        UnitKerja, null=True, blank=True, on_delete=models.SET_NULL
    )
    golongan = models.ForeignKey(
        Golongan, null=True, blank=True, on_delete=models.SET_NULL
    )
    eselon = models.CharField(
        choices=ESELON,
        max_length=6,
        verbose_name="Eselon",
        null=True,
        blank=True,
    )
    jenis_pegawai = models.CharField(
        choices=JENIS_PEGAWAI_CHOICES,
        default="PE",
        max_length=2,
        verbose_name="Jenis Pegawai",
        null=True,
        blank=True,
    )
    status_pegawai = models.CharField(
        max_length=50,
        verbose_name='Status Pegawai',
        choices=STATUS_PEGAWAI,
        null=True,
        blank=True
    )
    tangggal_nonaktif = models.DateField(
        null=True, blank=True, verbose_name="Tanggal Nonaktif"
    )
    id_sipo = models.CharField("ID SIPO", null=True, blank=True, max_length=50)
    foto = models.ImageField(
        upload_to=PathForFileModel("foto/"), max_length=255, null=True, blank=True
    )

    objects = AccountManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["nama_lengkap"]
    group_names = []

    def get_complete_name(self):
        nama = self.nama_lengkap
        if self.gelar_depan:
            if self.gelar_depan == "-":
                gelar_depan = ""
            else:
                gelar_depan = self.gelar_depan
            nama = gelar_depan + " " + nama
        if self.gelar_belakang:
            if self.gelar_belakang == "-":
                gelar_belakang = ""
            else:
                gelar_belakang = self.gelar_belakang
            nama = nama + ", " + gelar_belakang
        # print(nama)
        return nama

    def __str__(self):
        return "{} - {}".format(self.username, self.get_complete_name())

    class Meta:
        ordering = ["id"]
        verbose_name = "Akun"
        verbose_name_plural = "Akun"
