from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_exempt

from celery.result import AsyncResult

from .tasks import generate_document
from .models import CertificateDetails, ParticipantDetails

@csrf_exempt
def generate_view(request):
    print("INFO: Requesting generate_view method")
    if request.method == "POST":
        participant_id = request.POST.get("participant_id", "")
        participant = ParticipantDetails.objects.get(id=participant_id)
        # email = request.POST.get("email", "")
        # name = request.POST.get("name", "")
        # course = request.POST.get("course", "")
        
        email = participant.email
        name = participant.name
        course = participant.course
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

def participant_certificate_status(request, participant_id):
    certificate_details = CertificateDetails.objects.get(participant__participant_id=participant_id)
    if certificate_details:
        return JsonResponse(
            {
                "participant_id": certificate_details.participant.participant_id,
                "participant_email": certificate_details.participant.email,
                "participant_name": certificate_details.participant.name,
                "participant_course": certificate_details.participant.course,
                "certificate_url": certificate_details.file_url,
                "status": "SUCCESS",
                "message": "certificate successfully generated"
            }
        )
    else:
        return JsonResponse(
            "status": "FAILURE",
            "message": "certificate could not be generated"
        )


# def get_all_documents(request, participant_id):
#     documents = CertificateDetails.objects.all()
#     html_text = "<br><br>".join(
#         [
#             "{} : {}".format(doc, doc.file_url) for doc in documents
#         ]
#     )
#     return HttpResponse(
#         f"<html><body> {html_text} </body></html>"
#     )