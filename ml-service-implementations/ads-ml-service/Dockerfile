FROM debian:buster-backports


# set EML_RETRAIN_MODELS to always retrain all example models
# ARG EML_RETRAIN_MODELS=1
# Message color
ARG YELLOW='\033[1;33m'
ARG NC='\033[0m'
ARG APP_HOME="/app"

# ENV variables used by server
ENV MODEL_STORAGE=${APP_HOME}/storage
ENV MODEL_CACHE_SIZE=16
ENV CACHE_TTL=20


# Install dependences
# python3 -m pip is recommanded way of using pip
COPY requirements.txt requirements-ml.txt /tmp/repo/
RUN \
    echo "${YELLOW}[INFO] Preparing installation.${NC}" && \
    cd /tmp/repo && \
    apt-get -qq update && \
    apt-get -qq install -y python3.7 && \
    apt-get -qq install -y python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install --no-cache-dir --quiet --upgrade pip && \
    python3 -m pip install --no-cache-dir --quiet --requirement requirements-ml.txt && \
    python3 -m pip install --no-cache-dir --quiet --requirement requirements.txt


# Install this project
COPY . /tmp/repo/
RUN \
    mkdir ${APP_HOME}  && \
    cd /tmp/repo && \
    python3 setup.py --quiet install -O2 && \
    echo "${YELLOW}[INFO] Preparing examples.${NC}" && \
    python3 src/runtime/init.py && \
    cp -a /tmp/repo/src/runtime/. ${APP_HOME} && \
    cd ${APP_HOME} && \
    rm -rf /tmp/repo && \
    rm -rf /etc/mysql


# Security settings
# OpenShift inserted users is in root group (gid=0)
RUN \
    adduser --quiet --shell /bin/false --gid 0 --system ops && \
    chown --recursive ops:root ${APP_HOME} && \
    # Give inserted user permissions
    chmod --recursive g=u ${APP_HOME}


USER ops
WORKDIR ${APP_HOME}
EXPOSE 8080


# Default parameters:
#   Uvicorn worker class is required by Fastapi
#   Container schedulers typically expect logs to come out on stdout/stderr, thus gunicorn is configured to do so
#   Gunicorn needs to store its temporary file in memory (e.g. /dev/shm)
ENTRYPOINT \
    [ \
        "gunicorn", \
            "--worker-class=uvicorn.workers.UvicornWorker", \
            "--log-file=-", \
            "--worker-tmp-dir=/dev/shm", \
            "--config=file:gunicorn.init.py", \
            "asgi:app" \
    ]

# Default port is 8080
CMD ["--bind=:8080"]
