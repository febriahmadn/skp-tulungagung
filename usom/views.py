from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.
@login_required
def menu_pengguna(request):
    menus = []
    if request.user:
        menus += [
            dict(
                title='Beranda',
                icon='fa fa-home',
                url='/',
            ),
        ]
    return JsonResponse(menus, safe=False)

