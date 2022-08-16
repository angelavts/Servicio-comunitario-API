from strenum import StrEnum


class Status(StrEnum):
    PENDING = 'Pendiente',    # notice the trailing comma
    IN_PROGRESS = 'En progreso', 
    COMPLETED = 'Completada',
    INACTIVE = 'Inactiva'
