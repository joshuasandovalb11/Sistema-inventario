// Configuración de páginas disponibles y sus rutas
const pages = {
    'dashboard': '/pages/dashboard-content.html',
    'inventario': '/pages/inventario.html',
    'reporte': '/pages/reporte.html',
    'proveedores': '/pages/proveedores.html',
    'ventas': '/pages/ventas.html',
    'ajustes': '/pages/ajustes.html'
};

// Estado actual de la aplicación
let currentPage = 'dashboard';

// Elementos DOM
const contentArea = document.getElementById('content-area');
const loadingIndicator = document.getElementById('loading-indicator');
const menuLinks = document.querySelectorAll('[data-page]');

// Añade esta función para inicializar los modales después de cargar el contenido
function initializeModals() {
    // Para la página de inventario
    const btnAgregarProducto = document.getElementById('btn-agregar-producto');
    const modalAgregarProducto = document.getElementById('modal-agregar-producto');
    const btnDescartarProducto = document.getElementById('btn-descartar');
    
    if (btnAgregarProducto && modalAgregarProducto) {
        btnAgregarProducto.addEventListener('click', function() {
            modalAgregarProducto.classList.remove('hidden');
        });
        
        if (btnDescartarProducto) {
            btnDescartarProducto.addEventListener('click', function() {
                modalAgregarProducto.classList.add('hidden');
            });
        }
        
        // Cerrar modal al hacer clic fuera
        modalAgregarProducto.addEventListener('click', function(e) {
            if (e.target === modalAgregarProducto) {
                modalAgregarProducto.classList.add('hidden');
            }
        });
    }
    
    // Para la página de proveedores
    const btnAgregarProveedor = document.getElementById('btn-agregar-proveedor');
    const modalAgregarProveedor = document.getElementById('modal-agregar-proveedor');
    const btnDescartarProveedor = document.getElementById('btn-descartar-proveedor');
    
    if (btnAgregarProveedor && modalAgregarProveedor) {
        btnAgregarProveedor.addEventListener('click', function() {
            modalAgregarProveedor.classList.remove('hidden');
        });
        
        if (btnDescartarProveedor) {
            btnDescartarProveedor.addEventListener('click', function() {
                modalAgregarProveedor.classList.add('hidden');
            });
        }
        
        // Cerrar modal al hacer clic fuera
        modalAgregarProveedor.addEventListener('click', function(e) {
            if (e.target === modalAgregarProveedor) {
                modalAgregarProveedor.classList.add('hidden');
            }
        });
    }
}

// Función para cargar contenido
async function loadContent(pageName) {
    // No recargamos si ya estamos en la página
    if (pageName === currentPage && contentArea.innerHTML !== '') {
        return;
    }

    try {
        // Mostrar indicador de carga
        contentArea.innerHTML = '';
        loadingIndicator.classList.remove('hidden');
        contentArea.appendChild(loadingIndicator);

        // Actualizar estado
        currentPage = pageName;
        
        // Actualizar URL (opcional, para poder usar el botón atrás)
        history.pushState({page: pageName}, pageName, `#${pageName}`);
        
        // Actualizar clases del menú
        updateMenuClasses(pageName);

        // Simular una pequeña latencia para mostrar el loader (eliminar en producción)
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // Cargar el contenido
        const response = await fetch(pages[pageName]);
        
        if (!response.ok) {
            throw new Error(`Error al cargar ${pages[pageName]}: ${response.statusText}`);
        }
        
        const html = await response.text();
        
        // Ocultar indicador de carga
        loadingIndicator.classList.add('hidden');
        
        // Insertar el nuevo contenido
        contentArea.innerHTML = html;

        // Ejecutar cualquier script que venga en el contenido
        executeScripts(contentArea);

        // Inicializar los modales después de cargar el contenido
        initializeModals();
        
    } catch (error) {
        console.error('Error al cargar el contenido:', error);
        contentArea.innerHTML = `
            <div class="p-6 bg-red-50 text-red-500 rounded-lg">
                <h3 class="font-medium text-lg">Error al cargar la página</h3>
                <p>${error.message}</p>
                <button onclick="loadContent('dashboard')" class="mt-4 px-4 py-2 bg-primary text-white rounded-md">
                    Volver al Dashboard
                </button>
            </div>
        `;
        loadingIndicator.classList.add('hidden');
    }
}

// Función para ejecutar scripts en el contenido cargado
function executeScripts(container) {
    // Buscar todos los scripts en el contenido
    const scripts = container.querySelectorAll('script');
    
    scripts.forEach(script => {
        // Crear un nuevo elemento script
        const newScript = document.createElement('script');
        
        // Copiar atributos
        Array.from(script.attributes).forEach(attr => {
            newScript.setAttribute(attr.name, attr.value);
        });
        
        // Copiar contenido interno
        newScript.innerHTML = script.innerHTML;
        
        // Reemplazar el viejo script con el nuevo para que se ejecute
        script.parentNode.replaceChild(newScript, script);
    });
}

// Función para actualizar las clases del menú
function updateMenuClasses(activePage) {
    menuLinks.forEach(link => {
        const page = link.getAttribute('data-page');
        
        // Remover clases activas
        link.classList.remove('text-primary');
        link.classList.add('text-gray-600');
        
        // Agregar clase activa al elemento del menú actual
        if (page === activePage) {
            link.classList.remove('text-gray-600');
            link.classList.add('text-primary');
        }
    });
}

// Configurar los event listeners para los links del menú
menuLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const page = link.getAttribute('data-page');
        loadContent(page);
    });
});

// Manejar navegación con botones atrás/adelante del navegador
window.addEventListener('popstate', (event) => {
    if (event.state && event.state.page) {
        loadContent(event.state.page);
    } else {
        // Si no hay estado, cargar la página principal
        loadContent('dashboard');
    }
});

// Inicializar la aplicación cargando la página del hash URL o el dashboard por defecto
document.addEventListener('DOMContentLoaded', () => {
    // Verificar si hay un hash en la URL
    const hash = window.location.hash.substring(1);
    if (hash && pages[hash]) {
        loadContent(hash);
    } else {
        loadContent('dashboard');
    }
});