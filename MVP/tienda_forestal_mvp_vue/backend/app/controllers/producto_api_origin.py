# backend/app/controllers/producto_api.py
from flask import Blueprint, request, jsonify
from models.producto_model import (
    obtener_productos_db,
    buscar_productos_db,
    filtrar_productos_db,
    obtener_producto_por_id_db,
    crear_producto_db,
    actualizar_producto_db,
    eliminar_producto_db
)

producto_api_blueprint = Blueprint("producto_api", __name__)

@producto_api_blueprint.route("/productos", methods=["GET"])
def listar_productos():
    # Devuelve lista completa o paginada si se implementa aquí (pero preferimos que la paginación la gestione el Presentador)
    productos = obtener_productos_db()
    return jsonify(productos)

@producto_api_blueprint.route("/productos/buscar", methods=["GET"])
def buscar():
    termino = request.args.get("termino", "")
    resultados = buscar_productos_db(termino)
    return jsonify(resultados)

@producto_api_blueprint.route("/productos/filtrar", methods=["GET"])
def filtrar():
    # Este endpoint ofrece filtros en crudo: tipo, marca, precio_min, precio_max, page, per_page (si quieres)
    pagina = int(request.args.get("pagina", 1))
    por_pagina = int(request.args.get("por_pagina", 10))
    tipo = request.args.get("tipo')
    marca = request.args.get("marca')
    precio_min = request.args.get("precio_min')
    precio_max = request.args.get("precio_max')
    ordenar = request.args.get("ordenar')
    resultado = filtrar_productos_db(pagina=pagina, por_pagina=por_pagina, tipo=tipo, marca=marca,
                                      precio_min=precio_min, precio_max=precio_max, ordenar=ordenar)
    return jsonify(resultado)

# CRUD endpoints (opcional)
@producto_api_blueprint.route("/productos/<int:pid>", methods=["GET"])
def producto_por_id(pid):
    producto = obtener_producto_por_id_db(pid)
    if not producto:
        return jsonify({"error": "Not found"}), 404
    return jsonify(producto)

