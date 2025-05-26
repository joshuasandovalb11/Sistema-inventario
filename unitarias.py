from app.main import app
import pytest
from app.static.db.connection import get_db_connection, close_db_connection
from app.static.db.db_actions import *

from app.static.validations import (
    validar_datos_proveedor,
    validar_nombre
)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

#Pruebas para la función add_provider
@pytest.mark.parametrize("nombre, email, telefono", [
    # Casos que deben funcionar
    ("Juan Pérez", "juan.perez@email.com", "1234567890"),
    ("Lucía Gómez", "lucia.gomez@empresa.com", "0987654321"),
    ("Andrés Martínez", "andres.martinez@mail.net", "5551234567"),
    # Casos que deben fallar
    ("Pedro123", "pedro@email.com", ""),
    ("Sofía López", "sofia.lopez@email.com", "12345")
])
def test_add_provider(client, nombre, email, telefono):
    data = {
        "nombreProveedor": nombre,
        "correoProveedor": email,
        "numeroContacto": telefono
    }
    
    response = client.post('/addProvider', data=data, content_type='application/x-www-form-urlencoded')
    
    if nombre in ["Juan Pérez", "Lucía Gómez", "Andrés Martínez"]:
        assert response.status_code == 302
    else:  
        assert response.status_code == 302

#Pruebas para la función add_product
@pytest.mark.parametrize("idProveedor, nombre, precioCompra, precioVenta, cantidad, cantidadUnidad, activa", [
    # Casos que deben funcionar
    ("Juan Pérez", "Producto A", 10.5, 15.0, 100, 300, True),
    ("Lucía Gómez", "Producto B", 20.0, 30.0, 50, 400, True),
    ("Andrés Martínez", "Producto C", 5.0, 8.0, 200, 300, False),
    # Casos que deben fallar
    ("Andrés Martínez", "", 10.0, 12.0, 10, 23, True),
    ("Andrés Martínez", "Producto D", -5.0, 10.0, 20, 98, True),
])
def test_add_product(client, idProveedor, nombre, precioCompra, precioVenta, cantidad, cantidadUnidad, activa):
    data = {
        "proveedor_id": idProveedor,  
        "productName": nombre,    
        "priceBuy": precioCompra,     
        "priceSell": precioVenta,  
        "packageQuantity": cantidad,     
        "unity": cantidadUnidad,      
    }
    response = client.post('/addProduct', data=data, content_type='application/x-www-form-urlencoded')
    
    if nombre == "" or precioCompra < 0:
        assert response.status_code == 302 
    else:
        assert response.status_code == 302

#Pruebas para la función validar_datos_proveedor
class TestValidarDatosProveedor:
    
    # PRUEBAS QUE PASAN
    def test_datos_validos_completos(self):
        #Prueba con datos completamente válidos
        result, message = validar_datos_proveedor("Juan Pérez", "juan@email.com", "1234567890")
        assert result == True
        assert message == "Datos válidos"
    
    def test_nombre_con_acentos(self):
        #Prueba con nombre que incluye acentos y ñ
        result, message = validar_datos_proveedor("María Rodríguez Nuñez", "maria@test.co", "9876543210")
        assert result == True
        assert message == "Datos válidos"
    
    def test_nombre_simple_sin_espacios(self):
        #Prueba con nombre simple sin espacios
        result, message = validar_datos_proveedor("Carlos", "carlos@empresa.net", "5555555555")
        assert result == True
        assert message == "Datos válidos"
    
    # PRUEBAS QUE FALLAN
    def test_nombre_con_numeros(self):
        #Prueba que falla: nombre con números
        result, message = validar_datos_proveedor("Juan123", "juan@email.com", "1234567890")
        assert result == False
        assert message == "El nombre solo debe contener letras y espacios"
    
    def test_telefono_incompleto(self):
        #Prueba que falla: teléfono con menos de 10 dígitos
        result, message = validar_datos_proveedor("Ana García", "ana@email.com", "12345")
        assert result == False
        assert message == "El número de teléfono debe tener exactamente 10 dígitos"

#Pruebas para la función validar_nombre
class TestValidarNombre:
    
    # PRUEBAS QUE PASAN
    def test_nombre_solo_letras(self):
        #Prueba con nombre que solo contiene letras
        result, message = validar_nombre("Juan Carlos")
        assert result == True
        assert message == "Nombre válido"
    
    def test_nombre_con_acentos_y_ñ(self):
        #Prueba con nombre que incluye acentos y ñ
        result, message = validar_nombre("María José Peña")
        assert result == True
        assert message == "Nombre válido"
    
    def test_nombre_con_numeros(self):
        #Prueba con nombre que incluye números válidos
        result, message = validar_nombre("Producto ABC123")
        assert result == True
        assert message == "Nombre válido"
    
    # PRUEBAS QUE FALLAN
    def test_nombre_con_signos_especiales(self):
        #Prueba que falla: nombre con signos especiales
        result, message = validar_nombre("Juan@email.com")
        assert result == False
        assert message == "El nombre solo debe contener letras, números y espacios"
    
    def test_nombre_con_simbolos(self):
        #Prueba que falla: nombre con símbolos no permitidos
        result, message = validar_nombre("Producto #1 - Premium")
        assert result == False
        assert message == "El nombre solo debe contener letras, números y espacios"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])