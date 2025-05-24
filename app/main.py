from flask import Flask, render_template, request, redirect, url_for, session
from app.static.db.connection import get_db_connection, close_db_connection
from app.static.db.db_actions import *

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para usar sessions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deleteProduct/<int:product_id>', methods=['GET', 'POST'])
def deleteProduct(product_id):
    if request.method == 'POST':
        delete_product(product_id)
    # return render_template('deleteProduct.html')
    return redirect(url_for('dashboard') + '#inventario')

@app.route('/deleteProvider/<int:provider_id>', methods=['GET', 'POST'])
def deleteProvider(provider_id):
    if request.method == 'POST':
        delete_provider(provider_id)
    # return render_template('deleteProvider.html')
    return redirect(url_for('dashboard') + '#proveedores')

@app.route("/addProvider", methods=["GET", "POST"])
def connection():
    if request.method == "POST":
        provider_name = request.form.get("nombreProveedor")
        provider_email = request.form.get("correoProveedor")
        provider_phone = request.form.get("numeroContacto")

        # Llamar a la función para agregar el proveedor
        add_provider(provider_name, provider_email, provider_phone)

        return redirect(url_for('dashboard') + '#proveedores')

    # return render_template('addProvider.html')

@app.route("/editProvider", methods=["GET", "POST"])
def editProvider():
    if request.method == "POST":
        provider_id = request.form.get("editProviderId")
        provider_name = request.form.get("editNombreProveedor")
        provider_email = request.form.get("editCorreoProveedor")
        provider_phone = request.form.get("editNumeroContacto")

        # Llamar a la función para agregar el proveedor
        edit_provider(provider_id, provider_name, provider_email, provider_phone)

        return redirect(url_for('dashboard') + '#proveedores')

    # return render_template('addProvider.html')

@app.route("/addProduct", methods=["GET", "POST"])
def addProduct():
    if request.method == "POST":
        provider = request.form.get("proveedor_id")
        productName = request.form.get("productName")
        priceBuy = request.form.get("priceBuy")
        priceSell = request.form.get("priceSell")
        packageQuantity = request.form.get("packageQuantity")
        quantity = request.form.get("unity")
        isActive = True

        if provider is None:
            return redirect(url_for('dashboard') + '#proveedores')

        # Llamar a la función para agregar el proveedor
        add_product(provider, productName, priceBuy, priceSell, packageQuantity, quantity, isActive)

        return redirect(url_for('dashboard') + '#inventario')

    # return render_template('addProvider.html')

@app.route('/editProduct', methods=['GET', 'POST'])
def editProduct():
    if request.method == 'POST':
        product_id = request.form.get("editId")
        productName = request.form.get("editProductName")
        priceBuy = request.form.get("editPriceBuy")
        priceSell = request.form.get("editPriceSell")
        packageQuantity = request.form.get("editPackageQuantity")
        quantity = request.form.get("editUnity")

        # Llamar a la función para agregar el proveedor
        edit_product(product_id, productName, priceBuy, priceSell, packageQuantity, quantity)

        return redirect(url_for('dashboard') + '#inventario')

    # return render_template('addProvider.html')

@app.route('/sellProduct', methods=['GET', 'POST'])
def sellProduct():
    if request.method == 'POST':
        product_id = request.form.get("sellId")
        quantity = request.form.get("sellQuantity")

        # Llamar a la función para agregar el proveedor
        sell_product(product_id, quantity)

        return redirect(url_for('dashboard') + '#ventas')

    # return render_template('addProvider.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Aquí harías la validación real de credenciales
        # Por ejemplo, verificar contra una base de datos
        
        # Para este ejemplo, aceptamos cualquier combinación
        session['logged_in'] = True
        session['user_email'] = email
        
        # Redirigir al dashboard después de un login exitoso
        return redirect(url_for('dashboard'))
    
    # Si es GET, simplemente mostramos la página de login
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Verificar si el usuario está logueado
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    info = get_sells_information()
    prov = get_all_providers()
    productos = get_all_products()
    productLow = get_info_low()
    total = info["totals"]
    cantidad = info["cantidad"]
    # Si está logueado, mostrar el dashboard
    return render_template(
        'dashboard.html',
        content_template='pages/dashboard-content.html',
        label=info["labels"],
        total=info["totals"],
        productos=productos,
        prov=prov,
        productLow = productLow,
        cost = sum_costs(),
        cantidad=info["cantidad"]
    )

