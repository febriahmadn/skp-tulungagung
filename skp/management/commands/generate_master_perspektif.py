from django.core.management.base import BaseCommand

from skp.models import Perspektif


class Command(BaseCommand):
    help = "Generate Data Master Perspektif"

    def handle(self, *args, **options):
        hasil_list = [
            "Penerimaan Layanan",
            "Penguatan Internal",
            "Proses Bisnis",
            "Anggaran",
        ]
        self.stdout.write(self.style.NOTICE("PROSES DATA MASTER PERSPEKTIF"))
        for i in hasil_list:
            kategori_obj, created = Perspektif.objects.get_or_create(nama=i)
            kategori_obj.save()
        self.stdout.write(self.style.SUCCESS("SELESAI"))
