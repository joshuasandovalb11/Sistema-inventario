import psycopg2
from app.static.db.connection import get_db_connection, close_db_connection
from datetime import date, timedelta, datetime

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
                    ARRAY_AGG(p.nombre)           AS producto
                FROM proveedores AS pr
                LEFT JOIN productos   AS p
                    ON p."idProveedor" = pr."idProveedor"
                GROUP BY pr."idProveedor", pr.nombre, pr.correo, pr.numero
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

def get_all_products():
    """Obtiene todos los productos sin paginación para usar en formularios"""
    conn, cur = get_db_connection()
    if conn is None:
        return []
    else:
        try:
            cur.execute("""
                SELECT "idProducto", nombre, "precioCompra", "precioVenta", cantidad, "cantidadUnidad"
                FROM productos
                ORDER BY nombre
            """)
            
            products = cur.fetchall()
            product_list = [{"id": row[0], "nombre": row[1], "precioCompra": row[2], 
                           "precioVenta": row[3], "cantidad": row[4], "cantidadUnidad":row[5]} 
                          for row in products]
            
            return product_list
            
        except Exception as e:
            print("Error al obtener todos los productos:", e)
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

def get_max_sell():
    conn, cur = get_db_connection()
    if conn is None:
        return "Error al conectar a la base de datos", 500
    else:
        try:
            # Obtener el producto más vendido
            cur.execute("""
                SELECT p.nombre, SUM(dv.cantidad) AS total_vendido
                FROM "detalleVenta" AS dv
                JOIN ventas AS v ON dv."idVenta" = v."idVenta"
                JOIN productos AS p ON dv."idProducto" = p."idProducto"
                WHERE v.fecha >= CURRENT_DATE - INTERVAL '7 days'
                GROUP BY p.nombre
                ORDER BY total_vendido DESC
                LIMIT 1
            """)
            
            result = cur.fetchone()
            if result:
                product_name, total_sold = result
                return {"product": product_name, "total_sold": total_sold}
            else:
                return {"product": None, "total_sold": 0}
            
        except Exception as e:
            print("Error al obtener el producto más vendido:", e)
            return {"product": None, "total_sold": 0}, 500
        finally:
            close_db_connection(conn, cur)

def get_sells_information():
    conn, cur = get_db_connection()
    if conn is None:
        return "Error al conectar a la base de datos", 500
    else:
        try:
            # Paso 1: generar fechas de los últimos 7 días
            today = datetime.today().date()
            last_7_days = [(today - timedelta(days=i)) for i in reversed(range(7))]
            formatted_days = [day.strftime('%Y-%m-%d') for day in last_7_days]

            # Paso 2: obtener ventas agrupadas por fecha (solo días con ventas)
            cur.execute("""
                SELECT v.fecha, SUM(v.total) AS total_vendido, SUM(cantidad) AS cantidad_vendida
                FROM ventas AS v
                JOIN "detalleVenta" AS dv ON v."idVenta" = dv."idVenta"
                WHERE fecha >= CURRENT_DATE - INTERVAL '7 days'
                GROUP BY fecha
                ORDER BY fecha
            """)
            rows = cur.fetchall()

            # Paso 3: convertir a diccionario para fácil acceso
            ventas_dict = {row[0].strftime('%Y-%m-%d'): int(row[1]) for row in rows}

            # Paso 4: construir listas completas con 0 donde no hubo ventas
            totals = [ventas_dict.get(fecha, 0) for fecha in formatted_days]
            cantidades_dict = {row[0].strftime('%Y-%m-%d'): int(row[2]) for row in rows}

            cantidades = [cantidades_dict.get(fecha, 0) for fecha in formatted_days]


            return {"labels": formatted_days, "totals": totals, "cantidad":cantidades}

        except Exception as e:
            print("Error al obtener la información de ventas:", e)
            return {"labels": [], "totals": [], "cantidad":[]}, 500
        finally:
            close_db_connection(conn, cur)

