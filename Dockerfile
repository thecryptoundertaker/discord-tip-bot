FROM python:3.9

WORKDIR /plutus
COPY . .

RUN pip install --upgrade pip pipenv && pipenv install --deploy
