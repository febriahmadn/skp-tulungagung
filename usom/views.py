from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse


# from django.shortcuts import render
def loginas(request, target_user):
    if request.user.is_superuser:
        return True
    return False


def admin_menus(user=None):
    menus = [
        dict(
            title="Dashboard",
            icon="fa fa-home",
            url=reverse("admin_dashboard"),
        ),
    ]
    if user:
        menus += [
            dict(
                title="Profil",
                icon="fa fa-user",
                url=reverse("admin:usom_account_profile"),
            ),
            dict(
                title="SKP",
                icon="fa fa-file-alt",
                url=reverse("admin:skp_sasarankinerja_changelist"),
            ),
        ]
        if (
            user.is_superuser
            or user.jenis_jabatan == "JPT"
            or user.groups.filter(name="Bupati").exists()
        ):
            menus += [
                dict(
                    title="Rekonsiliasi SKP",
                    icon="fa fa-copy",
                    url=reverse("admin:skp_sasarankinerja_rekonsiliasi"),
                ),
            ]
        if user.is_superuser:
            menus += [
                dict(
                    title="SKP Manage",
                    header=True,
                ),
                dict(
                    title="Detail Sasaran Kinerja",
                    icon="fa fa-building",
                    url=reverse("admin:skp_detailsasarankinerja_changelist"),
                ),
                dict(
                    title="Rencana Hasil Kerja",
                    icon="fa fa-building",
                    url=reverse("admin:skp_rencanahasilkerja_changelist"),
                ),
                dict(
                    title="Indikator Kinerja Individu",
                    icon="fa fa-building",
                    url=reverse("admin:skp_indikatorkinerjaindividu_changelist"),
                ),
                dict(
                    title="Master SKP",
                    icon="fa fa-users-cog",
                    children=[
                        dict(
                            title="Perilaku Kerja",
                            icon="fa fa-home",
                            url=reverse("admin:skp_perilakukerja_changelist"),
                        ),
                        dict(
                            title="Perspektif",
                            icon="fa fa-home",
                            url=reverse("admin:skp_perspektif_changelist"),
                        ),
                        dict(
                            title="Lampiran",
                            icon="fa fa-home",
                            url=reverse("admin:skp_lampiran_changelist"),
                        ),
                    ],
                ),
                dict(
                    title="Daftar Lampiran",
                    icon="fa fa-building",
                    url=reverse("admin:skp_daftarlampiran_changelist"),
                ),
                dict(
                    title="Daftar Perilaku Kerja",
                    icon="fa fa-building",
                    url=reverse("admin:skp_daftarperilakukerja_changelist"),
                ),
                # dict(
                #     title="Daftar Hasil",
                #     icon="fas fa-bullseye",
                #     url=reverse("admin:skp_hasil_changelist"),
                # ),
            ]

            menus += [
                dict(
                    title="Khusus Administrator",
                    header=True,
                ),
                dict(
                    title="Usom",
                    icon="fa fa-users-cog",
                    children=[
                        dict(
                            title="Unit Kerja",
                            icon="fa fa-building",
                            url=reverse("admin:usom_unitkerja_changelist"),
                        ),
                        dict(
                            title="Pegawai",
                            icon="fa fa-user",
                            url=reverse("admin:usom_account_changelist"),
                        ),
                        dict(
                            title="Groups",
                            icon="fa fa-users",
                            url=reverse("admin:auth_group_changelist"),
                        ),
                    ],
                ),
                dict(
                    title="Configuration",
                    icon="fa fa-cog",
                    url=reverse("admin:services_configurations_changelist"),
                ),
            ]
    return menus


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
                url=reverse("admin:usom_account_profile"),
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
                    title="SKP Manage",
                    css_classes=["xn-title"],
                ),
                dict(
                    title="Detail Sasaran Kinerja",
                    icon="fa fa-building",
                    url=reverse("admin:skp_detailsasarankinerja_changelist"),
                ),
                dict(
                    title="Rencana Hasil Kerja",
                    icon="fa fa-building",
                    url=reverse("admin:skp_rencanahasilkerja_changelist"),
                ),
                dict(
                    title="Indikator Kinerja Individu",
                    icon="fa fa-building",
                    url=reverse("admin:skp_indikatorkinerjaindividu_changelist"),
                ),
                dict(
                    title="Master SKP",
                    icon="fa fa-users-cog",
                    children=[
                        dict(
                            title="Perilaku Kerja",
                            icon="fa fa-home",
                            url=reverse("admin:skp_perilakukerja_changelist"),
                        ),
                        dict(
                            title="Perspektif",
                            icon="fa fa-home",
                            url=reverse("admin:skp_perspektif_changelist"),
                        ),
                        dict(
                            title="Lampiran",
                            icon="fa fa-home",
                            url=reverse("admin:skp_lampiran_changelist"),
                        ),
                    ],
                ),
                dict(
                    title="Daftar Lampiran",
                    icon="fa fa-building",
                    url=reverse("admin:skp_daftarlampiran_changelist"),
                ),
                dict(
                    title="Daftar Perilaku Kerja",
                    icon="fa fa-building",
                    url=reverse("admin:skp_daftarperilakukerja_changelist"),
                ),
                # dict(
                #     title="Daftar Hasil",
                #     icon="fas fa-bullseye",
                #     url=reverse("admin:skp_hasil_changelist"),
                # ),
            ]

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
                            icon="fa fa-building",
                            url=reverse("admin:usom_unitkerja_changelist"),
                        ),
                        dict(
                            title="Pegawai",
                            icon="fa fa-user",
                            url=reverse("admin:usom_account_changelist"),
                        ),
                        dict(
                            title="Groups",
                            icon="fa fa-users",
                            url=reverse("admin:auth_group_changelist"),
                        ),
                    ],
                ),
                dict(
                    title="Configuration",
                    icon="fa fa-cog",
                    url=reverse("admin:services_configurations_changelist"),
                ),
            ]
    return JsonResponse(menus, safe=False)
