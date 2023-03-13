import uuid
from django.db import models


# class ContactForm(models.Model):
#     email = models.EmailField()
#     name = models.CharField(max_length=64)
#     subject = models.CharField(max_length=64)
#     message = models.TextField()
#     created_on = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = "contactform"
#         verbose_name = "contact form message"
#         verbose_name_plural = "contact form messages"

#     def __str__(self):
#         return self.email

class CertificateDetails(models.Model):
    participant = models.ForeignKey('ParticipantDetails', on_delete=models.CASCADE)
    file_url = models.FileField(upload_to="pdfs/", null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}_{}_{}".format(self.email, self.name, self.course)


# This model will come from the main web application
class ParticipantDetails(models.Model):
    participant_id = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField()
    name = models.CharField(max_length=64)
    course = models.CharField(max_length=64)