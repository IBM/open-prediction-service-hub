FROM python:3.7


ENV BUILD_DIR="/app/build"
ENV RUNTIME_DIR="/app/runtime"
ENV APP_USER="lml"

# Suppose user have at least 2 cpu cores. The recommended number of gunicorn worker is ((2 x $num_cores) + 1) = 5
ENV WORKER_NUM=5
ENV SERVICE_PORT=8080

# ENV variables used by server
ENV model_storage=${RUNTIME_DIR}/storage


# Install this project and prepare example for runtime
WORKDIR ${BUILD_DIR}
COPY . ${BUILD_DIR}
RUN adduser --system --no-create-home --group ${APP_USER} && \
    python3 -m pip install -r requirements.txt && \
    python3 setup.py install


# Prepare runtime
WORKDIR ${RUNTIME_DIR}
COPY ./runtime ${RUNTIME_DIR}
RUN chown --recursive ${APP_USER}:${APP_USER} ${RUNTIME_DIR}/*


USER ${APP_USER}
EXPOSE ${SERVICE_PORT}

# Default parameters:
#   Uvicorn worker class is required by Fastapi
#   Container schedulers typically expect logs to come out on stdout/stderr, thus gunicorn is configured to do so
#   Gunicorn needs to store its temporary file in memory (e.g. /dev/shm)
ENTRYPOINT gunicorn --worker-class=uvicorn.workers.UvicornWorker --log-file=- --worker-tmp-dir=/dev/shm \
                    --chdir=${RUNTIME_DIR} \
                    --bind=:${SERVICE_PORT} \
                    --workers=${WORKER_NUM} asgi:app
