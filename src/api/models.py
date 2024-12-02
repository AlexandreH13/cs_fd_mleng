import pickle

model = pickle.load(open("model/artifacts/model_AK.pkl", 'rb'))

def predict(data):
    # Exemplo: Pré-processa os dados antes de prever
    X = data
    prediction = model.predict(X)
    print(f'Fraude: {prediction[0]}')
    return str(prediction[0])
