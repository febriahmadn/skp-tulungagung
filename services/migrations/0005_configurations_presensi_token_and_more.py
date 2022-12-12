# Generated by Django 4.1.2 on 2022-12-12 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0004_alter_configurations_sipo_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="configurations",
            name="presensi_token",
            field=models.TextField(
                blank=True, null=True, verbose_name="Presensi Token"
            ),
        ),
        migrations.AddField(
            model_name="configurations",
            name="presensi_url",
            field=models.URLField(blank=True, null=True, verbose_name="Presensi URL"),
        ),
    ]
