from flask import Flask

# Iniciar flask
app = Flask(__name__)

# Ruta "/" respuesta en json
@app.route('/')
def home():
    return {
        'message': 'Hello, World!'
    }

# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)  # Modo de depuración activado para mostrar errores en tiempo real