"""
Capa de Controlador (Controller) del patrón MVC.
Define las rutas (endpoints) que se comunican con el modelo y devuelven respuestas JSON al frontend.
"""

from flask import Blueprint, jsonify, request
from models import producto_model

# Definimos un Blueprint, que agrupa todas las rutas relacionadas con productos
producto_blueprint = Blueprint('producto', __name__)

# --- RUTAS CRUD ---

@producto_blueprint.route('/productos', methods=['GET'])
def obtener_todos():
    """
    GET /api/productos
    Devuelve un listado de todos los productos en formato JSON.
    """
    productos = producto_model.obtener_productos()
    return jsonify(productos), 200


@producto_blueprint.route('/productos/<int:id>', methods=['GET'])
def obtener_por_id(id):
    """
    GET /api/productos/<id>
    Devuelve los datos de un solo producto.
    """
    producto = producto_model.obtener_producto_por_id(id)
    if producto:
        return jsonify(producto), 200
    else:
        return jsonify({'mensaje': 'Producto no encontrado'}), 404


@producto_blueprint.route('/productos', methods=['POST'])
def crear():
    """
    POST /api/productos
    Crea un nuevo producto a partir de los datos enviados en JSON.
    """
    datos = request.json
    id = producto_model.crear_producto(datos)
    return jsonify({'mensaje': 'Producto creado correctamente', 'id': id}), 201


@producto_blueprint.route('/productos/<int:id>', methods=['PUT'])
def actualizar(id):
    """
    PUT /api/productos/<id>
    Actualiza un producto existente con los datos proporcionados.
    """
    datos = request.json
    filas_afectadas = producto_model.actualizar_producto(id, datos)
    if filas_afectadas > 0:
        return jsonify({'mensaje': 'Producto actualizado correctamente'}), 200
    else:
        return jsonify({'mensaje': 'No se encontró el producto'}), 404


@producto_blueprint.route('/productos/<int:id>', methods=['DELETE'])
def eliminar(id):
    """
    DELETE /api/productos/<id>
    Elimina un producto por su ID.
    """
    filas_afectadas = producto_model.eliminar_producto(id)
    if filas_afectadas > 0:
        return jsonify({'mensaje': 'Producto eliminado correctamente'}), 200
    else:
        return jsonify({'mensaje': 'No se encontró el producto'}), 404


# --- RUTAS DE BÚSQUEDA Y FILTRADO ---

@producto_blueprint.route('/productos/buscar', methods=['GET'])
def buscar():
    """
    GET /api/productos/buscar?termino=stihl
    Busca productos que coincidan parcialmente con el término indicado.
    """
    termino = request.args.get('termino', '')
    if not termino:
        return jsonify({'mensaje': 'Debe proporcionar un término de búsqueda (?termino=...)'}), 400

    resultados = producto_model.buscar_productos(termino)
    if len(resultados) == 0:
        return jsonify({'mensaje': 'No se encontraron coincidencias'}), 404
    return jsonify(resultados), 200


@producto_blueprint.route('/productos/filtrar', methods=['GET'])
def filtrar():
    """
    API: /api/productos/filtrar
    Soporta filtros por:
    - tipo, marca
    - precio_min, precio_max
    - ordenar (asc, desc)
    - paginación (pagina, por_pagina)

    Devuelve:
    productos: lista de productos ya paginada
    total_resultados: total de coincidencias sin paginación
    pagina_actual: nº de página que se devuelve
    total_paginas: calculado según total_resultados
    """

    tipo = request.args.get('tipo')
    marca = request.args.get('marca')
    precio_min = request.args.get('precio_min', type=float)
    precio_max = request.args.get('precio_max', type=float)
    ordenar = request.args.get('ordenar')

    pagina = request.args.get('pagina', default=1, type=int)
    por_pagina = request.args.get('por_pagina', default=10, type=int)

    datos = producto_model.filtrar_productos(
        tipo=tipo,
        marca=marca,
        precio_min=precio_min,
        precio_max=precio_max,
        ordenar=ordenar,
        pagina=pagina,
        por_pagina=por_pagina
    )

    # Si no hay resultados, devolver 404
    if datos["total_resultados"] == 0:
        return jsonify({
            "mensaje": "No se encontraron productos con esos criterios",
            "total_resultados": 0,
            "pagina_actual": pagina,
            "total_paginas": 0,
            "productos": []
        }), 404

    return jsonify(datos), 200
