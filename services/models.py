from django.db import models
from django.utils import timezone
from solo.models import SingletonModel


class Configurations(SingletonModel):
    ekinerja_url = models.URLField("Ekinerja URL", null=True, blank=True)
    ekinerja_token = models.CharField(
        "Ekinerja Token API", null=True, blank=True, max_length=255
    )
    presensi_url = models.URLField("Presensi URL", null=True, blank=True)
    sipo_url = models.URLField("SIPO URL", null=True, blank=True)
    sipo_token = models.TextField("SIPO Token API", null=True, blank=True)
    sipo_username = models.CharField(
        "SIPO Username API",
        null=True,
        blank=True,
        max_length=255,
    )
    sipo_password = models.CharField(
        "SIPO Password API",
        null=True,
        blank=True,
        max_length=255,
    )
    batas_input = models.DateField(
        default=timezone.now,
        null=True,
        verbose_name="Batas Pengisian",
        help_text="Batas Pengisian SKP",
    )

    def __str__(self):
        return "Configurations"

    class Meta:
        verbose_name = "Configurations"
        verbose_name_plural = "Configurations"


class TaskList(models.Model):
    class JenisTask(models.IntegerChoices):
        SINKORN_PRESENSI = 1, "Sinkron Pegawai Presensi"
        SINKORN_SIPO_NIP = 2, "Sinkron Pegawai SIPO by NIP"

    jenis_task = models.IntegerField(
        "Jenis Task", choices=JenisTask.choices, null=True, blank=True
    )
    parameter = models.CharField("Parameter", max_length=255, null=True, blank=True)
    presentase = models.FloatField("Presentase", null=True, blank=True)
    is_done = models.BooleanField("Selesai", default=False)

    def proses(self):
        from services.functions.sinkron_presensi import ServicePresensi
        from services.functions.sinkron_sipo import ServiceSipo

        if self.jenis_task:
            if self.jenis_task == self.JenisTask.SINKORN_PRESENSI:
                ServicePresensi(self.id).get_pegawai_list()
            elif self.jenis_task:
                if self.parameter:
                    ServiceSipo().sinkron_pegawai_by_nip(self.parameter)
        return True

    def __str__(self):
        return "{} {}".format(str(self.id), self.get_jenis_task_display())

    class Meta:
        verbose_name = "Task List"
        verbose_name_plural = "Task List"
