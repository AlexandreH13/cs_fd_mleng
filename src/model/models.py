import joblib

# Carrega o modelo treinado
model = joblib.load("src/model/artifacts/model.pkl")

def predict(data):
    # Exemplo: Pré-processa os dados antes de prever
    X = [data["features"]]  # Assumindo entrada como {"features": [...]}
    prediction = model.predict(X)
    return {"prediction": int(prediction[0])}
