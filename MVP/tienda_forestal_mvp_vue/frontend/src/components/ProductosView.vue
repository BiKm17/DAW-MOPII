<template>
  <div>
    <input v-model="termino" @keyup.enter="buscar" />
    <button @click="buscar">Buscar</button>

    <div v-if="state.loading">Cargando...</div>

    <div v-else>
      <div v-for="p in state.productos" :key="p.id">
        <h3>{{ p.nombre }}</h3>
        <p>{{ p.precio }} €</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import ProductosPresenter from "@/presenters/ProductosPresenter";

const state = ref({});
const termino = ref("");

const presenter = new ProductosPresenter((s) => (state.value = s));

const buscar = () => presenter.buscar(termino.value);

onMounted(() => presenter.cargar());
</script>

