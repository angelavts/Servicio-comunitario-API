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
    for institution in institutions:
        db.add(institution)
        db.commit() 

def create_faculties(db: Session):
    faculties = []
    faculties.append(
        models.Faculty(
            name='Facultad Experimental de Ciencias y Tecnologías',
            acronym='FACYT',
            id_institution = 1
        )  
    )
    for faculty in faculties:
        db.add(faculty)
        db.commit()


def create_careers(db: Session):
    careers = []
    careers.append(
        models.Career(
            name='Computación',
            id_faculty= 1
        )  
    )
    careers.append(
        models.Career(
            name='Química',
            id_faculty= 1
        )  
    )
    careers.append(
        models.Career(
            name='Física',
            id_faculty= 1
        )  
    )
    careers.append(
        models.Career(
            name='Matemática',
            id_faculty= 1
        )  
    )
    careers.append(
        models.Career(
            name='Biología',
            id_faculty= 1
        )  
    )
    for career in careers:
        db.add(career)
        db.commit()