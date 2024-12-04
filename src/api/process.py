import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder


class process:
    """Class responsible for preparing the data for prediction."""

    def __init__(self, state):
        self.state = state

    def remove_quotation(self, df):
        df["job"] = df["job"].apply(lambda x: x.replace('"', ""))
        return df

    def job_encode(self, df) -> pd.DataFrame:
        """Performs label encoding on the categorical columns

        Returns:
            pd.DataFrame: Data Frame with new encoded columns
        """
        df_res = df
        encoder = LabelEncoder()
        encoded_column = encoder.fit_transform(df_res["job"])

        df_res["job"] = encoded_column

        joblib.dump(encoder, f"src/model/artifacts/encoder_{self.state}.pkl")
        print("Encoder Salvo!")

        return df_res

    def load_job_encoder(self):
        """Load the encoder pickle file.

        Returns:
            joblib.dump: Encoder pickle file
        """
        encoder = joblib.load(f"src/model/artifacts/encoder_{self.state}.pkl")
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
        return df_to_save[df_to_save["state"] == state].reset_index(drop=True)

    def fix_data_types(self, df) -> pd.DataFrame:
        """Fix the data type on the label column(is_fraud).

        Returns:
            pd.DataFrame: DataFrame ready for modeling.
        """
        label = df["is_fraud"]
        print(f"Invalid: {label[~label.isin(['0', '1'])].index}")

        df_res = df.iloc[label[label.isin(["0", "1"])].index]  ## Keep only valid data
        label = label.apply(self.convert_to_int)
        df_res["is_fraud"] = label
        return df_res

    def run(self):
        """Execute all the steps to prepare the data. Save inside the processed folder."""
        cols_ignore = [
            "trans_date_trans_time",
            "merchant",
            "category",
            "city",
            "trans_num",
            "dob",
            "is_fraud",
            "state",
        ]
        df_model = self.fix_data_types().sample(frac=1)
        df_model = df_model.drop(columns=cols_ignore, axis=1)
        return df_model