@app.route('/pages/<path:page_name>')
def serve_pages(page_name):
    print(f"page_name: {page_name}")
    # Obtener parámetro de página de la URL
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Número de elementos por página

    max = get_max_sell()    
    label = []
    total = []
    cantidad = []

    if page_name == 'dashboard-content.html':
        info = get_sells_information()
        label = info.get("labels", [])
        total = info.get("totals", [])
        cantidad = info.get("cantidad", [])
        prov = get_all_providers()
        productos = get_all_products()
        productLow = get_info_low()
        cost = sum_costs()
        top_products = get_top_selling_products(3)
        

    if page_name == 'inventario.html':
        # Obtener productos paginados
        pagination_data = get_products(page, per_page)
        productos = pagination_data["products"]
        pagination = {
            "page": pagination_data["current_page"],
            "pages": pagination_data["pages"],
            "has_prev": pagination_data["has_prev"],
            "has_next": pagination_data["has_next"],
            "total": pagination_data["total"]
        }
        prov = get_all_providers()
        low = get_product_low()
        sales = []
        productLow = []
        cost = sum_costs()

    elif page_name == 'reporte.html':
        prov = get_all_providers()
        info = get_sells_information()
        label = info.get("labels", [])
        total = info.get("totals", [])
        cantidad = info.get("cantidad", [])
        
        # NUEVAS LÍNEAS: Obtener datos del reporte
        summary = get_report_summary()
        top_products = get_top_selling_products(3)
        
        productos = []
        low = 0
        sales = []
        productLow = []
        cost = 0
        pagination = {"page": 1, "pages": 1, "has_prev": False, "has_next": False, "total": 0}

    
    elif page_name == 'proveedores.html':
        # Obtener proveedores paginados
        pagination_data = get_providers(page, per_page)
        prov = pagination_data["providers"]
        pagination = {
            "page": pagination_data["current_page"],
            "pages": pagination_data["pages"],
            "has_prev": pagination_data["has_prev"],
            "has_next": pagination_data["has_next"],
            "total": pagination_data["total"]
        }
        productos = []
        low = 0
        sales = []
        productLow = []
        cost = 0;
        
    elif page_name == 'ventas.html':
        # Obtener ventas paginadas
        pagination_data = get_sales(page, per_page)
        sales = pagination_data["sales"]
        pagination = {
            "page": pagination_data["current_page"],
            "pages": pagination_data["pages"],
            "has_prev": pagination_data["has_prev"],
            "has_next": pagination_data["has_next"],
            "total": pagination_data["total"]
        }
        productos = get_all_products()
        prov = []
        low = 0
        info = get_sells_information()
        label = info.get("labels", [])
        total = info.get("totals", [])
        cantidad = info.get("cantidad",[])
        productLow = []
        cost = 0;
        
    else:
        # Para otras páginas, usar datos no paginados
        pagination_data = get_providers()
        prov = pagination_data["providers"] if isinstance(pagination_data, dict) else []
        
        productos_data = get_products()
        productos = productos_data["products"] if isinstance(productos_data, dict) else []
        
        low = get_product_low()
        productLow = get_info_low()
        sales_data = get_sales()
        sales = sales_data["sales"] if isinstance(sales_data, dict) else []
        pagination = {"page": 1, "pages": 1, "has_prev": False, "has_next": False, "total": 0}

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template(f'pages/{page_name}', 
                            prov=prov, 
                            productos=productos, 
                            low=low,
                            max_sell=max, 
                            sales=sales,
                            pagination=pagination,
                            label=label,
                            total=total,
                            cost=cost,
                            cantidad=cantidad,
                            productLow=productLow,
                            summary=summary if page_name == 'reporte.html' else {},
                            top_products=top_products if page_name in ['reporte.html', 'dashboard-content.html'] else [],
                            current_page_name=page_name)

    return render_template(f'pages/{page_name}', 
                        prov=prov, 
                        productos=productos, 
                        low=low, 
                        sales=sales,
                        max_sell=get_max_sell,
                        pagination=pagination,
                        label=label,
                        total=total,
                        cost=cost,
                        cantidad=cantidad,
                        productLow=productLow,
                        summary=summary if page_name == 'reporte.html' else {},
                        top_products=top_products if page_name in ['reporte.html', 'dashboard-content.html'] else [],
                        current_page_name=page_name)

@app.route('/logout')
def logout():
    # Limpiar la sesión y redirigir al login
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)