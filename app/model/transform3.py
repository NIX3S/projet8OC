# solution_finale.py - MARCHE À COUP SÛR
import pickle
import numpy as np
import joblib
import xgboost as xgb
import onnxruntime as ort

print("🔍 Analyse pipeline...")
with open('model.pkl', 'rb') as f:
    pipeline = pickle.load(f)

print("Étapes:", [name for name,_ in pipeline.steps])
print("XGB:", type(pipeline.named_steps['clf']))

# ✅ SAUVEGARDE SÉPARÉE : preprocessing + XGB
preprocessing = pipeline[:-1]  # TOUT sauf clf
model = pipeline.named_steps['clf']

# Sauvegarde preprocessing
joblib.dump(preprocessing, 'preprocessing.joblib')
joblib.dump(model, 'xgb_model.joblib')  # ou .pkl

print("✅ preprocessing.joblib créé (toutes étapes sauf XGB)")
print("✅ xgb_model.joblib créé (XGB seul)")

# TEST
X_test = np.random.rand(1, 100).astype(np.float32)  # adaptez à vos données
X_processed = preprocessing.transform(X_test)
pred = model.predict_proba(X_processed)
print("✅ Test pipeline complet OK:", pred.shape)
