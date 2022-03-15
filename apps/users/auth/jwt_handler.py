from fastapi.exceptions import HTTPException
import time 
import jwt
from decouple import config

JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')


def token_response(access:str):
    return {"access token":access}

def tokens_response(access:str,refresh:str):
    return {"access token":access,'refresh':refresh}

def singJWT(userID:str,type:str='all'):
    payload_access = {
        "userID":userID,
        "type":'access',
        "expiry":time.time()+600
    }
    payload_refresh = {
        "userID":userID,
        "type":'refresh',
        "expiry":time.time()+10000
    }
    token = jwt.encode(payload_access,JWT_SECRET,JWT_ALGORITHM)
    if type == 'all':
        refresh_token = jwt.encode(payload_refresh,JWT_SECRET,JWT_ALGORITHM)
        return tokens_response(token,refresh_token)
    return token_response(token)


def decodeJWT(token:str):
    try:
        decode_token = jwt.decode(token,JWT_SECRET,JWT_ALGORITHM)
        if decode_token.get('expiry') >= time.time():
            return decode_token
        return  None
    except Exception:
        return None

def get_payload_jwt(token):
    try:
        decode_token = jwt.decode(token,JWT_SECRET,JWT_ALGORITHM)
        if decode_token.get('expiry') >= time.time():
            return decode_token
        raise HTTPException(status_code=400,detail='token invalid or expired')
    except Exception:
        print('что-то пошло не так')
        raise HTTPException(status_code=400,detail='token invalid or expired')

