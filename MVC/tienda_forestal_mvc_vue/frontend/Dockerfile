# ---------------------------
# ETAPA 1: BUILD DE VITE
# ---------------------------
FROM node:20-alpine AS build

WORKDIR /app

# Copiamos solo archivos esenciales primero (para cache de npm)
COPY package*.json ./

RUN npm install

# Copiamos el resto del código
COPY . .

# Construimos la aplicación
RUN npm run build


# ---------------------------
# ETAPA 2: SERVIDOR ESTÁTICO
# ---------------------------
FROM node:20-alpine

WORKDIR /app

# Importamos solo la carpeta dist generada en la etapa 1
COPY --from=build /app/dist ./dist

# Instalamos un servidor estático
RUN npm install -g serve

EXPOSE 8080

# IMPORTANTE: forzamos el puerto 8080
CMD ["serve", "-s", "dist", "-l", "8080"]

