import os
import pickle

import pandas as pd
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

## Load params and data

CONFIG_PATH = "."


def load_config(config_name):
    with open(os.path.join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)

    return config


config = load_config("train_params.yaml")

df = pd.read_csv(f'{config['processed_data_dir']}/train_{config["state"]}.csv')

## Split

X = df.drop(["is_fraud", "state"], axis=1)
y = df["is_fraud"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

## Model

model = LogisticRegression()
model.fit(X_train, y_train)

print(X_test.head().to_csv("input_format.csv"))
y_pred = model.predict(X_test)

## Evaluation

print("F1:", f1_score(y_test, y_pred))

## Persist


def persist_model(model, state):
    pickle.dump(model, open(f'{config["models_dir"]}/model_{state}.pkl', "wb"))


persist_model(model, config["state"])
