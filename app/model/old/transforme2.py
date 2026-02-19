import joblib
pipeline = joblib.load("model.joblib")
xgb_model = pipeline.named_steps['clf']

# Export natif XGBoost (fonctionne toujours)
xgb_model.save_model("model.json")

print("✅ model.json créé - compatible tous ONNX runtimes")
print("Utilisez preprocessing pipeline séparément")
