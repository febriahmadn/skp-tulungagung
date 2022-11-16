from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def view_dashboard(request):
    JENIS_STATISTIK = [
        {'id':1,"text":"Progress Pengisian"},
        {"id":2,"text":"Keterlibatan Matriks"},
        {"id":3,"text":"Penilaian Kurva"},
    ]
    TAHUN = []
    for i in range(2000, 2025):
        TAHUN.append({"id":i,"text":i})
    extra_context = {
        "title": "Home",
        "tahun": TAHUN,
        "jenis": JENIS_STATISTIK
    }
    return render(request, 'admin/dashboard.html', extra_context)

@login_required
def view_profil(request):
    extra_context = {
        "title": "Profil"
    }
    return render(request, 'admin/profil.html', extra_context)
