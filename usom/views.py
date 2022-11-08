from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# from django.shortcuts import render


@login_required
def menu_pengguna(request):
    menus = []
    if request.user:
        menus += [
            dict(
                title="Beranda",
                icon="fa fa-home",
                url="/",
            ),
            dict(
                title="Menu Pegawai",
                css_classes=["xn-title"],
            ),
            dict(
                title="SKP",
                icon="fa fa-home",
                url=reverse('admin:skp_sasarankinerja_changelist'),
            ),

            dict(
                title="Khusus Administrator",
                css_classes=["xn-title"],
            ),
            dict(
                title="Usom",
                icon='fa fa-users-cog',
                children=[
                    dict(
                        title="Unit Kerja",
                        icon='fa fa-users',
                        url=reverse('admin:usom_unitkerja_changelist')
                    ),
                    dict(
                        title="Pegawai",
                        icon='fa fa-users',
                        url=reverse('admin:usom_account_changelist')
                    ),
                ]
            ),
            dict(
                title="Auth Groups",
                icon="fa fa-home",
                url=reverse('admin:auth_group_changelist'),
            ),
        ]
    return JsonResponse(menus, safe=False)
