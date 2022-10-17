Para que la aplicación funcione correctamente, se recomienda la versión de python 3.8.5
Tambien se necesita tener instalado postgresql

1 - Crear un entorno virtual de python (preferiblemente fuera de la carpeta raiz del proyecto)

- python -m venv nombre_entorno

2 - Activar el entorno virtual creado 

 - C:\>c:\ruta\al\entorno\virtual\scripts\activate.bat

3 - Instalar los requerimientos:

- pip install -r requirements.txt 
- En caso de que en el desarrollo se agregue otro paquete, volver a generar los requerimientos: pip freeze > app/requirements.txt

4 - Configurar el archivo .env con el puerto y datos de la base de datos postgres que se usará

5 - Correr la aplicación ejecutando el archivo main.py

- (Estando en la carpeta raiz) python main.py


