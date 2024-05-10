from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("people/", views.people_get, name="people_get"),
    path("people/add/", views.people_post, name="people_post"),
    path("people/IDs/", views.people_IDs, name="people_IDs"),
    path("people/check/<str:ID>/", views.people_check, name="people_check"),
    path("qrcode/", views.qrcode_get, name="qrcode_get"),
    path("qrcode/add/", views.qrcode_post, name="qrcode_post"),
    path("qrcode/delete/<str:user_ID>/", views.qrcode_delete, name="qrcode_delete"),
    path("qrcode/check/<str:ID>/", views.qrcode_check, name="qrcode_check"),
    path("login-library/<str:qrcode_ID>/", views.login_library, name="login_library"),
    path(
        "qrcode/people/check/<str:people_id>/",
        views.people_has_qrcode,
        name="people_has_qrcode",
    ),
]

# Urls for admins

urlpatterns += [
    path("stats/<int:days>/", views.stats, name="stats"),
]
