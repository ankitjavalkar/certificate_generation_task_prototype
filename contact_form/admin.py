from django.contrib import admin

from .models import CertificateDetails, ParticipantDetails, TaskLog


class CertificateDetailsAdmin(admin.ModelAdmin):
    list_display = ("participant", "file_url", "created_on")

class ParticipantDetailsAdmin(admin.ModelAdmin):
    list_display = ("participant_id", "email", "name", "course")

class TaskLogAdmin(admin.ModelAdmin):
    list_display = ("state", "task_id", "created_on", "updated_on")

admin.site.register(CertificateDetails, CertificateDetailsAdmin)
admin.site.register(ParticipantDetails, ParticipantDetailsAdmin)
admin.site.register(TaskLog, TaskLogAdmin)
