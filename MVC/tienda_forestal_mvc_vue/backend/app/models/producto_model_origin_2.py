"""
Capa de Modelo (Model) del patrón MVC.
Aquí se gestiona el acceso y manipulación de los datos en la base de datos MySQL.
Incluimos funciones de búsqueda, filtrado y paginación.
"""

import MySQLdb
import os
import math

# -----------------------------------------
# CONEXIÓN A BASE DE DATOS MySQL
# -----------------------------------------

def obtener_conexion():
    """
    Crea y devuelve una conexión a la base de datos usando las variables
    de entorno definidas en docker-compose.yml.
    """
    return MySQLdb.connect(
        host=os.getenv('MYSQL_HOST', 'db'),
        user=os.getenv('MYSQL_USER', 'mopii'),
        passwd=os.getenv('MYSQL_PASSWORD', 'daw'),
        db=os.getenv('MYSQL_DB', 'tienda_forestal'),
        charset='utf8mb4'
    )

# -----------------------------------------
# CRUD BÁSICO (Create, Read, Update, Delete) ---
# -----------------------------------------

def obtener_productos():
    """Obtiene todos los productos de la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM productos;")
    productos = cursor.fetchall()
    conexion.close()
    return productos


def obtener_producto_por_id(id):
    """Devuelve un solo producto por su ID."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM productos WHERE id = %s;", (id,))
    producto = cursor.fetchone()
    conexion.close()
    return producto


def crear_producto(datos):
    """Inserta un nuevo producto en la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
        INSERT INTO productos (nombre, tipo, marca, descripcion, precio, stock, imagen)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, (
        datos['nombre'], datos['tipo'], datos['marca'], datos['descripcion'],
        datos['precio'], datos['stock'], datos['imagen']
    ))
    conexion.commit()
    conexion.close()
    return cursor.lastrowid


def actualizar_producto(id, datos):
    """Actualiza un producto existente por su ID."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
        UPDATE productos
        SET nombre=%s, tipo=%s, marca=%s, descripcion=%s, precio=%s, stock=%s, imagen=%s
        WHERE id=%s;
    """
    cursor.execute(query, (
        datos['nombre'], datos['tipo'], datos['marca'], datos['descripcion'],
        datos['precio'], datos['stock'], datos['imagen'], id
    ))
    conexion.commit()
    conexion.close()
    return cursor.rowcount


def eliminar_producto(id):
    """Elimina un producto de la base de datos por su ID."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s;", (id,))
    conexion.commit()
    conexion.close()
    return cursor.rowcount


# -----------------------------------------
# BÚSQUEDA SIMPLE 
# -----------------------------------------

def buscar_productos(termino):
    """
    Busca productos cuyo nombre, tipo o marca contenga el término proporcionado.
    Se usa LIKE con comodines para coincidencias parciales.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(MySQLdb.cursors.DictCursor)
    like = f"%{termino}%"
    query = """
        SELECT * FROM productos
        WHERE nombre LIKE %s OR tipo LIKE %s OR marca LIKE %s;
    """
    cursor.execute(query, (like, like, like))
    resultados = cursor.fetchall()
    conexion.close()
    return resultados


# -----------------------------------------
# FILTRADO, ORDENACIÓN Y PAGINACIÓN
# -----------------------------------------

def filtrar_productos(tipo=None, marca=None, precio_min=None, precio_max=None,
                      ordenar=None, pagina=1, por_pagina=10):
    """
    Filtra productos según varios criterios, permite paginación y devuelve:
    - productos paginados
    - total_resultados
    - total_paginas
    - pagina_actual

    Parámetros:
    tipo: filtrar por tipo  (string)
    marca: filtrar por marca (string)
    precio_min / precio_max: valores numéricos
    ordenar: 'asc' o 'desc' por precio
    pagina: número de página actual
    por_pagina: nº de productos por página (10 por defecto)
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor(MySQLdb.cursors.DictCursor)

    # ===========================
    # 1. Construir base de la consulta
    # ===========================
    base_query = "FROM productos WHERE 1=1"
    params = []

    # --- Filtros dinámicos según los parámetros ---
    if tipo:
        base_query += " AND tipo = %s"
        params.append(tipo)

    if marca:
        base_query += " AND marca = %s"
        params.append(marca)

    if precio_min is not None:
        base_query += " AND precio >= %s"
        params.append(precio_min)

    if precio_max is not None:
        base_query += " AND precio <= %s"
        params.append(precio_max)

    # ===========================
    # 2. Obtener TOTAL DE RESULTADOS (sin LIMIT)
    # ===========================
    query_count = f"SELECT COUNT(*) AS total {base_query}"
    cursor.execute(query_count, params)
    total_resultados = cursor.fetchone()['total']

    # Evitar división por 0
    if total_resultados == 0:
        return {
            "productos": [],
            "total_resultados": 0,
            "pagina_actual": pagina,
            "total_paginas": 0
        }

    # ===========================
    # 3. Calcular total de páginas
    # ===========================
    total_paginas = math.ceil(total_resultados / por_pagina)
    pagina = min(pagina, total_paginas)  # Ajustar si se pide una página mayor
    offset = (pagina - 1) * por_pagina

    # ===========================
    # 4. Construir consulta FINAL con LIMIT y OFFSET
    # ===========================
    query_final = f"SELECT * {base_query}"

    # Ordenación por precio
    if ordenar == "asc":
        query_final += " ORDER BY precio ASC"
    elif ordenar == "desc":
        query_final += " ORDER BY precio DESC"

    # Paginación
    query_final += " LIMIT %s OFFSET %s"
    params_final = params + [por_pagina, offset]

    cursor.execute(query_final, params_final)
    productos = cursor.fetchall()

    conexion.close()

    # ===========================
    # 5. Devolver respuesta estructurada
    # ===========================
    return {
        "productos": productos,
        "total_resultados": total_resultados,
        "pagina_actual": pagina,
        "total_paginas": total_paginas
    }

