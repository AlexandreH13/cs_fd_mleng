CREATE DATABASE IF NOT EXISTS `Db_Ml` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE Db_Ml;

CREATE TABLE Tb_Fraud (
    trans_date_trans_time DATETIME NOT NULL,
    merchant VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    amt DECIMAL(10, 2) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(2),
    lat DECIMAL(10, 7),
    longi DECIMAL(10, 7),
    city_pop INT,
    job VARCHAR(100),
    dob DATE,
    trans_num VARCHAR(50) NOT NULL,
    merch_lat DECIMAL(10, 7),
    merch_long DECIMAL(10, 7),
    is_fraud BOOLEAN NOT NULL,
    PRIMARY KEY (trans_num)
);

CREATE TABLE Tb_Treinamento (
    date_training DATE NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    score DECIMAL(5, 2) NOT NULL,
    PRIMARY KEY (date_training, model_name)
);

CREATE TABLE Tb_Predict (
    date_prediction DATE NOT NULL,
    value DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (date_prediction)
);