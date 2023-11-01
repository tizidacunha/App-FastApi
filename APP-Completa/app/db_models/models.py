from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Sequence
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = sqlalchemy.orm.declarative_base()


# CREACION DE LA TABLA Y ASIGNACION DE LAS COLUMNAS // SE PUEDEN CREAR MAS TABLAS Y RELACIONARLAS ENTRE SI 



    
class TizianoDB(Base):
    __tablename__ = 'Tiziano'

    id = Column(Integer, Sequence('seq_reg_id', start=1, increment=1),primary_key=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    

    def __init__(self, id, username, email, created_at):
        self.id = id
        self.username = username
        self.email = email
        self.created_at = created_at

    def __repr__(self):
        return f"Usuario({self.username},{self.email},{self.created_at})"

    def __str__(self):
        return self.username

#MODELOS DE TABLAS // VALIDACION DE LOS DATOS

class TizianoCreate(BaseModel):
    username: str
    email: str
    created_at: str


class TizianoUpdate(BaseModel):
    username: str
    email: str
    created_at: str