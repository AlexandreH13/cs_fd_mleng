import logging

logging.basicConfig(filename="src/logs/app.log", level=logging.DEBUG)

import pandas as pd

from api.process import process


class transform:
    """Get the raw data and transform to persist a training-ready dataset."""

    def __init__(self, state, prep):
        self.state = state
        self.prep = prep

    def load_raw_data(self):
        """Load the raw data from the raw folder.

        Returns:
            pd.DataFrame: DataFrame with raw data
        """
        try:
            df = pd.read_csv("src/data/raw/fraud_data.csv")
        except FileNotFoundError as e:
            logging.error(f"Raw data não foi encontrado. {e}")
  
        return df

    def run(self):
        """This function defines the algorithm to transform the raw data into a format that can be used by the model.
        It persist a training-ready dataset and also the encoder pickle file
        """

        logging.info("Iniciando a transformação dos dados para o fomato de treinamento...")

        # prep = process(self.load_raw_data(), self.state)
        filtered_df = self.prep.get_state_df(self.load_raw_data(), self.state)
        filtered_df = self.prep.remove_quotation(filtered_df)
        encoded_df = self.prep.job_encode(filtered_df)
        fixed_types_df = self.prep.fix_data_types(encoded_df)

        state = fixed_types_df["state"].iloc[0]
        cols_ignore = [
            "trans_date_trans_time",
            "merchant",
            "category",
            "city",
            "trans_num",
            "dob",
        ]
        df_train = fixed_types_df.drop(columns=cols_ignore, axis=1).sample(frac=1)
        df_train.to_csv(f"src/data/processed/train_{state}.csv", index=False)
