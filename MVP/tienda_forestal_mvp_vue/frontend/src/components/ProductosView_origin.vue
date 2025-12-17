<template>
  <div>
    <h2>Catalogo (MVP)</h2>

    <input v-model="termino" @keyup.enter="onBuscar" />
    <button @click="onBuscar">Buscar</button>

    <div v-if="state.loading">Cargando...</div>

    <div v-else>
      <div v-for="p in state.productos" :key="p.id" class="card">
        <img :src="'/img/' + p.imagen" alt="" />
        <h3>{{ p.nombre }}</h3>
        <p>{{ p.descripcion }}</p>
        <small>{{ p.disponibilidad }}</small>
        <strong>{{ p.precio_format }}</strong>
      </div>

      <div class="paginacion" v-if="state.total_paginas > 1">
        <button @click="onPagina(state.pagina - 1)" :disabled="state.pagina === 1">Anterior</button>

        <button v-for="n in state.total_paginas" :key="n" @click="onPagina(n)" :class="{ activo: n === state.pagina }">
          {{ n }}
        </button>

        <button @click="onPagina(state.pagina + 1)" :disabled="state.pagina === state.total_paginas">Siguiente</button>
      </div>
    </div>

    <div v-if="state.error" class="error">{{ state.error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import ProductosPresenter from "@/presenters/ProductosPresenter.js";

const state = ref({
  loading: true,
  productos: [],
  pagina: 1,
  por_pagina: 10,
  total_paginas: 1,
  total_resultados: 0,
  error: null
});

// Esta función será llamada por el presenter para actualizar la vista
function viewCallback(newState) {
  state.value = newState;
}

// instanciamos presenter con la función callback
const presenter = new ProductosPresenter(viewCallback);

const termino = ref("");

// métodos que delegan en el presenter
function onBuscar() {
  presenter.buscar(termino.value);
}

function onPagina(n) {
  presenter.cambiarPagina(n);
}

onMounted(() => {
  // carga inicial
  presenter.cargar();
});
</script>

<style scoped>
/* estilos sencillos */
</style>

