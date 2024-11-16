from django.contrib import admin
from file_share import models


# Register your models here.
@admin.register(models.UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ["user_id", "username", "email", "role"]


@admin.register(models.FileDetails)
class FileDetailsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "uploaded_by_id", "creation_datetime"]
