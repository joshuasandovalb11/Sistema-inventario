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
let currentPageNumber = 1;

// Elementos DOM
const contentArea = document.getElementById('content-area');
const loadingIndicator = document.getElementById('loading-indicator');
const menuLinks = document.querySelectorAll('[data-page]');

// Añade esta función para inicializar los modales después de cargar el contenido
function initializeModals() {
    // Modales generales con data attributes
    document.addEventListener('click', e => {
        // Abrir modal
        const opener = e.target.closest('[data-modal-open]');
        if (opener) {
            const id = opener.dataset.modalOpen;       
            const modal = document.getElementById(id);
            if (modal) modal.classList.remove('hidden');
            return;                                       
        }

        const closer = e.target.closest('[data-modal-close]');
        if (closer) {
            closer.closest('[id]').classList.add('hidden');
            return;
        }

        if (e.target.classList.contains('bg-gray-500') && e.target.classList.contains('bg-opacity-75')) {
            e.target.classList.add('hidden');
        }
    });

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
    
    // Para la página de proveedores - Corregir ID del botón
    const btnAgregarProveedor = document.getElementById('btn-agregar-producto'); // En proveedores.html también usa este ID
    const modalAgregarProveedor = document.getElementById('modal-agregar-producto');
    const btnDescartarProveedor = document.getElementById('btn-descartar');
    
    if (btnAgregarProveedor && modalAgregarProveedor && currentPage === 'proveedores') {
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

    // Para la página de ventas
    const btnVenderProducto = document.getElementById('btn-vender-producto');
    const modalVenderProducto = document.getElementById('modal-vender-producto');
    const btnDescartarVenta = document.getElementById('btn-descartar');
    
    if (btnVenderProducto && modalVenderProducto) {
        btnVenderProducto.addEventListener('click', function() {
            modalVenderProducto.classList.remove('hidden');
        });
        
        if (btnDescartarVenta) {
            btnDescartarVenta.addEventListener('click', function() {
                modalVenderProducto.classList.add('hidden');
            });
        }
        
        // Cerrar modal al hacer clic fuera
        modalVenderProducto.addEventListener('click', function(e) {
            if (e.target === modalVenderProducto) {
                modalVenderProducto.classList.add('hidden');
            }
        });
    }
}

// Nueva función para manejar la paginación
function initializePagination() {
    document.addEventListener('click', function(e) {
        const paginationLink = e.target.closest('a[data-pagination]');
        if (paginationLink) {
            e.preventDefault();
            const pageNumber = paginationLink.dataset.page || 1;
            loadPageWithPagination(currentPage, pageNumber);
        }
    });
}

// Función mejorada para cargar contenido con paginación
async function loadPageWithPagination(pageName, pageNumber = 1) {
    try {
        // Mostrar indicador de carga
        contentArea.innerHTML = '';
        loadingIndicator.classList.remove('hidden');
        contentArea.appendChild(loadingIndicator);

        // Actualizar estado
        currentPage = pageName;
        currentPageNumber = pageNumber;
        
        // Construir URL con parámetros de paginación
        const url = `${pages[pageName]}?page=${pageNumber}`;
        
        // Cargar el contenido
        const response = await fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        if (!response.ok) {
            throw new Error(`Error al cargar ${url}: ${response.statusText}`);
        }
        
        const html = await response.text();
        
        loadingIndicator.classList.add('hidden');
        
        contentArea.innerHTML = html;

        executeScripts(contentArea);

        initializeModals();
        addPaginationAttributes();
        
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

// Función para agregar atributos de paginación a los enlaces existentes
function addPaginationAttributes() {
    // Buscar todos los enlaces de paginación y agregarles el atributo data-pagination
    const paginationLinks = contentArea.querySelectorAll('a[href*="page="]');
    paginationLinks.forEach(link => {
        const url = new URL(link.href, window.location.origin);
        const pageNumber = url.searchParams.get('page');
        if (pageNumber) {
            link.setAttribute('data-pagination', 'true');
            link.setAttribute('data-page', pageNumber);
        }
    });
}

// Función para cargar contenido (versión original mejorada)
async function loadContent(pageName, pageNumber = 1) {
    // Si estamos cargando la misma página sin paginación, usar paginación
    if (pageName === currentPage && pageNumber !== currentPageNumber) {
        return loadPageWithPagination(pageName, pageNumber);
    }
    
    // No recargamos si ya estamos en la página y es la misma página de paginación
    if (pageName === currentPage && pageNumber === currentPageNumber && contentArea.innerHTML !== '') {
        return;
    }

    try {
        // Mostrar indicador de carga
        contentArea.innerHTML = '';
        loadingIndicator.classList.remove('hidden');
        contentArea.appendChild(loadingIndicator);

        // Actualizar estado
        currentPage = pageName;
        currentPageNumber = pageNumber;
        
        // Actualizar URL (opcional, para poder usar el botón atrás)
        const urlFragment = pageNumber > 1 ? `${pageName}?page=${pageNumber}` : pageName;
        history.pushState({page: pageName, pageNumber: pageNumber}, pageName, `#${urlFragment}`);
        
        // Actualizar clases del menú
        updateMenuClasses(pageName);

        // Simular una pequeña latencia para mostrar el loader (eliminar en producción)
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // Construir URL con parámetros de paginación
        const url = pageNumber > 1 ? `${pages[pageName]}?page=${pageNumber}` : pages[pageName];
        
        // Cargar el contenido
        const response = await fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        if (!response.ok) {
            throw new Error(`Error al cargar ${url}: ${response.statusText}`);
        }
        
        const html = await response.text();
        
        // Ocultar indicador de carga
        loadingIndicator.classList.add('hidden');
        
        // Insertar el nuevo contenido
        contentArea.innerHTML = html;

        // Ejecutar cualquier script que venga en el contenido
        executeScripts(contentArea);

        // Inicializar los modales y paginación después de cargar el contenido
        initializeModals();
        addPaginationAttributes();
        
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
        loadContent(page, 1); // Siempre empezar en la página 1 al cambiar de sección
    });
});

// Manejar navegación con botones atrás/adelante del navegador
window.addEventListener('popstate', (event) => {
    if (event.state && event.state.page) {
        loadContent(event.state.page, event.state.pageNumber || 1);
    } else {
        // Si no hay estado, cargar la página principal
        loadContent('dashboard');
    }
});

// Inicializar la aplicación cargando la página del hash URL o el dashboard por defecto
document.addEventListener('DOMContentLoaded', () => {
    // Inicializar paginación
    initializePagination();
    
    // Verificar si hay un hash en la URL
    const hash = window.location.hash.substring(1);
    if (hash && pages[hash]) {
        loadContent(hash);
    } else {
        loadContent('dashboard');
    }
});