# Generated by Django 4.1.2 on 2022-11-22 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("skp", "0009_rencanahasilkerja_aspek"),
    ]

    operations = [
        migrations.AddField(
            model_name="indikatorkinerjaindividu",
            name="ekinerja_id",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Ekinerja ID"
            ),
        ),
    ]
