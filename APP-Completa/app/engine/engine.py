from fastapi import FastAPI, HTTPException, APIRouter
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Sequence
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base

from app.db_models.models import TizianoDB, TizianoCreate
from app.db_models.models import TizianoCreate, TizianoDB
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
#SE CONECTA A LA BASE DE DATOS 

# HOST // BASE DE DATOS


DIALECT = ''
SQL_DRIVER = ''
USERNAME = ''  # Ingresa tu nombre de usuario
PASSWORD = ''  # Ingresa tu contraseña
HOST = ''  # Ingresa la URL del host de Oracle
PORT =   # Ingresa el número de puerto de Oracle
SERVICE = ''  # Ingresa el nombre del servicio de Oracle

ENGINE_PATH_WIN_AUTH = (
    DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +
    '@' + HOST + ':' + str(PORT) + '/?service_name=' + SERVICE
)



engine = create_engine(ENGINE_PATH_WIN_AUTH)
Session = sessionmaker(engine)
session = Session()
