# Utiliser l'image officielle Python
FROM python:3.10-slim

# Empêcher Python de créer des fichiers .pyc et activer le flush stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer dépendances système pour SQLite et compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Définir le dossier de travail
WORKDIR /app

# Copier les dépendances Python et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code du projet
COPY . .

# Collecter les fichiers statiques (si tu utilises collectstatic)
RUN python manage.py collectstatic --noinput

# Lancer l'application avec gunicorn
CMD ["gunicorn", "site_com.wsgi:application", "--bind", "0.0.0.0:8000"]
