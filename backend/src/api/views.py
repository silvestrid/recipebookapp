import requests

from django.http import JsonResponse
from django.shortcuts import render

from .models import BaserowUser


def index(request):
    baserow_users = BaserowUser.objects.all()
    ret = {}
    for user in baserow_users:
        ret[user.mail] = {
            'api_key': user.api_key
        }
    return JsonResponse(ret)
