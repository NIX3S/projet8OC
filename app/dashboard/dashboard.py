# dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from create_db import DATABASE_URL, MLMetrics, MLOutput

# ---------------------------
# Connexion à la base
# ---------------------------
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@st.cache_data(ttl=300)
def load_data():
    db = SessionLocal()
    try:
        metrics_df = pd.read_sql(db.query(MLMetrics).statement, db.bind)
        outputs_df = pd.read_sql(db.query(MLOutput).statement, db.bind)
    finally:
        db.close()
    # Conversion timestamp
    metrics_df['timestamp'] = pd.to_datetime(metrics_df['timestamp'])
    outputs_df['timestamp'] = pd.to_datetime(outputs_df['timestamp'])
    return metrics_df, outputs_df

metrics_df, outputs_df = load_data()

# ---------------------------
# Sidebar: filtre temporel
# ---------------------------
st.sidebar.title("Filtres")
max_date = metrics_df['timestamp'].max() if not metrics_df.empty else datetime.now()
min_date = metrics_df['timestamp'].min() if not metrics_df.empty else datetime.now() - timedelta(days=7)

start_date = st.sidebar.date_input("Date de début", min_date)
end_date = st.sidebar.date_input("Date de fin", max_date)

start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date) + pd.Timedelta(days=1)

metrics_filtered = metrics_df[
    (metrics_df['timestamp'] >= start_datetime) &
    (metrics_df['timestamp'] < end_datetime)
]

outputs_filtered = outputs_df[
    (outputs_df['timestamp'] >= start_datetime) &
    (outputs_df['timestamp'] < end_datetime)
]

# ---------------------------
# Titre
# ---------------------------
st.title("Dashboard ML Monitoring")
st.write("Visualisation des métriques opérationnelles et de la dérive des données.")

# ---------------------------
# Métriques opérationnelles
# ---------------------------
st.header("Métriques opérationnelles")

if not metrics_filtered.empty:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latence moyenne (ms)", f"{metrics_filtered['avg_latency'].mean():.2f}")
    col2.metric("Erreurs (count)", f"{metrics_filtered['error_count'].sum()}")
    col3.metric("Drift score (%)", f"{metrics_filtered['drift_score'].mean()*100:.2f}")
    col4.metric("Anomalies (count)", f"{metrics_filtered['anomaly_count'].sum()}")
else:
    st.warning("Aucune métrique disponible pour la période sélectionnée")

# ---------------------------
# Graphiques historiques
# ---------------------------
st.header("Évolution des métriques")

if not metrics_filtered.empty:
    fig, ax = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
    
    # Latence
    sns.lineplot(data=metrics_filtered, x='timestamp', y='avg_latency', ax=ax[0], marker='o')
    ax[0].set_title("Latence moyenne (ms)")
    
    # Erreurs
    sns.lineplot(data=metrics_filtered, x='timestamp', y='error_count', ax=ax[1], marker='o', color='red')
    ax[1].set_title("Nombre d'erreurs")
    
    st.pyplot(fig)
else:
    st.warning("Pas de données historiques disponibles")

# ---------------------------
# Répartition des prédictions
# ---------------------------
st.header("Répartition des prédictions")
if not outputs_filtered.empty:
    pred_counts = outputs_filtered['prediction'].value_counts(normalize=True) * 100
    st.bar_chart(pred_counts)
    
    st.write("Détail des classes (%)")
    st.table(pred_counts.reset_index().rename(columns={'index': 'Classe', 'prediction': '%'}))
else:
    st.warning("Aucune prédiction enregistrée pour la période sélectionnée")
