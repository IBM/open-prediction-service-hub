FROM python:3.7


ENV ENVIRONMENT="local"
ENV BUILD_DIR="/app/build"
ENV RUNTIME_DIR="/app/runtime"
# Suppose user have at least 2 cpu cores. The recommended number of gunicorn worker is ((2 x $num_cores) + 1) = 5
ENV WORKER_NUM=5
ENV SERVICE_PORT=8080


# Install this project and prepare example for runtime
WORKDIR ${BUILD_DIR}
COPY . ${BUILD_DIR}

RUN python3 -m pip install -r requirements.txt && \
    python3 setup.py install

RUN bash src/main/python/dynamic_hosting/example_model_training/train.sh &&\
    mkdir -p ${RUNTIME_DIR}/example_models/ &&\
    cp -r example_models/* ${RUNTIME_DIR}/example_models


# Prepare runtime
WORKDIR ${RUNTIME_DIR}
COPY ./runtime ${RUNTIME_DIR}


USER nobody
EXPOSE ${SERVICE_PORT}

# Default parameters:
#   Uvicorn worker class is required by Fastapi
#   Container schedulers typically expect logs to come out on stdout/stderr, thus gunicorn is configured to do so
#   Gunicorn needs to store its temporary file in memory (e.g. /dev/shm)
ENTRYPOINT gunicorn --worker-class=uvicorn.workers.UvicornWorker --log-file=- --worker-tmp-dir=/dev/shm \
                    --chdir=${RUNTIME_DIR} \
                    --bind=:${SERVICE_PORT} \
                    --workers=${WORKER_NUM} asgi:app
