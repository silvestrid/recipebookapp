from django.db import models


class BaserowUser(models.Model):
    mail = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, unique=True)
    recipebook_db_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.mail
