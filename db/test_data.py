# Llenar la base de datos con datos iniciales de prueba
from db import db_models as models 
from sqlalchemy.orm import Session
from db.db import get_db
from datetime import datetime

# crear una sesión global para este script
db = get_db()



students_json = [
    {
        'identification' : 'V-26000001',
        'first_name' : 'Nombre Estudiante 1',
        'last_name' : 'Apellido Estudiante 1',    
        'career_id' : 1,  
        'role' : 'Estudiante',
        'id' : 1
    },
    {
        'identification' : 'V-26000002',
        'first_name' : 'Nombre Estudiante 2',
        'last_name' : 'Apellido Estudiante 2',    
        'career_id' : 3,
        'role' : 'Estudiante',
        'id' : 2
    },
    {
        'identification' : 'V-26000003',
        'first_name' : 'Nombre Estudiante 3',
        'last_name' : 'Apellido Estudiante 3',    
        'career_id' : 5,
        'role' : 'Estudiante',
        'id' : 3
    },
    {
        'identification' : 'V-26000004',
        'first_name' : 'Nombre Estudiante 4',
        'last_name' : 'Apellido Estudiante 4',    
        'career_id' : 1,
        'role' : 'Estudiante',
        'id' : 4
    },
    {
        'identification' : 'V-26000005',
        'first_name' : 'Nombre Estudiante 5',
        'last_name' : 'Apellido Estudiante 5',    
        'career_id' : 4,
        'role' : 'Estudiante',
        'id' : 5
    },
    {
        'identification' : 'V-26000006',
        'first_name' : 'Nombre Estudiante 6',
        'last_name' : 'Apellido Estudiante 6',    
        'career_id' : 2,
        'role' : 'Estudiante',
        'id' : 6
    },
    {
        'identification' : 'V-26000007',
        'first_name' : 'Nombre Estudiante 7',
        'last_name' : 'Apellido Estudiante 7',    
        'career_id' : 3,
        'role' : 'Estudiante',
        'id' : 7
    },
    {
        'identification' : 'V-26000008',
        'first_name' : 'Nombre Estudiante 8',
        'last_name' : 'Apellido Estudiante 8',    
        'career_id' : 1,
        'role' : 'Estudiante',
        'id' : 8
    },
    {
        'identification' : 'V-26000009',
        'first_name' : 'Nombre Estudiante 9',
        'last_name' : 'Apellido Estudiante 9',    
        'career_id' : 2,
        'role' : 'Estudiante',
        'id' : 9
    },
    {
        'identification' : 'V-26000010',
        'first_name' : 'Nombre Estudiante 10',
        'last_name' : 'Apellido Estudiante 10',    
        'career_id' : 4,
        'role' : 'Estudiante',
        'id' : 10
    },
    {
        'identification' : 'V-26000011',
        'first_name' : 'Nombre Estudiante 11',
        'last_name' : 'Apellido Estudiante 11',    
        'career_id' : 5,
        'role' : 'Estudiante',
        'id' : 11
    },
    {
        'identification' : 'V-26000012',
        'first_name' : 'Nombre Estudiante 12',
        'last_name' : 'Apellido Estudiante 12',    
        'career_id' : 1,
        'role' : 'Estudiante',
        'id' : 12
    },
    {
        'identification' : 'V-26000013',
        'first_name' : 'Nombre Estudiante 13',
        'last_name' : 'Apellido Estudiante 13',    
        'career_id' : 4,
        'role' : 'Estudiante',
        'id' : 13
    },
    {
        'identification' : 'V-26000014',
        'first_name' : 'Nombre Estudiante 14',
        'last_name' : 'Apellido Estudiante 14',    
        'career_id' : 3,
        'role' : 'Estudiante',
        'id' : 14
    },
    {
        'identification' : 'V-26000015',
        'first_name' : 'Nombre Estudiante 15',
        'last_name' : 'Apellido Estudiante 15',    
        'career_id' : 2,
        'role' : 'Estudiante',
        'id' : 15
    },
    {
        'identification' : 'V-26000016',
        'first_name' : 'Nombre Estudiante 16',
        'last_name' : 'Apellido Estudiante 16',    
        'career_id' : 5,
        'role' : 'Estudiante',
        'id' : 16
    },
    {
        'identification' : 'V-26000017',
        'first_name' : 'Nombre Estudiante 17',
        'last_name' : 'Apellido Estudiante 17',    
        'career_id' : 1,
        'role' : 'Estudiante',
        'id' : 17
    },
    {
        'identification' : 'V-26000018',
        'first_name' : 'Nombre Estudiante 18',
        'last_name' : 'Apellido Estudiante 18',    
        'career_id' : 4,
        'role' : 'Estudiante',
        'id' : 18
    },
    {
        'identification' : 'V-26000019',
        'first_name' : 'Nombre Estudiante 19',
        'last_name' : 'Apellido Estudiante 19',    
        'career_id' : 3,
        'role' : 'Estudiante',
        'id' : 19
    },
    {
        'identification' : 'V-26000020',
        'first_name' : 'Nombre Estudiante 20',
        'last_name' : 'Apellido Estudiante 20',    
        'career_id' : 1,
        'role' : 'Estudiante',
        'id' : 20
    }
]

