from django.core.management.base import BaseCommand
from skp.models import Hasil

class Command(BaseCommand):
    help = 'Generate Data Master Hasil'

    def handle(self, *args, **options):
        hasil_list = [
            "Dibawah Ekspetasi",
            "Sesuai Ekspetasi",
            "Diatas Ekspetasi",
        ]
        self.stdout.write(self.style.NOTICE('PROSES DATA MASTER HASIL'))
        for i in hasil_list:
            kategori_obj, created = Hasil.objects.get_or_create(nama=i)
            kategori_obj.save() 
        self.stdout.write(self.style.SUCCESS('SELESAI'))