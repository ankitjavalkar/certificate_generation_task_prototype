import uuid
from django.db import models
from celery import signals


class CertificateDetails(models.Model):
    participant = models.ForeignKey('ParticipantDetails', on_delete=models.CASCADE)
    file_url = models.FileField(upload_to="pdfs/", null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)

class TaskLog(models.Model):
    PENDING = 'pending'
    STARTED = 'started'
    RETRY = 'retry'
    FAILURE = 'failure'
    SUCCESS = 'success'
    STATES_CHOICES = (
        (PENDING, 'PENDING'),
        (STARTED, 'STARTED'),
        (RETRY,   'RETRY'),
        (FAILURE, 'FAILURE'),
        (SUCCESS, 'SUCCESS'),
    )
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    state = models.CharField(choices=STATES_CHOICES, default=PENDING, max_length=10)
    task_id = models.CharField(max_length=255)
    participant = models.ForeignKey('ParticipantDetails', on_delete=models.CASCADE)

# This model will come from the main web application
class ParticipantDetails(models.Model):
    participant_id = models.UUIDField(default=uuid.uuid4, editable=True)
    email = models.EmailField()
    name = models.CharField(max_length=64)
    course = models.CharField(max_length=64)


@signals.before_task_publish.connect
def handle_before_task_publish(sender=None, body=None, headers=None, **kwargs):
    print(f"HELLOOO++++++++++++++++++++++++BEFORE---TASK---PUB======{body}=====HH=={headers.get('id')}")
    if headers and headers.get('id') and "generate_document" in headers.get("task"):
        # queryset = TaskLog.objects.filter(task_id=body['id'])
        # queryset.update(state=TaskLog.PENDING)

        # Actually created here
        queryset = TaskLog.objects.filter(task_id=headers.get('id'))
        if not queryset:
            participant_id = body[0][0]
            t1 = TaskLog.objects.create(
                state=TaskLog.PENDING,
                task_id=headers.get('id'),
                participant_id=participant_id,
            )

@signals.after_task_publish.connect
def handle_after_task_publish(sender=None, body=None, headers=None, **kwargs):
    print(f"HELLOOO++++++++++++++++++++++++AFTER---TASK---PUB")
    if headers and headers.get('id'):
        queryset = TaskLog.objects.filter(task_id=headers.get('id'))
        queryset.update(state=TaskLog.PENDING)

@signals.task_prerun.connect
def handle_task_prerun(sender=None, task_id=None, **kwargs):
    if task_id:
        print(f"HELLOOO+++++++++++++++++++PRERUN+++++STARTED===={task_id}")
        queryset = TaskLog.objects.filter(task_id=task_id)
        queryset.update(state=TaskLog.STARTED)
        # TaskLog.objects.create(state=TaskLog.STARTED, task_id=task_id)

@signals.task_postrun.connect
def handle_task_postrun(sender=None, task_id=None, state=None, **kwargs):
    if task_id and state:
        print(f"HELLOOO++++++++++++++++++++++++MOSTLY-SUCCESSS===={task_id}======={state}")
        queryset = TaskLog.objects.filter(task_id=task_id)
        queryset.update(state=getattr(TaskLog, state))
        # TaskLog.objects.create(state=getattr(TaskLog, state), task_id=task_id)

@signals.task_failure.connect
def handle_task_failure(sender=None, task_id=None, **kwargs):
    if task_id:
        queryset = TaskLog.objects.filter(task_id=task_id)
        queryset.update(state=TaskLog.FAILURE)
        # TaskLog.objects.create(state=TaskLog.FAILURE, task_id=task_id)

# @signals.task_received.connect
# def handle_task_receive(request=None, **kwargs):
#     print("HELLOOO++++++++++++++++++++++++RECEIVEEEEEE")