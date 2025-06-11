FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./preprocessing.py /code/preprocessing.py
COPY ./ai.joblib /code/ai.joblib

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "81"]