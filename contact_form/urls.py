from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import * # ContactFormView

app_name = "contact_form"
urlpatterns = [
    # path("", ContactFormView.as_view(), name="contact_form"),
    path("generate/", generate_view, name="generate_view"),
    path("status/<uuid:task_id>", task_status, name="task_status"),
    path("docs/", get_all_documents, name="get_all_documents"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

