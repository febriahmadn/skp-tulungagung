from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def view_dashboard(request):
    extra_context = {
        "title": "Home"
    }
    return render(request, 'admin/dashboard.html', extra_context)
