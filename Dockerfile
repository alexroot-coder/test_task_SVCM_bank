FROM python:3.11-alpine

RUN mkdir my_app

WORKDIR my_app

COPY requirements.txt /my_app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY zadanie_2 zadanie_2

CMD cd zadanie_2 && uvicorn main:app --host 0.0.0.0 --port 8000 --reload