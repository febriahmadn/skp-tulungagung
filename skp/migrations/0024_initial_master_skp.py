
from django.core.management import call_command
from django.db import migrations

from skp.models import Lampiran, PerilakuKerja, Perspektif


def forwards_func(apps, schema_editor):
    print('forwards')
    if not Perspektif.objects.exists():
        call_command('generate_master_perspektif', verbosity=0)
    else:
        print("Perspektif Exists")

    if not PerilakuKerja.objects.exists():
        call_command('generate_master_perilaku_kerja', verbosity=0)
    else:
        print("Perilaku Kerja Exists")
    
    if not Lampiran.objects.exists():
        call_command('generate_master_lampiran', verbosity=0)
    else:
        print("Lampiran Exists")

def reverse_func(apps, schema_editor):
    print('reverse')


class Migration(migrations.Migration):
    dependencies = [
        ('skp', '0023_initial_hasil'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func, elidable=False)
    ]