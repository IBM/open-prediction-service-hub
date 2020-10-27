FROM python:3.7-slim

RUN pip3 install connexion[swagger-ui]

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
RUN \
    cd /usr/src/app && \
    python3 setup.py --quiet install -O2

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]