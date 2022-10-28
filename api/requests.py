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
    print("TOKEN -------> " + token)
    headers = {
        'Authorization': 'Bearer ' + token
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

def update_user(user: User, token: str):
    modified_user = {
            "identification": user.identification,
            "email": user.email            
        }
    # definir header para el request
    print("TOKEN -------> " + token)
    headers = {
        'Authorization': token
    } 
    url = f'{settings.AUTH_SERVICE_URL}/api/edit-user-profile'
    response = requests.put(url, json=modified_user, headers=headers)
    # response.raise_for_status()
    try:
        response = response.json()
    except Exception as e:
        print(e)
        response = {'status_code': response.status_code, 'ok': False}
    return response


def create_users(users: List[User], role: str, token: str):
    print("Create users")
    users_list = []
    # armar la estructura json para registrar usuarios
    # en el servicio de autenticación
    print("TOKEN -------> " + token)
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

    print("USERS JSON")
    print(users_json)
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
        print("errorrrrrrrrrrrrrrrrrr")
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
    return response 

