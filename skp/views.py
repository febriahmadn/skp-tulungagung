from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from usom.models import UnitKerja


@login_required
def view_dashboard(request):
    JENIS_STATISTIK = [
        {"id": 1, "text": "Progress Pengisian"},
        {"id": 2, "text": "Keterlibatan Matriks"},
        {"id": 3, "text": "Penilaian Kurva"},
    ]
    TAHUN = []
    for i in range(2000, 2025):
        TAHUN.append({"id": i, "text": i})
    unor_list = UnitKerja.objects.filter(aktif=True)
    extra_context = {
        "title": "Home",
        "tahun": TAHUN,
        "jenis": JENIS_STATISTIK,
        'unitkerja': unor_list
    }
    return render(request, "admin/dashboard.html", extra_context)


@login_required
def view_profil(request):
    extra_context = {"title": "Profil"}
    return render(request, "admin/profil.html", extra_context)