def get_report_summary():
    """Obtiene el resumen para las tarjetas del reporte (beneficio total, ingresos, ventas)"""
    conn, cur = get_db_connection()
    if conn is None:
        return {"beneficio_total": 0, "ingresos": 0, "ventas": 0}, 500
    else:
        try:
            # 1. Calcular beneficio total
            #Solo beneficios de ventas reales de los últimos 7 días
            cur.execute("""
                SELECT 
                    COALESCE(SUM((p."precioVenta" - p."precioCompra") * dv.cantidad), 0) AS beneficio_total
                FROM "detalleVenta" AS dv
                JOIN ventas AS v ON dv."idVenta" = v."idVenta"
                JOIN productos AS p ON dv."idProducto" = p."idProducto"
                WHERE v.fecha >= CURRENT_DATE - INTERVAL '7 days'
                    AND p.activa = true
            """)
            beneficio_result = cur.fetchone()
            beneficio_total = beneficio_result[0] if beneficio_result[0] is not None else 0

            # 2. Calcular ingresos (suma del valor de inventario actual)
            # Esto representa el valor total del inventario basado en precios de compra
            cur.execute("""
                SELECT COALESCE(SUM("precioCompra" * cantidad * "cantidadUnidad"), 0) AS valor_inventario
                FROM productos
                WHERE activa = true
            """)
            ingresos_result = cur.fetchone()
            ingresos = ingresos_result[0] if ingresos_result[0] is not None else 0

            # 3. Calcular total de ventas (últimos 7 días)
            cur.execute("""
                SELECT COALESCE(SUM(v.total), 0) AS ventas_total
                FROM ventas AS v
                WHERE v.fecha >= CURRENT_DATE - INTERVAL '7 days'
            """)
            ventas_result = cur.fetchone()
            ventas_total = ventas_result[0] if ventas_result[0] is not None else 0

            return {
                "beneficio_total": round(float(beneficio_total), 2),
                "ingresos": round(float(ingresos), 2),
                "ventas": round(float(ventas_total), 2)
            }

        except Exception as e:
            print("Error al obtener resumen del reporte:", e)
            return {"beneficio_total": 0, "ingresos": 0, "ventas": 0}, 500
        finally:
            close_db_connection(conn, cur)


def get_top_selling_products(limit=10):
    """
    Obtiene los productos más vendidos (últimos 7 días)
    CORREGIDO: Agrupa por producto, no por venta individual
    """
    conn, cur = get_db_connection()
    if conn is None:
        return [], 500
    else:
        try:
            # CORREGIDO: Agrupamos por producto para obtener realmente los más vendidos
            cur.execute("""
                SELECT 
                    p.nombre AS producto,
                    SUM(dv.cantidad * p."precioVenta") AS valor_venta_total,
                    SUM(dv.cantidad) AS cantidad_vendida_total,
                    COUNT(DISTINCT v."idVenta") AS num_ventas,
                    MAX(v.fecha) AS ultima_venta
                FROM "detalleVenta" AS dv
                JOIN ventas AS v ON dv."idVenta" = v."idVenta"
                JOIN productos AS p ON dv."idProducto" = p."idProducto"
                WHERE v.fecha >= CURRENT_DATE - INTERVAL '7 days'
                    AND p.activa = true
                GROUP BY p."idProducto", p.nombre
                ORDER BY cantidad_vendida_total DESC, valor_venta_total DESC
                LIMIT %s
            """, (limit,))
            
            results = cur.fetchall()
            
            products_list = []
            for row in results:
                products_list.append({
                    "producto": row[0],
                    "valor_venta": round(float(row[1]), 2),
                    "cantidad_vendida": int(row[2]),
                    "id_venta": f"{int(row[3])} ventas",  # Número de transacciones
                    "fecha_venta": row[4].strftime("%d/%m/%Y") if row[4] else ""
                })
            
            return products_list

        except Exception as e:
            print("Error al obtener productos más vendidos:", e)
            return [], 500
        finally:
            close_db_connection(conn, cur)


