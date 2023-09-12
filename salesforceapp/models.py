from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class SalesforceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    instance_url = models.URLField()

    def __str__(self):
        return self.user.username


