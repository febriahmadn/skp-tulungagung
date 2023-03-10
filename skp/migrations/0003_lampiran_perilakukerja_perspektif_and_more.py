# Generated by Django 4.1.2 on 2022-11-02 05:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "skp",
            "0002_alter_sasarankinerja_options_sasarankinerja_created_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Lampiran",
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
                    "status",
                    models.IntegerField(
                        choices=[(1, "Aktif"), (2, "Non Aktif")],
                        default=1,
                        null=True,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Lampiran",
                "verbose_name_plural": "Lampiran",
            },
        ),
        migrations.CreateModel(
            name="PerilakuKerja",
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
                    "perilaku_kerja",
                    models.CharField(max_length=200, verbose_name="Perilaku Kerja"),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(1, "Aktif"), (2, "Non Aktif")],
                        default=1,
                        null=True,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Perilaku Kerja",
                "verbose_name_plural": "Perilaku Kerja",
            },
        ),
        migrations.CreateModel(
            name="Perspektif",
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
                    "perspektif",
                    models.CharField(max_length=255, verbose_name="Perspektif"),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Perspektif",
                "verbose_name_plural": "Perspektif",
            },
        ),
        migrations.AlterField(
            model_name="sasarankinerja",
            name="status",
            field=models.IntegerField(
                choices=[
                    (1, "Draft"),
                    (2, "Pengajuan"),
                    (3, "Persetujuan"),
                    (4, "Close"),
                ],
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="IndikatorKinerjaIndividu",
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
                    "indikator",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Indikator"
                    ),
                ),
                (
                    "target",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Target",
                    ),
                ),
                (
                    "perspektif",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="skp.perspektif",
                    ),
                ),
                (
                    "rencana_kerja",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="skp.rencanahasilkerja",
                        verbose_name="Rencana Hasil Kerja",
                    ),
                ),
            ],
            options={
                "verbose_name": "Indikator Kinerja Individu",
                "verbose_name_plural": "Indikator Kinerja Individu",
            },
        ),
        migrations.CreateModel(
            name="DaftarPerilakuKerja",
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
                    "keterangan",
                    models.CharField(
                        max_length=255, verbose_name="Keterangan Perilaku"
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(1, "Aktif"), (2, "Non Aktif")],
                        default=1,
                        null=True,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "perilaku_kerja",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="skp.perilakukerja",
                        verbose_name="Perilaku Kerja",
                    ),
                ),
            ],
            options={
                "verbose_name": "Daftar Perilaku Kerja",
                "verbose_name_plural": "Daftar Perilaku Kerja",
            },
        ),
        migrations.CreateModel(
            name="DaftarLampiran",
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
                    "isi",
                    models.TextField(
                        blank=True, null=True, verbose_name="Isi Lampiran"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "lampiran",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="skp.lampiran",
                    ),
                ),
            ],
            options={
                "verbose_name": "Daftar Lampiran",
                "verbose_name_plural": "Daftar Lampiran",
            },
        ),
    ]
