from flask import request, jsonify
from api.models import predict
import pandas as pd
import logging

def init_routes(app):
    @app.route("/predict", methods=["POST"])
    def predict_route():
        try:
            data = request.json
            df_pred = pd.DataFrame(data)
            result = predict(df_pred)
            return jsonify(result), 200
        except Exception as e:
            logging.error(f"Erro ao realizar a previsão: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200
