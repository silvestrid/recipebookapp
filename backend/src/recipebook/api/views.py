import logging
import random
import requests

from django.core.exceptions import BadRequest
from django.http import JsonResponse
from django.shortcuts import render

from .models import BaserowUser


API_URL = 'https://api.baserow.io/api'


logger = logging.getLogger(__name__)


def index(request):
    recipes = []
    for user in BaserowUser.objects.all():
        token = user.api_key
        if not token:
            logger.warning(
                "Invalid API token for baserow user %s.. skipping", user.mail)
            continue

        dishes_table_id = user.dishes_table_id
        if not dishes_table_id:
            logger.warning(
                "Invalid Dishes table id for %s. "
                "Check Token API documentation to have the valid table id...skipping",
                user.mail
            )
            continue

        # get table data and
        rsp_data = requests.get(
            f'{API_URL}/database/rows/table/{dishes_table_id}/?user_field_names=true',
            headers={'Authorization': f'Token {token}'}
        ).json()

        if 'results' not in rsp_data:
            logger.error("Something went wrong reading table: %s", rsp_data)
            continue

        recipes.extend([
            {
                "username": user.name,
                "baserow_user": user.baserow_mail,
                **{
                    k.lower().replace(' ', '_'): v for k, v in recipe.items()
                }
            }
            for recipe in rsp_data['results']
        ])

    # mix the recipes randomly
    random.shuffle(recipes)
    return JsonResponse({'recipes': recipes})