def get_sales_chart_data():
    """
    NUEVA FUNCIÓN: Obtiene datos para el gráfico de ventas de los últimos 7 días
    """
    conn, cur = get_db_connection()
    if conn is None:
        return {"labels": [], "totals": []}, 500
    else:
        try:
            cur.execute("""
                SELECT 
                    DATE(fecha) as fecha_venta,
                    COALESCE(SUM(total), 0) as total_dia
                FROM ventas 
                WHERE fecha >= CURRENT_DATE - INTERVAL '7 days'
                GROUP BY DATE(fecha)
                ORDER BY fecha_venta ASC
            """)
            
            results = cur.fetchall()
            
            # Crear arrays para los últimos 7 días, incluyendo días sin ventas
            import datetime
            labels = []
            totals = []
            
            # Generar los últimos 7 días
            today = datetime.date.today()
            for i in range(6, -1, -1):  # 6, 5, 4, 3, 2, 1, 0
                date = today - datetime.timedelta(days=i)
                labels.append(date.strftime("%d/%m"))
                
                # Buscar si hay ventas para este día
                total_for_date = 0
                for row in results:
                    if row[0] == date:
                        total_for_date = float(row[1])
                        break
                
                totals.append(round(total_for_date, 2))
            
            return {
                "labels": labels,
                "totals": totals
            }

        except Exception as e:
            print("Error al obtener datos del gráfico:", e)
            return {"labels": [], "totals": []}, 500
        finally:
            close_db_connection(conn, cur)


# FUNCIÓN ADICIONAL: Para validar consistencia de datos
def validate_report_data():
    """
    Función de validación para verificar la consistencia de los datos del reporte
    """
    conn, cur = get_db_connection()
    if conn is None:
        return False
    
    try:
        # Verificar que las ventas tengan detalles correspondientes
        cur.execute("""
            SELECT COUNT(*) 
            FROM ventas v 
            LEFT JOIN "detalleVenta" dv ON v."idVenta" = dv."idVenta"
            WHERE dv."idVenta" IS NULL
        """)
        ventas_sin_detalle = cur.fetchone()[0]
        
        # Verificar que los detalles tengan productos válidos
        cur.execute("""
            SELECT COUNT(*) 
            FROM "detalleVenta" dv 
            LEFT JOIN productos p ON dv."idProducto" = p."idProducto"
            WHERE p."idProducto" IS NULL OR p.activa = false
        """)
        detalles_sin_producto = cur.fetchone()[0]
        
        if ventas_sin_detalle > 0:
            print(f"⚠️  Advertencia: {ventas_sin_detalle} ventas sin detalles")
        
        if detalles_sin_producto > 0:
            print(f"⚠️  Advertencia: {detalles_sin_producto} detalles con productos inválidos")
        
        return ventas_sin_detalle == 0 and detalles_sin_producto == 0
        
    except Exception as e:
        print("Error en validación:", e)
        return False
    finally:
        close_db_connection(conn, cur)

def get_info_low():
    conn, cur = get_db_connection()
    if conn is None:
        return "Error al conectar a la base de datos", 500
    else:
        try:
            # Obtener el producto más vendido
            cur.execute("""
                SELECT p.nombre, p.cantidad
                FROM productos AS p
                WHERE p.cantidad <= 4
                ORDER BY p.cantidad ASC
                LIMIT 3
            """)
            
            result = cur.fetchall()
            if result:
                return [{"product": row[0], "quantity": row[1]} for row in result]
            else:
                return {"product": None, "quantity": 0}
            
        except Exception as e:
            print("Error al obtener el producto más vendido:", e)
            return {"product": None, "quantity": 0}, 500
        finally:
            close_db_connection(conn, cur)

def sum_costs():
    conn, cur = get_db_connection()
    if conn is None:
        return 0  # O podrías lanzar una excepción si prefieres
    else:
        try:
            cur.execute("""
                SELECT SUM("precioCompra" * cantidad) AS total
                FROM productos
            """)
            result = cur.fetchone()
            return result[0] if result[0] is not None else 0
        except Exception as e:
            print("Error al calcular el costo total:", e)
            return 0
        finally:
            close_db_connection(conn, cur)
