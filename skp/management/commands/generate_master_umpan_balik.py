import csv
import os
from pathlib import Path

from django.core.management.base import BaseCommand

from skp.models import UmpanBalik


class Command(BaseCommand):
    help = "Generate Data Master Umpan Balik"

    def handle(self, *args, **options):
        # file
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

        path_file = open(os.path.join(BASE_DIR, "static/master/master_umpan_balik.csv"))
        read = csv.reader(path_file)
        # print(read)
        self.stdout.write(self.style.NOTICE("PROSES DATA MASTER UMPAN BALIK"))
        for i in read:
            print(i[0].strip())
            obj, created = UmpanBalik.objects.get_or_create(nama=i[0].strip())
            obj.save()
        self.stdout.write(self.style.SUCCESS("SELESAI"))