tutors_json = [
    {
        'identification' : 'V-15000001',
        'first_name' : 'Nombre Tutor 1',
        'last_name' : 'Apellido Tutor 1',    
        'career_id' : 1,
        'role' : 'Tutor',
        'id' : 21
    },
    {
        'identification' : 'V-15000002',
        'first_name' : 'Nombre Tutor 2',
        'last_name' : 'Apellido Tutor 2',    
        'career_id' : 3,
        'role' : 'Tutor',
        'id' : 22
    },
    {
        'identification' : 'V-15000003',
        'first_name' : 'Nombre Tutor 3',
        'last_name' : 'Apellido Tutor 3',    
        'career_id' : 2,
        'role' : 'Tutor',
        'id' : 23
    },
    {
        'identification' : 'V-15000004',
        'first_name' : 'Nombre Tutor 4',
        'last_name' : 'Apellido Tutor 4',    
        'career_id' : 5,
        'role' : 'Tutor',
        'id' : 24
    },
    {
        'identification' : 'V-15000005',
        'first_name' : 'Nombre Tutor 5',
        'last_name' : 'Apellido Tutor 5',    
        'career_id' : 4,
        'role' : 'Tutor',
        'id' : 25
    },
    {
        'identification' : 'V-15000006',
        'first_name' : 'Nombre Tutor 6',
        'last_name' : 'Apellido Tutor 6',    
        'career_id' : 3,
        'role' : 'Tutor',
        'id' : 26
    },
    {
        'identification' : 'V-15000007',
        'first_name' : 'Nombre Tutor 7',
        'last_name' : 'Apellido Tutor 7',    
        'career_id' : 1,
        'role' : 'Tutor',
        'id' : 27
    },
    {
        'identification' : 'V-15000008',
        'first_name' : 'Nombre Tutor 8',
        'last_name' : 'Apellido Tutor 8',    
        'career_id' : 2,
        'role' : 'Tutor',
        'id' : 28
    },
    {
        'identification' : 'V-15000009',
        'first_name' : 'Nombre Tutor 9',
        'last_name' : 'Apellido Tutor 9',    
        'career_id' : 4,
        'role' : 'Tutor',
        'id' : 29
    },
    {
        'identification' : 'V-15000010',
        'first_name' : 'Nombre Tutor 10',
        'last_name' : 'Apellido Tutor 10',    
        'career_id' : 5,
        'role' : 'Tutor',
        'id' : 30
    },
    
]

coordinators_json = [
    {
        'identification' : 'V-12000001',
        'first_name' : 'Nombre Coord 1',
        'last_name' : 'Nombre Coord 1',    
        'career_id' : 2,
        'role' : 'Comunidad',
        'id' : 31
    },
    {
        'identification' : 'V-12000002',
        'first_name' : 'Nombre Coord 2',
        'last_name' : 'Apellido Coord 2',    
        'career_id' : 5,
        'role' : 'Comunidad',
        'id' : 32
    },
    {
        'identification' : 'V-12000003',
        'first_name' : 'Nombre Coord 3',
        'last_name' : 'Apellido Coord 3',    
        'career_id' : 3,
        'role' : 'Comunidad',
        'id' : 33
    },
    {
        'identification' : 'V-12000004',
        'first_name' : 'Nombre Coord 4',
        'last_name' : 'Apellido Coord 4',    
        'career_id' : 1,
        'role' : 'Comunidad',
        'id' : 34
    },
    {
        'identification' : 'V-12000005',
        'first_name' : 'Nombre Coord 5',
        'last_name' : 'Apellido Coord 5',    
        'career_id' : 4,
        'role' : 'Comunidad',
        'id' : 35
    },

]

