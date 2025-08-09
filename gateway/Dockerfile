FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Variables d'environnement
ENV SERVER_HOST=0.0.0.0
ENV SERVER_PORT=8080
ENV CORS_ORIGINS=*
ENV LOG_LEVEL=INFO

# Exposition du port
EXPOSE 8080

# Commande de démarrage avec un seul worker
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]