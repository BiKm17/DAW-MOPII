"""
Controlador de Productos (Capa C del patrón MVC)

Este archivo gestiona:
- Rutas/Endpoints relacionados con productos
- Validación de parámetros de entrada
- Manejo de errores
- Respuestas JSON uniformes
- Interacción con la capa Modelo (producto_model)

IMPORTANTE:
El controlador no debe contener lógica de negocio ni SQL directamente.
Solo coordina la petición ↔ servicio ↔ respuesta.
"""

from flask import Blueprint, request, jsonify
from models import producto_model

# Definimos un Blueprint, que agrupa todas las rutas relacionadas con productos
producto_blueprint = Blueprint("producto", __name__)


# ----------------------------------------------------------------------
# FUNCIÓN AUXILIAR PARA RESPUESTAS JSON CONSISTENTES
# ----------------------------------------------------------------------

def response_ok(data=None, message="OK", status=200):
    return jsonify({
        "status": "success",
        "message": message,
        "data": data
    }), status


def response_error(message="Error", status=400, details=None):
    return jsonify({
        "status": "error",
        "message": message,
        "details": details
    }), status

# ---- RUTAS CRUD ----
# ----------------------------------------------------------------------
# RUTA: LISTAR TODOS LOS PRODUCTOS (simple)
# ----------------------------------------------------------------------

@producto_blueprint.route("/productos", methods=["GET"])
def listar_productos():
    """
    Devuelve todos los productos sin filtrado.
    Endpoint sencillo para pruebas iniciales.
    """
    try:
        productos = producto_model.obtener_productos()
        return response_ok(productos)
    except Exception as e:
        return response_error("Error al obtener productos", 500, str(e))


# ----------------------------------------------------------------------
# RUTA: PRODUCTO POR ID
# ----------------------------------------------------------------------

@producto_blueprint.route("/productos/<int:producto_id>", methods=["GET"])
def obtener_producto(producto_id):
    """Obtiene un único producto mediante su ID."""
    try:
        producto = producto_model.obtener_producto_por_id(producto_id)

        if not producto:
            return response_error("Producto no encontrado", 404)

        return response_ok(producto)

    except Exception as e:
        return response_error("Error al obtener el producto", 500, str(e))


# ----------------------------------------------------------------------
# RUTA: BÚSQUEDA SIMPLE
# ----------------------------------------------------------------------

@producto_blueprint.route("/productos/buscar", methods=["GET"])
def buscar_producto():
    """
    Búsqueda general por nombre, tipo o marca.
    Ejemplo:
    /api/productos/buscar?termino=motosierra
    """
    termino = request.args.get("termino")

    if not termino:
        return response_error("Debe proporcionar un parámetro 'termino'.", 400)

    try:
        resultados = producto_model.buscar_productos(termino)
        return response_ok(resultados)
    except Exception as e:
        return response_error("Error al realizar la búsqueda", 500, str(e))


# ----------------------------------------------------------------------
# RUTA: FILTRADO + ORDENACIÓN + PAGINACIÓN
# ----------------------------------------------------------------------

@producto_blueprint.route("/productos/filtrar", methods=["GET"])
def filtrar_productos():
    """
    Filtros disponibles:
    - tipo
    - marca
    - precio_min
    - precio_max
    - ordenar: "asc" o "desc"
    - pagina: int >= 1
    - por_pagina: int >= 1

    Ejemplo:
    /api/productos/filtrar?tipo=motosierra&marca=stihl&pagina=2&ordenar=asc
    """

    # ------------------------------
    # VALIDACIÓN Y PARSING DE DATOS
    # ------------------------------

    tipo = request.args.get("tipo")
    marca = request.args.get("marca")

    # Convertir números de manera segura
    def to_int(value, default=None):
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def to_float(value, default=None):
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    precio_min = to_float(request.args.get("precio_min"))
    precio_max = to_float(request.args.get("precio_max"))

    pagina = to_int(request.args.get("pagina"), 1)
    por_pagina = to_int(request.args.get("por_pagina"), 10)

    ordenar = request.args.get("ordenar")
    if ordenar not in (None, "asc", "desc"):
        return response_error("El parámetro 'ordenar' solo puede ser 'asc' o 'desc'.")

    if pagina < 1:
        return response_error("'pagina' debe ser un número mayor o igual a 1.")

    if por_pagina < 1:
        return response_error("'por_pagina' debe ser un número mayor o igual a 1.")

    # ------------------------------
    # EJECUCIÓN DEL MODELO
    # ------------------------------

    try:
        resultado = producto_model.filtrar_productos(
            tipo=tipo,
            marca=marca,
            precio_min=precio_min,
            precio_max=precio_max,
            ordenar=ordenar,
            pagina=pagina,
            por_pagina=por_pagina
        )

        return response_ok(resultado)

    except Exception as e:
        return response_error("Error al filtrar productos", 500, str(e))


# ----------------------------------------------------------------------
# RUTA: CREAR PRODUCTO (POST)
# ----------------------------------------------------------------------

@producto_blueprint.route("/productos", methods=["POST"])
def crear_producto():
    """
    Crea un producto nuevo. Espera un JSON con todos los campos requeridos.
    """

    datos = request.get_json()

    if not datos:
        return response_error("Debe enviar un cuerpo JSON válido.", 400)

    requeridos = ["nombre", "tipo", "marca", "descripcion", "precio", "stock", "imagen"]

    faltantes = [campo for campo in requeridos if campo not in datos]
    if faltantes:
        return response_error(f"Faltan campos obligatorios: {', '.join(faltantes)}", 400)

    try:
        nuevo_id = producto_model.crear_producto(datos)
        return response_ok({"id": nuevo_id}, "Producto creado correctamente", 201)
    except Exception as e:
        return response_error("Error al crear producto", 500, str(e))


# ----------------------------------------------------------------------
# RUTA: ACTUALIZAR PRODUCTO (PUT)
# ----------------------------------------------------------------------

@producto_blueprint.route("/productos/<int:producto_id>", methods=["PUT"])
def actualizar_producto(producto_id):
    datos = request.get_json()

    if not datos:
        return response_error("Debe enviar un cuerpo JSON válido.", 400)

    try:
        filas = producto_model.actualizar_producto(producto_id, datos)

        if filas == 0:
            return response_error("No se encontró el producto para actualizar.", 404)

        return response_ok(message="Producto actualizado correctamente")

    except Exception as e:
        return response_error("Error al actualizar producto", 500, str(e))


# ----------------------------------------------------------------------
# RUTA: ELIMINAR PRODUCTO (DELETE)
# ----------------------------------------------------------------------

@producto_blueprint.route("/productos/<int:producto_id>", methods=["DELETE"])
def eliminar_producto(producto_id):
    try:
        filas = producto_model.eliminar_producto(producto_id)

        if filas == 0:
            return response_error("No se encontró el producto para eliminar.", 404)

        return response_ok(message="Producto eliminado correctamente")

    except Exception as e:
        return response_error("Error al eliminar producto", 500, str(e))