projects_json = [
    {
        'name' : 'Proyecto 1',
        'description' : 'Descripción proyecto 1',   
        'coordinator_id' : 34,
        'career_id' : 1
    },
    {
        'name' : 'Proyecto 2',
        'description' : 'Descripción proyecto 2', 
        'coordinator_id' : 31,
        'career_id' : 2
    },
    {
        'name' : 'Proyecto 3',
        'description' : 'Descripción proyecto 3', 
        'coordinator_id' : 33,
        'career_id' : 3
    },
    {
        'name' : 'Proyecto 4',
        'description' : 'Descripción proyecto 4', 
        'coordinator_id' : 35,
        'career_id' : 4
    },
    {
        'name' : 'Proyecto 5',
        'description' : 'Descripción proyecto 5', 
        'coordinator_id' : 32,
        'career_id' : 5
    },
    {
        'name' : 'Proyecto 6',
        'description' : 'Descripción proyecto 6', 
        'coordinator_id' : 33,
        'career_id' : 3
    }  
]

inactive_projects_json = [
    {
        'name' : 'Proyecto 7',
        'description' : 'Descripción proyecto 7',   
        'coordinator_id' : 34,
        'career_id' : 1,
        'date_end': datetime.now()
    },
    {
        'name' : 'Proyecto 8',
        'description' : 'Descripción proyecto 8', 
        'coordinator_id' : 31,
        'career_id' : 2,
        'date_end': datetime.now()
    },
    {
        'name' : 'Proyecto 9',
        'description' : 'Descripción proyecto 9', 
        'coordinator_id' : 33,
        'career_id' : 3,
        'date_end': datetime.now()
    },

]

