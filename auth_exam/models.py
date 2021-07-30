from django.db import models
from django.contrib.auth.models import AbstractUser
from unixtimestampfield.fields import UnixTimeStampField
# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        return self.username




class ToDo(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=150)
    due = UnixTimeStampField(use_numeric=True, default=0.0)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.title