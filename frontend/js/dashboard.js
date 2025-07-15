// Configuration de l'URL du gateway
const GATEWAY_URL = 'http://localhost:8080';

// Fonction pour formater les dates
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('fr-FR', options);
}

// Fonction pour rafraîchir le token
async function refreshToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        window.location.href = 'index.html';
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

        window.location.href = 'index.html';
        return false;
    } catch (error) {
        console.error('Erreur lors du rafraîchissement du token:', error);
        window.location.href = 'index.html';
        return false;
    }
}

// Fonction pour effectuer des requêtes authentifiées
async function authenticatedFetch(url, options = {}) {
    let accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
        window.location.href = 'index.html';
        return null;
    }

    // Ajouter le token aux headers
    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
    };

    try {
        const response = await fetch(url, { ...options, headers });

        if (response.status === 401) {
            // Tenter de rafraîchir le token
            const refreshed = await refreshToken();
            if (!refreshed) return null;

            // Réessayer la requête avec le nouveau token
            accessToken = localStorage.getItem('accessToken');
            headers.Authorization = `Bearer ${accessToken}`;
            return await fetch(url, { ...options, headers });
        }

        return response;
    } catch (error) {
        console.error('Erreur lors de la requête:', error);
        return null;
    }
}

// Fonction pour charger les statistiques
async function loadStatistics() {
    const response = await authenticatedFetch(`${GATEWAY_URL}/analytics/stats`);
    if (!response || !response.ok) return;

    const stats = await response.json();
    updateDashboardStats(stats);
}

// Fonction pour charger les activités récentes
async function loadRecentActivities() {
    const response = await authenticatedFetch(`${GATEWAY_URL}/user/activities`);
    if (!response || !response.ok) return;

    const activities = await response.json();
    updateRecentActivities(activities);
}

// Fonction pour mettre à jour les statistiques du tableau de bord
function updateDashboardStats(stats) {
    document.getElementById('totalCourses').textContent = stats.total_courses || 0;
    document.getElementById('completedLessons').textContent = stats.completed_lessons || 0;
    document.getElementById('averageScore').textContent = stats.average_score ? `${stats.average_score}%` : 'N/A';
    document.getElementById('totalTime').textContent = stats.total_time || '0h';
}

// Fonction pour mettre à jour les activités récentes
function updateRecentActivities(activities) {
    const activitiesList = document.getElementById('recentActivities');
    activitiesList.innerHTML = '';

    activities.forEach(activity => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
            <div>
                <i class="bi ${getActivityIcon(activity.type)} me-2"></i>
                ${activity.description}
                <small class="text-muted d-block">${formatDate(activity.timestamp)}</small>
            </div>
            ${getActivityBadge(activity.status)}
        `;
        activitiesList.appendChild(li);
    });
}

// Fonction pour obtenir l'icône appropriée selon le type d'activité
function getActivityIcon(type) {
    const icons = {
        'course': 'bi-book',
        'quiz': 'bi-question-circle',
        'assignment': 'bi-pencil',
        'discussion': 'bi-chat-dots',
        'default': 'bi-clock-history'
    };
    return icons[type] || icons.default;
}

// Fonction pour obtenir le badge approprié selon le statut
function getActivityBadge(status) {
    const badges = {
        'completed': '<span class="badge bg-success">Terminé</span>',
        'in_progress': '<span class="badge bg-warning">En cours</span>',
        'pending': '<span class="badge bg-info">En attente</span>',
        'default': ''
    };
    return badges[status] || badges.default;
}

// Fonction pour mettre à jour le rôle de l'utilisateur dans l'interface
function updateUserRole() {
    const role = localStorage.getItem('role');
    const username = localStorage.getItem('username');
    
    // Mettre à jour le nom d'utilisateur
    const userNameElement = document.getElementById('userName');
    if (userNameElement) {
        userNameElement.textContent = username || 'Utilisateur';
    }

    // Afficher/masquer les éléments selon le rôle
    const teacherElements = document.querySelectorAll('.teacher-only');
    const studentElements = document.querySelectorAll('.student-only');

    teacherElements.forEach(el => {
        el.style.display = role === 'teacher' ? '' : 'none';
    });

    studentElements.forEach(el => {
        el.style.display = role === 'student' ? '' : 'none';
    });
}

// Fonction de déconnexion
function logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('username');
    localStorage.removeItem('role');
    window.location.href = 'index.html';
}

// Initialisation du tableau de bord
async function initializeDashboard() {
    updateUserRole();
    await Promise.all([
        loadStatistics(),
        loadRecentActivities()
    ]);
}

// Événements au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    initializeDashboard();

    // Gestionnaire pour le bouton de déconnexion
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }
});