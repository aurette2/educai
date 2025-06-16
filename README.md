# EducAI2025 – Plateforme Éducative Intelligente

**Version** : 1.0  
**État du projet** : ⚙️ En cours  

---

## Objectif du projet

EducAI2025 est une plateforme web éducative basée sur l’intelligence artificielle, visant à :
- Analyser en temps réel les performances des élèves,
- Proposer des contenus personnalisés (cours, exercices, vidéos),
- Offrir un chatbot éducatif conversationnel,
- Stimuler l’engagement par des éléments de gamification.

---

## Architecture Microservices

| Microservice              | Description principale                                      |
|--------------------------|-------------------------------------------------------------|
| `auth-service`           | Authentification, gestion JWT, rôles utilisateurs           |
| `user-service`           | Profils et données utilisateurs                             |
| `analytics-service`      | Suivi de performance, tracking comportemental               |
| `recommender-service`    | Système de recommandation IA (ML/Scikit-learn)              |
| `chatbot-service`        | Assistant IA conversationnel (OpenAI/Ollama)                |
| `content-service`        | Gestion de contenus pédagogiques                            |
| `gamification-service`   | Système de badges, scores et défis                          |
| `api-gateway`            | Routage et sécurité via Nginx + JWT                         |
| `frontend`               | Interface web (Next.js + Tailwind CSS)                      |



## Stack Technologique

### Backend
- Python 3.11+, Django REST Framework, PostgreSQL
- RabbitMQ / Kafka, Redis, Docker, Django Channels

### IA & ML
- Scikit-learn, XGBoost, Pandas
- sentence-transformers, FAISS
- Ollama / OpenAI, MLflow, Jupyter, W&B

### Frontend
- Next.js ou React.js, Tailwind CSS
- Axios / Fetch (auth via JWT)

### DevOps & MLOps
- Docker, Docker Compose, GitHub Actions
- Nginx, Prometheus, Grafana, ELK Stack


## Structure du projet

```
/ai-learning-platform
│
├── gateway/                  # Nginx Reverse Proxy
├── auth-service/             # JWT Authentication
├── user-service/             # User CRUD
├── analytics-service/        # Tracking et Statistiques
├── recommender-service/      # IA de recommandation
├── chatbot-service/          # LLM pédagogique
├── frontend/                 # UI Next.js + Tailwind
├── docker-compose.yml        # Orchestration locale
├── .github/                  # CI/CD GitHub Actions
└── docs/                     # Documentation technique
```


## Tests

- Tests unitaires (Pytest, DRF)
- Tests d’intégration API (Swagger, Postman)
- Tests manuels UI
- Suivi IA (MLflow, W&B)


## Roadmap

- [-] Auth & User Services
- [-] Infrastructure Docker + Gateway
- [-] MVP Analytics + Recommender
- [-] Frontend : login + dashboard
- [-] Chatbot IA : prototype intégré
- [-] CI/CD + Monitoring de base


## Contributeurs

- **IA Engineer** – Recommandation, NLP, MLOps
- **DevOps 1** – CI/CD, Orchestration, Monitoring
- **DevOps 2** – Backend APIs, Frontend Integration


> Ce projet est sous licence MIT. Pour toute collaboration ou suggestion, veuillez ouvrir une issue ou un pull request.

