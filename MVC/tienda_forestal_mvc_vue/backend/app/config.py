"""
Archivo de configuración de la aplicación Flask.
Define los parámetros de conexión a la base de datos.
"""

import os

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'db')
    MYSQL_USER = os.getenv('MYSQL_USER', 'mopii')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'daw')
    MYSQL_DB = os.getenv('MYSQL_DB', 'tienda_forestal')
    MYSQL_CHARSET = 'utf8mb4'

