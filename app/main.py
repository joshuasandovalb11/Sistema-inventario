from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para usar sessions

@app.route('/')
def index():
    return render_template('index.html')

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
    return render_template(f'pages/{page_name}')

@app.route('/logout')
def logout():
    # Eliminar información de la sesión
    session.pop('logged_in', None)
    session.pop('user_email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)