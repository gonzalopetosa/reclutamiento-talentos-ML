// app.js
// Configuración de la API
const API_BASE_URL = 'http://127.0.0.1:5000';

// Variables de estado global
let createSubmitHandler = null;
let currentEditId = null;

function getCookie(nombre) {
    const match = document.cookie.match(new RegExp('(^| )' + nombre + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
}

function completarDatosUsuario() {
    const email = getCookie("reclutador_email") || "No disponible";
    const rol = getCookie("reclutador_rol") || "Reclutador";

    document.getElementById("username-display").textContent = email;
    document.getElementById("user-role-display").textContent = rol;
}

document.addEventListener('DOMContentLoaded', completarDatosUsuario);

// Función para mostrar vistas
function showView(viewId) {
    // Ocultar todas las vistas
    document.querySelectorAll('.tech-view').forEach(view => {
        view.classList.remove('active');
    });
    
    // Mostrar la vista seleccionada
    document.getElementById(viewId).classList.add('active');
    
    // Actualizar elementos activos en el menú
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Actualizar botón activo basado en la vista
    if (viewId === 'offers-view') {
        document.querySelectorAll('.nav-item')[0].classList.add('active');
    } else if (viewId === 'candidates-view') {
        document.querySelectorAll('.nav-item')[1].classList.add('active');
    } else if (viewId === 'analytics-view') {
        document.querySelectorAll('.nav-item')[2].classList.add('active');
    }
}

// Función específica para mostrar la vista de ofertas y cargar los datos
function showOffersView() {
    showView('offers-view');
    loadOffers();
}

// Función para cargar ofertas desde la API
function loadOffers() {
    // Mostrar estado de carga
    document.getElementById('offers-loading').style.display = 'flex';
    document.getElementById('offers-table').style.display = 'none';
    document.getElementById('offers-error').style.display = 'none';
    document.getElementById('add-offer-form').style.display = 'none';
    
    // Hacer la petición a la API
    fetch(`${API_BASE_URL}/oferta/all`, {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta de la red');
        }
        return response.json();
    })
    .then(offers => {
        // Ocultar estado de carga
        document.getElementById('offers-loading').style.display = 'none';
        
        // Verificar si hay ofertas
        if (offers && offers.length > 0) {
            renderOffersTable(offers);
        } else {
            // Mostrar mensaje si no hay ofertas
            document.getElementById('offers-table-body').innerHTML = `
                <tr>
                    <td colspan="5" style="text-align: center;">No hay ofertas disponibles</td>
                </tr>
            `;
            document.getElementById('offers-table').style.display = 'table';
        }
    })
    .catch(error => {
        console.error('Error al cargar las ofertas:', error);
        document.getElementById('offers-loading').style.display = 'none';
        document.getElementById('offers-error').style.display = 'flex';
    });
}

// Función para renderizar la tabla de ofertas
function renderOffersTable(offers) {
    const tableBody = document.getElementById('offers-table-body');
    tableBody.innerHTML = '';
    
    // Agregar cada oferta a la tabla
    offers.forEach(offer => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>
                <div class="offer-title">
                    <i class="fas fa-briefcase"></i>
                    <div>
                        <div>${offer.puesto}</div>
                        <div class="offer-id">#ID-${offer.id}</div>
                    </div>
                </div>
            </td>
            <td>
                <div class="tech-tags">
                    ${offer.etiquetas.split(',').map(tag => `<span>${tag.trim()}</span>`).join('')}
                </div>
            </td>
            <td>${offer.reclutador}</td>
            <td><span class="status-badge active">Activa</span></td>
            <td>
                <div class="action-buttons">
                    <button class="action-btn view" onclick="viewOffer(${offer.id})"><i class="fas fa-eye"></i></button>
                    <button class="action-btn edit" onclick="editOffer(${offer.id})"><i class="fas fa-edit"></i></button>
                    <button class="action-btn delete" onclick="deleteOffer(${offer.id})"><i class="fas fa-trash"></i></button>
                </div>
            </td>
        `;
        tableBody.appendChild(row);
    });
    
    // Mostrar la tabla
    document.getElementById('offers-table').style.display = 'table';
}

// Función para mostrar el formulario de agregar oferta
function showAddOfferForm() {
    document.getElementById('offers-table').style.display = 'none';
    document.getElementById('add-offer-form').style.display = 'block';
    document.getElementById('offer-form').reset();
    
    // Restablecer textos si estamos en modo creación
    if (!currentEditId) {
        document.querySelector('#add-offer-form h3').textContent = 'Agregar Nueva Oferta';
        document.querySelector('#offer-form button[type="submit"]').innerHTML = '<i class="fas fa-save"></i> Guardar Oferta';
    }
}

// Función para cancelar la adición de oferta
function cancelAddOffer() {
    document.getElementById('add-offer-form').style.display = 'none';
    document.getElementById('offers-table').style.display = 'table';
    currentEditId = null;
    setupCreateForm(); // Restaurar modo creación
}

// Configurar el formulario para creación de ofertas
function setupCreateForm() {
    const form = document.getElementById('offer-form');
    
    // Eliminar cualquier manejador previo
    form.onsubmit = null;
    if (createSubmitHandler) {
        form.removeEventListener('submit', createSubmitHandler);
    }
    
    // Configurar nuevo manejador para creación
    createSubmitHandler = function(e) {
        e.preventDefault();
        
        const newOffer = {
            puesto: document.getElementById('offer-puesto').value,
            etiquetas: document.getElementById('offer-etiquetas').value,
            id_reclutador: document.getElementById('offer-reclutador').value,
        };
        
        fetch(`${API_BASE_URL}/oferta/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newOffer),
            credentials: 'include'
        })
        .then(response => {
            if (!response.ok) throw new Error('Error al crear la oferta');
            return response.json();
        })
        .then(() => {
            alert('Oferta creada con éxito');
            cancelAddOffer();
            loadOffers();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al crear la oferta');
        });
    };
    
    form.addEventListener('submit', createSubmitHandler);
    currentEditId = null;
}

