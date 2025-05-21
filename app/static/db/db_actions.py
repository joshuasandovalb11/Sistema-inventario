import psycopg2
from app.static.db.connection import get_db_connection, close_db_connection
from datetime import date

def add_provider(provider_name, provider_email, provider_phone):
    conn, cur = get_db_connection()
    if conn is None:
        print("Error al conectar a la base de datos")
        return "Error al conectar a la base de datos", 500
    else:
        print("Conexión exitosa a la base de datos")
        try:
            # Insertar el nuevo proveedor en la tabla providers
            cur.execute("""
                INSERT INTO proveedores (nombre, correo, numero)
                VALUES (%s, %s, %s)
            """, (provider_name, provider_email, provider_phone))
            conn.commit()
            print("Proveedor agregado exitosamente")
            # return "Proveedor agregado exitosamente", 200
        except Exception as e:
            print("Error al agregar el proveedor:", e)
            # return "Error al agregar el proveedor", 500
        finally:
            close_db_connection(conn, cur)

def get_providers():   
    conn, cur = get_db_connection()
    if conn is None:
        print("Error al conectar a la base de datos")
        return "Error al conectar a la base de datos", 500
    else:
        print("Conexión exitosa a la base de datos")
        try:
            # Obtener todos los proveedores de la tabla providers
            cur.execute("""
            SELECT
                pr.nombre          AS proveedor,
                pr."idProveedor"   AS id,
                pr.numero,
                pr.correo,
                p.nombre           AS producto
            FROM proveedores AS pr
            LEFT JOIN productos   AS p
                ON p."idProveedor" = pr."idProveedor";
            """)
            providers = cur.fetchall()
            print("Proveedores obtenidos exitosamente")

            return [{"nombre": row[0], "id":row[1], "numero": row[2], "correo": row[3], "producto":row[4]} for row in providers]
            # return providers, 200
        except Exception as e:
            print("Error al obtener los proveedores:", e)
            return "Error al obtener los proveedores", 500
        finally:
            close_db_connection(conn, cur)

def edit_provider(provider_id, provider_name, provider_email, provider_phone):
    conn, cur = get_db_connection()
    if conn is None:
        print("Error al conectar a la base de datos")
        return "Error al conectar a la base de datos", 500
    else:
        print("Conexión exitosa a la base de datos")
        try:
            # Insertar el nuevo proveedor en la tabla providers
            cur.execute("""
                UPDATE proveedores
                SET nombre = %s, correo = %s, numero = %s
                WHERE "idProveedor" = %s
            """, (provider_name, provider_email, provider_phone, provider_id))
            conn.commit()
            print("Proveedor editado exitosamente")
            # return "Proveedor editado exitosamente", 200
        except Exception as e:
            print("Error al editar el proveedor:", e)
            # return "Error al editar el proveedor", 500
        finally:
            close_db_connection(conn, cur)

def delete_provider(provider_id):
    conn, cur = get_db_connection()
    if conn is None:
        print("Error al conectar a la base de datos")
        return "Error al conectar a la base de datos", 500
    else:
        cur.execute("""UPDATE productos SET activa = %s WHERE "idProveedor %s" """, ("false", provider_id,))
        conn.commit()
        cur.execute('DELETE FROM proveedores WHERE "idProveedor" = %s', (provider_id,))
        conn.commit()
        print("Proveedor eliminado exitosamente")
        # return "Proveedor eliminado exitosamente", 200
        close_db_connection(conn, cur)

