<h1 align="center"> CS_FD_MLENG - A simple case </h1>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![YAML](https://img.shields.io/badge/yaml-%23ffffff.svg?style=for-the-badge&logo=yaml&logoColor=151515)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

---

### Table of Contents

- [Description](#description)
- [How to run](#how-to-run)
- [Training](#training)
- [Data Preparation](#data-preparation)
- [Quality Code](#quality-code)
- [Logging](#logging)
- [High Level Diagram](#high-level-diagram)

---

### Description

This repo is a case of how to productionize a machine learning model for fraud detection. It is a **Flask** API and has two endpoints:

- `/predict`: predict the probability of fraud
- `/transform`: transform the data to persist a training-ready dataset

The model is persisted in the `artifacts` folder. To run the model training, check the session [Training](#training)

---

### How to run

For now **the case is in development**. The sugestion is to build the docker image and run the container.

```bash
docker build -t project_tag .
```

After that, you can run the container with the following command:

```bash
docker run -it -p 5000:5000 --mount type=bind,source=/src/logs,target=/app/src/logs image_name
```

NOTE: The model is currently persisted in the `artifacts` folder.

Once the conteiner is runnint, you can choose one of the states to prepare the data for training. At localhost:5000/transform use the following input:

```json
{"state": "CA"}
```

A new file will be created in the `src/data/processed` folder. This file is the training-ready dataset. To train the model, check the [Training](#training) section.

After the training is finished, you can use the `/predict` endpoint to predict the probability of fraud. At localhost:5000/predict use the following input as an example:

```json
{"trans_date_trans_time":"23-03-2019 01:09","merchant":"Greenholt, Jacobi and Gleason","category":"gas_transport","amt":9.94,"city":"Kaktovik","state":"AK","lat":66.6933,"long":-153.994,"city_pop":239,"job":"Careers information officer","dob":"01-04-1996","trans_num":"da81318af6e1918b067de24bbd9744d5","merch_lat":66.252098,"merch_long":-154.718147}
```

---

### Training

The model training is **parameterized** by the `train_params.yaml` file in order to facilitate the experimenting process for data scientists. For our purpose, the training is divided for each **state**. In that sense, the main parameters are:

- Model: The model to be used. Currently, the model is **Logistic Regression**.
- State_Name: The name of the state.

Please, check the `train_params.yaml` file for more details.

To run an experiment, you can use the `train.sh` script:

```bash
./train.sh
```

---

### Data Preparation

An endpoint is defined to transform the data. The goal is to read the raw data and persist a training-ready dataset. Also, the encoder pickle file is persisted in the `artifacts` folder. An important reminder is that **the data is not versioned**. 

---

### Quality Code

For this project, we used the following tools:

- [isort](https://github.com/PyCQA/isort): sort imports
- [black](https://github.com/psf/black): format code

---

### Logging

The logging module is used to log the information of the application. Error information and the metrics are logged in the `app.log` file. The log file is located in the `src/logs` folder. NOTE: The log file is not versioned.

---

### High Level Diagram

![High Level Diagram](resources/sol_design.png)