from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group

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
    nama_lengkap = models.CharField("Nama Lengkap", max_length=150)
    gelar_depan = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Gelar Depan"
    )
    gelar_belakang = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Gelar Belakang"
    )
    objects = AccountManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["nama_lengkap"]
    group_names = []

    class Meta:
        ordering = ["id"]
        verbose_name = "Akun"
        verbose_name_plural = "Akun"

