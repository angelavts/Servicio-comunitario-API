import requests
import json
from schemas.users_schema import User, row_to_schema
from typing import List
from core.config import settings
from db.enums import UserStatusEnum, RoleEnum
from core.config import settings
from core import utils

def create_user(user: User, role: str, token: str):
    new_user = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "identification": user.identification,
            "role": role
        }
    # definir header para el request
    headers = {
        'Authorization': token 
    } 
    url = f'{settings.AUTH_SERVICE_URL}/api/register'
    response = requests.post(url, json=new_user, headers=headers)
    # response.raise_for_status()
    try:
        response = response.json()
    except Exception as e:
        print(e)
        response = {'status_code': response.status_code}
    return response


def create_users(users: List[User], role: str, token: str):
    users_list = []
    # armar la estructura json para registrar usuarios
    # en el servicio de autenticación
    for user in users:
        new_user = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "identification": utils.format_identication(user.identification),
                "role": role
            }
        users_list.append(new_user)

    users_json = {
        "users": users_list
    }
    # definir header para el request
    headers = {
        'Authorization': token 
    } 
    url = f'{settings.AUTH_SERVICE_URL}/api/register-masivo'
    response = requests.post(url, json=users_json, headers=headers)
    # response.raise_for_status()
    try:
        response = response.json()
    except Exception as e:
        print(e)
        response = {'status_code': response.status_code}
    return response


def login():
    user =  {            
        "username": "admin",
        "password": "12345678"
    }
    url = f'{settings.AUTH_SERVICE_URL}/api/login'
    response = requests.post(url, json=user)
    response = response.json()
    settings.CURRENT_TOKEN = response['token']
    return response 

