#Presenter del backend - Importantisimo para MVP
from flask import Blueprint, request, jsonify

# Importamos el modelo (lógica de datos)
from models.producto_model import (
    obtener_productos,
    buscar_productos,
    filtrar_productos
)

# Blueprint = módulo independiente de rutas
producto_api_blueprint = Blueprint("producto_api", __name__)

# -------------------------
# ENDPOINT: listar productos
# -------------------------
@producto_api_blueprint.route("/productos", methods=["GET"])
def listar_productos():
    """
    Devuelve todos los productos.
    No contiene lógica de negocio.
    Solo orquesta la llamada al modelo.
    """
    productos = obtener_productos()
    return jsonify(productos)

# -------------------------
# ENDPOINT: búsqueda simple
# -------------------------
@producto_api_blueprint.route("/productos/buscar", methods=["GET"])
def buscar():
    """
    Recibe un término por query string
    y delega la búsqueda al modelo.
    """
    termino = request.args.get("termino", "")
    productos = buscar_productos(termino)
    return jsonify(productos)

# -------------------------
# ENDPOINT: filtrado básico
# -------------------------
@producto_api_blueprint.route("/productos/filtrar", methods=["GET"])
def filtrar():
    """
    Ejemplo de endpoint preparado
    para paginación y filtros.
    """
    pagina = int(request.args.get("pagina", 1))
    por_pagina = int(request.args.get("por_pagina", 10))
    ordenar = request.args.get("ordenar", "")

    resultado = filtrar_productos(
        pagina=pagina,
        por_pagina=por_pagina,
        ordenar=ordenar
    )

    return jsonify(resultado)
