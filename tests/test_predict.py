# tests/test_predict.py
import pytest
from fastapi import HTTPException
from app.services.prediction import predict
from app.api.endpoints import InputData
from fastapi.testclient import TestClient
from app.main import app
from tests.validata import valid_data

client = TestClient(app)

def test_predict_valid():
    result = predict(valid_data)
    assert isinstance(result, float)

def test_predict_missing_column():
    # Supprime volontairement une feature
    invalid_data = valid_data.model_dump()
    del invalid_data["AMT_INSTALMENT_max"]
    
    # Pydantic ne permet plus de créer l'objet → test via HTTP endpoint
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422
    assert any("Feature manquante" in msg for msg in response.json()["detail"])
    
def test_predict_wrong_type():
    invalid_data = valid_data.model_dump()
    invalid_data["AMT_INSTALMENT_max"] = "cinquante"
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422
    assert any(
        "AMT_INSTALMENT_max" in msg and "valid number" in msg
        for msg in json_resp["detail"]
    )

def test_predict_edge_values():
    # Valeurs extrêmes
    edge_data = valid_data.model_copy(update={
        "DAYS_BIRTH": 0,
        "AMT_PAYMENT_CURRENT_min": -100000,
        "CNT_CHILDREN": 1e6
    })
    result = predict(edge_data)
    assert isinstance(result, float)    
