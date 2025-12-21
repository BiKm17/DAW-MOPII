<!-- La Vista no sabe cómo llegan los datos, sólo los muestra -->
<template>
  <div>
    <h2>Catálogo de Productos</h2>

    <!-- BUSCADOR -->
    <input
      v-model="filtros.termino"
      placeholder="Buscar producto..."
      @keyup.enter="buscar"
    />
    <button @click="buscar">Buscar</button>

    <!-- FILTROS -->
    <div class="filtros">
      <input v-model="filtros.tipo" placeholder="Tipo" />
      <input v-model="filtros.marca" placeholder="Marca" />
      <input v-model.number="filtros.precio_min" placeholder="Precio mín." />
      <input v-model.number="filtros.precio_max" placeholder="Precio máx." />
    </div>

    <!-- ESTADOS -->
    <p v-if="loading">Cargando productos...</p>
    <p v-if="error">{{ error }}</p>

    <!-- LISTADO -->
    <div class="grid">
      <div
        v-for="p in productos"
        :key="p.id"
        class="card"
      >
        <img :src="`/img/${p.imagen}`" />
        <h3>{{ p.nombre }}</h3>
        <p>{{ p.descripcion }}</p>
        <strong>{{ p.precio }} €</strong>
      </div>
    </div>

    <!-- PAGINACIÓN -->
    <div class="paginacion" v-if="totalPaginas > 1">
      <button
        @click="cambiarPagina(paginaActual - 1)"
        :disabled="paginaActual === 1"
      >
        Anterior
      </button>

      <button
        v-for="n in totalPaginas"
        :key="n"
        @click="cambiarPagina(n)"
        :class="{ activo: n === paginaActual }"
      >
        {{ n }}
      </button>

      <button
        @click="cambiarPagina(paginaActual + 1)"
        :disabled="paginaActual === totalPaginas"
      >
        Siguiente
      </button>
    </div>
  </div>
</template>

<script setup>
// ===============================
// ProductosView.vue
// ===============================
// - NO contiene lógica de negocio
// - Consume el Presenter
// ===============================

import ProductsPresenter from '@/presenters/ProductsPresenter.js'

// Instanciamos el Presenter
const {
  productos,
  loading,
  error,
  paginaActual,
  totalPaginas,
  filtros,
  cargarProductos,
  buscar,
  cambiarPagina
} = ProductsPresenter()

// Carga inicial
cargarProductos()
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}
.card {
  padding: 1rem;
  background: white;
  border-radius: 10px;
}
.paginacion button.activo {
  background: #4caf50;
  color: white;
}
</style>
