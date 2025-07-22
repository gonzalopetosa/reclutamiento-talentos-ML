const API_BASE_URL = 'http://127.0.0.1:5000';

document.addEventListener('DOMContentLoaded', function() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const switchTabs = document.querySelectorAll('.switch-tab');
    
    function switchTab(tabName) {
        tabBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `${tabName}-form`);
        });
    }
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });
    
    switchTabs.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            switchTab(this.dataset.tab);
        });
    });

    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        
        if (!email || !password) {
            showAlert('Por favor completa todos los campos', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}/auth/reclutador/login`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email, contraseña: password}),
                credentials: 'include'
            });
            
            const data = await response.json();
            
            if (response.ok) {
                if (data.Token) {
                    localStorage.setItem('authToken', data.Token);
                    localStorage.setItem('reclutadorId', data['id reclutador']);
                }
                showAlert('¡Inicio de sesión exitoso! Redirigiendo...', 'success');
                setTimeout(() => window.location.href = '/dashboard', 1500);
            } else {
                showAlert(data.error || 'Credenciales incorrectas', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert('Error al conectar con el servidor', 'error');
        }
    });

    const signupForm = document.getElementById('signup-form');
    signupForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const nombre = document.getElementById('full-name').value;
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        const terms = document.getElementById('terms').checked;
        
        if (!nombre || !email || !password || !confirmPassword || !terms) {
            showAlert('Completa todos los campos y acepta los términos.', 'error');
            return;
        }
        if (password !== confirmPassword) {
            showAlert('Las contraseñas no coinciden.', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}/auth/reclutador/register`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({nombre, email, contraseña: password}),
                credentials: 'include'
            });
            const data = await response.json();
            if (response.ok) {
                showAlert('¡Cuenta creada correctamente!', 'success');
                setTimeout(() => switchTab('login'), 2000);
            } else {
                showAlert(data.error || 'Error al crear la cuenta.', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert('Error al conectar con el servidor.', 'error');
        }
    });
});

function showAlert(message, type = 'success') {
    let alert = document.querySelector('.custom-alert');
    if (!alert) {
        alert = document.createElement('div');
        alert.className = 'custom-alert';
        document.body.appendChild(alert);
    }
    alert.className = `custom-alert show ${type}`;
    alert.textContent = message;
    setTimeout(() => alert.classList.remove('show'), 3000);
}
