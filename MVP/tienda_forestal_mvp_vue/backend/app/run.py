from flask import Flask
from flask_cors import CORS

# Importamos la API (Presenter del backend)
#from controllers.producto_api import producto_api_blueprint
from controllers.producto_api import producto_api

# Creamos la aplicación Flask
app = Flask(__name__)

# Permitimos peticiones desde el frontend (Vue)
CORS(app)

# Ruta de prueba para verificar que el backend está vivo
@app.route("/")
def index():
    return "Backend MVP funcionando correctamente."

# Registramos la API de productos bajo /api
#app.register_blueprint(producto_api_blueprint, url_prefix="/api")
app.register_blueprint(producto_api, url_prefix="/api")

# Punto de entrada de la aplicación
if __name__ == "__main__":
    # 0.0.0.0 es obligatorio en Docker
    app.run(debug=True, host="0.0.0.0", port=5000)
