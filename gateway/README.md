# Service de Passerelle EducAI

Ce service agit comme point d'entrée unique pour toutes les communications entre le frontend et les différents microservices de l'application EducAI.

## Fonctionnalités

- Routage des requêtes vers les services appropriés
- Authentification et autorisation centralisées
- Gestion des tokens JWT
- Communication inter-services sécurisée

## Services Intégrés

- Service d'Authentification (Port 8001)
- Service Utilisateur (Port 8002)
- Service d'Analytique (Port 8003)
- Service de Recommandation (Port 8004)
- Service de Gamification (Port 8005)
- Service Chatbot (Port 8006)

## Configuration Requise

- Python 3.8+
- FastAPI
- Uvicorn
- HTTPX

## Installation

1. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix/macOS
venv\Scripts\activate  # Sur Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Démarrage

1. Lancer le service :
```bash
python app.py
```

Ou avec uvicorn directement :
```bash
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

## Points d'Entrée API

### Authentication
- POST `/auth/login` - Connexion utilisateur
- POST `/auth/token/refresh` - Rafraîchissement du token

### Utilisateur
- GET `/user/profile` - Obtenir le profil utilisateur
- GET `/user/activities` - Obtenir les activités de l'utilisateur

### Analytique
- GET `/analytics/stats` - Obtenir les statistiques utilisateur

### Recommandation
- GET `/recommender/suggestions` - Obtenir des recommandations personnalisées

### Gamification
- GET `/gamification/achievements` - Obtenir les réalisations de l'utilisateur

### Chatbot
- POST `/chatbot/message` - Envoyer un message au chatbot

## Sécurité

Tous les points d'entrée (sauf login et refresh) nécessitent un token JWT valide dans l'en-tête Authorization :
```
Authorization: Bearer <token>
```

## Documentation API

La documentation Swagger UI est disponible à l'adresse :
```
http://localhost:8080/docs
```

## Environnement de Production

Pour la production :
1. Configurer les URLs des services dans des variables d'environnement
2. Restreindre les origines CORS
3. Activer HTTPS
4. Configurer un proxy inverse (nginx recommandé)