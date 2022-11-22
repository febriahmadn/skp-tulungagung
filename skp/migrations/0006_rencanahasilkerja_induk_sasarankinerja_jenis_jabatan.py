# Generated by Django 4.1.2 on 2022-11-18 03:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("skp", "0005_alter_sasarankinerja_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="rencanahasilkerja",
            name="induk",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="skp.rencanahasilkerja",
            ),
        ),
        migrations.AddField(
            model_name="sasarankinerja",
            name="jenis_jabatan",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (1, "Jabatan Pimpinan Tinggi"),
                    (2, "Jabatan Fungsional"),
                    (3, "Jabatan Administrator"),
                ],
                null=True,
                verbose_name="Jenis Jabatan",
            ),
        ),
    ]