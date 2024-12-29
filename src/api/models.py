import logging

logging.basicConfig(filename="src/logs/app.log", level=logging.DEBUG)

import pickle
from datetime import date

import pandas as pd
from data.db import Database

from api.process import Process


class Models:
    """Class responsible for loading the model and predicting."""

    def __init__(self, prep, state):
        self.prep = prep
        self.config = prep.load_config("config.yaml")
        self.model = pickle.load(open(f"src/model/artifacts/model_{state}.pkl", "rb"))
        self.state = state
        self.db = Database()

    def prepare_prediction(self, data):
        """Prepare the data for prediction.

        Args:
            data (pd.DataFrame): DataFrame with the data to be predicted

        Returns:
            pd.DataFrame: DataFrame with the data ready for prediction
        """

        logging.info("Preparando os dados para a previsão...")

        clean_data = self.prep.remove_quotation(data, self.config["categorical_cols"])

        for col in self.config["categorical_cols"]:
            logging.info(f"Transformando {col}...")
            encoder = self.prep.load_job_encoder(col)
            encoded_data = encoder.transform(clean_data[col])
            clean_data[col] = encoded_data

        df_pred = clean_data.drop(
            columns=self.config["ignore_cols_predict"], axis=1
        ).sample(frac=1)
        return df_pred

    def predict(self, data):
        """Return the probability of fraud.

        Args:
            data pd.DataFrame: DataFrame with the data to be predicted

        Returns:
            str: Probability of fraud
        """
        prediction_prob = self.model.predict_proba(data)
        prediction = self.model.predict(data)

        logging.info(f"Fraude Prob: {prediction_prob[0]}")
        logging.info(f"Fraude: {prediction}")

        ## DF para salvar no banco
        today = date.today()
        df_to_save = pd.DataFrame({"date_prediction": [today], "value": [prediction]})

        self.db.connect()
        self.db.insert_data_from_df(self.db.conn, "Tb_Predict", df_to_save)

        return str(prediction_prob[0])
