# backend/app/models/producto_model.py
import mysql.connector
from flask import current_app

def obtener_conexion():
    return mysql.connector.connect(
        host=current_app.config["DB_HOST"],
        user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"],
        database=current_app.config["DB_NAME"]
    )

def obtener_productos_db():
    conn = obtener_conexion()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM productos ORDER BY id;")
    rows = cur.fetchall()
    conn.close()
    return rows

# ... implementar buscar_productos_db, filtrar_productos_db idénticas a tu modelo MVC (retornan dicts)

