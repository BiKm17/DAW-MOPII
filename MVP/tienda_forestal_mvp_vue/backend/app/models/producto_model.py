"""
producto_model.py
=================
Capa MODELO del patrón MVP.

Responsabilidad:
- Conectarse a la base de datos MySQL
- Ejecutar consultas SQL
- Devolver datos en estructuras Python (listas/dict)

❌ No sabe nada de Flask
❌ No sabe nada de Vue
❌ No sabe nada de Presenters
"""

import os
import mysql.connector


def obtener_conexion():
    """
    Crea y devuelve una conexión a MySQL usando
    variables de entorno (definidas en docker-compose.yml)
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


def obtener_productos_filtrados(
    termino=None,
    tipo=None,
    marca=None,
    precio_min=None,
    precio_max=None,
    pagina=1,
    por_pagina=10,
    ordenar=None
):
    """
    Devuelve productos aplicando filtros, búsqueda y paginación.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    condiciones = []
    parametros = []

    # -------------------------
    # BÚSQUEDA GENERAL
    # -------------------------
    if termino:
        condiciones.append(
            "(nombre LIKE %s OR descripcion LIKE %s OR marca LIKE %s)"
        )
        like = f"%{termino}%"
        parametros.extend([like, like, like])

    # -------------------------
    # FILTROS ESPECÍFICOS
    # -------------------------
    if tipo:
        condiciones.append("tipo = %s")
        parametros.append(tipo)

    if marca:
        condiciones.append("marca = %s")
        parametros.append(marca)

    if precio_min is not None:
        condiciones.append("precio >= %s")
        parametros.append(precio_min)

    if precio_max is not None:
        condiciones.append("precio <= %s")
        parametros.append(precio_max)

    where_clause = ""
    if condiciones:
        where_clause = "WHERE " + " AND ".join(condiciones)

    # -------------------------
    # ORDENACIÓN
    # -------------------------
    order_clause = ""
    if ordenar == "asc":
        order_clause = "ORDER BY precio ASC"
    elif ordenar == "desc":
        order_clause = "ORDER BY precio DESC"

    # -------------------------
    # PAGINACIÓN
    # -------------------------
    offset = (pagina - 1) * por_pagina

    query = f"""
        SELECT *
        FROM productos
        {where_clause}
        {order_clause}
        LIMIT %s OFFSET %s
    """

    parametros.extend([por_pagina, offset])

    cursor.execute(query, parametros)
    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return productos


def contar_productos_filtrados(
    termino=None,
    tipo=None,
    marca=None,
    precio_min=None,
    precio_max=None
):
    """
    Devuelve el total de productos que cumplen los filtros.
    Necesario para calcular paginación.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    condiciones = []
    parametros = []

    if termino:
        condiciones.append(
            "(nombre LIKE %s OR descripcion LIKE %s OR marca LIKE %s)"
        )
        like = f"%{termino}%"
        parametros.extend([like, like, like])

    if tipo:
        condiciones.append("tipo = %s")
        parametros.append(tipo)

    if marca:
        condiciones.append("marca = %s")
        parametros.append(marca)

    if precio_min is not None:
        condiciones.append("precio >= %s")
        parametros.append(precio_min)

    if precio_max is not None:
        condiciones.append("precio <= %s")
        parametros.append(precio_max)

    where_clause = ""
    if condiciones:
        where_clause = "WHERE " + " AND ".join(condiciones)

    query = f"""
        SELECT COUNT(*) 
        FROM productos
        {where_clause}
    """

    cursor.execute(query, parametros)
    total = cursor.fetchone()[0]

    cursor.close()
    conexion.close()

    return total
