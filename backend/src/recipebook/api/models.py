from django.db import models


class BaserowUser(models.Model):
    name = models.CharField(max_length=100)
    baserow_mail = models.CharField(max_length=255, unique=True)
    api_key = models.CharField(max_length=255, unique=True)
    dishes_table_id = models.IntegerField()

    def __str__(self) -> str:
        return self.name