// Función para editar una oferta
function editOffer(offerId) {
    currentEditId = offerId;
    
    fetch(`${API_BASE_URL}/oferta/get/${offerId}`)
        .then(response => response.json())
        .then(offer => {
            document.getElementById('offer-puesto').value = offer.puesto;
            document.getElementById('offer-etiquetas').value = offer.etiquetas;
            document.getElementById('offer-reclutador').value = offer.id_reclutador;
            
            showAddOfferForm();
            document.querySelector('#add-offer-form h3').textContent = 'Editar Oferta';
            document.querySelector('#offer-form button[type="submit"]').innerHTML = '<i class="fas fa-save"></i> Actualizar Oferta';
            
            const form = document.getElementById('offer-form');
            form.onsubmit = null;
            if (createSubmitHandler) {
                form.removeEventListener('submit', createSubmitHandler);
            }
            
            form.addEventListener('submit', function editSubmitHandler(e) {
                e.preventDefault();
                
                const updatedOffer = {
                    id: currentEditId,
                    puesto: document.getElementById('offer-puesto').value,
                    etiquetas: document.getElementById('offer-etiquetas').value,
                    id_reclutador: document.getElementById('offer-reclutador').value
                };
                
                fetch(`${API_BASE_URL}/oferta/modify`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(updatedOffer),
                    credentials: 'include'
                })
                .then(response => {
                    if (!response.ok) throw new Error('Error al actualizar');
                    return response.json();
                })
                .then(() => {
                    alert('Oferta actualizada con éxito');
                    cancelAddOffer();
                    loadOffers();
                    setupCreateForm(); // Restaurar modo creación
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert(error.Error || 'Error al actualizar');
                });
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al obtener datos');
        });
}

// Función para eliminar una oferta
function deleteOffer(offerId) {
    if (confirm('¿Estás seguro de que deseas eliminar esta oferta?')) {
        fetch(`${API_BASE_URL}/oferta/delete/id`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: offerId }),
            credentials: 'include'
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; });
            }
            return response.json();
        })
        .then(data => {
            alert(data.data || 'Oferta eliminada con éxito');
            loadOffers();
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.Error || 'Error al eliminar la oferta');
        });
    }
}

// Función para ver una oferta
function viewOffer(offerId) {
    fetch(`${API_BASE_URL}/oferta/get/${offerId}`)
        .then(response => response.json())
        .then(offer => {
            alert(`Detalles de la oferta:\nPuesto: ${offer.puesto}\nEtiquetas: ${offer.etiquetas}\nReclutador: ${offer.id_reclutador}`);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al obtener detalles de la oferta');
        });
}

// Función para cerrar sesión
function logout() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        fetch(`${API_BASE_URL}/auth/logout`, {
            method: 'POST',
            credentials: 'include'
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/login';
            }
        })
        .catch(error => {
            console.error('Error al cerrar sesión:', error);
        });
    }
}

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    setupCreateForm(); // Configurar formulario para creación por defecto
    showOffersView();
    
    // Añadir efecto de iluminación a los elementos principales
    setTimeout(() => {
        document.querySelector('.tech-logo').classList.add('glow');
        document.querySelector('.tech-btn.primary').classList.add('glow');
    }, 1000);
});