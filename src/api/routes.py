import logging

import pandas as pd
from flask import jsonify, request

from api.models import Models
from api.process import Process
from api.transform import transform


def init_routes(app):
    """Define the prediction route."""

    @app.route("/predict", methods=["POST"])
    def predict_route():
        try:
            data = request.json
            state = data[0]["state"]
            df_pred = pd.DataFrame(data)

            prep = Process(state)
            model = Models(prep, state)  # Injeta

            df_pred = model.prepare_prediction(df_pred)
            prediction = model.predict(df_pred)
            return jsonify(prediction), 200
        except Exception as e:
            logging.error(f"Erro ao realizar a previsão: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/transform", methods=["POST"])
    def transform_data():
        """Define the transformation route."""
        try:
            state = request.json[0]["state"]
            prep = Process(state)
            prep_training = transform(state, prep)  # Injeta
            prep_training.run()
            return jsonify({"status": "Dados transformados"}), 200
        except Exception as e:
            logging.error(f"Erro ao realizar a transformação dos dados: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200
