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
        recipebook_db_name = user.recipebook_db_name
        # check if a recipe book db exists
        if not recipebook_db_name:
            continue

        # API_TOKEN doesn't work, so use user authentication
        rsp = requests.post(
            f'{API_URL}/user/token-auth/',
            data={
                'username': user.mail,
                'password': user.password,
            }
        ).json()

        if 'token' not in rsp:
            logger.error("Failed to get token for user %s", user.mail)
            continue
        jwt = rsp['token']

        # "Recipe Book" is the name of the application
        # every application has a unique name and contains all the tables
        applications = requests.get(
            f'{API_URL}/applications/',
            headers={'Authorization': f'JWT {jwt}'}
        ).json()

        # look for the table fields id
        dishes_fields_id = None
        for app in applications:
            if app['name'] == recipebook_db_name:
                for table in app['tables']:
                    if table['name'] == 'Dishes':
                        dishes_fields_id = table['id']
                        break
                if dishes_fields_id is not None:
                    break
        else:
            logger.error("Failed to find dishes table for user %s", user.mail)
            continue

        # get table data and
        table_info = requests.get(
            f'{API_URL}/database/views/table/{dishes_fields_id}/?include=filter,sortings',
            headers={'Authorization': f'JWT {jwt}'}
        ).json()

        # first object of the list is the "All Dishes" grid
        dishes_table_id = table_info[0]['id']
        table_data = requests.get(
            f'{API_URL}/database/views/grid/{dishes_table_id}/?limit=80&offset=0&',
            headers={'Authorization': f'JWT {jwt}'}
        ).json()

        table_fields = requests.get(
            f'{API_URL}/database/fields/table/{dishes_fields_id}/',
            headers={'Authorization': f'JWT {jwt}'}
        ).json()

        for row in table_data['results']:
            recipe = {'owner': user.name}
            for field in table_fields:
                name = field['name'].lower().replace(' ', '_')
                recipe[name] = row[f'field_{field["id"]}']
            recipes.append(recipe)
    # mix the recipes randomly
    random.shuffle(recipes)
    return JsonResponse({'recipes': recipes})
