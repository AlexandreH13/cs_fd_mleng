import logging

logging.basicConfig(filename="src/logs/app.log", level=logging.DEBUG)

import pickle

from api.process import process


class models:
    """Class responsible for loading the model and predicting."""

    def __init__(self, prep, state):
        self.prep = prep
        self.model = pickle.load(open(f"src/model/artifacts/model_{state}.pkl", "rb"))
        self.state = state

    def prepare_prediction(self, data):
        """Prepare the data for prediction.

        Args:
            data (pd.DataFrame): DataFrame with the data to be predicted

        Returns:
            pd.DataFrame: DataFrame with the data ready for prediction
        """

        logging.info("Preparando os dados para a previsão...")

        clean_data = self.prep.remove_quotation(data)
        encoder = self.prep.load_job_encoder()
        encoded_data = encoder.transform(clean_data["job"])
        data["job"] = encoded_data

        fixed_types_df = self.prep.fix_data_types(data)
        cols_ignore = [
            "trans_date_trans_time",
            "merchant",
            "category",
            "city",
            "trans_num",
            "dob",
            "state",
            "is_fraud",
        ]
        df_pred = fixed_types_df.drop(columns=cols_ignore, axis=1).sample(frac=1)

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
        return str(prediction_prob[0])
