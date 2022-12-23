# Generated by Django 4.1.2 on 2022-12-20 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("skp", "0024_initial_master_skp"),
    ]

    operations = [
        migrations.CreateModel(
            name="UmpanBalik",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nama", models.TextField(null=True, verbose_name="Nama Umpan Balik")),
                (
                    "status",
                    models.IntegerField(
                        choices=[(1, "Aktif"), (2, "Non Aktif")], default=1, null=True
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Umpan Balik",
                "verbose_name_plural": "Umpan Balik",
            },
        ),
    ]
