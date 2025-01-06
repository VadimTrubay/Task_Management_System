from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(validators=[EmailValidator()], unique=True)

    def __str__(self):
        return self.username
