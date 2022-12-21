import csv
import os
from pathlib import Path

from django.core.management.base import BaseCommand

from skp.models import DaftarEkspetasi, PerilakuKerja


class Command(BaseCommand):
    help = "Generate Data Master Daftar Ekspetasi"

    def handle(self, *args, **options):
        # file
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

        path_file = open(os.path.join(BASE_DIR, "static/master/master_ekspektasi.csv"))
        read = csv.reader(path_file)
        # print(read)
        self.stdout.write(self.style.NOTICE("PROSES DATA MASTER Daftar Ekspetasi"))
        for i in read:
            perilaku = i[0]
            isi = i[1]
            find_perilaku = PerilakuKerja.objects.filter(
                perilaku_kerja__icontains=perilaku
            )
            if find_perilaku.exists():
                perilaku_obj = find_perilaku.last()
                obj, created = DaftarEkspetasi.objects.get_or_create(
                    ekspetasi=isi.strip(), perilaku_kerja=perilaku_obj
                )
                obj.save()
        self.stdout.write(self.style.SUCCESS("SELESAI"))
