from django.contrib import admin
from .models import People, QrCode, Data


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = "name", "phone_number", "created"
    list_filter = "name", "phone_number"
    search_fields = "name", "phone_number"


@admin.register(QrCode)
class QrCodeAdmin(admin.ModelAdmin):
    list_display = "people", "created"
    list_filter = "people", "created"
    search_fields = ("people",)


@admin.register(Data)
class QrCodeAdmin(admin.ModelAdmin):
    list_display = "people", "purpose", "type", "created"
    list_filter = "people", "created"
    search_fields = ("people",)
