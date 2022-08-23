import uploads
from os import path
from pydantic import BaseSettings
from sqlalchemy.engine.url import URL

# PENDIENTE: DEFINIR LAS VARIABLES EN UN .ENV
# os.getenv("NOMBRE_VARIABLE", "nombre_archivo")
class Settings(BaseSettings):
    PROJECT_TITLE: str = "Servicio Comunitario"    
    SERVICE_NAME: str = "FastApi"
    DEBUG: bool = False
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123456789"
    DB_DATABASE: str = "Test"
    DATABASE_URL: str = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'
    APP_HOST: str = "localhost"
    APP_PORT: int = 8000
    VALID_FILE_EXTENSIONS: list = ['.xlsx', '.xls']
    ROOT_DIR: str = path.dirname(path.abspath('main.py'))
    UPLOAD_FOLDER: str = "uploads"
    UPLOAD_PATH: str = uploads.UPLOAD_PATH
    # formatos de entrada de archivos excel
    TASK_FILE_FORMAT = ['NOMBRE', 'DESCRIPCIÓN', 'HORAS', 'ESTUDIANTE', 'PROYECTO', 'TUTOR']
    USERS_FILE_FORMAT = ['CÉDULA', 'NOMBRE', 'APELLIDO', 'CARRERA']
    PROJECTS_FILE_FORMAT = ['NOMBRE', 'DESCRIPCIÓN', 'FECHA INICIO', 'CARRERA', 'NOMBRE COORDINADOR',
                            'APELLLIDO COORDINADOR', 'CÉDULA COORDINADOR', 'CARRERA COORDINADOR']


settings = Settings()