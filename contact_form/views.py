from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_exempt

from celery.result import AsyncResult

# from .forms import ContactFormModelForm
from .tasks import generate_document
from .models import CertificateDetails


# class ContactFormView(FormView):
#     form_class = ContactFormModelForm
#     template_name = "contact_form/contact_form.html"
#     success_url = "/"

#     def form_valid(self, form):
#         form.save()
#         self.send_email(form.cleaned_data)

#         return super().form_valid(form)

#     def send_email(self, valid_data):
#         email = valid_data["email"]
#         subject = "Contact form sent from website"
#         message = (
#             f"You have received a contact form.\n"
#             f"Email: {valid_data['email']}\n"
#             f"Name: {valid_data['name']}\n"
#             f"Subject: {valid_data['subject']}\n"
#             f"{valid_data['message']}\n"
#         )
#         send_email_task.delay(
#             email, subject, message,
#         )

@csrf_exempt
def generate_view(request):
    print("INFO: Requesting generate_view method")
    if request.method == "POST":
        email = request.POST.get("email", "")
        name = request.POST.get("name", "")
        course = request.POST.get("course", "")    
        filename = slugify("{}_{}_{}".format(email, name, course)) + ".txt"

        task_inst = generate_document.delay(
            email,
            name,
            course,
            filename,
        )

        print("INFO: generate_view method execution complete")
        
        return JsonResponse(
            {
                "task_id": task_inst.id,
            }
        )

def task_status(request, task_id):
    result = AsyncResult(str(task_id))
    return JsonResponse(
        {
            "task_id": task_id,
            "state": result.state,
        }
    )

def get_all_documents(request):
    documents = CertificateDetails.objects.all()
    html_text = "<br><br>".join(
        [
            "{} : {}".format(doc, doc.file_url) for doc in documents
        ]
    )
    return HttpResponse(
        f"<html><body> {html_text} </body></html>"
    )