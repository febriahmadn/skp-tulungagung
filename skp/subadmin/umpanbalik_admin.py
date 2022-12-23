from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

from skp.models import UmpanBalik


class UmpanBalikAdmin(admin.ModelAdmin):
    list_display = ("pk", "nama", "created")

    def load(self, request):
        data = []
        qs = UmpanBalik.objects.filter(status=UmpanBalik.Status.ACTIVE).order_by("nama")
        for i in qs:
            data.append({"id": i.id, "nama": i.nama})
        respon = {"success": True, "data": data}
        return JsonResponse(respon, safe=False)

    def get_urls(self):
        admin_url = super().get_urls()
        custom_url = [
            path(
                "load/",
                self.admin_site.admin_view(self.load),
                name="umpan-balik-load",
            ),
        ]
        return custom_url + admin_url
