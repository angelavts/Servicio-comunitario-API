import uvicorn
from fastapi import FastAPI
from db.session import engine, Base 
from core.config import settings
from api.tasks_router import tasks_router
from api.api_router import api_router
from api.users_router import users_router
from api.projects_router import projects_router
from fastapi.middleware.cors import CORSMiddleware
from db.populate_db import populate_static_db



def create_tables():
    # puede incluir condiciones en caso de que una tabla ya esté creada
    Base.metadata.drop_all(engine) # PARA PRUEBAS
    Base.metadata.create_all(engine)

def create_and_populate_db():
    create_tables()
    populate_static_db()
    # create_tasks()

def start_application():
    # crear e incluir todas las rutas
    _api = FastAPI(title=settings.PROJECT_TITLE)
    _api.include_router(api_router, prefix='/api', tags=['api'])
    _api.include_router(tasks_router, prefix='/tasks', tags=['tasks'])
    _api.include_router(users_router, prefix='/users', tags=['users'])
    _api.include_router(projects_router, prefix='/projects', tags=['projects'])
    
    create_and_populate_db()
    return CORSMiddleware(_api)



app = start_application()
def start_server():
    
    uvicorn.run(
        app='main:app',
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        workers=1,
    )





if __name__ == "__main__":
    start_server()