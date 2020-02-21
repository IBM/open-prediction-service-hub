FROM python:3.7

WORKDIR /app/

COPY requirements.txt /app/

COPY ml-model-dynamic-hosting/models/miniloandefault-rfc.joblib /app/models/
COPY ml-model-dynamic-hosting/models/miniloandefault-svc.joblib /app/models/
COPY ml-model-dynamic-hosting/models/miniloandefault-lr.joblib /app/models/

COPY ml-model-dynamic-hosting/models/miniloandefault-rfc.pkl /app/models/
COPY ml-model-dynamic-hosting/models/miniloandefault-svc.pkl /app/models/
COPY ml-model-dynamic-hosting/models/miniloandefault-lr.pkl /app/models/

RUN pip install -r ./requirements.txt

COPY ml-model-dynamic-hosting/main.py ml-model-dynamic-hosting/__init__.py /app/

#COPY data/miniloan-decisions-default-1K.csv /app/data/



# ENTRYPOINT /bin/bash
EXPOSE 5000

ENV ENVIRONMENT local

ENTRYPOINT python ./main.py