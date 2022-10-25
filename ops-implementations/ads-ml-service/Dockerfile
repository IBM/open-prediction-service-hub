FROM --platform=${BUILDPLATFORM} python:3.11-slim AS python-base

ENV \
    OPS_HOME="/usr/src/ads-ml-service" \
    VIRTUAL_ENV="/usr/src/ads-ml-service/venv" \
    CUSTOM_MODULES='/var/lib/ads-ml-service/custom' \
    PATH="/usr/src/ads-ml-service/venv/bin:${PATH}" \
    PYTHONPATH="/var/lib/ads-ml-service/custom:/usr/src/ads-ml-service:${PYTHONPATH}" \
    MODEL_STORAGE="/var/lib/ads-ml-service/models" \
    RETRAIN_MODELS=FALSE
WORKDIR /usr/src/ads-ml-service


FROM python-base AS codegen-image

COPY app/gen/. app/gen/
RUN \
    python3 -m pip install -q --no-cache-dir --upgrade pip && \
    python3 -m pip install -q datamodel-code-generator~=0.11.19 && \
    datamodel-codegen \
		--input app/gen/tmp.schemas.ops.yaml \
		--input-file-type openapi \
		--target-python-version 3.7 \
		--output app/gen/schemas/ops_schemas.py


FROM python-base AS build-image

COPY requirements.txt ./
COPY logging.yaml /etc/ads-ml-service/logging/logging.yaml
RUN \
    python3 -m venv /usr/src/ads-ml-service/venv && \
    python3 -m pip install -q --no-cache-dir --upgrade pip && \
    python3 -m pip install -q --no-cache-dir --requirement requirements.txt && \
    mkdir -p /var/log/ads-ml-service && \
    mkdir -p /var/lib/ads-ml-service/models


FROM python-base AS runtime-image

COPY --chown=nobody:root --from=codegen-image /usr/src/ads-ml-service/app/gen/schemas/ops_schemas.py app/gen/schemas/
COPY --chown=nobody:root --from=build-image /usr/src/ads-ml-service/venv /usr/src/ads-ml-service/venv
COPY --chown=nobody:root --from=build-image /var/lib/ads-ml-service/models /var/lib/ads-ml-service/models
COPY --chown=nobody:root --from=build-image /var/log/ads-ml-service /var/log/ads-ml-service
COPY --chown=nobody:root --from=build-image /etc/ads-ml-service /etc/ads-ml-service
COPY --chown=nobody:root entrypoint.sh /entrypoint.sh
COPY --chown=nobody:root logging.yaml /usr/src/ads-ml-service/logging.yaml
COPY --chown=nobody:root custom_modules/. /var/lib/ads-ml-service/custom/
COPY --chown=nobody:root prestart.sh /usr/src/ads-ml-service/prestart.sh
COPY --chown=nobody:root preload-conf.yaml /usr/src/ads-ml-service/preload-conf.yaml
COPY --chown=nobody:root app /usr/src/ads-ml-service/app
COPY --chown=nobody:root alembic.ini /usr/src/ads-ml-service/alembic.ini
COPY --chown=nobody:root alembic /usr/src/ads-ml-service/alembic
COPY --chown=nobody:root examples/model_training_and_deployment /usr/src/ads-ml-service/examples/model_training_and_deployment
RUN \
    apt-get -q update && \
    mkdir -p /usr/share/man/man1 && apt-get -q install --assume-yes libgomp1 openjdk-11-jre-headless && \
    rm -rf /var/lib/apt/lists/* && \
    chmod u+x /entrypoint.sh && \
    chmod g=u /entrypoint.sh && \
    chmod --recursive g=u app/tests && \
    chmod --recursive g=u /var/log/ads-ml-service && \
    chmod --recursive g=u /etc/ads-ml-service && \
    chmod --recursive g=u /var/lib/ads-ml-service/models

VOLUME /var/lib/ads-ml-service/models
VOLUME /var/log/ads-ml-service

EXPOSE 8080
USER nobody

ENTRYPOINT ["/entrypoint.sh"]
