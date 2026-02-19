# convert_xgb_clean.py
import joblib
import numpy as np
from onnxmltools.convert import convert_xgboost
from onnxmltools.convert.common.data_types import FloatTensorType
import onnx
import onnxruntime as ort

# Chargement XGB pur
model = joblib.load('xgb_model.joblib')
print(f"✅ XGB chargé: {type(model).__name__}")

# CRUCIAL : Forcer feature_names AVANT conversion
model.feature_names = [f'f{i}' for i in range(212)]
print("✅ Features forcées: f0-f211")

# Conversion avec types onnxmltools (pas skl2onnx)
initial_types = [('input', FloatTensorType([None, 212]))]
onnx_model = convert_xgboost(model, initial_types=initial_types, target_opset=12)

# Vérif + save
onnx.checker.check_model(onnx_model)
with open('model.onnx', 'wb') as f:
    f.write(onnx_model.SerializeToString())

print("✅ model.onnx créé!")

# Test
session = ort.InferenceSession('model.onnx')
test_data = np.random.rand(1, 212).astype(np.float32)
result = session.run(None, {session.get_inputs()[0].name: test_data})
print(f"✅ ONNX OK: {result[0].shape}")
