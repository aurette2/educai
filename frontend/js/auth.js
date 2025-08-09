// Configuration de l'URL du gateway
const GATEWAY_URL = 'http://localhost:8080';

// Fonction pour afficher les messages d'erreur
function showError(message) {
    const loginForm = document.getElementById('loginForm');
    const existingAlert = loginForm.querySelector('.alert');
    if (existingAlert) {
        existingAlert.remove();
    }

    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show mt-3';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    loginForm.appendChild(alertDiv);
}

// Fonction pour vérifier si l'utilisateur est déjà authentifié
async function checkAuth() {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
        return false;
    }

    try {
        const response = await fetch(`${GATEWAY_URL}/auth/verify`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            return true;
        } else if (response.status === 401) {
            const refreshed = await refreshToken();
            return refreshed;
        }

        return false;
    } catch (error) {
        console.error('Erreur lors de la vérification de l\'authentification:', error);
        return false;
    }
}

// Fonction pour rafraîchir le token
async function refreshToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        return false;
    }

    try {
        const response = await fetch(`${GATEWAY_URL}/auth/token/refresh`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ refresh: refreshToken })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('accessToken', data.access);
            return true;
        }

        return false;
    } catch (error) {
        console.error('Erreur lors du rafraîchissement du token:', error);
        return false;
    }
}

// Fonction pour nettoyer les données d'authentification
function clearAuthData() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('username');
    localStorage.removeItem('role');
}

// Redirection vers le tableau de bord si déjà authentifié
document.addEventListener('DOMContentLoaded', async () => {
    const isAuthenticated = await checkAuth();
    if (isAuthenticated && window.location.pathname.endsWith('index.html')) {
        window.location.href = 'dashboard.html';
    }
});

// Gestion du formulaire de connexion
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${GATEWAY_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('accessToken', data.access);
            localStorage.setItem('refreshToken', data.refresh);
            localStorage.setItem('username', username);
            localStorage.setItem('role', data.role);
            window.location.href = 'dashboard.html';
        } else {
            showError(data.message || 'Identifiants invalides');
        }
    } catch (error) {
        console.error('Erreur lors de la connexion:', error);
        showError('Une erreur est survenue lors de la connexion. Veuillez réessayer.');
    }
});