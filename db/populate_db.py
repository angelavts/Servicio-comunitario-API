from db import db_models as models 
from sqlalchemy.orm import Session
from db.db import get_db


def populate_static_db():
    create_institutions(get_db())
    create_faculties(get_db())
    create_careers(get_db())

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
    