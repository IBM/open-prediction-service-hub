FROM python:3.7-slim


# build args
ARG OPS_HOME="/app"

# ENV variables used by server
ENV PYTHONPATH="${OPS_HOME}:${PYTHONPATH}"
ENV OPS_HOME=${OPS_HOME}
ENV MODEL_STORAGE=${OPS_HOME}
ENV RETRAIN_MODELS=FALSE
ENV SSL_SETTINGS=${OPS_HOME}
ENV ENABLE_SSL=FALSE
## ENV GUNICORN_TIMEOUT=30
## ENV GUNICORN_WORKER_NUM=16


# add service user
RUN \
    adduser --quiet --shell /bin/false --gid 0 --system ops


# Install dependences
COPY requirements.txt requirements-ml.txt ${OPS_HOME}/
WORKDIR ${OPS_HOME}
RUN \
    apt-get -qq clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get -qq clean && \
    apt-get -qq update && \
    apt-get -qq install --assume-yes --fix-missing git libgomp1 && \
    python3 -m pip install --no-cache-dir --upgrade pip --q && \
    python3 -m pip install --no-cache-dir --use-feature=2020-resolver --requirement requirements.txt -q && \
    # requirements-ml will overrides some libraries in requirements.txt which might raise some false positive
    # incompatibility errors.
    python3 -m pip install --no-cache-dir --use-feature=2020-resolver --requirement requirements-ml.txt -q && \
    apt-get -qq purge --auto-remove --assume-yes git && \
    rm -rf /var/lib/apt/lists/*


# Install this project
COPY . ${OPS_HOME}
COPY entrypoint.sh /entrypoint.sh
RUN \
    datamodel-codegen \
		--input app/gen/tmp.schemas.ops.yaml \
		--input-file-type openapi \
		--target-python-version 3.7 \
		--output app/gen/schemas/ops_schemas.py && \
    chown ops:root /entrypoint.sh && \
    chmod u+x /entrypoint.sh && \
    chmod g=u /entrypoint.sh && \
    chown --recursive ops:root ${OPS_HOME} && \
    chmod --recursive g=u ${OPS_HOME}


ENV CUSTOM_MODULES='/var/lib/ads-ml-service/custom'
ENV PYTHONPATH="${CUSTOM_MODULES}:${PYTHONPATH}"
COPY custom_modules ${CUSTOM_MODULES}
RUN chown --recursive ops:root ${CUSTOM_MODULES} && \
    chmod --recursive g=u ${CUSTOM_MODULES}
VOLUME ${CUSTOM_MODULES}


ENV LOG_DIR="/var/log/ads-ml-service"
RUN \
    mkdir -p "${LOG_DIR}" && \
    chown --recursive ops:root ${LOG_DIR} && \
    chmod --recursive g=u ${LOG_DIR}
VOLUME ${LOG_DIR}


USER ops
EXPOSE 8080
WORKDIR ${OPS_HOME}/app


ENTRYPOINT ["/entrypoint.sh"]
