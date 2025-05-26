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

// Funcion para cargar contenido de una página específica
async function loadContent(pageName, pageNumber = 1) {
    console.log(`loadContent llamado con: ${pageName}, página: ${pageNumber}`);
    console.log(`Estado actual: currentPage=${currentPage}, currentPageNumber=${currentPageNumber}`);
    
    // Si estamos cargando la misma página sin paginación, usar paginación
    if (pageName === currentPage && pageNumber !== currentPageNumber) {
        return loadPageWithPagination(pageName, pageNumber);
    }
    
    // Solo evitar recarga si es exactamente la misma página Y ya hay contenido Y no es recarga inicial
    if (pageName === currentPage && 
        pageNumber === currentPageNumber && 
        contentArea.innerHTML !== '' && 
        !contentArea.innerHTML.includes('loading-indicator') &&
        !window.location.hash.includes(pageName)) {
        console.log('Contenido ya cargado, no recargando');
        return;
    }

    try {
        console.log('Iniciando carga de contenido...');
        
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
        
        console.log('Cargando URL:', url);
        
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
        
        console.log(`Contenido de ${pageName} cargado exitosamente`);

        // Ejecutar cualquier script que venga en el contenido
        executeScripts(contentArea);

        // Inicializar los modales y paginación después de cargar el contenido
        initializeModals();
        addPaginationAttributes();
        
        // Inicializar gráfico solo si estamos en dashboard
        if (pageName === 'dashboard') {
            console.log('Iniciando gráfico para dashboard');
            waitForElementVisible('#ventasChart', () => {
                initializeChart();
            });
        }
        
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

function waitForElementVisible(selector, callback, retries = 20) {
    const el = document.querySelector(selector);
    const isVisible = el && el.offsetWidth > 0 && el.offsetHeight > 0;

    if (isVisible) {
        callback(el);
    } else if (retries > 0) {
        setTimeout(() => waitForElementVisible(selector, callback, retries - 1), 100);
    } else {
        console.warn(`Elemento ${selector} no visible tras múltiples intentos`);
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

    if (currentPage === 'dashboard' || currentPage === 'dashboard-content.html') {
        console.log("estas en el dashboard")
        waitForElementVisible('#ventasChart', () => {
            initializeChart();
        });
    }
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

// Funcion para verificar y redirigir al hash
function ensureHashRoute() {
    // Si no hay hash en la URL, redirigir a #dashboard
    if (!window.location.hash || window.location.hash === '#') {
        console.log('No hay hash, redirigiendo a #dashboard');
        window.location.hash = '#dashboard';
        return true; // Indica que se hizo una redirección
    }
    return false; // No se hizo redirección
}

// Inicialización principal
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded - Iniciando aplicación');
    console.log('URL actual:', window.location.href);
    console.log('Hash actual:', window.location.hash);
    
    initializePagination();

    // Verificar y redirigir al hash si es necesario
    const wasRedirected = ensureHashRoute();
    
    if (wasRedirected) {
        console.log('Se hizo redirección automática, esperando al hashchange...');
        // El hashchange event se encargará de cargar el contenido
        return;
    }

    // Obtener la página inicial del hash
    let initialPage = window.location.hash.substring(1);
    
    // Extraer solo el nombre de la página (por si hay parámetros como ?page=2)
    if (initialPage.includes('?')) {
        initialPage = initialPage.split('?')[0];
    }
    
    console.log('Página inicial detectada:', initialPage);
    
    // Validar si la página existe
    if (!initialPage || !pages[initialPage]) {
        console.log('Página no válida, redirigiendo a dashboard');
        window.location.hash = '#dashboard';
        return;
    }

    // Cargar contenido inmediatamente
    console.log('Cargando contenido de:', initialPage);
    loadContent(initialPage, 1);
});

// Escuchar cambios de hash (cuando haces click en menú por ejemplo)
window.addEventListener('hashchange', () => {
    const newHash = window.location.hash.substring(1);
    let pageName = newHash;
    
    // Extraer solo el nombre de la página si hay parámetros
    if (pageName.includes('?')) {
        pageName = pageName.split('?')[0];
    }
    
    console.log('Hash cambió a:', newHash, 'Página:', pageName);
    
    // Si no hay página o no es válida, redirigir a dashboard
    if (!pageName || !pages[pageName]) {
        console.log('Hash inválido, redirigiendo a dashboard');
        window.location.hash = '#dashboard';
        return;
    }
    
    // Solo cargar si es diferente a la página actual
    if (pageName !== currentPage) {
        console.log('Cargando nueva página desde hashchange:', pageName);
        loadContent(pageName, 1);
    }
});