from sqlalchemy.orm import Session
from datetime import datetime, timezone as UTC
import sys
import os

# Ajouter la racine du projet au PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)
from create_db import MLMetrics
from app.services.monitoring import compute_monitoring_metrics
from app.services.drift_metrics import compute_drift_metrics
from app.services.anomalies import compute_anomalies

def update_all_metrics(db: Session):
    """
    Calcule les métriques opérationnelles, drift, anomalies et insère une ligne dans MLMetrics.
    """
    error_count, avg_latency = compute_monitoring_metrics(db)
    drift_score = compute_drift_metrics()
    anomaly_count = compute_anomalies(db)

    metric_entry = MLMetrics(
        timestamp=datetime.now(UTC.utc),
        error_count=error_count,
        avg_latency=avg_latency,
        drift_score=drift_score,
        anomaly_count=anomaly_count
    )

    db.add(metric_entry)
    db.commit()
    return metric_entry
