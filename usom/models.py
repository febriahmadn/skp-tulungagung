from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UnitKerja(models.Model):
    unitkerja = models.CharField(
        max_length=200, null=True, verbose_name="Nama Unit Kerja"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.unitkerja)

    class Meta:
        verbose_name = "Unit Kerja"
        verbose_name_plural = "Unit Kerja"


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
        Creates and saves a superuser with the given identity number, nama_lengkap and password.
        """
        user = self.create_user(username, password=password, nama_lengkap=nama_lengkap)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Account(AbstractUser):
    JENIS_PEGAWAI_CHOICES = [("PI", "Pimpinan"), ("PA", "Atasan"), ("PE", "Pegawai")]
    GOLONGAN = [
        ("I/A", "I/A"),
        ("I/B", "I/B"),
        ("I/C", "I/C"),
        ("I/D", "I/D"),
        ("II/A", "II/A"),
        ("II/B", "II/B"),
        ("II/C", "II/C"),
        ("II/D", "II/D"),
        ("III/A", "III/A"),
        ("III/B", "III/B"),
        ("III/C", "III/C"),
        ("III/D", "III/D"),
        ("IV/A", "IV/A"),
        ("IV/B", "IV/B"),
        ("IV/C", "IV/C"),
        ("IV/D", "IV/D"),
        ("IV/E", "IV/E"),
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

    # JPT (Jabatan Pimpinan Tinggi) (beda pengisian), JF (Jabatan Fungsional), JA (Jabatan Administrator)
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
    golongan = models.CharField(
        choices=GOLONGAN, max_length=6, verbose_name="Golongan", null=True, blank=True
    )
    eselon = models.CharField(
        choices=ESELON, max_length=6, verbose_name="Eselon", null=True, blank=True
    )
    jenis_pegawai = models.CharField(
        choices=JENIS_PEGAWAI_CHOICES,
        default="PE",
        max_length=2,
        verbose_name="Jenis Pegawai",
        null=True,
        blank=True,
    )

    objects = AccountManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["nama_lengkap"]
    group_names = []

    class Meta:
        ordering = ["id"]
        verbose_name = "Akun"
        verbose_name_plural = "Akun"