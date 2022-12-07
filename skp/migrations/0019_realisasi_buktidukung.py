# Generated by Django 4.1.2 on 2022-12-06 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("skp", "0018_rencanaaksi"),
    ]

    operations = [
        migrations.AddField(
            model_name="sasarankinerja",
            name="induk",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="skp.sasarankinerja",
            ),
        ),
        migrations.CreateModel(
            name="Realisasi",
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
                    "periode",
                    models.IntegerField(
                        choices=[
                            (1, "Januari"),
                            (2, "Februari"),
                            (3, "Maret"),
                            (4, "April"),
                            (5, "Mei"),
                            (6, "Juni"),
                            (7, "Juli"),
                            (8, "Agustus"),
                            (9, "September"),
                            (10, "Oktober"),
                            (11, "November"),
                            (12, "Desember"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "realisasi",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Realisasi"
                    ),
                ),
                (
                    "sumber",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Sumber Data",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "rhk",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="skp.rencanahasilkerja",
                        verbose_name="Rencana Hasil Kerja Pegawai",
                    ),
                ),
                (
                    "skp",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="skp.sasarankinerja",
                        verbose_name="Sasaran Kinerja Pegawai",
                    ),
                ),
            ],
            options={
                "verbose_name": "Realisasi",
                "verbose_name_plural": "Realisasi",
            },
        ),
        migrations.CreateModel(
            name="BuktiDukung",
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
                    "periode",
                    models.IntegerField(
                        choices=[
                            (1, "Januari"),
                            (2, "Februari"),
                            (3, "Maret"),
                            (4, "April"),
                            (5, "Mei"),
                            (6, "Juni"),
                            (7, "Juli"),
                            (8, "Agustus"),
                            (9, "September"),
                            (10, "Oktober"),
                            (11, "November"),
                            (12, "Desember"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "nama_bukti_dukung",
                    models.TextField(
                        blank=True, null=True, verbose_name="Nama Bukti Dukung"
                    ),
                ),
                ("link", models.URLField(blank=True, null=True, verbose_name="Link")),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "rhk",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="skp.rencanahasilkerja",
                        verbose_name="Rencana Hasil Kerja Pegawai",
                    ),
                ),
                (
                    "skp",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="skp.sasarankinerja",
                        verbose_name="Sasaran Kinerja Pegawai",
                    ),
                ),
            ],
            options={
                "verbose_name": "Bukti Dukung",
                "verbose_name_plural": "Bukti Dukung",
            },
        ),
    ]
