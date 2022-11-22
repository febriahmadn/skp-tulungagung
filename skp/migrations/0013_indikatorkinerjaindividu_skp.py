# Generated by Django 4.1.2 on 2022-11-22 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("skp", "0012_alter_indikatorkinerjaindividu_rencana_kerja"),
    ]

    operations = [
        migrations.AddField(
            model_name="indikatorkinerjaindividu",
            name="skp",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="skp.sasarankinerja",
                verbose_name="Sasaran Kinerja Pegawai",
            ),
        ),
    ]
