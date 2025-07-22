// Configuración de la API
const API_BASE_URL = 'http://127.0.0.1:5000'; // Cambia esto por tu URL de API

// Variables de estado global
let createSubmitHandler = null;
let currentEditId = null;

// Función para mostrar vistas
function showView(viewId) {
    // Ocultar todas las vistas
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });
    
    // Mostrar la vista seleccionada
    document.getElementById(viewId).classList.add('active');
    
    // Actualizar botones activos
    document.querySelectorAll('.nav-button').forEach(button => {
        button.classList.remove('active');
    });
    
    // Marcar el botón correspondiente como activo
    const buttons = document.querySelectorAll('.nav-button');
    if (viewId === 'offers-view') {
        buttons[1].classList.add('active');
    } else if (viewId === 'candidates-view') {
        buttons[2].classlist.add('active');
    } else {
        buttons[0].classList.add('active');
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
    document.getElementById('offers-loading').style.display = 'block';
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
                        <td colspan="4" style="text-align: center;">No hay ofertas disponibles</td>
                    </tr>
                `;
                document.getElementById('offers-table').style.display = 'table';
            }
        })
        .catch(error => {
            console.error('Error al cargar las ofertas:', error);
            document.getElementById('offers-loading').style.display = 'none';
            document.getElementById('offers-error').style.display = 'block';
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
            <td>${offer.puesto}</td>
            <td>${offer.etiquetas}</td>
            <td>${offer.reclutador}</td>
            <td>
                <button class="action-btn view-btn" onclick="viewOffer(${offer.id})">Ver</button>
                <button class="action-btn edit-btn" onclick="editOffer(${offer.id})">Editar</button>
                <button class="action-btn delete-btn" onclick="deleteOffer(${offer.id})">Eliminar</button>
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
        document.querySelector('#offer-form button[type="submit"]').textContent = 'Guardar Oferta';
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
            document.querySelector('#offer-form button[type="submit"]').textContent = 'Actualizar Oferta';
            
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
                    body: JSON.stringify(updatedOffer)
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
            body: JSON.stringify({ id: offerId })
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

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    setupCreateForm(); // Configurar formulario para creación por defecto
    showOffersView();
});