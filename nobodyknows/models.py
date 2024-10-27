from django.db import models
from django.conf import settings

class user_contact_review(models.Model):
    name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    subject = models.CharField(max_length = 60)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
class mam_wa_group(models.Model):
    wa_number = models.CharField(max_length = 50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)