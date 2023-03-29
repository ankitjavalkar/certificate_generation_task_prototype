from __future__ import absolute_import, unicode_literals
from io import BytesIO, StringIO
import time
import subprocess
from datetime import datetime, timedelta
import os

from celery import task, shared_task
from celery.utils.log import get_task_logger
from celery.exceptions import OperationalError
from django.core.files import File
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify

from contact_form.models import CertificateDetails, TaskLog, ParticipantDetails
from celery_project.settings import MEDIA_ROOT


logger = get_task_logger(__name__)

TASK_MAX_TIME_LIMIT = 30 * 1


@task(
    bind=True, 
    autoretry_for=(subprocess.CalledProcessError,),
    retry_kwargs={'max_retries': 3},
    time_limit=60,
    default_retry_delay=2
)
@task(bind=True, time_limit=TASK_MAX_TIME_LIMIT)
def generate_document(self, participant_pk, email, name, course, filename):

    myfile = "{} // {} // {}".format(email, name, course)
    p = subprocess.Popen(
        [
            "/tmp/test.sh '{}' '{}'".format(filename, myfile)
        ],
        shell = True,
    )
    p.communicate()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, p.args)

    # Generate file here
    # Save details to DB
    # with open(filename, mode='rb') as f:
    #     certi = CertificateDetails.objects.create(
    #         participant_id=participant_pk,
    #         file_url=File(f, name=filename.rsplit('/', 1))
    #     )
    logger.info(f"Task successfully executed {filename}")


@shared_task(name="schedule_retry")
def schedule_retry():
    unsuccess_tasks = TaskLog.objects.filter(
        state__in=[TaskLog.PENDING, TaskLog.STARTED, TaskLog.RETRY],
        created_on__lte=datetime.now()-timedelta(seconds=20)
    )
    logger.info(f"$$$$$$$========SCHEDULED BEAT")
    for t in unsuccess_tasks:
        logger.info(f"$$$$$$$========SCHEDULED SPAWN TASKS============{t.task_id}===={t.participant.participant_id}")
        participant = ParticipantDetails.objects.get(participant_id=t.participant.participant_id)
        email = participant.email
        name = participant.name
        course = participant.course
        filename = slugify("{}_{}_{}".format(email, name, course)) + ".txt"
        filepath = '{}/pdfs/{}'.format(MEDIA_ROOT, filename)
        generate_document.apply_async(
            (
                participant.pk,
                email, name, course,
                filepath,
            ),
            task_id=t.task_id
        )