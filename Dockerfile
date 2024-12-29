FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    vim

RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

COPY requirements_dev.txt .

RUN pip install -r requirements_dev.txt

COPY src/ ./src

RUN chmod +x src/model/train_model.sh

EXPOSE 5000

CMD ["python3", "src/api/app.py"]