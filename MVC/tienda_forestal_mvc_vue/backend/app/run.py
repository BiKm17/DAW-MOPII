
from flask import Flask
from flask_cors import CORS

# Import del blueprint
from controllers.producto_controller import producto_blueprint

app = Flask(__name__)

# Habilitar CORS
CORS(app)

# Registrar blueprint
app.register_blueprint(producto_blueprint, url_prefix="/api")

@app.route("/")
def home():
    # Mensaje de bienvenida personalizado
    return "¡Conexión establecida! El sistema de la Tienda Forestal está operativo."

if __name__ == "__main__":
    # Ejecución de la aplicación en el puerto 5000
    app.run(debug=True, host="0.0.0.0", port=5000)

