from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# from django.shortcuts import render
def loginas(request, target_user):
    if request.user.is_superuser:
        return True
    return False

@login_required
def menu_pengguna(request):
    menus = [
        dict(
            title="Dashboard",
            icon="fa fa-home",
            url="/",
        ),
    ]
    if request.user:
        menus += [
            # dict(
            #     title="Menu Pegawai",
            #     css_classes=["xn-title"],
            # ),
            dict(
                title="Profil",
                icon="fa fa-user",
                url="#",
            ),
            dict(
                title="SKP",
                icon="fa fa-file-alt",
                url=reverse("admin:skp_sasarankinerja_changelist"),
            ),
        ]
        if request.user.is_superuser:
            menus += [
                dict(
                    title="Khusus Administrator",
                    css_classes=["xn-title"],
                ),
                dict(
                    title="Usom",
                    icon="fa fa-users-cog",
                    children=[
                        dict(
                            title="Unit Kerja",
                            icon="fa fa-users",
                            url=reverse("admin:usom_unitkerja_changelist"),
                        ),
                        dict(
                            title="Pegawai",
                            icon="fa fa-users",
                            url=reverse("admin:usom_account_changelist"),
                        ),
                    ],
                ),
                dict(
                    title="Auth Groups",
                    icon="fa fa-home",
                    url=reverse("admin:auth_group_changelist"),
                ),
            ]
    return JsonResponse(menus, safe=False)
