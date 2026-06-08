import pandas as pd


class Extractor:

    def load_patients(self, file_path):
        try:
            dataframe = pd.read_csv(
                file_path,
                on_bad_lines="skip"
            )

            return dataframe

        except Exception as error:
            print(f"Error loading patients file: {error}")
            return pd.DataFrame()

    def load_appointments(self, file_path):
        try:
            dataframe = pd.read_csv(
                file_path,
                on_bad_lines="skip"
            )

            return dataframe

        except Exception as error:
            print(f"Error loading appointments file: {error}")
            return pd.DataFrame()

    def load_treatments(self, file_path):
        try:
            dataframe = pd.read_csv(
                file_path,
                on_bad_lines="skip"
            )

            return dataframe

        except Exception as error:
            print(f"Error loading treatments file: {error}")
            return pd.DataFrame()