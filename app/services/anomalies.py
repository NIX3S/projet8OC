import pandas as pd
from sqlalchemy.orm import Session
from create_db import MLOutput

def compute_anomalies(db: Session):
    outputs = pd.read_sql(db.query(MLOutput).statement, db.bind)

    anomaly_count = 0

    if not outputs.empty:

        # Classes invalides
        invalid_classes = outputs.loc[~outputs['prediction'].isin([0, 1])]
        anomaly_count += len(invalid_classes)

        # Vérifier proportion
        counts = outputs['prediction'].value_counts(normalize=True)
        prop_0 = counts.get(0, 0)
        prop_1 = counts.get(1, 0)

        if prop_1 > prop_0:
            anomaly_count += 1

    print(f"Anomalies détectées : {anomaly_count}")
    return anomaly_count
