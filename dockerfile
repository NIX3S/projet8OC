# -----------------------------
# Étape 1 : Image de base
# -----------------------------
FROM python:3.12-slim

# -----------------------------
# Variables d'environnement
# -----------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DB_USER=postgres
ENV DB_PASSWORD=5345
ENV DB_HOST=db
ENV DB_PORT=5432
ENV DB_NAME=scoring_ml
# -----------------------------
# Dossier de travail
# -----------------------------
WORKDIR /app

# Copier requirements
COPY requirements.txt .

# Installer dépendances
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir psycopg[binary] onnxruntime skl2onnx joblib pandas scikit-learn xgboost mlflow

# Copier tout le projet
COPY . .
RUN rm -f .env

# Exposer les ports
EXPOSE 8000
EXPOSE 8501
EXPOSE 8502

# Commande par défaut : FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# Pour Streamlit dashboard, remplacer par :
# CMD ["streamlit", "run", "app/dashboard/performance_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
