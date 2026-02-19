import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.test_api import valid_data
client = TestClient(app)



def test_predict_valid():
    response = client.post("/predict", json=valid_data)
    assert response.status_code == 200
    json_resp = response.json()
    assert "prediction" in json_resp
    assert isinstance(json_resp["prediction"], float)

def test_predict_missing_column():
    invalid_data = valid_data.copy()
    del invalid_data["AMT_INSTALMENT_max"]  # Supprime une colonne
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422
    json_resp = response.json()
    assert any("Feature manquante" in msg for msg in json_resp["detail"])

def test_predict_wrong_type():
    invalid_data = valid_data.copy()
    invalid_data["AMT_INSTALMENT_max"] = "cinquante"
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422
    json_resp = response.json()
    # Vérifie le message Pydantic plutôt que "Type incorrect"
    assert any("Input should be a valid integer" in msg for msg in json_resp["detail"])