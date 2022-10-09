import uploads
import os
from os import path
from dotenv.main import load_dotenv
from pydantic import BaseSettings
from sqlalchemy.engine.url import URL

load_dotenv()

# PENDIENTE: DEFINIR LAS VARIABLES EN UN .ENV
# os.getenv("NOMBRE_VARIABLE", "nombre_archivo")
class Settings(BaseSettings):
    PROJECT_TITLE: str = os.getenv('PROJECT_TITLE')
    SERVICE_NAME: str = os.getenv('SERVICE_NAME')
    DEBUG: bool = False
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = int(os.getenv('DB_PORT'))
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_DATABASE: str = os.getenv('DB_DATABASE')
    DATABASE_URL: str = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'
    APP_HOST: str = os.getenv('APP_HOST')
    APP_PORT: int = os.getenv('APP_PORT')
    VALID_FILE_EXTENSIONS = os.getenv('VALID_FILE_EXTENSIONS')
    ROOT_DIR: str = path.dirname(path.abspath('main.py'))
    UPLOAD_FOLDER: str = "uploads"
    UPLOAD_PATH: str = uploads.UPLOAD_PATH
    # formatos de entrada de archivos excel
    TASK_FILE_FORMAT = os.getenv('TASK_FILE_FORMAT')
    USERS_FILE_FORMAT = os.getenv('USERS_FILE_FORMAT')
    PROJECTS_FILE_FORMAT = os.getenv('PROJECTS_FILE_FORMAT')
    API_KEYS = os.getenv('API_KEYS')
    ORIGINS = os.getenv('ORIGINS')
    AUTH_SERVICE_URL: str = os.getenv('AUTH_SERVICE_URL')

settings = Settings()
settings.VALID_FILE_EXTENSIONS = settings.VALID_FILE_EXTENSIONS.split(' ')
settings.TASK_FILE_FORMAT = settings.TASK_FILE_FORMAT.split('-')
settings.USERS_FILE_FORMAT = settings.USERS_FILE_FORMAT.split('-')
settings.PROJECTS_FILE_FORMAT = settings.PROJECTS_FILE_FORMAT.split('-')
settings.API_KEYS = settings.API_KEYS.split(' ')
settings.ORIGINS = settings.ORIGINS.split(' ')
