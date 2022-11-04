import crud.users_crud as users_crud
from db import db_models as models 
from sqlalchemy.orm import Session
from db.db import get_db
from db.enums import RoleEnum
from schemas.users_schema import User
import os

def populate_static_db():
    create_institutions(get_db())
    create_faculties(get_db())
    create_careers(get_db())
    create_admin_user(get_db())

def create_admin_user(db: Session):
    try:
        admin = models.User(
            identification= str(os.getenv('ADMIN_IDENTIFICATION')),
            first_name=str(os.getenv('ADMIN_FIRSTNAME')),
            last_name=str(os.getenv('ADMIN_LASTNAME')),
            career_id = int(os.getenv('ADMIN_CAREER')),
            email = str(os.getenv('ADMIN_EMAIL')),
            phone = str(os.getenv('ADMIN_PHONE')),
            role = RoleEnum.Coordinator
        )
        db.add(admin)
        db.commit() 
    except Exception as e:
        print(e)
        db.rollback()
    db.close()


def create_institutions(db: Session):
    institutions = []
    institutions.append(
        models.Institution(
            name='Universidad de Carabobo'
        )  
    )
    try:
        for institution in institutions:
            db.add(institution)
            db.commit() 
    except Exception as e:
        print(e)
        db.rollback()
    db.close()

def create_faculties(db: Session):
    faculties = []
    faculties.append(
        models.Faculty(
            name='Facultad Experimental de Ciencias y Tecnologías',
            acronym='FACYT',
            institution_id = 1
        )  
    )
    try:
        for faculty in faculties:
            db.add(faculty)
            db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    db.close()


def create_careers(db: Session):
    careers = []
    careers.append(
        models.Career(
            name='Computación',
            faculty_id= 1
        )  
    )
    careers.append(
        models.Career(
            name='Química',
            faculty_id= 1
        )  
    )
    careers.append(
        models.Career(
            name='Física',
            faculty_id= 1
        )  
    )
    careers.append(
        models.Career(
            name='Matemática',
            faculty_id= 1
        )  
    )
    careers.append(
        models.Career(
            name='Biología',
            faculty_id= 1
        )  
    )
    try:
        for career in careers:
            db.add(career)
            db.commit()   
    except Exception as e:
        print(e)
        db.rollback()
    db.close()
    