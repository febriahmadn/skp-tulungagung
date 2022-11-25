from django.contrib import admin
from solo.admin import SingletonModelAdmin

from services.models import Configurations

admin.site.register(Configurations, SingletonModelAdmin)
