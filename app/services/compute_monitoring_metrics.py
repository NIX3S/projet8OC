# app/monitoring/compute_monitoring_metrics.py

import pandas as pd
from sqlalchemy.orm import Session
from create_db import DATABASE_URL, APILogs, MLInput, MLOutput
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def compute_metrics(limit_logs: int = 30, start_date: str = None, end_date: str = None):
    """
    Calcule les métriques principales et retourne :
    - error_count
    - avg_latency
    - drift_score
    - class_distribution
    - recent_logs (dernieres N entrées)
    
    start_date / end_date format: 'YYYY-MM-DD' (optionnel)
    """
    db: Session = SessionLocal()
    try:
        logs_query = db.query(APILogs)
        if start_date:
            logs_query = logs_query.filter(APILogs.timestamp >= start_date)
        if end_date:
            logs_query = logs_query.filter(APILogs.timestamp <= end_date)
        logs = pd.read_sql(logs_query.statement, db.bind)
        
        # Métriques globales
        error_count = (logs['status_code'] >= 400).sum()
        avg_latency = logs['latency_ms'].mean()

        # Récupération dernières N entrées triées par timestamp desc
        recent_logs = logs.sort_values('timestamp', ascending=False).head(limit_logs)
        recent_logs = recent_logs[['timestamp', 'endpoint', 'latency_ms', 'status_code', 'error_message']]
        recent_logs = recent_logs.to_dict(orient='records')

        # Distribution des classes
        outputs = pd.read_sql(db.query(MLOutput).statement, db.bind)
        if not outputs.empty:
            class_dist = outputs['prediction'].value_counts(normalize=True).to_dict()
            for cls in [0, 1]:
                if cls not in class_dist:
                    class_dist[cls] = 0.0
        else:
            class_dist = {0: 0.0, 1: 0.0}

        # Drift score (placeholder si script drift séparé)
        drift_score = 0.0

        return {
            "error_count": int(error_count),
            "avg_latency": float(avg_latency) if not pd.isna(avg_latency) else 0.0,
            "drift_score": float(drift_score),
            "class_distribution": {str(k): v for k, v in class_dist.items()},
            "recent_logs": recent_logs
        }

    finally:
        db.close()
