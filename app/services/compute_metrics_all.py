from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from create_db import DATABASE_URL, MLMetrics
from app.services.monitoring import compute_monitoring_metrics
from app.services.drift_metrics import compute_drift_metrics
from app.services.anomalies import compute_anomalies
from datetime import datetime, UTC


# Setup DB
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

if __name__ == "__main__":

    db = SessionLocal()

    try:
        print("=== Calcul des métriques opérationnelles ===")
        error_count, avg_latency = compute_monitoring_metrics(db)

        print("=== Calcul du drift ===")
        drift_score = compute_drift_metrics()

        print("=== Détection anomalies ===")
        anomaly_count = compute_anomalies(db)

        # ✅ UNE SEULE INSERTION
        metric_entry = MLMetrics(
            timestamp=datetime.now(UTC),
            error_count=error_count,
            avg_latency=avg_latency,
            anomaly_count=anomaly_count,
            drift_score=drift_score
        )

        db.add(metric_entry)
        db.commit()

        print("\n✅ Toutes les métriques ont été sauvegardées proprement.")

    except Exception as e:
        db.rollback()
        print(f"❌ ERREUR GLOBALE: {e}")

    finally:
        db.close()