tasks_json = [
    {
        'name' : 'Tarea 1',
        'description' : 'Descripción tarea 1',   
        'cost' : 2,
        'status' : 'Pendiente', # ('Pendiente','En progreso', 'Completada', 'Inactiva')
        'student_id' : 1, # ID's del 1 al 20
        'project_id' : 6,
        'tutor_id' : 22 # ID's del 21 al 30
    },
    {
        'name' : 'Tarea 2',
        'description' : 'Descripción tarea 2',   
        'cost' : 5,
        'status' : 'Pendiente',
        'student_id' : 1,
        'project_id' : 6,
        'tutor_id' : 22
    },
    {
        'name' : 'Tarea 3',
        'description' : 'Descripción tarea 3',   
        'cost' : 3,
        'status' : 'Inactiva',
        'student_id' : 1,
        'project_id' : 6,
        'tutor_id' : 22
    },
    {
        'name' : 'Tarea 4',
        'description' : 'Descripción tarea 4',   
        'cost' : 1,
        'status' : 'En progreso',
        'student_id' : 2,
        'project_id' : 3,
        'tutor_id' : 25
    },
    {
        'name' : 'Tarea 5',
        'description' : 'Descripción tarea 5',   
        'cost' : 9,
        'status' : 'Pendiente',
        'student_id' : 2,
        'project_id' : 3,
        'tutor_id' : 25
    },
    {
        'name' : 'Tarea 6',
        'description' : 'Descripción tarea 6',   
        'cost' : 12,
        'status' : 'Completada',
        'student_id' : 2,
        'project_id' : 3,
        'tutor_id' : 25
    },
    {
        'name' : 'Tarea 7',
        'description' : 'Descripción tarea 7',   
        'cost' : 20,
        'status' : 'Pendiente',
        'student_id' : 3,
        'project_id' : 1,
        'tutor_id' : None
    },
    {
        'name' : 'Tarea 8',
        'description' : 'Descripción tarea 8',   
        'cost' : 13,
        'status' : 'Inactiva',
        'student_id' : 3,
        'project_id' : 1,
        'tutor_id' : 30
    },
    {
        'name' : 'Tarea 9',
        'description' : 'Descripción tarea 9',   
        'cost' : 15,
        'status' : 'En progreso',
        'student_id' : 3,
        'project_id' : 1,
        'tutor_id' : 30
    },
    {
        'name' : 'Tarea 10',
        'description' : 'Descripción tarea 10',   
        'cost' : 12,
        'status' : 'Pendiente',
        'student_id' : 4,
        'project_id' : 5,
        'tutor_id' : 28
    },
    {
        'name' : 'Tarea 11',
        'description' : 'Descripción tarea 11',   
        'cost' : 4,
        'status' : 'Pendiente',
        'student_id' : 4,
        'project_id' : 5,
        'tutor_id' : 28
    },
    {
        'name' : 'Tarea 12',
        'description' : 'Descripción tarea 12',   
        'cost' : 6,
        'status' : 'Completada',
        'student_id' : 4,
        'project_id' : 5,
        'tutor_id' : 28
    },
    {
        'name' : 'Tarea 13',
        'description' : 'Descripción tarea 13',   
        'cost' : 8,
        'status' : 'Pendiente',
        'student_id' : 5,
        'project_id' : 3,
        'tutor_id' : 26
    },
    {
        'name' : 'Tarea 14',
        'description' : 'Descripción tarea 14',   
        'cost' : 2,
        'status' : 'Inactiva',
        'student_id' : 5,
        'project_id' : 3,
        'tutor_id' : 26
    },
    {
        'name' : 'Tarea 15',
        'description' : 'Descripción tarea 15',   
        'cost' : 3,
        'status' : 'En progreso',
        'student_id' : 5,
        'project_id' : 3,
        'tutor_id' : 26
    },
    {
        'name' : 'Tarea 16',
        'description' : 'Descripción tarea 16',   
        'cost' : 7,
        'status' : 'En progreso',
        'student_id' : 6,
        'project_id' : 4,
        'tutor_id' : 23
    },
    {
        'name' : 'Tarea 17',
        'description' : 'Descripción tarea 17',   
        'cost' : 14,
        'status' : 'Completada',
        'student_id' : 6,
        'project_id' : 4,
        'tutor_id' : 23
    },
    {
        'name' : 'Tarea 18',
        'description' : 'Descripción tarea 18',   
        'cost' : 17,
        'status' : 'En progreso',
        'student_id' : 6,
        'project_id' : 4,
        'tutor_id' : 23
    },
    {
        'name' : 'Tarea 19',
        'description' : 'Descripción tarea 19',   
        'cost' : 12,
        'status' : 'En progreso',
        'student_id' : 7,
        'project_id' : 1,
        'tutor_id' : 25
    },
    {
        'name' : 'Tarea 20',
        'description' : 'Descripción tarea 20',   
        'cost' : 8,
        'status' : 'En progreso',
        'student_id' : 7,
        'project_id' : 1,
        'tutor_id' : 25
    },
    {
        'name' : 'Tarea 21',
        'description' : 'Descripción tarea 21',   
        'cost' : 5,
        'status' : 'Inactiva',
        'student_id' : 7,
        'project_id' : 1,
        'tutor_id' : 25
    },
    {
        'name' : 'Tarea 22',
        'description' : 'Descripción tarea 22',   
        'cost' : 6,
        'status' : 'En progreso',
        'student_id' : 8,
        'project_id' : 3,
        'tutor_id' : 29
    },
    {
        'name' : 'Tarea 23',
        'description' : 'Descripción tarea 23',   
        'cost' : 1,
        'status' : 'Pendiente',
        'student_id' : 8,
        'project_id' : 3,
        'tutor_id' : 29
    },
    {
        'name' : 'Tarea 24',
        'description' : 'Descripción tarea 24',   
        'cost' : 19,
        'status' : 'Inactiva',
        'student_id' : 8,
        'project_id' : 3,
        'tutor_id' : 29
    },
    {
        'name' : 'Tarea 25',
        'description' : 'Descripción tarea 25',   
        'cost' : 20,
        'status' : 'En progreso',
        'student_id' : 9,
        'project_id' : 2,
        'tutor_id' : 26
    },
    {
        'name' : 'Tarea 26',
        'description' : 'Descripción tarea 26',   
        'cost' : 2,
        'status' : 'Completada',
        'student_id' : 9,
        'project_id' : 2,
        'tutor_id' : 26
    },
    {
        'name' : 'Tarea 27',
        'description' : 'Descripción tarea 27',   
        'cost' : 13,
        'status' : 'En progreso',
        'student_id' : 9,
        'project_id' : 2,
        'tutor_id' : 26
    },
    {
        'name' : 'Tarea 28',
        'description' : 'Descripción tarea 28',   
        'cost' : 11,
        'status' : 'Pendiente',
        'student_id' : 10,
        'project_id' : 5,
        'tutor_id' : 24
    },
    {
        'name' : 'Tarea 29',
        'description' : 'Descripción tarea 29',   
        'cost' : 7,
        'status' : 'En progreso',
        'student_id' : 10,
        'project_id' : 5,
        'tutor_id' : 24
    },
    {
        'name' : 'Tarea 30',
        'description' : 'Descripción tarea 30',   
        'cost' : 3,
        'status' : 'Completada',
        'student_id' : 10,
        'project_id' : 5,
        'tutor_id' : 24
    },
    {
        'name' : 'Tarea 31',
        'description' : 'Descripción tarea 31',   
        'cost' : 7,
        'status' : 'En progreso',
        'student_id' : 11,
        'project_id' : 6,
        'tutor_id' : 22
    },
    {
        'name' : 'Tarea 32',
        'description' : 'Descripción tarea 32',   
        'cost' : 10,
        'status' : 'Completada',
        'student_id' : 11,
        'project_id' : 6,
        'tutor_id' : 22
    },
    {
        'name' : 'Tarea 33',
        'description' : 'Descripción tarea 33',   
        'cost' : 15,
        'status' : 'Pendiente',
        'student_id' : 11,
        'project_id' : 6,
        'tutor_id' : 22
    },
    {
        'name' : 'Tarea 34',
        'description' : 'Descripción tarea 34',   
        'cost' : 4,
        'status' : 'En progreso',
        'student_id' : 12,
        'project_id' : 1,
        'tutor_id' : 30
    },
    {
        'name' : 'Tarea 35',
        'description' : 'Descripción tarea 35',   
        'cost' : 9,
        'status' : 'En progreso',
        'student_id' : 12,
        'project_id' : 1,
        'tutor_id' : 30
    },
    {
        'name' : 'Tarea 36',
        'description' : 'Descripción tarea 36',   
        'cost' : 13,
        'status' : 'Completada',
        'student_id' : 12,
        'project_id' : 1,
        'tutor_id' : 30
    },
    {
        'name' : 'Tarea 37',
        'description' : 'Descripción tarea 37',   
        'cost' : 20,
        'status' : 'Pendiente',
        'student_id' : 13,
        'project_id' : 4,
        'tutor_id' : 21
    },
    {
        'name' : 'Tarea 38',
        'description' : 'Descripción tarea 38',   
        'cost' : 5,
        'status' : 'En progreso',
        'student_id' : 13,
        'project_id' : 4,
        'tutor_id' : 21
    },
    {
        'name' : 'Tarea 39',
        'description' : 'Descripción tarea 39',   
        'cost' : 3,
        'status' : 'Inactiva',
        'student_id' : 13,
        'project_id' : 4,
        'tutor_id' : 21
    },
    {
        'name' : 'Tarea 40',
        'description' : 'Descripción tarea 40',   
        'cost' : 2,
        'status' : 'En progreso',
        'student_id' : 14,
        'project_id' : 2,
        'tutor_id' : 24
    },
    {
        'name' : 'Tarea 41',
        'description' : 'Descripción tarea 41',   
        'cost' : 8,
        'status' : 'Completada',
        'student_id' : 14,
        'project_id' : 2,
        'tutor_id' : 24
    },
    {
        'name' : 'Tarea 42',
        'description' : 'Descripción tarea 42',   
        'cost' : 17,
        'status' : 'En progreso',
        'student_id' : 14,
        'project_id' : 2,
        'tutor_id' : 24
    },
    {
        'name' : 'Tarea 43',
        'description' : 'Descripción tarea 43',   
        'cost' : 15,
        'status' : 'Pendiente',
        'student_id' : 15,
        'project_id' : 5,
        'tutor_id' : 21
    },
    {
        'name' : 'Tarea 44',
        'description' : 'Descripción tarea 44',   
        'cost' : 10,
        'status' : 'Pendiente',
        'student_id' : 15,
        'project_id' : 5,
        'tutor_id' : 21
    },
    {
        'name' : 'Tarea 45',
        'description' : 'Descripción tarea 45',   
        'cost' : 1,
        'status' : 'Inactiva',
        'student_id' : 15,
        'project_id' : 5,
        'tutor_id' : 21
    },
    {
        'name' : 'Tarea 46',
        'description' : 'Descripción tarea 46',   
        'cost' : 2,
        'status' : 'Pendiente',
        'student_id' : 16,
        'project_id' : 3,
        'tutor_id' : 22
    },
    {
        'name' : 'Tarea 47',
        'description' : 'Descripción tarea 47',   
        'cost' : 5,
        'status' : 'Completada',
        'student_id' : 16,
        'project_id' : 3,
        'tutor_id' : 22
    },
    {
        'name' : 'Tarea 48',
        'description' : 'Descripción tarea 48',   
        'cost' : 3,
        'status' : 'En progreso',
        'student_id' : 16,
        'project_id' : 3,
        'tutor_id' : 22
    },
    {
        'name' : 'Tarea 49',
        'description' : 'Descripción tarea 49',   
        'cost' : 19,
        'status' : 'Completada',
        'student_id' : 17,
        'project_id' : 6,
        'tutor_id' : 29
    },
    {
        'name' : 'Tarea 50',
        'description' : 'Descripción tarea 50',   
        'cost' : 11,
        'status' : 'En progreso',
        'student_id' : 17,
        'project_id' : 6,
        'tutor_id' : 29
    },
    {
        'name' : 'Tarea 51',
        'description' : 'Descripción tarea 51',   
        'cost' : 2,
        'status' : 'Pendiente',
        'student_id' : 17,
        'project_id' : 6,
        'tutor_id' : 29
    },
    {
        'name' : 'Tarea 52',
        'description' : 'Descripción tarea 52',   
        'cost' : 4,
        'status' : 'Pendiente',
        'student_id' : 18,
        'project_id' : 4,
        'tutor_id' : 21
    },
    {
        'name' : 'Tarea 53',
        'description' : 'Descripción tarea 53',   
        'cost' : 7,
        'status' : 'En progreso',
        'student_id' : 18,
        'project_id' : 4,
        'tutor_id' : 21
    },
    {
        'name' : 'Tarea 54',
        'description' : 'Descripción tarea 54',   
        'cost' : 18,
        'status' : 'Inactiva',
        'student_id' : 18,
        'project_id' : 4,
        'tutor_id' : 21
    },
    {
        'name' : 'Tarea 55',
        'description' : 'Descripción tarea 55',   
        'cost' : 12,
        'status' : 'En progreso',
        'student_id' : 19,
        'project_id' : 1,
        'tutor_id' : 25
    },
    {
        'name' : 'Tarea 56',
        'description' : 'Descripción tarea 56',   
        'cost' : 2,
        'status' : 'En progreso',
        'student_id' : 19,
        'project_id' : 1,
        'tutor_id' : 25
    },
    {
        'name' : 'Tarea 57',
        'description' : 'Descripción tarea 57',   
        'cost' : 8,
        'status' : 'Completada',
        'student_id' : 19,
        'project_id' : 1,
        'tutor_id' : 25
    },
    {
        'name' : 'Tarea 58',
        'description' : 'Descripción tarea 58',   
        'cost' : 10,
        'status' : 'En progreso',
        'student_id' : 20,
        'project_id' : 5,
        'tutor_id' : 27
    },
    {
        'name' : 'Tarea 59',
        'description' : 'Descripción tarea 59',   
        'cost' : 5,
        'status' : 'Inactiva',
        'student_id' : 20,
        'project_id' : 5,
        'tutor_id' : 27
    },
    {
        'name' : 'Tarea 60',
        'description' : 'Descripción tarea 60',   
        'cost' : 18,
        'status' : 'Pendiente',
        'student_id' : 20,
        'project_id' : 5,
        'tutor_id' : 27
    },

]

