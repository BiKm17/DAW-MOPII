"""
producto_api.py
===============
Capa API del patrón MVP.

Responsabilidad:
- Exponer endpoints REST
- Validar parámetros
- Llamar al modelo
- Devolver JSON limpio al frontend

❌ No contiene lógica de presentación

Esta capa:

recibe peticiones HTTP

valida parámetros

llama al modelo

devuelve JSON

❌ No renderiza HTML
❌ No decide vistas
"""

from flask import Blueprint, request, jsonify
from models.producto_model import (
    obtener_productos_filtrados,
    contar_productos_filtrados
)

producto_api = Blueprint("producto_api", __name__)


@producto_api.route("/productos", methods=["GET"])
def listar_productos():
    """
    Endpoint principal para:
    - listado
    - filtros
    - búsqueda
    - paginación
    """

    # -------------------------
    # LECTURA DE PARÁMETROS
    # -------------------------
    termino = request.args.get("termino")
    tipo = request.args.get("tipo")
    marca = request.args.get("marca")

    precio_min = request.args.get("precio_min", type=float)
    precio_max = request.args.get("precio_max", type=float)

    pagina = request.args.get("pagina", default=1, type=int)
    por_pagina = request.args.get("por_pagina", default=10, type=int)

    ordenar = request.args.get("ordenar")

    # -------------------------
    # LLAMADA AL MODELO
    # -------------------------
    productos = obtener_productos_filtrados(
        termino=termino,
        tipo=tipo,
        marca=marca,
        precio_min=precio_min,
        precio_max=precio_max,
        pagina=pagina,
        por_pagina=por_pagina,
        ordenar=ordenar
    )

    total = contar_productos_filtrados(
        termino=termino,
        tipo=tipo,
        marca=marca,
        precio_min=precio_min,
        precio_max=precio_max
    )

    total_paginas = (total + por_pagina - 1) // por_pagina

    # -------------------------
    # RESPUESTA JSON
    # -------------------------
    return jsonify({
        "productos": productos,
        "pagina_actual": pagina,
        "total_paginas": total_paginas,
        "total_resultados": total
    })
