import logging
import os

import yaml

logging.basicConfig(filename="src/logs/app.log", level=logging.DEBUG)

import pandas as pd

from api.process import Process


class transform:
    """Get the raw data and transform to persist a training-ready dataset."""

    def __init__(self, state, prep):
        self.CONFIG_PATH = "src/api/"
        self.state = state
        self.prep = prep
        self.config = self.load_config("config.yaml")

    def load_raw_data(self):
        """Load the raw data from the raw folder.

        Returns:
            pd.DataFrame: DataFrame with raw data
        """
        try:
            df = pd.read_csv("src/data/processed/fraud_data_train.csv")
        except FileNotFoundError as e:
            logging.error(f"Raw data não foi encontrado. {e}")

        return df

    def load_config(self, config_name):
        """Load the config file.

        Args:
            config_name (str): Name of the config file

        Returns:
            dict: Config file
        """
        with open(os.path.join(self.CONFIG_PATH, config_name)) as file:
            config = yaml.safe_load(file)

        return config

    def run(self):
        """This function defines the algorithm to transform the raw data into a format that can be used by the model.
        It persist a training-ready dataset and also the encoder pickle file
        """

        logging.info(
            "Iniciando a transformação dos dados para o fomato de treinamento..."
        )

        filtered_df = self.prep.get_state_df(self.load_raw_data(), self.state)
        filtered_df = self.prep.remove_quotation(
            filtered_df, self.config["categorical_cols"]
        )
        encoded_df = self.prep.encode_cols(filtered_df, self.config["categorical_cols"])
        fixed_types_df = self.prep.fix_data_types(encoded_df)

        state = fixed_types_df["state"].iloc[0]
        df_train = fixed_types_df.drop(
            columns=self.config["ignore_cols_transform"], axis=1
        ).sample(frac=1)
        df_train.to_csv(f"src/data/processed/train_{state}.csv", index=False)
