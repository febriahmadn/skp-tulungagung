# Generated by Django 4.1.2 on 2022-11-17 06:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usom", "0003_account_jenis_jabatan"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="atasan",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="pegawai_atasan",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
