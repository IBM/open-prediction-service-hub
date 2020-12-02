# The build-stage image:
FROM smizy/scikit-learn

RUN pip install connexion[swagger-ui]

COPY . /app

EXPOSE 8080

ENTRYPOINT cd /app && \
           python -m openapi_server