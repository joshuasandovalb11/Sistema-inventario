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

def get_providers(page=1, per_page=10):
    conn, cur = get_db_connection()
    if conn is None:
        return {"providers": [], "total": 0, "pages": 0}, 500
    else:
        try:
            # Contar total de proveedores
            cur.execute('SELECT COUNT(*) FROM proveedores')
            total_providers = cur.fetchone()[0]
            
            # Calcular offset
            offset = (page - 1) * per_page
            
            # Obtener proveedores con límite y offset
            cur.execute("""
                SELECT
                    pr.nombre          AS proveedor,
                    pr."idProveedor"   AS id,
                    pr.numero,
                    pr.correo,
                    p.nombre           AS producto
                FROM proveedores AS pr
                LEFT JOIN productos   AS p
                    ON p."idProveedor" = pr."idProveedor"
                ORDER BY pr."idProveedor"
                LIMIT %s OFFSET %s
            """, (per_page, offset))
            
            providers = cur.fetchall()
            
            # Calcular número total de páginas
            total_pages = (total_providers + per_page - 1) // per_page
            
            provider_list = [{"nombre": row[0], "id":row[1], "numero": row[2], 
                            "correo": row[3], "producto":row[4]} for row in providers]
            
            return {
                "providers": provider_list,
                "total": total_providers,
                "pages": total_pages,
                "current_page": page,
                "per_page": per_page,
                "has_prev": page > 1,
                "has_next": page < total_pages
            }
            
        except Exception as e:
            print("Error al obtener proveedores paginados:", e)
            return {"providers": [], "total": 0, "pages": 0}, 500
        finally:
            close_db_connection(conn, cur)

def get_all_providers():
    """Obtiene todos los proveedores sin paginación para usar en formularios"""
    conn, cur = get_db_connection()
    if conn is None:
        return []
    else:
        try:
            cur.execute("""
                SELECT "idProveedor", nombre, correo, numero
                FROM proveedores
                ORDER BY nombre
            """)
            
            providers = cur.fetchall()
            provider_list = [{"id": row[0], "nombre": row[1], "correo": row[2], "numero": row[3]} 
                           for row in providers]
            
            return provider_list
            
        except Exception as e:
            print("Error al obtener todos los proveedores:", e)
            return []
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

def get_products(page=1, per_page=10):
    conn, cur = get_db_connection()
    if conn is None:
        return {"products": [], "total": 0, "pages": 0}, 500
    else:
        try:
            # Contar total de productos activos
            cur.execute('SELECT COUNT(*) FROM productos WHERE activa = true')
            total_products = cur.fetchone()[0]
            
            # Calcular offset
            offset = (page - 1) * per_page
            
            # Obtener productos con límite y offset
            cur.execute('''
                SELECT "idProducto", nombre, "precioCompra", "precioVenta", cantidad, "cantidadUnidad" 
                FROM productos 
                WHERE activa = true 
                ORDER BY "idProducto" 
                LIMIT %s OFFSET %s
            ''', (per_page, offset))
            
            products = cur.fetchall()
            
            # Calcular número total de páginas
            total_pages = (total_products + per_page - 1) // per_page
            
            product_list = [{"id": row[0], "nombre": row[1], "precioCompra": row[2], 
                           "precioVenta": row[3], "cantidad": row[4], "cantidadUnidad":row[5]} 
                          for row in products]
            
            return {
                "products": product_list,
                "total": total_products,
                "pages": total_pages,
                "current_page": page,
                "per_page": per_page,
                "has_prev": page > 1,
                "has_next": page < total_pages
            }
            
        except Exception as e:
            print("Error al obtener productos paginados:", e)
            return {"products": [], "total": 0, "pages": 0}, 500
        finally:
            close_db_connection(conn, cur)

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

def get_sales(page=1, per_page=10):
    conn, cur = get_db_connection()
    if conn is None:
        return {"sales": [], "total": 0, "pages": 0}, 500
    else:
        try:
            # Contar total de ventas
            cur.execute('SELECT COUNT(*) FROM ventas')
            total_sales = cur.fetchone()[0]
            
            # Calcular offset
            offset = (page - 1) * per_page
            
            # Obtener ventas con límite y offset
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
                    ON dv."idProducto" = p."idProducto"
                ORDER BY v."idVenta" DESC
                LIMIT %s OFFSET %s
            """, (per_page, offset))
            
            sales = cur.fetchall()
            
            # Calcular número total de páginas
            total_pages = (total_sales + per_page - 1) // per_page
            
            sales_list = [{"id":row[0], "fecha": row[1], "total": row[2], 
                         "producto": row[3], "cantidad": row[4]} for row in sales]
            
            return {
                "sales": sales_list,
                "total": total_sales,
                "pages": total_pages,
                "current_page": page,
                "per_page": per_page,
                "has_prev": page > 1,
                "has_next": page < total_pages
            }
            
        except Exception as e:
            print("Error al obtener ventas paginadas:", e)
            return {"sales": [], "total": 0, "pages": 0}, 500
        finally:
            close_db_connection(conn, cur)