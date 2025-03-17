from django.db import models
from django.contrib.auth.models import User

class Applicant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    application_status = models.CharField(max_length=100, choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ])
    
    def __str__(self):
        return self.name
<<<<<<< HEAD
=======

class UploadedDocument(models.Model):
    document_type = models.CharField(max_length=255)
    document = models.FileField(upload_to='media/uploads/')  # Saves inside 'media/uploads/'

    def __str__(self):
        return self.document_type
>>>>>>> 69002000 (made changes)
