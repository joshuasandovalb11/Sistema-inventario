import re

import bcrypt
from app.static.db.connection import get_db_connection, close_db_connection

def validar_datos_proveedor(nombre, correo, telefono):
    # Validar que el nombre solo contenga letras (y opcionalmente espacios)
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÑáéíóúñ\s]+", nombre):
        return False, "El nombre solo debe contener letras y espacios"

    # Validar formato de correo electrónico
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", correo):
        return False, "Correo electrónico no válido"

    # Validar número de teléfono: solo dígitos, y que tenga 10 caracteres (por ejemplo, para México)
    if not re.fullmatch(r"\d{10}", telefono):
        return False, "El número de teléfono debe tener exactamente 10 dígitos"

    return True, "Datos válidos"

def validar_campos_numericos(priceBuy, priceSell, packageQuantity, quantity):
    campos = {
        "Precio de compra": priceBuy,
        "Precio de venta": priceSell,
        "Cantidad por paquete": packageQuantity,
        "Cantidad en unidad": quantity
    }

    for nombre, valor in campos.items():
        try:
            numero = int(valor)
            if numero < 1:
                return False, f"{nombre} debe ser un número entero mayor a 0"
        except (ValueError, TypeError):
            return False, f"{nombre} debe ser un número entero válido"

    return True, "Campos válidos"

def validar_nombre(nombre):
    # Patrón diseñado para permitir en el nombre solo letras, números y espacios
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÑáéíóúñ0-9\s]+", nombre):
        return False, "El nombre solo debe contener letras, números y espacios"

    return True, "Nombre válido"



def proveedor_existe(provider_id):
    try:
        conn,cur = get_db_connection()
        
        cur.execute('SELECT * FROM proveedores WHERE "idProveedor" = %s', (provider_id,))
        resultado = cur.fetchone()
        
        close_db_connection(conn, cur) 
        
        if resultado is not None:
            return True, "Proveedor válido."
        else:
            return False, "El proveedor seleccionado no existe."
        
    except Exception as e:
        return False, f"Error al validar el proveedor: {e}"

def validar_cantidad_venta(product_id, cantidad):
    try:
        cantidad = int(cantidad)
    except (ValueError, TypeError):
        return False, "La cantidad debe ser un número entero válido"

    if cantidad < 1:
        return False, "La cantidad debe ser un número entero 1 o mayor"

    conn, cur = get_db_connection()
    if conn is None:
        return False, "Error al conectar a la base de datos"

    try:
        cur.execute('SELECT cantidad FROM productos WHERE "idProducto" = %s', (product_id,))
        resultado = cur.fetchone()
        if not resultado:
            return False, "Producto no encontrado"

        cantidad_disponible = resultado[0]
        if cantidad > cantidad_disponible:
            return False, f"Cantidad insuficiente. Disponible: {cantidad_disponible}"

        return True, "Cantidad válida"
    except Exception as e:
        return False, f"Error al validar cantidad: {str(e)}"
    finally:
        close_db_connection(conn, cur)

# Funcion para validar si un producto existe en la base de datos
def existe_producto(product_name):
    try:
        conn, cur = get_db_connection()
        if conn is None:
            return False, "Error al conectar a la base de datos"
        
        product_name = product_name.lower()  
        cur.execute('SELECT * FROM productos WHERE "nombre" = %s', (product_name,))
        resultado = cur.fetchone()

        close_db_connection(conn, cur)

        if resultado is None:
            return True, "Producto válido."
        else:
            return False, "El producto ya existe."
    except Exception as e:
        return False, f"Error al validar el producto: {e}"
    finally:
        if conn:
            close_db_connection(conn, cur)

def validar_login(user, password):
    conn, cur = get_db_connection()
    if conn is None:
        print("Error al conectar a la base de datos")
        return False

    try:
        # Buscar usuario por nombre
        cur.execute('SELECT * FROM admin WHERE "user" = %s', (user,))
        resultado = cur.fetchone()

        if resultado is None:
            return False

        hashed_password_db = resultado[1]

        # Verificamos contraseña
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password_db.encode('utf-8')):
            return True
        else:
            return False

    except Exception as e:
        print("Error durante la validación:", e)
        return False

    finally:
        close_db_connection(conn, cur)