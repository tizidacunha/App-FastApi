from fastapi import FastAPI, HTTPException, APIRouter, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Sequence
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
import logging
from app.db_models.models import TizianoDB, TizianoCreate, TizianoUpdate
from app.db_models.models import TizianoCreate, TizianoDB
from app.engine.engine import session

logging.basicConfig(filename="Registro de creaciones.log", level=logging.INFO)

router = APIRouter()

# MANEJO DE IDss

class ManejoID:
    def __init__(self):
        self.deleted_ids = set()
        self.next_id = 1

    def get_next_id(self):
        if self.deleted_ids:
            return self.deleted_ids.pop()
        else:
            self.next_id += 1
            return self.next_id

id_manejo = ManejoID()



#------------------------------------------------------------------------------------------
from app.auth.authentication import get_user_disable_current
#--------------------------------------------------------------------------------------------------

# EJECUCIONES REST 

from fastapi import HTTPException

@router.get("/")
def pner_docs():
    return "Pone /docs"

@router.get("/usuarios/leer")
def leer_usuarios(current_user: str = Depends(get_user_disable_current)):
    try:
        users = session.query(TizianoDB).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/usuarios/crear")
def create_user(user: TizianoCreate, current_user: str = Depends(get_user_disable_current)):
    try:
        dia_ = datetime.fromisoformat(user.created_at)
        new_user = TizianoDB(id=id_manejo.get_next_id(),username=user.username, email=user.email, created_at=dia_)
        logging.info(f"Nuevo usuario creado: Nombre: {user.username}, Email: {user.email}")
        session.add(new_user)
        session.commit()
        return {"message": "Usuario creado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/usuarios/actualizar/{user_id}")
def update_user(user_id: int, user_update: TizianoUpdate, current_user: str = Depends(get_user_disable_current)):
    user = session.query(TizianoDB).filter_by(id=user_id).first()
    if user:
        # Busca el usuario
        if user_update.username:
            user.username = user_update.username
        if user_update.email:
            user.email = user_update.email
        if user_update.created_at:
            user.created_at = datetime.fromisoformat(user_update.created_at)

        session.commit()
        return {"message": "Usuario actualizado"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.delete("/usuarios/borrar")
def delete_users(user_id: int, current_user: str = Depends(get_user_disable_current)):
    try:
        user = session.query(TizianoDB).filter_by(id=user_id).first()
        if user:
            id_manejo.deleted_ids.add(user.id)
            session.delete(user)
            session.commit()
            return {"message": "Usuario eliminado"} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#-----------------------------------------------------------------------------------------------------------



@router.delete("/usuarios/borrar-todos")
def delete_all_users(current_user: str = Depends(get_user_disable_current)):
    try:
        deleted_count = session.query(TizianoDB).delete()
        session.commit()
        id_manejo.deleted_ids.clear()  # Limpia todos los IDs eliminados
        return {"message": f"Se eliminaron {deleted_count} usuarios"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


    