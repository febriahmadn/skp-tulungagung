
from django.core.management import call_command
from django.db import migrations

from skp.models import Hasil


def forwards_func(apps, schema_editor):
    print('forwards')
    if not Hasil.objects.exists():
        call_command('generate_master_hasil', verbosity=0)
    else:
        print('Hasil Exists')


def reverse_func(apps, schema_editor):
    print('reverse')


class Migration(migrations.Migration):
    dependencies = [
        ('skp', '0022_hasil_penilaianbawahan'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func, elidable=False)
    ]