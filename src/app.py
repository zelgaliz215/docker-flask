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
    """
    Maneja la solicitud GET a la ruta '/products' para devolver una lista de IDs de productos.

    Descripción:
        Esta función devuelve la lista global `product_ids` en formato JSON.
        Si la lista está vacía, devuelve una lista vacía.

    Returns:
        Response: Una respuesta JSON con el formato:
            {
                "Id de productos": [<list of IDs>]
            }
        Ejemplo:
            - Si `product_ids` contiene [101, 102, 103]:
              {
                  "Id de productos": [101, 102, 103]
              }
            - Si `product_ids` está vacío:
              {
                  "Id de productos": []
              }

    HTTP Status Code:
        200 OK: La solicitud fue exitosa.
    """
    return jsonify ({"Id de productos": product_ids })

@app.route('/products', methods=['PUT'])
def update_products_ids():
    """
    Actualiza la lista global `product_ids` con nuevos IDs de productos recibidos en una solicitud PUT.

    La función maneja la ruta '/products' y espera recibir un JSON en el cuerpo de la solicitud que contenga
    una clave "new_ids" con una lista de IDs de productos para agregar a la lista global `product_ids`.

    Proceso:
    1. Imprime los encabezados y el contenido recibido en la solicitud para propósitos de depuración.
    2. Extrae la clave "new_ids" del JSON enviado por el cliente.
    3. Si "new_ids" no está presente, utiliza una lista vacía como valor predeterminado.
    4. Extiende la lista global `product_ids` con los nuevos IDs recibidos.
    5. Devuelve una respuesta en formato JSON con un mensaje de confirmación y la lista actualizada de IDs.

    Returns:
        Response: Una respuesta JSON que contiene:
            - message (str): Mensaje indicando que los IDs de productos fueron actualizados.
            - new_ids (list): La lista completa de IDs de productos después de la actualización.
    """
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
    """
    Maneja la solicitud GET a la ruta '/product' para devolver información sobre un producto específico.

    Descripción:
        Esta función devuelve los detalles de un producto representado por una tupla `product`.
        La respuesta incluye los siguientes campos:
        - id (int): Identificador único del producto.
        - name (str): Nombre del producto.
        - price (float): Precio del producto.
        - stock (bool): Disponibilidad del producto (True si está en stock, False si no).

    Returns:
        Response: Una respuesta JSON con el formato:
            {
                "message": "Respuesta",
                "producto": {
                    "id": <int>,
                    "name": <str>,
                    "price": <float>,
                    "stock": <bool>
                }
            }
        Ejemplo:
            - Si `product` es (101, "Producto 1", 10.99, True):
              {
                  "message": "Respuesta",
                  "producto": {
                      "id": 101,
                      "name": "Producto 1",
                      "price": 10.99,
                      "stock": True
                  }
              }

    HTTP Status Code:
        200 OK: La solicitud fue exitosa.
    """
    return jsonify({"message":"Respuesta","producto": { "id": product[0], "name": product[1], "price": product[2], "stock": product[3]}})    


## Listas POST
quantities = [10, 5, 15]

@app.route('/quantities', methods=['POST'])
def add_quantity():
    """
    Maneja la solicitud POST a la ruta '/quantities' para agregar una nueva cantidad a la lista global `quantities`.

    Descripción:
        Este endpoint permite agregar una nueva cantidad a la lista global `quantities`. 
        La solicitud debe incluir un JSON en el cuerpo con una clave `new_quantity`. 
        Si la cantidad está presente y es válida, se agrega a la lista y se devuelve la lista actualizada.
        Si no se proporciona el valor `new_quantity`, se devuelve un error con el código de estado HTTP 400.

    Parámetros de entrada:
        - new_quantity (int o float): La nueva cantidad que se agregará a la lista. Es un parámetro obligatorio.

    Returns:
        Response:
            - En caso de éxito (HTTP 201 Created):
                {
                    "message": "Cantidad añadida",
                    "new_quantity": <valor recibido>,
                    "quantities": [<lista actualizada de cantidades>]
                }
            - En caso de error (HTTP 400 Bad Request):
                {
                    "error": "Falta el valor de 'quantity"
                }

    HTTP Status Codes:
        - 201 Created: La cantidad se añadió exitosamente a la lista.
        - 400 Bad Request: No se encontró la clave `new_quantity` en el JSON enviado.

    Ejemplo:
        Solicitud válida:
            - JSON de entrada:
                {
                    "new_quantity": 20
                }
            - Respuesta:
                {
                    "message": "Cantidad añadida",
                    "new_quantity": 20,
                    "quantities": [10, 5, 15, 20]
                }

        Solicitud inválida:
            - JSON de entrada:
                {
                    "invalid_key": 20
                }
            - Respuesta:
                {
                    "error": "Falta el valor de 'quantity"
                }
    """
    data = request.json
    new_quantity = data.get('new_quantity')
    if new_quantity is not None:
        quantities.append(new_quantity)
        return jsonify({"message": "Cantidad añadida", "new_quantity": new_quantity, "quantities": quantities}), 201
    return jsonify({"error": "Falta el valor de 'quantity"}), 400

## --- Diccionarios ruta path
product_details = {"id":101, "name": "Laptop", "price": 1500.0, "quantity": 10}
@app.route("/product/details", methods=["PATCH"])
def update_product_details():
    """
    PATCH /product/details
    ---
    Descripción:
        Actualiza los detalles de un producto existente, permitiendo la modificación de campos como 
        nombre, precio y cantidad. Si un campo no existe, se devuelve un error 404.
        
    Parámetros:
        - body (JSON): Los campos a actualizar con sus nuevos valores. 
            Ejemplo:
            ```json
            {
                "name": "Smartphone",
                "price": 1200.0,
                "quantity": 15
            }
            ```

    Respuestas:
        200 OK:
            Descripción: Los detalles del producto fueron actualizados con éxito.
            Ejemplo:
            ```json
            {
                "message": "Detalles del producto actualizados",
                "product_details": {
                    "id": 101,
                    "name": "Smartphone",
                    "price": 1200.0,
                    "quantity": 15
                }
            }
            ```
        404 Not Found:
            Descripción: Si algún campo proporcionado no se encuentra en los detalles del producto.
            Ejemplo:
            ```json
            {
                "error": "No se encontró el campo 'invalid_field'"
            }
            ```
    """
    # Obtener los datos enviados en el cuerpo de la solicitud
    data = request.json 
    for key,value in data.items():
        if key in product_details:
            product_details[key] = value
        else:
            return jsonify({"error": f"No se encontró el campo '{key}'"}), 404
    return jsonify({"message": "Detalles del producto actualizados", "product_details": product_details}), 200



# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)  # Modo de depuración activado para mostrar errores en tiempo real