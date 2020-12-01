FROM python:3.7-slim AS python-base

ENV \
    OPS_HOME="/usr/src/ads-ml-service" \
    VIRTUAL_ENV="/opt/ads-ml-service/venv" \
    CUSTOM_MODULES='/var/lib/ads-ml-service/custom' \
    LOG_DIR="/var/log/ads-ml-service"
ENV \
    PATH="${VIRTUAL_ENV}/bin:${PATH}" \
    PYTHONPATH="${CUSTOM_MODULES}:${OPS_HOME}:${PYTHONPATH}"
WORKDIR ${OPS_HOME}


FROM python-base AS codegen-image

COPY app/gen/. app/gen/
RUN \
    python3 -m pip install -q --no-cache-dir --upgrade pip && \
    python3 -m pip install -q datamodel-code-generator~=0.5.30 && \
    datamodel-codegen \
		--input app/gen/tmp.schemas.ops.yaml \
		--input-file-type openapi \
		--target-python-version 3.7 \
		--output app/gen/schemas/ops_schemas.py


FROM python-base AS build-image

COPY requirements.txt requirements-ml.txt ./
RUN \
    apt-get -q update && \
    apt-get -q install --assume-yes git && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m venv ${VIRTUAL_ENV} && \
    python3 -m pip install -q --no-cache-dir --upgrade pip && \
    python3 -m pip install -q --no-cache-dir --use-feature=2020-resolver --requirement requirements.txt && \
    # requirements-ml will overrides some libraries in requirements.txt. This procedure might raise some false positive
    # incompatibility errors.
    python3 -m pip install -q --no-cache-dir --use-feature=2020-resolver --requirement requirements-ml.txt


FROM python-base AS runtime-image

ENV \
    MODEL_STORAGE="/var/lib/ads-ml-service" \
    RETRAIN_MODELS=FALSE \
    SETTINGS="/etc/ads-ml-service" \
    ENABLE_SSL=FALSE
    # ENV GUNICORN_TIMEOUT=30
    # ENV GUNICORN_WORKER_NUM=16

COPY . ./
COPY custom_modules ${CUSTOM_MODULES}
# COPY --from=codegen-image ${OPS_HOME}/app/gen/schemas/ops_schemas.py app/gen/schemas/
# COPY --from=build-image ${VIRTUAL_ENV} ${VIRTUAL_ENV}
# OpenShift 4.3 does not support ENV variables in COPY
COPY --from=codegen-image /usr/src/ads-ml-service/app/gen/schemas/ops_schemas.py app/gen/schemas/
COPY --from=build-image /opt/ads-ml-service/venv /opt/ads-ml-service/venv
COPY scripts/. scripts/
COPY entrypoint.sh /entrypoint.sh
COPY logging.yaml ${SETTINGS}/
RUN \
    apt-get -q update && \
    mkdir -p /usr/share/man/man1 && \
    apt-get -q install --assume-yes libgomp1 default-jre-headless && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p ${MODEL_STORAGE} && \
    mkdir -p "${LOG_DIR}" && \
    adduser --quiet --shell /bin/false --gid 0 --system ops && \
    chown ops:root /entrypoint.sh && \
    chmod u+x /entrypoint.sh && \
    chmod g=u /entrypoint.sh && \
    chown --recursive ops:root ${OPS_HOME} && \
    chmod --recursive g=u ${OPS_HOME} && \
    chown --recursive ops:root ${MODEL_STORAGE} && \
    chmod --recursive g=u ${MODEL_STORAGE} && \
    chown --recursive ops:root ${SETTINGS} && \
    chmod --recursive g=u ${SETTINGS} && \
    chown --recursive ops:root ${CUSTOM_MODULES} && \
    chmod --recursive g=u ${CUSTOM_MODULES} && \
    chown --recursive ops:root ${LOG_DIR} && \
    chmod --recursive g=u ${LOG_DIR}

VOLUME ${MODEL_STORAGE}
VOLUME ${SETTINGS}
VOLUME ${CUSTOM_MODULES}
VOLUME ${LOG_DIR}


USER ops
EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
