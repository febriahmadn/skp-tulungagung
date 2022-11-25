# Generated by Django 4.1.2 on 2022-11-22 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Configurations",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ekinerja_url",
                    models.URLField(blank=True, null=True, verbose_name="Ekinerja URL"),
                ),
                (
                    "ekinerja_token",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Ekinerja Token API",
                    ),
                ),
                (
                    "sipo_url",
                    models.URLField(blank=True, null=True, verbose_name="SIPO URL"),
                ),
                (
                    "sipo_token",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="SIPO Token API",
                    ),
                ),
            ],
            options={
                "verbose_name": "Configurations",
                "verbose_name_plural": "Configurations",
            },
        ),
    ]
