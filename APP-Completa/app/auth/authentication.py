# AUTENTICACION // TOKEN 

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Union
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

fake_user_db = {
"tiziano": {
        "username": "tiziano",
        "full_name": "Tiziano da Cunha",
        "email": "tizidac2004@gmail.com",
        "password": "$2a$10$ArW7ZFG7kabgW4E0iGIrGuB.XM6byUhv1nMSdZyEWBiYypkChPAa.", #secret
        "disable": False,
}
}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

SECRET_KEY = "hola"
ALGORITHM = "HS256"


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer("/token")

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
    email: Union[str, None] = None
    disable: Union[bool, None] = None


class UserINDB(User):
    password: str



def get_user(db, username):
    if username in db:
        user_data = db[username]
        return UserINDB(**user_data)
    else:
       return []


def verify_password(plane_passoword, password):
    return pwd_context.verify(plane_passoword, password)

def authenticate_user(db, username, password):
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers= {"WWW-Authenticate": "Bearer"})
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers= {"WWW-Authenticate": "Bearer"})
    return user



def create_token(data: dict, time_expire: Union[datetime, None] = None):
    data_copy = data.copy()
    if time_expire is None:
        expires = datetime.utcnow() + timedelta(minutes=15)
    else:
        expires = datetime.utcnow() + time_expire
    data_copy.update({"exp": expires})
    token_jwt = jwt.encode(data_copy, key = SECRET_KEY , algorithm=ALGORITHM)
    return token_jwt

def get_user_current(token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = token_decode.get("sub")
        if username == None:
            raise HTTPException(status_code=401, detail="Could not validate credentials", headers= {"WWW-Authenticate": "Bearer"})
    except JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials", headers= {"WWW-Authenticate": "Bearer"})
    user = get_user(fake_user_db, username)
    if not user:
            raise HTTPException(status_code=401, detail="Could not validate credentials", headers= {"WWW-Authenticate": "Bearer"})
    return user


def get_user_disable_current(user: User = Depends(get_user_current)):
    if user.disable:
        raise HTTPException(status_code=400, detail="Inactive User")
    return user

#--------------------------------------------------------------------------------------------------

from app.routers.ejecuciones import router
#--------------------------------------------------------------------------------------------------


@router.get("/users/me")
def user(user: User = Depends(get_user_disable_current)):
    return user


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_user_db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = create_token({"sub": user.username}, access_token_expires)
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }
