import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import sys
import os

# Ajouter le chemin vers le projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from create_db import DATABASE_URL, APILogs

# ---------------------------
# Connexion à la base
# ---------------------------
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@st.cache_data(ttl=60)
def load_logs():
    db = SessionLocal()
    try:
        logs_df = pd.read_sql(db.query(APILogs).statement, db.bind)
    finally:
        db.close()
    # Conversion timestamp
    logs_df['timestamp'] = pd.to_datetime(logs_df['timestamp'])
    return logs_df

logs_df = load_logs()

# ---------------------------
# Sidebar: filtre temporel
# ---------------------------
st.sidebar.title("Filtres")
max_date = logs_df['timestamp'].max() if not logs_df.empty else datetime.now()
min_date = logs_df['timestamp'].min() if not logs_df.empty else datetime.now() - timedelta(days=1)

start_date = st.sidebar.date_input("Date de début", min_date)
end_date = st.sidebar.date_input("Date de fin", max_date)

# Filtrer les données
logs_filtered = logs_df[(logs_df['timestamp'] >= pd.to_datetime(start_date)) & 
                        (logs_df['timestamp'] <= pd.to_datetime(end_date))]

# ---------------------------
# Dashboard
# ---------------------------
st.title("Dashboard Technique - API Performance")
st.write("Visualisation des métriques de latence et CPU pour chaque requête")

# ---------------------------
# Indicateurs principaux
# ---------------------------
st.header("Indicateurs clés")

if not logs_filtered.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Latence totale (ms)", f"{logs_filtered['latency_ms'].mean():.2f}")
    col2.metric("Temps d'inférence (ms)", f"{logs_filtered['inference_time_ms'].mean():.2f}")
    col3.metric("CPU utilisé (%)", f"{logs_filtered['cpu_usage'].mean():.2f}")
else:
    st.warning("Aucune donnée pour la période sélectionnée")

# ---------------------------
# Graphiques historiques
# ---------------------------
st.header("Évolution des métriques")

if not logs_filtered.empty:
    fig, ax = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
    
    sns.lineplot(data=logs_filtered, x='timestamp', y='latency_ms', ax=ax[0], marker='o', color='blue')
    ax[0].set_title("Latence totale (ms)")
    
    sns.lineplot(data=logs_filtered, x='timestamp', y='inference_time_ms', ax=ax[1], marker='o', color='green')
    ax[1].set_title("Temps d'inférence (ms)")
    
    sns.lineplot(data=logs_filtered, x='timestamp', y='cpu_usage', ax=ax[2], marker='o', color='orange')
    ax[2].set_title("CPU utilisé (%)")
    
    st.pyplot(fig)
else:
    st.warning("Pas de données historiques disponibles")

# ---------------------------
# Histogrammes
# ---------------------------
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.header("Distribution des métriques")

if not logs_filtered.empty:
    col1, col2, col3 = st.columns(3)

    # Latence
    fig1, ax1 = plt.subplots()
    sns.histplot(logs_filtered['latency_ms'], bins=20, color='blue', ax=ax1)
    ax1.set_title("Latence totale (ms)")
    col1.pyplot(fig1)

    # Temps d'inférence
    fig2, ax2 = plt.subplots()
    sns.histplot(logs_filtered['inference_time_ms'], bins=20, color='green', ax=ax2)
    ax2.set_title("Temps d'inférence (ms)")
    col2.pyplot(fig2)

    # CPU
    fig3, ax3 = plt.subplots()
    sns.histplot(logs_filtered['cpu_usage'], bins=20, color='red', ax=ax3)
    ax3.set_title("CPU utilisé (%)")
    col3.pyplot(fig3)
else:
    st.warning("Aucune donnée disponible pour la période sélectionnée")

import streamlit as st
import subprocess
import pandas as pd
import re
import os 
import tempfile
# Chemin absolu vers profile_model.py
#profile_dir = os.path.abspath("app/monitoring")
#csv_file = os.path.join(profile_dir, "profiling_top20.csv")
# Chemin absolu basé sur l'emplacement du dashboard
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
profile_dir = os.path.join(dashboard_dir, "..", "monitoring")
profile_dir = os.path.abspath(profile_dir)
csv_file = os.path.join(profile_dir, "profiling_top20.csv")


if st.button("Lancer Profiling"):
    import subprocess
    print(["python", os.path.join(profile_dir, "profile_model.py")])
    result = subprocess.run(
        ["python", os.path.join(profile_dir, "profile_model.py")],
        capture_output=True,
        text=True
    )
    st.subheader("Sortie brute du profiling")
    st.text(result.stdout)
    st.write(f"Chemin CSV attendu : {csv_file}")
    st.write(f"Existe ? : {os.path.exists(csv_file)}")

    if os.path.exists(csv_file):
        df_top20 = pd.read_csv(csv_file)
        st.subheader("TOP 20 fonctions les plus coûteuses")
        st.dataframe(df_top20, height=400)
    else:
        st.warning("Impossible de récupérer le TOP 20. Vérifie que profile_model.py s'est bien exécuté.")
        
