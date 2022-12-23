
from django.core.management import call_command
from django.db import migrations

from skp.models import DaftarEkspetasi


def forwards_func(apps, schema_editor):
    print('forwards')
    if not DaftarEkspetasi.objects.exists():
        call_command('generate_master_daftar_ekspetasi', verbosity=0)
    else:
        print("Daftar Ekspetasi Exists")

def reverse_func(apps, schema_editor):
    print('reverse')


class Migration(migrations.Migration):
    dependencies = [
        ('skp', '0027_daftarekspetasi_and_more'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func, elidable=False)
    ]