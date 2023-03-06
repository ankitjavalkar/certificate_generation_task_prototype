from __future__ import absolute_import, unicode_literals
from io import BytesIO, StringIO

from celery import task
from celery.utils.log import get_task_logger
from django.core.files import File
from django.core.files.base import ContentFile

from contact_form.models import CertificateDetails

logger = get_task_logger(__name__)


@task(bind=True)
def generate_document(self, email, name, course, filename):

    # Generate file here
    myfile = "{} // {} // {}".format(email, name, course)
    # Save details to DB
    # certi = CertificateDetails.objects.create(
    #     email=email,
    #     name=name,
    #     course=course,
    #     file_url=File(myfile, name=filename)      
    # )
    certi = CertificateDetails.objects.create(
        email=email,
        name=name,
        course=course,
        file_url=ContentFile(myfile, name=filename)    
    )
    # certi.file_url.save(filename, myfile, save=True)
    # for pdfs use BytesIO https://www.codingforentrepreneurs.com/blog/save-a-auto-generated-pdf-file-django-model/
    # certi.file_url.save(filename, File(myfile))

    logger.info(f"This task is executed :- {filename}")

