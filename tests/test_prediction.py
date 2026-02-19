# tests/test_prediction.py
import pytest
from fastapi import HTTPException
from app.services import prediction
from app.api.endpoints import InputData
from tests.validata import valid_data


# ----------------------
# Cas 1: prédiction normale
# ----------------------
def test_predict_valid():
    result = prediction.predict(valid_data)
    assert isinstance(result, float)

# ----------------------
# Cas 2: prédiction factice si modèle None
# ----------------------
def test_predict_fallback(monkeypatch):
    monkeypatch.setattr(prediction, "model", None)
    result = prediction.predict(valid_data)
    assert result == 42

# ----------------------
# Cas 3: feature manquante
# ----------------------
def test_missing_feature(monkeypatch):
    # Remplace les colonnes pour forcer un KeyError
    monkeypatch.setattr(prediction, "columns", list(valid_data.model_dump().keys()) + ["fake_column"])
    with pytest.raises(HTTPException) as exc:
        prediction.predict(valid_data)
    assert exc.value.status_code == 422
    assert "Feature manquante" in exc.value.detail
