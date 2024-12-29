import logging
import os

import mysql.connector
import pandas as pd


class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        """Connect to the database."""

        db_config = {
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
        }

        try:
            logging.info("Conectando à base de dados")
            self.conn = mysql.connector.connect(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["password"],
                database=db_config["database"],
            )
        except mysql.connector.Error as err:
            logging.error(f"Erro ao conectar-se à base de dados: {err}")

    def insert_data_from_df(self, conn, table_name, df):
        cursor = conn.cursor()
        cols = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

        logging.info(f"Inserindo os dados {df}")
        logging.info(f"SQL: {sql}")

        val = (df["date_prediction"].iloc[0], int(df["value"].iloc[0][0]))

        try:
            cursor.execute(sql, val)
            conn.commit()
            logging.info(f"Dados inseridos na tabela {table_name}")
        except Exception as e:
            logging.error(f"Erro ao inserir os dados na tabela {table_name}: {e}")
