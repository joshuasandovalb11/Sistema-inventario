from app.static.db.connection import get_db_connection, close_db_connection
from app.static.db.db_actions import sell_product, delete_provider, get_all_products
from app.static.validations import *
from decimal import *
from memory_profiler import profile
from datetime import date
from psycopg2.extras import RealDictCursor
import psycopg2

proveedor_existe = profile(proveedor_existe)
validar_nombre = profile(validar_nombre)
sell_product = profile(sell_product)
existe_producto = profile(existe_producto)
get_all_products = profile(get_all_products)
delete_provider = profile(delete_provider)



# Para refactorizar la función, unicamente que se retorne un 1 si el proveedor existe
# Eso en lugar de retornar el objeto completo
@profile
def proveedor_existe_ref(provider_id):
    try:
        conn,cur = get_db_connection()
        
        cur.execute('SELECT 1 FROM proveedores WHERE "idProveedor" = %s', (provider_id,))
        resultado = cur.fetchone()
        
        close_db_connection(conn, cur) 
        
        if resultado is not None:
            return True, "Proveedor válido."
        else:
            return False, "El proveedor seleccionado no existe."
        
    except Exception as e:
        return False, f"Error al validar el proveedor: {e}"

#Funcion para obtener los productos de la base de datos refactorizada
@profile
def sell_product_ref(product_id, quantity):
    conn, cur = get_db_connection()
    if conn is None:
        return "Error al conectar a la base de datos", 500
    else:
        fecha = date.today()
        try:
            # Buscar el producto en la base de datos y obtener su precio
            cur.execute('SELECT "precioVenta" FROM productos WHERE "idProducto" = %s', (product_id,))
            price = cur.fetchone()[0]
            if not price:
                return "Producto no encontrado", 404
            
            total = int(price) * int(quantity)  
            
            # Crear una nueva venta y obtener su ID
            cur.execute("""
                INSERT INTO ventas (fecha, total)
                VALUES (%s, %s)
                RETURNING "idVenta"
            """, (fecha, total))
            venta_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO "detalleVenta" ("idProducto", "idVenta", cantidad)
                VALUES (%s, %s, %s)
            """, (product_id, venta_id, quantity,))

            # Actualizar la cantidad del producto vendido
            cur.execute("""
                UPDATE productos
                SET cantidad = cantidad - %s
                WHERE "idProducto" = %s
            """, (quantity, product_id))

            conn.commit()
            return "Producto vendido exitosamente", 200
        except Exception as e:
            conn.rollback()
            return "Error al vender el producto", 500
        finally:
            close_db_connection(conn, cur)

# Para la refactorizacion de esta funcion, se dejó únicamente un commit al final de todas las instrucciones
@profile
def delete_provider_ref(provider_id):
    conn, cur = get_db_connection()
    if conn is None:
        close_db_connection(conn, cur)
        return "Error al conectar a la base de datos", 500
    else:
        cur.execute("""UPDATE productos SET "idProveedor" = NULL, activa = %s WHERE "idProveedor" = %s""", ("false", provider_id,))
        cur.execute('DELETE FROM proveedores WHERE "idProveedor" = %s', (provider_id,))

        conn.commit()
        close_db_connection(conn, cur)
        return "Proveedor eliminado exitosamente", 200
    

NOMBRE_PATTERN = re.compile(r"^[A-Za-zÁÉÍÓÚÑáéíóúñ0-9\s]+$")
# Para optimizar el rendimiento de la funcion se decidio definir el patrón fuera del método
# Además de reducir todo el proceso a una sola línea de código.
@profile
def validar_nombre_ref(nombre):
    return (True, "Nombre válido") if NOMBRE_PATTERN.match(nombre) else (False, "El nombre solo debe contener letras, números y espacios")

# Para refactorizar la función, se usa directamente el cursor de la conexión en lugar de definirlo en una variable aparte
@profile
def get_all_products_ref():
    conn, cur = get_db_connection()
    if conn is None:
        return []
    
    try:
        cur.execute("""
            SELECT "idProducto", nombre, "precioCompra", "precioVenta", cantidad, "cantidadUnidad"
            FROM productos
            WHERE activa = true
            ORDER BY nombre
        """)
        product_list = [{"id": row[0], "nombre": row[1], "precioCompra": row[2], 
                       "precioVenta": row[3], "cantidad": row[4], "cantidadUnidad":row[5]} 
                      for row in cur.fetchall()]
        
        return product_list
        
    except Exception as e:
        print("Error al obtener todos los productos:", e)
        return []
    finally:
        close_db_connection(conn, cur)

# Para refactorizar la función, se usa retorna un 1 en lugar de un objeto completo
@profile
def existe_producto_ref(product_name):
    try:
        conn, cur = get_db_connection()
        if conn is None:
            return False, "Error al conectar a la base de datos"
        
        product_name = product_name.lower() 
        cur.execute('SELECT 1 FROM productos WHERE "nombre" = %s', (product_name,))
        resultado = cur.fetchone()

        close_db_connection(conn, cur)

        if resultado is None:
            return True, "Producto válido."
        else:
            return False, "El producto ya existe."
    except Exception as e:
        return False, f"Error al validar el producto: {e}"
        

def principal():
    # proveedor_existe(14)
    proveedor_existe_ref(14)

    # validar_nombre("Juan Pérez")
    validar_nombre_ref("Juan Pérez")

    # productos = get_all_products()
    productos_ref = get_all_products_ref()

    # existe_producto("Nike Blazer Mid")
    existe_producto_ref("Nike Blazer Mid")

    # sell_product(27, 1)
    sell_product_ref(27, 1)

    # delete_provider(65)
    delete_provider_ref(65)
    
if __name__ == "__main__":
    principal()