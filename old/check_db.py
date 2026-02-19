from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import DATABASE_URL, APILogs, MLMetrics

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Logs récents
logs = db.query(APILogs).order_by(APILogs.timestamp.desc()).limit(5).all()
for log in logs:
    print(log.endpoint, log.latency_ms, log.status_code, log.error_message)

# Métriques récentes
metrics = db.query(MLMetrics).order_by(MLMetrics.timestamp.desc()).limit(5).all()
for m in metrics:
    print(m.timestamp, m.error_count, m.avg_latency, m.drift_score, m.anomaly_count)
