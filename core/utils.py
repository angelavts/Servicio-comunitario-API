import openpyxl
import pandas as pd
from pydantic import BaseModel
from os import path, getcwd
from core.config import settings 
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
    #  revisar si las columnas tienen el formato correcto
    if not is_correct_header(df.columns, correct_columns):
        raise HTTPException(status_code=400, detail="Invalid table format")
    else:
        schema_list = []
        df = df.to_numpy().tolist()
        for i in range(len(df)):
            schema_list.append(row_to_schema(df[i]))
    return schema_list

    
def is_correct_header(current_columns: list, correct_columns:list):
    """
        Verifica que dos listas tengan los mismos nombres de columnas
    """
    is_correct = False
    if len(current_columns) == len(correct_columns):
        is_correct = True
        for i in range(len(current_columns)):
            if normalize(current_columns[i]) != normalize(correct_columns[i]):
                is_correct = False
                break
    return is_correct

def normalize(word: str):
    """
        Convierte todos los caracteres de una cadena en minúsculas y quita los espacios
    """
    return word.lower().strip()

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
    id_parts = identification.split('-')
    if id_parts[0].upper() == 'V' or id_parts[0].upper() == 'E':
        if id_parts[1].replace('.', '').isdigit():
            is_valid = True
    return is_valid
        




