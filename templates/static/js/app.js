// Configuración de la API
const API_BASE_URL = 'http://localhost:5000'; // Cambia esto por tu URL de API

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
        buttons[2].classList.add('active');
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
    fetch(`${API_BASE_URL}/oferta/all`)
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
}

// Función para cancelar la adición de oferta
function cancelAddOffer() {
    document.getElementById('add-offer-form').style.display = 'none';
    document.getElementById('offers-table').style.display = 'table';
}

// Función para manejar el envío del formulario
document.getElementById('offer-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const newOffer = {
        puesto: document.getElementById('offer-puesto').value,
        etiquetas: document.getElementById('offer-etiquetas').value,
        id_reclutador: document.getElementById('offer-reclutador').value,
    };
    
    // Enviar la nueva oferta a la API
    fetch(`${API_BASE_URL}/oferta/add`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newOffer)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al crear la oferta');
        }
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
});

// Funciones para manejar acciones de ofertas
function viewOffer(offerId) {
    // Obtener detalles de la oferta
    fetch(`${API_BASE_URL}/oferta/${offerId}`)
        .then(response => response.json())
        .then(offer => {
            alert(`Detalles de la oferta:\nTítulo: ${offer.titulo}\nEmpresa: ${offer.empresa}\nUbicación: ${offer.ubicacion}\nSalario: ${offer.salario}`);
        })
        .catch(error => {
            console.error('Error al obtener detalles de la oferta:', error);
            alert('Error al obtener detalles de la oferta');
        });
}

function editOffer(offerId) {
    // Obtener datos de la oferta
    fetch(`${API_BASE_URL}/oferta/${offerId}`)
        .then(response => response.json())
        .then(offer => {
            // Rellenar formulario con datos existentes
            document.getElementById('offer-title').value = offer.titulo;
            document.getElementById('offer-company').value = offer.empresa;
            document.getElementById('offer-location').value = offer.ubicacion;
            document.getElementById('offer-salary').value = offer.salario;
            document.getElementById('offer-description').value = offer.descripcion;
            
            // Mostrar formulario
            showAddOfferForm();
            
            // Cambiar texto del botón
            document.querySelector('#add-offer-form h3').textContent = 'Editar Oferta';
            document.querySelector('#offer-form button[type="submit"]').textContent = 'Actualizar Oferta';
            
            // Cambiar el evento del formulario para actualizar
            const form = document.getElementById('offer-form');
            form.onsubmit = function(e) {
                e.preventDefault();
                
                const updatedOffer = {
                    titulo: document.getElementById('offer-title').value,
                    empresa: document.getElementById('offer-company').value,
                    ubicacion: document.getElementById('offer-location').value,
                    salario: document.getElementById('offer-salary').value,
                    descripcion: document.getElementById('offer-description').value
                };
                
                // Enviar actualización
                fetch(`${API_BASE_URL}/oferta/${offerId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(updatedOffer)
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error al actualizar la oferta');
                    }
                    return response.json();
                })
                .then(() => {
                    alert('Oferta actualizada con éxito');
                    cancelAddOffer();
                    loadOffers();
                    // Restaurar formulario para crear nuevas ofertas
                    form.onsubmit = arguments.callee;
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error al actualizar la oferta');
                });
            };
        })
        .catch(error => {
            console.error('Error al obtener datos de la oferta:', error);
            alert('Error al obtener datos de la oferta');
        });
}

function deleteOffer(offerId) {
    if (confirm('¿Estás seguro de que deseas eliminar esta oferta?')) {
        fetch(`${API_BASE_URL}/oferta/${offerId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al eliminar la oferta');
            }
            return response.json();
        })
        .then(() => {
            alert('Oferta eliminada con éxito');
            loadOffers();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al eliminar la oferta');
        });
    }
}

// Inicializar la vista de ofertas al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    showOffersView();
});