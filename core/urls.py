"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django_cas_ng.views
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from skp.views import view_dashboard, view_profil
from usom.views import menu_pengguna

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='/'), name="admin_logout"),
    path("menu-pengguna", menu_pengguna, name="menu_pengguna"),
    path("", view_dashboard, name="admin_dashboard"),
    path("profil/", view_profil, name="admin_profil"),
    path(
        "accounts/login",
        django_cas_ng.views.LoginView.as_view(),
        name="cas_ng_login",
    ),
    path(
        "accounts/logout",
        django_cas_ng.views.LogoutView.as_view(),
        name="cas_ng_logout",
    ),
    path(
        "accounts/callback",
        django_cas_ng.views.CallbackView.as_view(),
        name="cas_ng_proxy_callback",
    ),
    path("", include("usom.urls")),
    path("admin/", include("loginas.urls")),
    path("admin/", admin.site.urls),
]
