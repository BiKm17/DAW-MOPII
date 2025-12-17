import axios from "axios";

const api = axios.create({
  baseURL: "/api"
});

export const filtrarProductos = (params) =>
  api.get("/productos/filtrar", { params });

export const buscarProductos = (termino) =>
  api.get("/productos/buscar", { params: { termino } });
