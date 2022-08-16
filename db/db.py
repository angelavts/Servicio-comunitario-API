from db.session import SessionLocal


def get_db():
    """
    Retornar la instancia de una sesión
    """
    db = SessionLocal()
    return db