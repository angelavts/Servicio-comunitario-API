import openpyxl
import pandas as pd
from pydantic import BaseModel
from os import path, getcwd
from core.config import settings 
from core.messages import messages
from fastapi import HTTPException, File
from typing import Callable

def is_valid_file(filename: str):
    """
        Verifica que la extensión de un archivo es correcta
    """
    file_extension = path.splitext(filename)[-1]
    return file_extension in settings.VALID_FILE_EXTENSIONS


def get_upload_path(filename: str):
    """
        Retorna la ruta completa de un archivo
    """
    upload_folder = path.join(settings.ROOT_DIR, settings.UPLOAD_FOLDER)
    file_path = path.join(settings.UPLOAD_PATH, filename)
    return file_path

def get_schema_list_from_file(file_path: str, row_to_schema: Callable, correct_columns: list):
    """
        Convierte un archivo excel con registros a una lista de Schemas
    """
    # To open Workbook
    df = pd.read_excel(file_path)
    # poner todos los elementos de la columna en mayusculas
    df.columns = list(map(normalize, df.columns))
    #  revisar si las columnas tienen el formato correcto
    if not is_correct_header(df.columns, correct_columns):
        raise HTTPException(status_code=400, detail=messages['invalid_document_format'])
    else:
        schema_list = []
        df = df[correct_columns].to_numpy().tolist()
        for i in range(len(df)):
            schema_list.append(row_to_schema(df[i]))
    return schema_list

    
def is_correct_header(current_columns: list, correct_columns:list):
    """
        Verifica que los items de la lista correcta existan dentro de la lista dada
    """
    is_correct = True
    for column in correct_columns:
        if column not in current_columns:
            is_correct = False
            break
    return is_correct

def normalize(word: str):
    """
        Convierte todos los caracteres de una cadena en mayúsculas y quita los espacios
    """
    return word.upper().strip()

def remove_accent_marks(word: str):
    """
        Quita todas las tildes de una cadena
    """
    word = (word.replace('á', 'a').replace('é', 'e').replace('í', 'i')
               .replace('ó', 'o').replace('ú', 'u'))
    return word

def is_valid_identication(identification: str):
    """
        Verifica que una cédula tenga el siguiente formato: V-0000000 o E-0000000
    """
    is_valid = False
    if len(identification) > 1:       
        id_parts = identification.split('-')
        if id_parts[0].upper() == 'V' or id_parts[0].upper() == 'E':
            if id_parts[1].replace('.', '').isdigit():
                is_valid = True
    return is_valid



def validate_and_convert_identication(identification: str):
    """
        Verifica que una cédula tenga el siguiente formato: V-0000000 o E-0000000
    """
    # quitar puntos, si los tiene
    new_identification = identification.replace('.', '').replace(' ', '').upper()  
    return_identification = None
    if len(new_identification) > 1:
        # Verificar que inicie con 'V' o 'E'
        if new_identification[0] == 'V' or  new_identification[0] == 'E':
            # Verificar que tenga '-' y continúe con una cadena de digitos
            if new_identification[1] == '-' and len(new_identification) > 2 and new_identification[2:].isdigit():
                return_identification = new_identification
            # No tiene '-', verificar que siga una cadena de números
            elif new_identification[1:].isdigit():
                # Agregar el '-'
                return_identification = new_identification[0] + '-' + new_identification[1:]
    return return_identification


   
        