def add_product(provider, productName, priceBuy, priceSell, packageQuantity, quantity, isActive):
    conn, cur = get_db_connection()
    if conn is None:
        print("Error al conectar a la base de datos")
        return "Error al conectar a la base de datos", 500
    else:
        print("Conexión exitosa a la base de datos")
        try:
            # Insertar el nuevo producto en la tabla products
            cur.execute("""
                INSERT INTO productos ("idProveedor", nombre, "precioCompra", "precioVenta", cantidad, "cantidadUnidad", activa)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (provider, productName, priceBuy, priceSell, packageQuantity, quantity, isActive))
            conn.commit()
            print("Producto agregado exitosamente")
            # return "Producto agregado exitosamente", 200
        except Exception as e:
            print("Error al agregar el producto:", e)
            # return "Error al agregar el producto", 500
        finally:
            close_db_connection(conn, cur)

def get_products():
    conn, cur = get_db_connection()
    if conn is None:
        return "Error al conectar a la base de datos", 500
    else:
        cur.execute('SELECT "idProducto", nombre, "precioCompra", "precioVenta", cantidad, "cantidadUnidad" FROM productos WHERE activa = true')
        products = cur.fetchall()

        return [{"id": row[0], "nombre": row[1], "precioCompra": row[2], "precioVenta": row[3], "cantidad": row[4], "cantidadUnidad":row[5]} for row in products]
    
def delete_product(product_id):
    conn, cur = get_db_connection()
    if conn is None:
        print("Error al conectar a la base de datos")
        return "Error al conectar a la base de datos", 500
    else:
        cur.execute('UPDATE productos SET activa = %s, "idProveedor"=%s WHERE "idProducto" = %s', ("false", None , product_id,))
        conn.commit()
        print("Producto eliminado exitosamente")
        # return "Producto eliminado exitosamente", 200
        close_db_connection(conn, cur)

def get_product_low():
    conn, cur = get_db_connection()
    if conn is None:
        return "Error al conectar a la base de datos", 500
    else:
        cur.execute('SELECT COUNT(*) FROM productos WHERE cantidad <= 4')
        count = cur.fetchone()[0]

        return count

def edit_product(product_id, productName, priceBuy, priceSell, packageQuantity, quantity):
    conn, cur = get_db_connection()
    if conn is None:
        print("Error al conectar a la base de datos")
        return "Error al conectar a la base de datos", 500
    else:
        print("Conexión exitosa a la base de datos")
        try:
            # Insertar el nuevo producto en la tabla products
            cur.execute("""
                UPDATE productos
                SET nombre = %s, "precioCompra" = %s, "precioVenta" = %s, cantidad = %s, "cantidadUnidad" = %s
                WHERE "idProducto" = %s
            """, (productName, priceBuy, priceSell, packageQuantity, quantity, product_id))
            conn.commit()
            print("Producto editado exitosamente")
            # return "Producto editado exitosamente", 200
        except Exception as e:
            print("Error al editar el producto:", e)
            # return "Error al editar el producto", 500
        finally:
            close_db_connection(conn, cur)

def sell_product(product_id, quantity):
    conn, cur = get_db_connection()
    if conn is None:
        print("Error al conectar a la base de datos")
        return "Error al conectar a la base de datos", 500
    else:
        print("Conexión exitosa a la base de datos")
        fecha = date.today()
        try:
            cur.execute('SELECT "precioVenta" FROM productos WHERE "idProducto" = %s', (product_id,))
            price = cur.fetchone()[0]
            total = int(price) * int(quantity)  
            # Insertar el nuevo producto en la tabla products
            cur.execute("""
                INSERT INTO ventas (fecha, total)
                VALUES (%s, %s)
                RETURNING "idVenta"
            """, (fecha, total))
            venta_id = cur.fetchone()[0]
            conn.commit()

            cur.execute("""
                INSERT INTO "detalleVenta" ("idProducto", "idVenta", cantidad)
                VALUES (%s, %s, %s)
            """, (product_id, venta_id, quantity,))

            conn.commit()
            print("Producto vendido exitosamente")
            # return "Producto vendido exitosamente", 200
        except Exception as e:
            print("Error al vender el producto:", e)
            # return "Error al vender el producto", 500
        finally:
            close_db_connection(conn, cur)

def get_sales():
    conn, cur = get_db_connection()
    if conn is None:
        print("Error al conectar a la base de datos")
        return "Error al conectar a la base de datos", 500
    else:
        print("Conexión exitosa a la base de datos")
        try:
            # Obtener todos los proveedores de la tabla providers
            cur.execute("""
            SELECT
                v."idVenta",
                v.fecha,
                v.total,
                p.nombre,
                dv.cantidad
            FROM ventas AS v
            LEFT JOIN "detalleVenta" AS dv
                ON dv."idVenta" = v."idVenta"
            LEFT JOIN productos AS p
                ON dv."idProducto" = p."idProducto";
            """)
            sales = cur.fetchall()
            print("Ventas obtenidas exitosamente")

            return [{"id":row[0], "fecha": row[1], "total": row[2], "producto": row[3], "cantidad": row[4]} for row in sales]
            # return providers, 200
        except Exception as e:
            print("Error al obtener las ventas:", e)
            return "Error al obtener las ventas", 500
        finally:
            close_db_connection(conn, cur)