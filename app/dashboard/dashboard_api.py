import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

API_URL = "http://localhost:8000/monitoring" 

# ---------------------------
# Sidebar: filtre temporel
# ---------------------------
st.sidebar.title("Filtres")
start_date = st.sidebar.date_input("Date de début", datetime.now() - timedelta(days=7))
end_date = st.sidebar.date_input("Date de fin", datetime.now())
limit_logs = st.sidebar.number_input("Nombre de logs récents", min_value=10, max_value=100, value=30)

# ---------------------------
# Appel à l'API
# ---------------------------
params = {
    "start_date": start_date.strftime("%Y-%m-%d"),
    "end_date": end_date.strftime("%Y-%m-%d"),
    "limit_logs": limit_logs
}

try:
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    st.error(f"Impossible de récupérer les données depuis l'API: {e}")
    st.stop()

# Récupérer les infos
error_count = data.get("error_count", 0)
avg_latency = data.get("avg_latency", 0)
drift_score = data.get("drift_score", 0)
class_distribution = data.get("class_distribution", {})
recent_logs = pd.DataFrame(data.get("recent_logs", []))
recent_logs['timestamp'] = pd.to_datetime(recent_logs['timestamp'])

# ---------------------------
# Titre
# ---------------------------
st.title("Dashboard ML Monitoring (API)")
st.write("Visualisation des métriques opérationnelles et de la dérive des données via API.")

# ---------------------------
# Métriques opérationnelles
# ---------------------------
st.header("Métriques opérationnelles")
col1, col2, col3 = st.columns(3)
col1.metric("Latence moyenne (ms)", f"{avg_latency:.2f}")
col2.metric("Erreurs (count)", f"{error_count}")
col3.metric("Drift score (%)", f"{drift_score*100:.2f}")

# ---------------------------
# Logs récents
# ---------------------------
st.header(f"Derniers {limit_logs} appels API")
if not recent_logs.empty:
    st.dataframe(recent_logs[['timestamp', 'endpoint', 'latency_ms', 'status_code', 'error_message']])
else:
    st.warning("Aucun log disponible pour la période sélectionnée")

# ---------------------------
# Répartition des prédictions
# ---------------------------
st.header("Répartition des prédictions")
if class_distribution:
    class_df = pd.DataFrame({
        "Classe": list(class_distribution.keys()),
        "%": [v*100 for v in class_distribution.values()]
    })
    st.bar_chart(class_df.set_index("Classe")["%"])
    st.table(class_df)
else:
    st.warning("Aucune prédiction enregistrée")
