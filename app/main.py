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
    
    # Si está logueado, mostrar el dashboard
    return render_template('dashboard.html', content_template='pages/dashboard-content.html')

@app.route('/pages/<path:page_name>')
def serve_pages(page_name):
    prov = get_providers()
    productos = get_products()
    low = get_product_low()
    sales = get_sales()
    if page_name == 'proveedores.html':
        # Aquí puedes pasar los proveedores a la plantilla
        print("Estas en proveedores")

    return render_template(f'pages/{page_name}', prov=prov, productos=productos, low=low, sales=sales)

@app.route('/logout')
def logout():
    # Eliminar información de la sesión
    session.pop('logged_in', None)
    session.pop('user_email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)