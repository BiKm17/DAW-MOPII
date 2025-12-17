// frontend/src/presenters/ProductosPresenter.js
// Presentador para el listado de productos (MVP).
// Responsable de: validaciones, transformaciones, paginación y orquestación de llamadas al API.

import { filtrarProductos, buscarProductos } from "@/services/api";

/**
 * ProductosPresenter: clase que encapsula la lógica de presentación.
 * - viewCallback: función que actualiza la vista (por ejemplo: setState en la Vue component).
 * - Se puede usar también con patterns de eventos (emitters) o inyección de dependencias.
 */
export default class ProductosPresenter {
  constructor(viewCallback) {
    // viewCallback es una función que el presenter llama con { loading, productos, pagina, totalPaginas, totalResultados, error }
    this.viewCallback = viewCallback;
    this.state = {
      loading: false,
      productos: [],
      pagina: 1,
      por_pagina: 10,
      total_paginas: 1,
      total_resultados: 0,
      error: null
    };
  }

  // pasar nuevo estado a la vista
  _notify() {
    if (typeof this.viewCallback === "function") {
      this.viewCallback({ ...this.state });
    }
  }

  // Cargar con filtros (orquesta la llamada al API)
  async cargar(params = {}) {
    this.state.loading = true;
    this._notify();

    try {
      // normalizamos params: evitamos enviar undefined/empty
      const payload = {
        pagina: params.pagina ?? this.state.pagina,
        por_pagina: params.por_pagina ?? this.state.por_pagina,
        tipo: params.tipo ?? undefined,
        marca: params.marca ?? undefined,
        precio_min: params.precio_min ?? undefined,
        precio_max: params.precio_max ?? undefined,
        ordenar: params.ordenar ?? undefined
      };

      // Llamada al backend
      const res = await filtrarProductos(payload);

      // Backend devuelve { productos, pagina_actual, total_paginas, total_resultados }
      const data = res.data;

      // Transformaciones (ejemplo): calcular etiquetas legibles o flags
      const productosTransformados = data.productos.map(p => ({
        ...p,
        disponibilidad: p.stock > 0 ? "En stock" : "Sin stock",
        precio_format: `${Number(p.precio).toFixed(2)} €`
      }));

      // Actualizamos estado
      this.state.productos = productosTransformados;
      this.state.pagina = data.pagina_actual;
      this.state.total_paginas = data.total_paginas;
      this.state.total_resultados = data.total_resultados;
      this.state.error = null;
    } catch (err) {
      console.error("Presenter error:", err);
      this.state.error = err.message || "Error desconocido";
      this.state.productos = [];
      this.state.total_paginas = 1;
      this.state.total_resultados = 0;
    } finally {
      this.state.loading = false;
      this._notify();
    }
  }

  // Búsqueda general que usa otro endpoint
  async buscar(termino) {
    if (!termino || termino.trim() === "") {
      // si termino vacío, recargar lista normal
      this.state.pagina = 1;
      return this.cargar({});
    }

    this.state.loading = true;
    this._notify();

    try {
      const res = await buscarProductos(termino);
      const productos = res.data.map(p => ({
        ...p,
        disponibilidad: p.stock > 0 ? "En stock" : "Sin stock",
        precio_format: `${Number(p.precio).toFixed(2)} €`
      }));

      this.state.productos = productos;
      this.state.total_resultados = productos.length;
      this.state.total_paginas = Math.ceil(productos.length / this.state.por_pagina);
      this.state.pagina = 1;
      this.state.error = null;
    } catch (err) {
      this.state.error = err.message || "Error en búsqueda";
      this.state.productos = [];
    } finally {
      this.state.loading = false;
      this._notify();
    }
  }

  // Cambiar página (simple wrapper)
  async cambiarPagina(nuevaPagina) {
    if (nuevaPagina < 1 || nuevaPagina > this.state.total_paginas) return;
    this.state.pagina = nuevaPagina;
    await this.cargar({ pagina: nuevaPagina });
  }
}