project_student_json = [
    {
        'project_id' : 6,
        'student_id' : 3,  
        'active': False

    },
    {
        'project_id' : 3,
        'student_id' : 3,  
        'active': True

    },
    {
        'project_id' : 3,
        'student_id' : 2,  
        'active': False
    },
    {
        'project_id' : 1,
        'student_id' : 3,  
        'active': False
    },
    {
        'project_id' : 5,
        'student_id' : 4,  
        'active': True
    },
    {
        'project_id' : 3,
        'student_id' : 5,  
        'active': True
    },
    {
        'project_id' : 4,
        'student_id' : 6,  
        'active': True
    },
    {
        'project_id' : 1,
        'student_id' : 7,  
        'active': True
    },
    {
        'project_id' : 3,
        'student_id' : 8,  
        'active': True
    },
    {
        'project_id' : 2,
        'student_id' : 9,  
        'active': True
    },
    {
        'project_id' : 5,
        'student_id' : 10,  
        'active': True
    },
    {
        'project_id' : 6,
        'student_id' : 11,  
        'active': True
    },
    {
        'project_id' : 1,
        'student_id' : 12,  
        'active': True
    },
    {
        'project_id' : 4,
        'student_id' : 13,  
        'active': True
    },
    {
        'project_id' : 2,
        'student_id' : 14,  
        'active': True
    },
    {
        'project_id' : 5,
        'student_id' : 15,  
        'active': True
    },
    {
        'project_id' : 3,
        'student_id' : 16,  
        'active': True
    },
    {
        'project_id' : 6,
        'student_id' : 17,  
        'active': True
    },
    {
        'project_id' : 4,
        'student_id' : 18,  
        'active': True
    },
    {
        'project_id' : 1,
        'student_id' : 19,  
        'active': True
    },
    {
        'project_id' : 5,
        'student_id' : 20,  
        'active': True
    },

]



