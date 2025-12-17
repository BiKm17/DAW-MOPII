#Modelo puro - sin Flask ni HTTP
import mysql.connector
import os

# ----------------------------------------
# CONEXIÓN A BD USANDO VARIABLES DE ENTORNO
# ----------------------------------------
def obtener_conexion():
    """
    Crea una conexión a MySQL leyendo
    las credenciales desde Docker.
    """
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

# -------------------------
# OBTENER TODOS LOS PRODUCTOS
# -------------------------
def obtener_productos():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    conn.close()
    return productos

# -------------------------
# BÚSQUEDA POR TEXTO
# -------------------------
def buscar_productos(termino):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT * FROM productos
        WHERE nombre LIKE %s OR marca LIKE %s
        """,
        (f"%{termino}%", f"%{termino}%")
    )

    productos = cursor.fetchall()
    conn.close()
    return productos

# -------------------------
# FILTRADO BÁSICO CON PAGINACIÓN
# -------------------------
def filtrar_productos(pagina, por_pagina, ordenar):
    offset = (pagina - 1) * por_pagina

    orden_sql = ""
    if ordenar == "asc":
        orden_sql = "ORDER BY precio ASC"
    elif ordenar == "desc":
        orden_sql = "ORDER BY precio DESC"

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    query = f"""
        SELECT * FROM productos
        {orden_sql}
        LIMIT %s OFFSET %s
    """

    cursor.execute(query, (por_pagina, offset))
    productos = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) AS total FROM productos")
    total = cursor.fetchone()["total"]

    conn.close()

    return {
        "productos": productos,
        "pagina_actual": pagina,
        "total_paginas": (total + por_pagina - 1) // por_pagina,
        "total_resultados": total
    }
