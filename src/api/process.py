import logging
import os

import joblib
import yaml

logging.basicConfig(filename="src/logs/app.log", level=logging.DEBUG)

import pandas as pd
from sklearn.preprocessing import LabelEncoder


class Process:
    """Class responsible for preparing the data for prediction."""

    def __init__(self, state):
        self.state = state
        self.CONFIG_PATH = "src/api/"

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

    def remove_quotation(self, df, cols):
        for col in cols:
            df[col] = df[col].apply(lambda x: x.replace('"', ""))
        return df

    def job_encode(self, df, cols) -> pd.DataFrame:
        """Performs label encoding on the categorical columns

        Returns:
            pd.DataFrame: Data Frame with new encoded columns
        """
        df_res = df

        try:
            for col in cols:
                encoder = LabelEncoder()
                encoded_column = encoder.fit_transform(df_res[col])
                df_res[col] = encoded_column
                joblib.dump(
                    encoder, f"src/model/artifacts/encoder_{self.state}_{col}.pkl"
                )
                logging.info(f"Encoder {col} Salvo!")
        except Exception as e:
            logging.error(f"Erro ao realizar o encoding: {e}")

        return df_res

    def load_job_encoder(self, col):
        """Load the encoder pickle file.

        Returns:
            joblib.dump: Encoder pickle file
        """

        try:
            encoder = joblib.load(f"src/model/artifacts/encoder_{self.state}_{col}.pkl")
        except FileNotFoundError as e:
            logging.error(
                f"Arquivo de encoder não encontrado. Talvez os dados não tenham sido processados. {e}"
            )
        return encoder

    def convert_to_int(self, value):
        """Convert str values to int.

        Args:
            value (str, object): column value

        Returns:
            int: converted value
        """
        try:
            return int(value)  # Tentar converter para inteiro
        except (ValueError, TypeError):
            return None  # Substituir valores inválidos por None

    def get_state_df(self, df, state):
        """Filter the DataFrame by state.

        Args:
            df (pd.DataFrame): DataFrame to filter

        Returns:
            pd.DataFrame: Filtered DataFrame
        """
        df_to_save = df
        try:
            df_to_save = df_to_save[df_to_save["state"] == state].reset_index(drop=True)
        except Exception as e:
            logging.error(
                f"Erro ao filtrar o DataFrame. O estado {state} não existe. {e}"
            )
        return df_to_save[df_to_save["state"] == state].reset_index(drop=True)

    def fix_data_types(self, df) -> pd.DataFrame:
        """Fix the data type on the label column(is_fraud).

        Returns:
            pd.DataFrame: DataFrame ready for modeling.
        """
        label = df["is_fraud"]

        df_res = df.iloc[label[label.isin(["0", "1"])].index]  ## Keep only valid data
        label = label.apply(self.convert_to_int)
        df_res["is_fraud"] = label
        return df_res
