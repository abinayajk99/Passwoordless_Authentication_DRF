from django.contrib.auth.models import AbstractUser
from django.db import models


class EmailRegister(models.Model):
    email = models.EmailField(max_length=50,unique = True)
    def __str__(self):
      return "{}".format(self.email)