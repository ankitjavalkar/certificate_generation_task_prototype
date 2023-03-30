Certificate Generation Task Queue Prototype

This is a simple POC or prototype for a certificate generator using Django and Celery task queue


How To Run:

Step 1: Run the Django server:

```python manage.py runserver```


Step 2: Run the celery worker

```python -m celery -A celery_project worker -l info -P solo```


Step 3: Optionally run the celery beat worker

```python -m celery -A celery_project beat -l info```


Celery tasks:

1. Place the test.sh script in the /tmp/ folder
2. Run the command ```chmod +x /tmp/test.sh```

Django API Endpoints:

```generate/``` [POST Request]

This endpoint triggers the task to generate a document. The body of the request should contain the ```participant_id``` parameter as a UUID

```task_status/<uuid:task_id>``` [GET Request]

This endpoint gives the current status of a running task

```certificate_status/<uuid:participant_id>``` [GET Request]

This endpoint gives the status and availability of the certificate associated with a participant_id

```participant_task_status/<uuid:participant_id>``` [GET Request]

This endpoint gives the status of the latest task associated with the participant_id