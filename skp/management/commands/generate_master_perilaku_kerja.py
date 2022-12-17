from django.core.management.base import BaseCommand

from skp.models import DaftarPerilakuKerja, PerilakuKerja


class Command(BaseCommand):
    help = "Generate Data Master Perilaku Kerja"

    # Initial Data ==> Belum Selesai
    def handle(self, *args, **options):
        data = [
            {
                "nama": "Berorientasi Pelayanan",
                "anak": [
                    {"nama": "Memahami dan memenuhi kebutuhan masyarakat"},
                    {"nama": "Ramah, cekatan, solutif, dan dapat diandalkan"},
                    {"nama": "Melakukan pebaikan tiada henti"},
                ],
            },
            {
                "nama": "Akuntabel",
                "anak": [
                    {
                        "nama": "Melaksanakan tugas dengan jujur bertanggung jawab "
                        "cermat disiplin dan berintegritas tinggi"
                    },
                    {
                        "nama": "Menggunakan kekayaan dan BMN secara betranggung "
                        "jawab efektif dan efisien"
                    },
                    {"nama": "Tidak menyalahgunakan kewenangan jabatan"},
                ],
            },
            {
                "nama": "Kompeten",
                "anak": [
                    {
                        "nama": "Meningkatkan kompetensi diri untuk menjawab "
                        "tantangan yang selalu berubah"
                    },
                    {"nama": "Membantu orang lain belajar"},
                    {"nama": "Membangun lingkungan kerja yang kondusif"},
                ],
            },
            {
                "nama": "Harmonis",
                "anak": [
                    {"nama": "Menghargai setiap orang apapun latar belakangnya"},
                    {"nama": "Suka menolong orang lain"},
                    {"nama": "Membangun lingkungan kerja yang kondusif"},
                ],
            },
            {
                "nama": "Loyal",
                "anak": [
                    {
                        "nama": "Memegang teguh ideologi Pancasila, Undang-Undang "
                        "Dasar Negara Republik Indonesia Tahun 1945, setia pada NKRI "
                        "serta pemerintahan yang sah"
                    },
                    {
                        "nama": "Menjaga nama baik sesama ASN, Pimpinan, Instansi dan "
                        "Negara"
                    },
                    {"nama": "Menjaga rahasia jabatan dan negara"},
                ],
            },
            {
                "nama": "Adaptif",
                "anak": [
                    {"nama": "Cepat menyesuaikan diri menghadapi perubahan"},
                    {"nama": "Terus berinovasi dan mengembangkan kreativitas"},
                    {
                        "nama": "Memberi kesempatan kepada beragai pihak untuk "
                        "berkontribusi"
                    },
                ],
            },
            {
                "nama": "Kolaboratif",
                "anak": [
                    {
                        "nama": "Memberi kesempatan kepada beragai pihak untuk "
                        "berkontribusi"
                    },
                    {
                        "nama": "Terbuka dalam bekerja sama untuk menghasilkan "
                        "nilai tambah"
                    },
                    {
                        "nama": "Menggerakkan pemanfaatan berbagai sumberdaya untuk "
                        "tujuan bersama"
                    },
                ],
            },
        ]
        for i in data:
            print(i["nama"])
            obj, created = PerilakuKerja.objects.get_or_create(perilaku_kerja=i["nama"])
            obj.save()
            print(obj)
            if created:
                for anak in i["anak"]:
                    anak_obj, anak_created = DaftarPerilakuKerja.objects.get_or_create(
                        perilaku_kerja=obj, keterangan=anak["nama"]
                    )
                    anak_obj.save()
                    print(anak_obj)
        self.stdout.write(self.style.NOTICE("PROSES DATA MASTER PERILAKU KERJA"))
        self.stdout.write(self.style.SUCCESS("SELESAI"))
