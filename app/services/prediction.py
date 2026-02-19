import joblib
import os
import pandas as pd
from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
#from app.database import SessionLocal
# SQLAlchemy pour BDD
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from dotenv import load_dotenv
import numpy as np
from app.model.data import InputData
#load_dotenv(override=True)  # IMPORTANT
from app.model.databdd import Base, MLInput, MLOutput
# ----------------------------
# CONFIG BDD POSTGRESQL LOCALE
# ----------------------------
# Charge .env local seulement s'il existe
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
print(env_path)
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)

# PostgreSQL config via env
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "futurisys_ml")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

#Base = declarative_base()
Base.metadata.create_all(engine)  # Crée les tables si elles n'existent pas
# ----------------------------
# CHARGER LE MODELE ML
# ----------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../model/xgb_model.joblib")

try:
    model = joblib.load(MODEL_PATH)
    #model = model_dict["model"]
    columns = model.feature_names_in_ 
    print("Modèle chargé avec succès")
except FileNotFoundError:
    model = None
    print("Modèle non trouvé, utilisez un modèle fictif pour tester.")


# ----------------------------
# PREDICT + ENREGISTREMENT BDD
# ----------------------------
def predict(data: InputData | dict) -> float:
    #session = SessionLocal()
    if isinstance(data, InputData):
        data_dict = data.model_dump()
    else:
        data_dict = data

    # Insert input dans BDD
    input_row = MLInput(**data_dict)
    session.add(input_row)
    session.commit()  # On commit pour récupérer l'ID

    # Si pas de modèle, prédiction factice
    if model is None:
        raw_pred = 42
    else:
        remap = {
            "NAME_CONTRACT_TYPE_Cash_loans": "NAME_CONTRACT_TYPE_Cash loans",
            "cc_status_Sent_proposal_sum": "cc_status_Sent proposal_sum",
            "pos_status_Returned_to_the_store_sum": "pos_status_Returned to the store_sum",
            "NAME_CONTRACT_STATUS_Unused_offer_sum": "NAME_CONTRACT_STATUS_Unused offer_sum",
            "NAME_CONTRACT_TYPE_Revolving_loans_sum": "NAME_CONTRACT_TYPE_Revolving loans_sum",
            "NAME_CONTRACT_TYPE_Consumer_loans_sum": "NAME_CONTRACT_TYPE_Consumer loans_sum"
        }
         
        X_row = []
        for col in columns:
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
            X_row.append(value)

        X = pd.DataFrame([X_row], columns=columns)
        #pred_value = float(model.predict(X)[0])
        raw_pred = model.predict(X)[0]
        # Convertir numpy => python natif
        if isinstance(raw_pred, (np.integer, np.floating)):
            raw_pred = raw_pred.item()
        #pred_value = float(np.expm1(raw_pred))

    # Insert output dans BDD
    output_row = MLOutput(input_id=input_row.id, prediction=raw_pred)
    session.add(output_row)
    session.commit()

    return float(raw_pred)
