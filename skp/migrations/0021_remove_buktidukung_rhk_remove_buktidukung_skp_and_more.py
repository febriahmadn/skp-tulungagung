# Generated by Django 4.1.2 on 2022-12-09 03:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("skp", "0020_realisasi_buktidukung"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="buktidukung",
            name="rhk",
        ),
        migrations.RemoveField(
            model_name="buktidukung",
            name="skp",
        ),
        migrations.RemoveField(
            model_name="realisasi",
            name="rhk",
        ),
        migrations.RemoveField(
            model_name="realisasi",
            name="skp",
        ),
        migrations.AddField(
            model_name="buktidukung",
            name="indikator",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="skp.indikatorkinerjaindividu",
                verbose_name="Indikator Kerja Individu",
            ),
        ),
        migrations.AddField(
            model_name="realisasi",
            name="indikator",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="skp.indikatorkinerjaindividu",
                verbose_name="Indikator Kerja Individu",
            ),
        ),
    ]