def populate_students():
    for student in students_json:
        new_student = models.User(
            identification=student['identification'],
            first_name=student['first_name'],
            last_name=student['last_name'],            
            role = 'Estudiante',
            career_id = student['career_id']
        )  
        try:
            db.add(new_student)
            db.commit()        
        except Exception as e:
            print(e)
            db.rollback()


def populate_tutors():
    for tutor in tutors_json:
        new_tutor = models.User(
            identification=tutor['identification'],
            first_name=tutor['first_name'],
            last_name=tutor['last_name'],            
            role = 'Tutor',
            career_id = tutor['career_id']
        )  
        try:
            db.add(new_tutor)
            db.commit()        
        except Exception as e:
            db.rollback()

def populate_coordinators():
    for coordinator in coordinators_json:
        new_coordinator = models.User(
            identification=coordinator['identification'],
            first_name=coordinator['first_name'],
            last_name=coordinator['last_name'],            
            role = 'Comunidad',
            career_id = coordinator['career_id']
        )  
        try:
            db.add(new_coordinator)
            db.commit()        
        except Exception as e:
            db.rollback()


def populate_projects():
    for project in projects_json:
        new_project = models.Project(
            name=project['name'],
            description=project['description'],
            coordinator_id=project['coordinator_id'],            
            career_id = project['career_id']
        )  
        try:
            db.add(new_project)
            db.commit()        
        except Exception as e:
            db.rollback()

def populate_inactive_projects():
    for project in inactive_projects_json:
        new_project = models.Project(
            name=project['name'],
            description=project['description'],
            coordinator_id=project['coordinator_id'],            
            career_id = project['career_id'],
            date_end = project['date_end'],
            status = 'Inactivo'
        )  
        try:
            db.add(new_project)
            db.commit()        
        except Exception as e:
            db.rollback()

def populate_projects_students():
    for project_student in project_student_json:
        new_project_student = models.ProjectStudent(
            project_id=project_student['project_id'],            
            student_id = project_student['student_id'],
            active = project_student['active']
        )  
        try:
            db.add(new_project_student)
            db.commit()        
        except Exception as e:
            db.rollback()

def populate_tasks():
    for task in tasks_json:
        new_task = models.Task(
            name=task['name'],            
            description = task['description'],
            cost = task['cost'],
            status = task['status'],
            student_id = task['student_id'],
            project_id = task['project_id'],
            tutor_id = task['tutor_id']
        )  
        try:
            db.add(new_task)
            db.commit()        
        except Exception as e:
            db.rollback()


def populate_db():
    populate_students()
    populate_tutors()
    populate_coordinators()
    populate_projects()
    populate_inactive_projects()
    populate_projects_students()
    populate_tasks()


