from django.db import models


class BaserowUser(models.Model):
    mail = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.mail
