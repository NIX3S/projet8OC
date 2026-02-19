import pandas as pd
from sqlalchemy.orm import Session
from create_db import APILogs

def compute_monitoring_metrics(db: Session):

    logs = pd.read_sql(db.query(APILogs).statement, db.bind)

    if logs.empty:
        return 0, 0.0

    error_count = (logs['status_code'] >= 400).sum()
    avg_latency = logs['latency_ms'].dropna().mean()

    avg_latency = float(avg_latency) if pd.notna(avg_latency) else 0.0

    print(f"Métriques calculées : erreurs={error_count}, latence moyenne={avg_latency:.2f} ms")

    return int(error_count), avg_latency
