<!-- src/components/ProductosView.vue -->
<template>
  <div class="productos">
    <h2>Catálogo de productos</h2>

    <!-- =========================
         BUSCADOR
         ========================= -->
    <input
      type="text"
      v-model="termino"
      placeholder="Buscar producto..."
      @keyup.enter="onBuscar"
    />
    <button @click="onBuscar">Buscar</button>

    <!-- =========================
         ESTADOS
         ========================= -->
    <p v-if="loading">Cargando productos...</p>
    <p v-if="error" class="error">{{ error }}</p>

    <!-- =========================
         LISTADO
         ========================= -->
    <div class="grid" v-if="!loading && productos.length">
      <div
        class="card"
        v-for="producto in productos"
        :key="producto.id"
      >
        <img
          :src="`/img/${producto.imagen}`"
          :alt="producto.nombre"
        />

        <h3>{{ producto.nombre }}</h3>
        <p>{{ producto.descripcion }}</p>
        <strong>{{ producto.precio }} €</strong>
      </div>
    </div>

    <p v-if="!loading && productos.length === 0">
      No hay productos para mostrar
    </p>
  </div>
</template>

<script setup>
// ===================================================
// VIEW (MVP)
// Solo se encarga de mostrar datos y reaccionar a eventos
// ===================================================

import { ref, onMounted } from 'vue'
import ProductsPresenter from '@/presenters/ProductsPresenter.js'

// Instanciamos el Presenter
const {
  productos,
  loading,
  error,
  cargarProductos,
  buscar
} = ProductsPresenter()

// Estado local de la vista
const termino = ref('')

// Eventos
const onBuscar = () => {
  buscar(termino.value)
}

// Carga inicial
onMounted(() => {
  cargarProductos()
})
</script>

<style scoped>
.productos {
  padding: 1rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}

.card {
  background: #fff;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 0 5px rgba(0,0,0,0.1);
}

.card img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.error {
  color: red;
  font-weight: bold;
}
</style>

