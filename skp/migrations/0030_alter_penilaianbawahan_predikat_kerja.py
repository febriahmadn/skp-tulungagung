# Generated by Django 4.1.2 on 2022-12-26 06:32

from django.db import migrations, models

from skp.models import PenilaianBawahan


def forwards_func(apps, schema_editor):
    print('forwards')
    penlaiana_qs = PenilaianBawahan.objects.all()
    for i in penlaiana_qs:
        if i.predikat_kerja and i.predikat_kerja != "":
            text = i.predikat_kerja.lower()
            if text == "sangat kurang":
                i.predikat_kerja = PenilaianBawahan.PredikatKerja.SANGAT_KURANG.as_integer_ratio()[0]
            elif text == "butuh perbaikan":
                i.predikat_kerja = PenilaianBawahan.PredikatKerja.BUTUH_PERBAIKAN.as_integer_ratio()[0]
            elif text == "kurang":
                i.predikat_kerja = PenilaianBawahan.PredikatKerja.KURANG.as_integer_ratio()[0]
            elif text == "baik":
                i.predikat_kerja = PenilaianBawahan.PredikatKerja.BAIK.as_integer_ratio()[0]
            elif text == "sangat baik":
                i.predikat_kerja = PenilaianBawahan.PredikatKerja.SANGAT_BAIK.as_integer_ratio()[0]
            else:
                i.predikat_kerja = None
        i.save()

def reverse_func(apps, schema_editor):
    print('reverse')

class Migration(migrations.Migration):

    dependencies = [
        ("skp", "0029_umpanbalikpegawai"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func, elidable=False),
        migrations.AlterField(
            model_name="penilaianbawahan",
            name="predikat_kerja",
            field=models.IntegerField(
                choices=[
                    (1, "Sangat Kurang"),
                    (2, "Butuh Perbaikan"),
                    (3, "Kurang"),
                    (4, "Baik"),
                    (5, "Sangat Baik"),
                ],
                null=True,
                verbose_name="Predikat Kerja",
            ),
        ),
    ]
