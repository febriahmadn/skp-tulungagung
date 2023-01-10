# Generated by Django 4.1.2 on 2022-12-26 06:32

from django.db import migrations
from skp.models import DetailSasaranKinerja


def forwards_func(apps, schema_editor):
    print('forwards')
    for i in DetailSasaranKinerja.objects.all():
        i.golongan_pegawai = "{}/{}".format(i.golongan_pegawai.split('/')[0],i.golongan_pegawai.split('/')[1].lower())
        if i.golongan_pejabat:
            i.golongan_pejabat = "{}/{}".format(i.golongan_pejabat.split('/')[0],i.golongan_pejabat.split('/')[1].lower())
        i.save()


def reverse_func(apps, schema_editor):
    print('reverse')

class Migration(migrations.Migration):

    dependencies = [
        ("skp", "0031_riwayatketeranganskp"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func, elidable=False),
    ]
