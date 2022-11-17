from django.contrib.auth import views as auth_views
from django.urls import path


urlpatterns = [
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # path(
    #     "usom/login",
    #     django_cas_ng.views.LoginView.as_view(),
    #     name="cas_ng_login"
    # ),
    # path(
    #     "usom/logout",
    #     django_cas_ng.views.LogoutView.as_view(),
    #     name="cas_ng_logout"
    # ),
    # path(
    #     "usom/callback",
    #     django_cas_ng.views.CallbackView.as_view(),
    #     name="cas_ng_proxy_callback"
    # )
]
