from django.db import models

# Create your models here.
class Email(models.Model):
    email = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)