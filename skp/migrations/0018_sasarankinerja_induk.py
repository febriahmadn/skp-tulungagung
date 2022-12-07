# Generated by Django 4.1.2 on 2022-12-06 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("skp", "0017_daftarperilakukerjapegawai"),
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
    ]
