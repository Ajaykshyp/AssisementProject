import datetime
import jwt
import datetime
from django.conf import settings 
import jwt
from api.v1.models import *
from django.conf import settings
import random
import string

def get_access_tokens_for_user(user,remember_me):
    if remember_me:
        access_token_payload = {
            'user_id': user,
            'token_type': 'access',
            'exp': datetime.datetime.now() + datetime.timedelta(days=1),
            'jti': "b932ba39d8024b39a55b3850129cbd10"}
    else:
        access_token_payload = {
            'user_id': user,
            'token_type': 'access',
            'exp': datetime.datetime.now() + datetime.timedelta(days=4),
            'jti': "b932ba39d8024b39a55b3850129cbd10"}
    return jwt.encode(access_token_payload,settings.SECRET_KEY, algorithm='HS256')


def get_refres_tokens_for_user(user,remember_me):
    if remember_me:
        refresh_token_payload = {
            'user_id': user,
            'token_type': 'refresh',
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=500),
            'jti': "b932ba39d8024b39a55b3850129cbd10"}
    else:
        refresh_token_payload = {
            'user_id': user,
            'token_type': 'refresh',
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=4),
            'jti': "b932ba39d8024b39a55b3850129cbd10"}
    return jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')


def generate_emp_id(role_id):
    S = 10 
    role_prefix_map = {
        '1': 'AD',
        '2': 'US',
       }

    prefix = role_prefix_map.get(str(role_id), "")  
    if not prefix:
        return None  
    while True:
        ran_data = ''.join(random.choices(string.digits, k=S))
        new_emp_id = f"{prefix}{ran_data}"
        if not UserMaster.objects.filter(employee_id=new_emp_id).exists():
            return new_emp_id