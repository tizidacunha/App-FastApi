from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Sequence
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from app.engine.engine import ENGINE_PATH_WIN_AUTH
from app.routers.ejecuciones import router as user_router
from app.db_models.models import TizianoDB
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import time
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

# CREACION DE LA APP Y ROUTER 
engine = create_engine(ENGINE_PATH_WIN_AUTH)
Session = sessionmaker(engine)
session = Session()

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = sqlalchemy.orm.declarative_base()

app = FastAPI()
app.include_router(user_router)

from app.engine.engine import session  

def delete_all_users():
    try:
        session.query(TizianoDB).delete()
        session.commit()
        return {"message": "Todos los usuarios han sido eliminados"}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


engine = create_engine(ENGINE_PATH_WIN_AUTH)
Session = sessionmaker(engine)
session = Session()

app = FastAPI()
app.include_router(user_router)


@app.middleware("http")
async def verify_user(request: Request, call_next):
    if request.headers.get("User-Agent", "").find("Mobile") == -1:
        response = await call_next(request)
        return response
    else:
        return JSONResponse(content={"message": "error: Estás en Mobile"}, status_code=401)


class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["Tiempo-Respuesta"] = str(process_time)
        return response


origins = [
    "https://localhost",
    "http://localhost",
    "http://localhost:8000",
    "https://127.0.0.1",
    "http://127.0.0.1",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="https://.*\.afip\.gob\.ar",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(MyMiddleware)  



