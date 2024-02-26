from fastapi import Depends, security, HTTPException, status
from database import Mysql
import hashlib, jwt
from typing import Annotated
from datetime import timedelta, datetime


username = 'test'
password = 'test'
SECRET_KEY, ALGORITH = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NSwidXNlcm5hbWUiOiJ0ZXN0MiIsImV4cCI6MTcwMTI1OTYwOH0.6lCZJuzqvptm9xM1JVhwEMWUUqzN3qSZ8ipz2sPjwN4', 'HS256'


async def basic_authentication(credentials: security.HTTPBasicCredentials = Depends(security.HTTPBasic())) -> str|None:
    if credentials.username != username or credentials.password != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid credentails', headers={"WWW-Authenticate": "Basic"})
    return credentials.username


async def authencticate_admin(username: str, password: str) -> None|dict:
    db_obj = Mysql()
    try:
        user_dict = db_obj.select(query_str="select username from user where username = %s and password = %s", query_params=(username, hashlib.sha1(bytes(password, 'utf-8')).hexdigest()), is_fetch_one=True)
    except Exception as e:
        user_dict = None
    finally:
        del db_obj
    return user_dict


async def create_access_token(user_dict: dict, expiry_time_duration: timedelta) -> str:
    user_dict['exp'] = datetime.utcnow() + expiry_time_duration
    return jwt.encode(user_dict, SECRET_KEY, algorithm=ALGORITH)


async def verify_token(token: Annotated[str, Depends(security.OAuth2PasswordBearer(tokenUrl='admin/login'))]) -> None|dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=ALGORITH)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='token is invalid or expired.')
    
verify_token_dep = Annotated[dict, Depends(verify_token)]
