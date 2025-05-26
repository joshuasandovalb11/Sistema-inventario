# 🛒 Sistema inventario - STOCKY

**Stocky** es un sistema de control de inventario básico que tiene como objetivo el administrar una tienda de artículos varios (estilo bazar) que realiza sus transacciones únicamente de manera física en su único punto de venta.

---

## ⚙️ Instalación y configuración

Sigue los siguientes pasos para clonar el repositorio, crear un entorno virtual, instalar las dependencias y ejecutar el sistema:

```bash
# Clonar el repositorio
git clone https://github.com/joshuasandovalb11/Sistema-inventario.git

# Dirigete a la dirección principal
cd Sistema-inventario

# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```
## 🛠️ Ejecutar el servidor de flask

Para correr el servidor desde la dirección principal ingresa:
```bash
python -m app.main
```

## ✅ Ejecutar pruebas
Para ejecutar las pruebas unitarias, solo es necesario ejecutar el siguiente comando:

```bash
 pytest unitarias.py -v
```

## 📊 Perfilado del rendimiento
Se usarón herramientas de perfilado como cProfile y memory_profiler, así como sus extensiones visuales como mprof y snakeviz. En dado caso de querer correr estas pruebas solo siga las siguientes indicaciones:

### Usar cProfile (análisis de CPU)
```bash
python -m cProfile -o salida.prof rendimiento.py
snakeviz salida.prof
```
Esto mostrará de manera gráfica los tiempos de ejecucción de cada función en snakeviz.

### Usar memory_profiler (análisis de uso de memoria)
```bash
mprof run rendimiento.py
mprof plot
```
Esto generará una gráfica visual del uso de memoria durante la ejecución.

## ✅ Credenciales
Credenciales necesarias para iniciar sesión en la pestaña de Login:

## Usuario: admin
## Contraseña: admin1234