FROM debian:buster-backports


# build args
ARG OPS_HOME="/app"

# ENV variables used by server
ENV PYTHONPATH="${OPS_HOME}:${PYTHONPATH}"
ENV OPS_HOME=${OPS_HOME}
ENV MODEL_STORAGE=${OPS_HOME}
ENV RETRAIN_MODELS=FALSE
ENV SSL_SETTINGS=${OPS_HOME}
ENV ENABLE_SSL=FALSE

RUN \
    echo "Acquire::http::Pipeline-Depth 0; \
Acquire::http::No-Cache true; \
Acquire::BrokenProxy    true;" > /etc/apt/apt.conf.d/99fixbadproxy

# Prepare python env
RUN \
    echo "\
    Acquire::http::Pipeline-Depth 0; \
    Acquire::http::No-Cache true; \
    Acquire::BrokenProxy    true; \
    " > /etc/apt/apt.conf.d/99fixbadproxy && \
    apt-get -qq update && \
    apt-get -qq --assume-yes --fix-missing install python3.7-dev git && \
    apt-get -qq --assume-yes --fix-missing install python3-pip && \
    rm -rf /var/lib/apt/lists/*


# add service user
RUN \
    adduser --quiet --shell /bin/false --gid 0 --system ops


# Install dependences
COPY requirements.txt requirements-ml.txt requirements-test.txt ${OPS_HOME}/
WORKDIR ${OPS_HOME}
RUN \
    python3 -m pip install --no-cache-dir --quiet --upgrade pip && \
    python3 -m pip install --no-cache-dir --quiet --requirement requirements-ml.txt && \
    python3 -m pip install --no-cache-dir --quiet --requirement requirements.txt && \
    python3 -m pip install --no-cache-dir --quiet --requirement requirements-test.txt


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
    chmod +x /entrypoint.sh && \
    chmod g=u /entrypoint.sh && \
    chown --recursive ops:root ${OPS_HOME} && \
    chmod --recursive g=u ${OPS_HOME}


USER ops
EXPOSE 8080
WORKDIR ${OPS_HOME}/app


ENTRYPOINT ["/entrypoint.sh"]
