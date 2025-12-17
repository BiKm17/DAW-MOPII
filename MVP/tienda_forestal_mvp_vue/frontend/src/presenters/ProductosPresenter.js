import { filtrarProductos, buscarProductos } from "@/services/api";

export default class ProductosPresenter {
  constructor(callback) {
    this.callback = callback;
    this.state = {
      productos: [],
      loading: false,
      pagina: 1,
      total_paginas: 1
    };
  }

  notify() {
    this.callback({ ...this.state });
  }

  async cargar() {
    this.state.loading = true;
    this.notify();

    const res = await filtrarProductos({ pagina: this.state.pagina });
    this.state.productos = res.data.productos;
    this.state.total_paginas = res.data.total_paginas;

    this.state.loading = false;
    this.notify();
  }

  async buscar(termino) {
    this.state.loading = true;
    this.notify();

    const res = await buscarProductos(termino);
    this.state.productos = res.data;

    this.state.loading = false;
    this.notify();
  }
}

