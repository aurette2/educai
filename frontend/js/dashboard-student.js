// Configuration du gateway
const GATEWAY_URL = 'http://localhost:8080';

// État global pour stocker les données de l'utilisateur
let userData = {
    profile: null,
    activities: [],
    progress: {},
    badges: []
};

// Fonction pour vérifier si l'utilisateur est connecté
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'index.html';
        return false;
    }
    return token;
}

// Fonction pour charger les données du profil
async function loadProfile() {
    const token = checkAuth();
    try {
        const response = await fetch(`${GATEWAY_URL}/user/profile`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) throw new Error('Erreur lors du chargement du profil');
        
        userData.profile = await response.json();
        updateProfileUI();
    } catch (error) {
        console.error('Erreur:', error);
        showNotification('Erreur lors du chargement du profil', 'error');
    }
}

// Fonction pour charger les activités récentes
async function loadActivities() {
    const token = checkAuth();
    try {
        const response = await fetch(`${GATEWAY_URL}/user/activities`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) throw new Error('Erreur lors du chargement des activités');
        
        userData.activities = await response.json();
        updateActivitiesUI();
    } catch (error) {
        console.error('Erreur:', error);
        showNotification('Erreur lors du chargement des activités', 'error');
    }
}

// Fonction pour charger les progrès
async function loadProgress() {
    const token = checkAuth();
    try {
        const response = await fetch(`${GATEWAY_URL}/analytics/stats`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) throw new Error('Erreur lors du chargement des progrès');
        
        userData.progress = await response.json();
        updateProgressUI();
    } catch (error) {
        console.error('Erreur:', error);
        showNotification('Erreur lors du chargement des progrès', 'error');
    }
}

// Fonction pour charger les badges
async function loadBadges() {
    const token = checkAuth();
    try {
        const response = await fetch(`${GATEWAY_URL}/gamification/achievements`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) throw new Error('Erreur lors du chargement des badges');
        
        userData.badges = await response.json();
        updateBadgesUI();
    } catch (error) {
        console.error('Erreur:', error);
        showNotification('Erreur lors du chargement des badges', 'error');
    }
}

// Fonctions de mise à jour de l'interface utilisateur
function updateProfileUI() {
    if (!userData.profile) return;

    // Mise à jour des informations du profil
    const profileName = document.querySelector('.profile-name');
    const profileClass = document.querySelector('.profile-class');
    const profileSchool = document.querySelector('.profile-school');
    
    if (profileName) profileName.textContent = userData.profile.name;
    if (profileClass) profileClass.textContent = userData.profile.class;
    if (profileSchool) profileSchool.textContent = userData.profile.school;

    // Mise à jour des statistiques générales
    const averageScore = document.querySelector('.average-score');
    const completedExercises = document.querySelector('.completed-exercises');
    const studyTime = document.querySelector('.study-time');
    
    if (averageScore) averageScore.textContent = `${userData.profile.average}/20`;
    if (completedExercises) completedExercises.textContent = userData.profile.completedExercises;
    if (studyTime) studyTime.textContent = formatStudyTime(userData.profile.studyTimeMinutes);
}

function updateActivitiesUI() {
    const activitiesContainer = document.querySelector('.activities-container');
    if (!activitiesContainer) return;
    
    activitiesContainer.innerHTML = '';

    userData.activities.forEach(activity => {
        const activityElement = createActivityElement(activity);
        activitiesContainer.appendChild(activityElement);
    });
}

function updateProgressUI() {
    Object.entries(userData.progress).forEach(([subject, progress]) => {
        const progressBar = document.querySelector(`[data-subject="${subject}"] .progress-bar`);
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
            progressBar.setAttribute('aria-valuenow', progress);
        }
    });
}

function updateBadgesUI() {
    const badgesContainer = document.querySelector('.badges-container');
    if (!badgesContainer) return;
    
    badgesContainer.innerHTML = '';

    userData.badges.forEach(badge => {
        const badgeElement = createBadgeElement(badge);
        badgesContainer.appendChild(badgeElement);
    });
}

// Fonctions utilitaires
function formatStudyTime(minutes) {
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return `${hours}h ${remainingMinutes}m`;
}

function createActivityElement(activity) {
    const div = document.createElement('div');
    div.className = 'activity-card p-4 bg-gray-50 rounded-lg';
    div.innerHTML = `
        <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="h-10 w-10 rounded-full bg-${activity.type}-100 flex items-center justify-center">
                    <svg class="h-6 w-6 text-${activity.type}-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        ${getActivityIcon(activity.type)}
                    </svg>
                </div>
                <div>
                    <h3 class="text-sm font-medium text-gray-900">${activity.title}</h3>
                    <p class="text-sm text-gray-600">${activity.description}</p>
                </div>
            </div>
            <span class="text-sm text-gray-500">${formatTimeAgo(activity.timestamp)}</span>
        </div>
    `;
    return div;
}

function createBadgeElement(badge) {
    const div = document.createElement('div');
    div.className = 'text-center';
    div.innerHTML = `
        <div class="h-16 w-16 mx-auto bg-${badge.color}-100 rounded-full flex items-center justify-center mb-2">
            <svg class="h-8 w-8 text-${badge.color}-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                ${getBadgeIcon(badge.type)}
            </svg>
        </div>
        <span class="text-sm font-medium text-gray-900">${badge.name}</span>
    `;
    return div;
}

function getActivityIcon(type) {
    const icons = {
        'exercise': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>',
        'lesson': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>',
        'quiz': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>'
    };
    return icons[type] || icons['exercise'];
}

function getBadgeIcon(type) {
    const icons = {
        'expert': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path>',
        'reader': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>'
    };
    return icons[type] || icons['expert'];
}

function formatTimeAgo(timestamp) {
    const now = new Date();
    const date = new Date(timestamp);
    const seconds = Math.floor((now - date) / 1000);

    const intervals = {
        année: 31536000,
        mois: 2592000,
        semaine: 604800,
        jour: 86400,
        heure: 3600,
        minute: 60
    };

    for (let [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return `Il y a ${interval} ${unit}${interval > 1 ? 's' : ''}`;
        }
    }

    return 'À l\'instant';
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed bottom-4 right-4 p-4 rounded-lg shadow-lg ${type === 'error' ? 'bg-red-500' : 'bg-green-500'} text-white z-50`;
    notification.textContent = message;

    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

// Initialisation du tableau de bord
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadProfile();
    loadActivities();
    loadProgress();
    loadBadges();

    // Gestionnaire pour la déconnexion
    document.querySelector('.logout-button')?.addEventListener('click', () => {
        localStorage.removeItem('token');
        window.location.href = 'index.html';
    });
});