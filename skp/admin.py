from django.contrib import admin

#model import 
from .models import DetailSasaranKinerja

#admin Import 
from .subadmin.detailsasarankerja_admin import DetailsasarankerjaAdmin



admin.site.register(DetailSasaranKinerja, DetailsasarankerjaAdmin)