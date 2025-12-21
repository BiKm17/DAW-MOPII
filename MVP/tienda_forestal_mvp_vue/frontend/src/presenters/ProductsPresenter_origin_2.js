// ===============================
// ProductsPresenter.js
// ===============================
// Actúa como "cerebro" del frontend MVP.
// - Gestiona estado
// - Habla con la API
// - Expone métodos que la Vista utiliza
//
// El Presenter es un servicio de lógica reutilizable, no un componente visual. 
// ===============================

import { ref } from 'vue'
//import api from '@/services/api.js'
import {getProductos} from '@/services/api.js'

export default function ProductsPresenter() {

  // ===============================
  // ESTADO (reactivo)
  // ===============================
  const productos = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Paginación
  const paginaActual = ref(1)
  const porPagina = ref(10)
  const totalPaginas = ref(1)
  const totalResultados = ref(0)

  // Filtros
  const filtros = ref({
    termino: '',
    tipo: '',
    marca: '',
    precio_min: null,
    precio_max: null,
    ordenar: ''
  })

  // ===============================
  // MÉTODO PRINCIPAL
  // ===============================
  const cargarProductos = async () => {
    loading.value = true
    error.value = null

    try {
  //  const response = await api.get('/productos', {
      const response = await getProductos(), {
        params: {
          pagina: paginaActual.value,
          por_pagina: porPagina.value,
          ...filtros.value
        }
      })

      productos.value = response.data.productos
      totalPaginas.value = response.data.total_paginas
      totalResultados.value = response.data.total_resultados

    } catch (err) {
      error.value = 'Error cargando productos'
      productos.value = []
    } finally {
      loading.value = false
    }
  }

  // ===============================
  // ACCIONES DE USUARIO
  // ===============================
  const buscar = () => {
    paginaActual.value = 1
    cargarProductos()
  }

  const cambiarPagina = (nuevaPagina) => {
    if (nuevaPagina < 1 || nuevaPagina > totalPaginas.value) return
    paginaActual.value = nuevaPagina
    cargarProductos()
  }

  // ===============================
  // EXPONEMOS TODO A LA VISTA
  // ===============================
  return {
    // estado
    productos,
    loading,
    error,
    paginaActual,
    totalPaginas,
    totalResultados,
    filtros,

    // acciones
    cargarProductos,
    buscar,
    cambiarPagina
  }
}
