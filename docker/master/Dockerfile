FROM python:3.7


VOLUME /app

# set EML_RETRAIN_MODELS to always retrain all example models
ARG EML_RETRAIN_MODELS=1
# Message color
ARG YELLOW='\033[1;33m'
ARG NC='\033[0m'

# Suppose server have 6 cpu cores. The recommended number of gunicorn worker is ((2 x $num_cores) + 1) = 13
ENV WORKER_NUM=13
# ENV variables used by server
ENV model_storage=/app


COPY . /tmp/repo/
RUN \
    echo "${YELLOW}[INFO] Preparing installation.${NC}" && \
    cd /tmp/repo && \
    python3 -m pip install --quiet --upgrade pip && \
    python3 -m pip install --quiet -r requirements-ml.txt && \
    python3 -m pip install --quiet -r requirements.txt && \
    python3 setup.py --quiet install -O2 && \
    python3 -m pip cache purge --quiet && \
    echo "${YELLOW}[INFO] Preparing examples.${NC}" && \
    python3 runtime/init.py && \
    cp -r runtime /app && \
    rm -rf /tmp/repo && \
    adduser --quiet --system --no-create-home --group lml && \
    chown --recursive lml:lml /app


USER lml
WORKDIR /app
EXPOSE 8080


# Default parameters:
#   Uvicorn worker class is required by Fastapi
#   Container schedulers typically expect logs to come out on stdout/stderr, thus gunicorn is configured to do so
#   Gunicorn needs to store its temporary file in memory (e.g. /dev/shm)
ENTRYPOINT gunicorn \
            --worker-class=uvicorn.workers.UvicornWorker \
            --log-file=- \
            --worker-tmp-dir=/dev/shm \
            --chdir=/app \
            --bind=:${SERVICE_PORT} \
            --workers=${WORKER_NUM} \
            asgi:app
