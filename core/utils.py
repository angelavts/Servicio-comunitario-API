import openpyxl
import pandas as pd
from pydantic import BaseModel
from os import path, getcwd
from core.config import settings 
from fastapi import HTTPException, File

def is_valid_file(filename: str):
    file_extension = path.splitext(filename)[-1]
    return file_extension in settings.VALID_FILE_EXTENSIONS


def get_upload_path(filename: str):
    upload_folder = path.join(settings.ROOT_DIR, settings.UPLOAD_FOLDER)
    file_path = path.join(settings.UPLOAD_PATH, filename)
    return file_path

def get_schema_list_from_file(file_path: str, schema: BaseModel, correct_columns: list):
    # To open Workbook
    df = pd.read_excel(file_path)
    #  revisar si las columnas tienen el formato correcto
    if not is_correct_header(df.columns, correct_columns):
        raise HTTPException(status_code=400, detail="Invalid table format")
    else:
        schema_list = []
        df = df.to_numpy().tolist()
        for i in range(len(df)):
            schema_list.append(schema(df[i]))
    return schema_list

    

def is_correct_header(current_columns: list, correct_columns:list):
    is_correct = False
    if len(current_columns) == len(correct_columns):
        is_correct = True
        for i in range(len(current_columns)):
            if current_columns[i].lower() != correct_columns[i].lower():
                is_correct = False
                break
    return is_correct



