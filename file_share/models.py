from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum

class UserRoleEnum(Enum):
    OPS = "OPS"
    CLIENT = "CLIENT"


class FileTypeEnum(Enum):
    PPTX = "PPTX"
    DOCX = "DOCX"
    XLSX = "XLSX"


# Create your models here.


class UserAccount(AbstractUser):
    user_id = models.CharField(max_length=36, primary_key=True, default=uuid4)
    is_email_verified = models.BooleanField(default=False)
    role = models.CharField(
        max_length=64,
        choices=[(each.value, each.name.capitalize()) for each in UserRoleEnum])

    def __str__(self):
        return f"UserAccount: {self.user_id}"


class FileDetails(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=64,
        choices=[(each.value, each.name.capitalize()) for each in FileTypeEnum])
    uploaded_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_update_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"FileDetails: {self.id} - {self.name}"
