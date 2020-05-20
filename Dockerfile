FROM python:3.7


ARG BUILD_DIR="/app/build"
# set EML_RETRAIN_MODELS to retrain all example models
ARG EML_RETRAIN_MODELS=1
# Message color
ARG YELLOW='\033[1;33m'
ARG NC='\033[0m'


ENV RUNTIME_DIR="/app/runtime"
ENV APP_USER="lml"
ENV SERVICE_PORT=8080
# Suppose server have 10 cpu cores. The recommended number of gunicorn worker is ((2 x $num_cores) + 1) = 21
ENV WORKER_NUM=21
# ENV variables used by server
ENV model_storage=${RUNTIME_DIR}/storage


# Install dependences
WORKDIR ${BUILD_DIR}
COPY requirements.txt requirements-ml.txt ${BUILD_DIR}/
RUN python3 -m pip install --quiet --upgrade pip && \
    echo "${YELLOW}[INFO] Preparing installation. This may take up to 10 minutes${NC}" && \
    python3 -m pip install --quiet -r requirements-ml.txt && \
    python3 -m pip install --quiet -r requirements.txt


# Install this project
COPY . ${BUILD_DIR}
RUN adduser --system --no-create-home --group ${APP_USER} && \
    python3 setup.py --quiet install -O2 && \
    # prepare example for runtime
    echo "${YELLOW}[INFO] Preparing examples. This may take up to 2 minutes${NC}" && \
    python3 runtime/init.py && \
    cp -r runtime ${RUNTIME_DIR}


# Prepare runtime
WORKDIR ${RUNTIME_DIR}
RUN chown --recursive ${APP_USER}:${APP_USER} ${RUNTIME_DIR}/*


USER ${APP_USER}
EXPOSE ${SERVICE_PORT}


# Default parameters:
#   Uvicorn worker class is required by Fastapi
#   Container schedulers typically expect logs to come out on stdout/stderr, thus gunicorn is configured to do so
#   Gunicorn needs to store its temporary file in memory (e.g. /dev/shm)
ENTRYPOINT gunicorn --worker-class=uvicorn.workers.UvicornWorker \
                    --log-file=- \
                    --worker-tmp-dir=/dev/shm \
                    --chdir=${RUNTIME_DIR} \
                    --bind=:${SERVICE_PORT} \
                    --workers=${WORKER_NUM} asgi:app
