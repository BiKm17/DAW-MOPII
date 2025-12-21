// src/services/api.js
// ===================================================
// Capa de acceso a la API (backend Flask)
// En MVP: esta capa SOLO se encarga de pedir datos
// ===================================================

import axios from 'axios'

// Axios usará rutas relativas (proxy o nginx)
const API_BASE = '/api/productos'

/**
 * Obtener todos los productos
 */
export async function getProductos() {
  const response = await axios.get(API_BASE)
  return response.data
}

/**
 * Buscar productos por término
 * @param {string} termino
 */
export async function buscarProductos(termino) {
  const response = await axios.get(`${API_BASE}/buscar`, {
    params: { termino }
  })
  return response.data
}
