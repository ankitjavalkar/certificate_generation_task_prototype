from django.contrib import admin

from .models import CertificateDetails


class CertificateDetailsAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "course", "file_url", "created_on")


admin.site.register(CertificateDetails, CertificateDetailsAdmin)
