// src/presenters/ProductsPresenter.js
// ===================================================
// PRESENTER (MVP)
// Orquesta la lógica entre la View y la API
//
// Actúa como "cerebro" del frontend MVP.
// - Gestiona estado
// - Habla con la API
// - Expone métodos que la Vista utiliza
//
// El Presenter es un servicio de lógica reutilizable, no un componente visual. 
// ===================================================

import { ref } from 'vue'
import { getProductos, buscarProductos } from '@/services/api.js'

export default function ProductsPresenter() {
  // ---------------------------
  // Estado (reactivo)
  // ---------------------------
  const productos = ref([])
  const loading = ref(false)
  const error = ref(null)

  // ---------------------------
  // Casos de uso
  // ---------------------------

  /**
   * Cargar todos los productos
   */
  const cargarProductos = async () => {
    loading.value = true
    error.value = null

    try {
      const data = await getProductos()
      productos.value = data.productos ?? data
    } catch (err) {
      console.error(err)
      error.value = 'Error al cargar productos'
    } finally {
      loading.value = false
    }
  }

  /**
   * Buscar productos por término
   */
  const buscar = async (termino) => {
    loading.value = true
    error.value = null

    try {
      if (!termino || termino.trim() === '') {
        await cargarProductos()
      } else {
        const data = await buscarProductos(termino)
        productos.value = data.productos ?? data
      }
    } catch (err) {
      console.error(err)
      error.value = 'Error en la búsqueda'
    } finally {
      loading.value = false
    }
  }

  // ---------------------------
  // API pública del Presenter
  // ---------------------------
  return {
    productos,
    loading,
    error,
    cargarProductos,
    buscar
  }
}

