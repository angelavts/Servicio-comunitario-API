# -----------------------------------------------------------------------
# Registrar un estudiante: users/create_student
# Registrar un tutor: users/create_tutor
# -----------------------------------------------------------------------
create_student_request = {
    "identification": "string",
    "first_name": "string",
    "last_name": "string",
    "career": "string"
}
create_student_response_body_success = {
    "status_code": 200,
    "detail": "User created successfully"
}

create_student_response_body_fail_1 = {
    "status_code": 400,
    "detail": "User already exists"
}
create_student_response_body_fail_2 = {
    "status_code": 500,
    "detail": "Internal server error" 
}

# -----------------------------------------------------------------------
# Registrar varios estudiantes: users/create_students
# Registrar varios tutores: users/create_tutors
# -----------------------------------------------------------------------
create_students_request = [
    {
        "identification": "string",
        "first_name": "string",
        "last_name": "string",
        "career": "string"
    },
    {
        "identification": "string",
        "first_name": "string",
        "last_name": "string",
        "career": "string"
    }
]
create_students_response_body_success = {
    "status_code": 200,
    "successful": [
        {
            "identification": "string",
            "first_name": "string",
            "last_name": "string",
            "career": "string"
        },
        {
            "identification": "string",
            "first_name": "string",
            "last_name": "string",
            "career": "string"
        }
    ]

    "failed": [
        {
            "identification": "string",
            "first_name": "string",
            "last_name": "string",
            "career": "string"
        },
        {
            "identification": "string",
            "first_name": "string",
            "last_name": "string",
            "career": "string"
        }
    ]
}

