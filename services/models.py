from django.db import models
from django.utils import timezone
from solo.models import SingletonModel


class Configurations(SingletonModel):
    ekinerja_url = models.URLField("Ekinerja URL", null=True, blank=True)
    ekinerja_token = models.CharField(
        "Ekinerja Token API", null=True, blank=True, max_length=255
    )
    sipo_url = models.URLField("SIPO URL", null=True, blank=True)
    sipo_token = models.CharField(
        "SIPO Token API", null=True, blank=True, max_length=255
    )
    batas_input = models.DateField(
        default=timezone.now,
        null=True,
        verbose_name="Batas Pengisian",
        help_text="Batas Pengisian SKP"
    )

    def __str__(self):
        return "Configurations"

    class Meta:
        verbose_name = "Configurations"
        verbose_name_plural = "Configurations"
