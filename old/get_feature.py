import mlflow.sklearn
import pandas as pd
import os

# Chemin du modèle exporté
MODEL_PATH = "models/champion_model"

# Charger le modèle
model = mlflow.sklearn.load_model(MODEL_PATH)

# Récupérer les features utilisées par le modèle
try:
    features = model.named_steps["clf"].feature_names_in_
except AttributeError:
    # fallback : définir la liste manuellement
    features = [
        "NumberofFloors",
        "NumberofBuildings",
        "LotArea",
        "YearBuilt"
    ]

# Définir le type souhaité pour chaque feature (exemple : int/float)
feature_types = {
    "NumberofFloors": int,
    "NumberofBuildings": float,
    # tu peux compléter ici selon ton dataset
}

print("Features attendues par le modèle :\n")
for f in features:
    f_type = feature_types.get(f, float)  # float par défaut si pas défini
    print(f"{f}: {f_type.__name__}")

# Générer un exemple JSON pour l'API
example_json = {f: 0 if feature_types.get(f, float) == int else 0.0 for f in features}

print("\nExemple JSON pour /predict :\n")
import json
print(json.dumps({"data": example_json}, indent=4))
