from flask import Flask, jsonify, request

# Iniciar flask
app = Flask(__name__)

# Ruta "/" respuesta en json
@app.route('/')
def home():
    return {
        'message': 'Hello, Backend para diferentes tipos de datos!'
    }
# Variable global--------------------------
## Ruta /stock 
stock = 100
@app.route("/stock", methods=['GET'])
def get_stock():
    return jsonify({'message':'Producto en inventario', 'stock': stock})

## /stock PUT
@app.route("/stock", methods=['PUT'])
def put_stock():
    global stock
    # request.json: Es un método proporcionado por Flask para acceder al cuerpo de la solicitud en formato JSON.
    data = request.json # El contenido del JSON enviado por el cliente se almacena en la variable data.
    """
    Intenta obtener el valor asociado a la clave "new_stock" del JSON enviado por el cliente. Si "new_stock" no está presente en el JSON, utiliza el valor actual de stock como predeterminado.
    """
    stock = data.get('new_stock', stock)
    return jsonify({'message' : 'Stock actualizado','stock': stock})

# Arreglos --------------
## Lista de id de productos

product_ids = [101,102,103,104,105,106,107]

@app.route('/products', methods=['GET'])
def get_products_ids():
    return jsonify ({"Id de productos": product_ids })

@app.route('/products', methods=['PUT'])
def update_products_ids():
    global product_ids
    
    ## Información de la peticion
    print("Encabezados recibidos:", request.headers)
    print("Contenido recibido:", request.data)
    data = request.json
    """
    Busca la clave "new_ids" en el JSON enviado por el cliente.
    Si "new_ids" no está presente en el JSON, devuelve una lista vacía como valor predeterminado.
    """
    new_ids = data.get('new_ids', [])
    product_ids.extend(new_ids) # Añade los elementos a la lista
    return jsonify({"message": "Ids de productos actualizados", "new_ids": product_ids})

## Tupla para representar un producto especifo
product = (101, "Producto 1", 10.99, True)
@app.route('/product', methods=['GET'])
def get_product():
    return jsonify({"message":"Respuesta","producto": { "id": product[0], "name": product[1], "price": product[2], "stock": product[3]}})    


## Listas POST
quantities = [10, 5, 15]

@app.route('/quantities', methods=['POST'])
def add_quantity():
    data = request.json
    new_quantity = data.get('new_quantity')
    if new_quantity is not None:
        quantities.append(new_quantity)
        return jsonify({"message": "Cantidad añadida", "new_quantity": new_quantity, "quantities": quantities}),201
    return jsonify({"error": "Falta el valor de 'quantity"}), 400


# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)  # Modo de depuración activado para mostrar errores en tiempo real