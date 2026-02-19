from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import mlflow.sklearn
import psutil
import os
import pandas as pd
import time
from datetime import datetime, timezone
from app.model.data import InputData
from app.services.prediction import predict
from fastapi import APIRouter, HTTPException, Request
from sqlalchemy.orm import Session
from create_db import DATABASE_URL, APILogs  # si APILogs est dans create_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services.compute_monitoring_metrics import compute_metrics
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


router = APIRouter()



class OutputData(BaseModel):
    prediction: float

# --- Enregistrement du temps de démarrage ---
START_TIME = time.time()

# --- Charger le modèle champion une seule fois ---
#MODEL_PATH = "models/champion_model"
#if not os.path.exists(MODEL_PATH):
#    raise Exception(f"Modèle introuvable à {MODEL_PATH}. Exporter le modèle avant de lancer l'API.")
#
#model = mlflow.sklearn.load_model(MODEL_PATH)


# -----------------------------
# Endpoints
# -----------------------------
@router.get("/metadata")
def get_metadata():
    return {
        "name": "Prêt à Dépenser - Scoring API",
        "version": "1.0.0",
        "description": "API pour prédire le score de crédit des clients",
        "status": "POC-ready"
    }

@router.get("/health")
def health_check():
    uptime_seconds = int(time.time() - START_TIME)
    return {
        "status": "ok",
        "uptime_seconds": uptime_seconds,
        "uptime_human": str(datetime.now(timezone.utc) - datetime.fromtimestamp(START_TIME, timezone.utc))
    }


@router.post("/predict", response_model=OutputData)
def make_prediction(data: InputData, request: Request):
    process = psutil.Process(os.getpid())
    process.cpu_percent(interval=None)

    db: Session = SessionLocal()

    status_code = 200
    error_message = None
    inference_time_ms = None

    try:
        total_start = time.time()

        # --- Mesure inférence uniquement ---
        inference_start = time.time()
        result = predict(data)
        inference_time_ms = (time.time() - inference_start) * 1000

        total_latency_ms = (time.time() - total_start) * 1000
        cpu_usage = process.cpu_percent(interval=None)

    except ValueError as ve:
        status_code = 422
        error_message = str(ve)
        raise HTTPException(status_code=422, detail=str(ve))

    except Exception as e:
        status_code = 500
        error_message = str(e)
        raise HTTPException(status_code=500, detail="Erreur interne")

    finally:
        log_entry = APILogs(
            endpoint=str(request.url.path),
            latency_ms=total_latency_ms,
            inference_time_ms=inference_time_ms,
            cpu_usage=cpu_usage,
            status_code=status_code,
            error_message=error_message
        )
        db.add(log_entry)
        db.commit()
        db.close()

    return {"prediction": result}


@router.get("/monitoring")
def get_monitoring(limit_logs: int = 30, start_date: str = None, end_date: str = None):
    """
    Renvoie les métriques et les derniers logs.
    Params:
    - limit_logs : combien de logs récents renvoyer (default 30)
    - start_date / end_date : filtres optionnels 'YYYY-MM-DD'
    """
    metrics = compute_metrics(limit_logs=limit_logs, start_date=start_date, end_date=end_date)
    return metrics