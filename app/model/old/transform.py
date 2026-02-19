import pickle
import joblib

#  Charger le modèle depuis un pickle
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

#  Sauvegarder le modèle en joblib
joblib.dump(model, "model.joblib")
print("Modèle sauvegardé en model.joblib")
