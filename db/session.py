from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings 
from sqlalchemy.pool import NullPool


#conectar al servidor
engine = create_engine(settings.DATABASE_URL, poolclass=NullPool)

# base de la cual van a heredar todas las clases de la BD
Base = declarative_base()

# crear una sesion (puente entre la conexión y nuestros modelos)
SessionLocal = sessionmaker(engine) 