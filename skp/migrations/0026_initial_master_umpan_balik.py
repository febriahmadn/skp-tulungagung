
from django.core.management import call_command
from django.db import migrations

from skp.models import UmpanBalik


def forwards_func(apps, schema_editor):
    print('forwards')
    if not UmpanBalik.objects.exists():
        call_command('generate_master_umpan_balik', verbosity=0)
    else:
        print("Umpan Balik Exists")

def reverse_func(apps, schema_editor):
    print('reverse')


class Migration(migrations.Migration):
    dependencies = [
        ('skp', '0025_umpanbalik'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func, elidable=False)
    ]