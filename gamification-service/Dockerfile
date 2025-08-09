FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Variables d'environnement
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=backend.settings

# Exposition du port
EXPOSE 8003

# Commande de démarrage
CMD ["python", "manage.py", "runserver", "0.0.0.0:8003"]