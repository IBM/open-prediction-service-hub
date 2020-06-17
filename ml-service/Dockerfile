FROM python:3.7


# set EML_RETRAIN_MODELS to always retrain all example models
# ARG EML_RETRAIN_MODELS=1
# Message color
ARG YELLOW='\033[1;33m'
ARG NC='\033[0m'
ARG APP_HOME="/app"

# ENV variables used by server
ENV model_storage=${APP_HOME}/storage


# Install dependences
COPY requirements.txt requirements-ml.txt /tmp/repo/
RUN \
    echo "${YELLOW}[INFO] Preparing installation.${NC}" && \
    cd /tmp/repo && \
    pip3 install --no-cache-dir --quiet --upgrade pip && \
    pip3 install --no-cache-dir --quiet --requirement requirements-ml.txt && \
    pip3 install --no-cache-dir --quiet --requirement requirements.txt


# Install this project
COPY . /tmp/repo/
RUN \
    mkdir ${APP_HOME}  && \
    cd /tmp/repo && \
    python3 setup.py --quiet install -O2 && \
    echo "${YELLOW}[INFO] Preparing examples.${NC}" && \
    python3 runtime/init.py && \
    cp -a /tmp/repo/runtime/. ${APP_HOME} && \
    rm -rf /tmp/repo && \
    adduser --quiet --system --no-create-home --group ops && \
    chown --recursive ops:ops ${APP_HOME}


USER ops
WORKDIR ${APP_HOME}
EXPOSE 8080


# Default parameters:
#   Uvicorn worker class is required by Fastapi
#   Container schedulers typically expect logs to come out on stdout/stderr, thus gunicorn is configured to do so
#   Gunicorn needs to store its temporary file in memory (e.g. /dev/shm)
ENTRYPOINT gunicorn \
            --worker-class=uvicorn.workers.UvicornWorker \
            --log-file=- \
            --worker-tmp-dir=/dev/shm \
            --chdir=${APP_HOME} \
            --bind=:8080 \
            --config=file:gunicorn.init.py \
            asgi:app
