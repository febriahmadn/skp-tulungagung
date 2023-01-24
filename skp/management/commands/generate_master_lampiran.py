from django.core.management.base import BaseCommand

from skp.models import Lampiran


class Command(BaseCommand):
    help = "Generate Data Master Perspektif"

    def handle(self, *args, **options):
        hasil_list = [
            "DUKUNGAN SUMBER DAYA",
            "SKEMA PERTANGGUNGJAWABAN",
            "KONSEKUENSI",
        ]
        self.stdout.write(self.style.NOTICE("PROSES DATA MASTER LAMPIRAN"))
        for i in hasil_list:
            lampiran_obj, created = Lampiran.objects.get_or_create(lampiran=i)
            lampiran_obj.save()
        self.stdout.write(self.style.SUCCESS("SELESAI"))
