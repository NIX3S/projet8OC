import os
import tempfile
import time
import cProfile
import pstats
import psutil
import mlflow.sklearn
import pandas as pd
import sys
import os

# Ajouter la racine du projet au PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)
from tests.validata import valid_data
from app.model.data import InputData
from app.services.prediction import predict

# ============================
# PROFILING
# ============================
validate_data = valid_data
process = psutil.Process()
process.cpu_percent(interval=None)

def run_prediction():
    return predict(validate_data)

start_time = time.time()

profiler = cProfile.Profile()
profiler.enable()

prediction = run_prediction()

profiler.disable()

latency_ms = (time.time() - start_time) * 1000
cpu_usage = process.cpu_percent(interval=None)

# ============================
# EXTRACTION DES STATS
# ============================
stats = pstats.Stats(profiler)
stats.sort_stats("cumulative")

# Extraire toutes les lignes sous forme de tuples
stats_list = []
for func_tuple, func_stats in stats.stats.items():
    ncalls, nprimcalls, tottime, cumtime, callers = func_stats
    filename, lineno, func_name = func_tuple
    stats_list.append({
        "Fichier": filename,
        "Ligne": lineno,
        "Fonction": func_name,
        "Appels (ncalls)": ncalls,
        "Appels primaires (nprimcalls)": nprimcalls,
        "Temps total (s)": tottime,
        "Temps cumulé (s)": cumtime
    })

# Trier par temps cumulé et prendre le top 20
df_stats = pd.DataFrame(stats_list)
df_top20 = df_stats.sort_values(by="Temps cumulé (s)", ascending=False).head(20)


# ============================
# Sauvegarder le TOP 20 dans un CSV temporaire
# ============================
# Chemin absolu basé sur le dossier du script
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "profiling_top20.csv")
df_top20.to_csv(csv_path, index=False)

# ============================
# AFFICHAGE
# ============================
print(f"Prédiction : {prediction}")
print(f"Latence totale : {latency_ms:.2f} ms")
print(f"CPU utilisé : {cpu_usage:.2f} %")
print("\n--- TOP 20 fonctions les plus coûteuses ---\n")
print(df_top20)

# On peut aussi retourner le DataFrame pour l'utiliser dans Streamlit
