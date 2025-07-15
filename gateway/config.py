import os
from typing import Dict

# Configuration des services
SERVICE_URLS: Dict[str, str] = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://localhost:8001"),
    "user": os.getenv("USER_SERVICE_URL", "http://localhost:8002"),
    "analytics": os.getenv("ANALYTICS_SERVICE_URL", "http://localhost:8003"),
    "recommender": os.getenv("RECOMMENDER_SERVICE_URL", "http://localhost:8004"),
    "gamification": os.getenv("GAMIFICATION_SERVICE_URL", "http://localhost:8005"),
    "chatbot": os.getenv("CHATBOT_SERVICE_URL", "http://localhost:8006")
}

# Configuration du serveur
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8080"))

# Configuration CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Configuration de sécurité
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Configuration du client HTTP
HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# Configuration des logs
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"