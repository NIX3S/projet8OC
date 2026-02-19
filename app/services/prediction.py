import joblib
import os
import pandas as pd
from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from dotenv import load_dotenv
import numpy as np
import xgboost as xgb
import onnxruntime as ort
from app.model.data import InputData
from app.model.databdd import Base, MLInput, MLOutput

# ----------------------------
# CONFIG BDD POSTGRESQL LOCALE
# ----------------------------
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
print(env_path)
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "futurisys_ml")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

# ----------------------------
# CHARGER LES MODÈLES ONNX + XGBoost
# ----------------------------
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../model")
PREPROC_PATH = os.path.join(MODEL_DIR, "preprocessor.onnx")
XGB_PATH = os.path.join(MODEL_DIR, "xgb_model.json")

# Colonnes du modèle original (récupérées du preprocessor ONNX)
try:
    # Charger preprocessor ONNX pour récupérer les noms des colonnes
    preproc_session = ort.InferenceSession(PREPROC_PATH)
    columns = [inp.name for inp in preproc_session.get_inputs()]
    print(f"✅ Colonnes chargées depuis preprocessor.onnx: {len(columns)}")
    
    # Charger XGBoost natif
    xgb_model = xgb.Booster()
    xgb_model.load_model(XGB_PATH)
    print("✅ xgb_model.json chargé")
    
except FileNotFoundError as e:
    print(f"❌ Modèles non trouvés: {e}")
    print("Utilisez un modèle fictif pour tester.")
    preproc_session = None
    xgb_model = None
    columns = []

# ----------------------------
# FONCTION PREPROCESSING ONNX
# ----------------------------
def preprocess_onnx(data_dict: dict, columns: list) -> np.ndarray:
    """Applique le preprocessing ONNX sur les données d'entrée"""
    input_feeds = {}
    
    for col in columns:
        # Remap des noms (comme avant)
        remap = {
            "NAME_CONTRACT_TYPE_Cash_loans": "NAME_CONTRACT_TYPE_Cash loans",
            "cc_status_Sent_proposal_sum": "cc_status_Sent proposal_sum",
            "pos_status_Returned_to_the_store_sum": "pos_status_Returned to the store_sum",
            "NAME_CONTRACT_STATUS_Unused_offer_sum": "NAME_CONTRACT_STATUS_Unused offer_sum",
            "NAME_CONTRACT_TYPE_Revolving_loans_sum": "NAME_CONTRACT_TYPE_Revolving loans_sum",
            "NAME_CONTRACT_TYPE_Consumer_loans_sum": "NAME_CONTRACT_TYPE_Consumer loans_sum"
        }
        key = next((k for k, v in remap.items() if v == col), col)
        
        if key not in data_dict:
            raise HTTPException(
                status_code=422,
                detail=f"Feature manquante pour le modèle: {key}"
            )
        
        value = data_dict[key]
        if not isinstance(value, (int, float)):
            raise HTTPException(
                status_code=422,
                detail=f"Type incorrect pour la feature {key}: attendu int ou float, reçu {type(value).__name__}"
            )
        
        # Préparer pour ONNX: shape (1,1) float32
        input_feeds[col] = np.array([[float(value)]], dtype=np.float32)
    
    # Exécuter preprocessing ONNX
    outputs = preproc_session.run(None, input_feeds)
    return outputs[0]  # Tableau numpy transformé

# ----------------------------
# PREDICT + ENREGISTREMENT BDD (ONNX)
# ----------------------------
def predict(data: InputData) -> float:
    data_dict = data.model_dump()

    # Insert input dans BDD
    input_row = MLInput(**data_dict)
    session.add(input_row)
    session.commit()

    # Si pas de modèles, prédiction factice
    if preproc_session is None or xgb_model is None:
        raw_pred = 42
    else:
        try:
            # 1️⃣ PREPROCESSING ONNX
            X_processed = preprocess_onnx(data_dict, columns)
            
            # 2️⃣ Prédiction XGBoost natif
            dmatrix = xgb.DMatrix(X_processed)
            raw_pred = xgb_model.predict(dmatrix)[0]
            
            # Convertir numpy → python natif
            if isinstance(raw_pred, (np.integer, np.floating)):
                raw_pred = raw_pred.item()
                
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur prédiction ONNX/XGBoost: {str(e)}"
            )

    # Insert output dans BDD
    output_row = MLOutput(input_id=input_row.id, prediction=raw_pred)
    session.add(output_row)
    session.commit()

    return raw_pred
