FROM debian:buster-backports


# Message color
ARG YELLOW='\033[1;33m'
ARG NC='\033[0m'

ARG APP_HOME="/app"
ARG RETRAIN_MODELS=false
ENV PYTHONPATH="${PYTHONPATH}:${APP_HOME}/src"

# ENV variables used by server
ENV MODEL_STORAGE=${APP_HOME}
ENV MODEL_CACHE_SIZE=16
ENV CACHE_TTL=20

RUN \
    echo "Acquire::http::Pipeline-Depth 0; \
Acquire::http::No-Cache true; \
Acquire::BrokenProxy    true;" > /etc/apt/apt.conf.d/99fixbadproxy

# Prepare python env
RUN \
    rm -rf /var/lib/apt/lists/* && \
    apt-get -qq update && \
    apt-get -qq --assume-yes --fix-missing install python3.7-dev && \
    apt-get -qq --assume-yes --fix-missing install python3-pip && \
    rm -rf /var/lib/apt/lists/*


WORKDIR ${APP_HOME}

# Install dependences
# python3 -m pip is the recommanded way of using pip
COPY requirements.txt requirements-ml.txt ${APP_HOME}/
RUN \
    echo "${YELLOW}[INFO] Preparing installation.${NC}" && \
    cd /tmp/repo && \
    python3 -m pip install --no-cache-dir --quiet --upgrade pip && \
    python3 -m pip install --no-cache-dir --quiet --requirement requirements-ml.txt && \
    python3 -m pip install --no-cache-dir --quiet --requirement requirements.txt


# Install this project
COPY . ${APP_HOME}
RUN \
    echo "${YELLOW}[INFO] Preparing examples.${NC}" && \
    chmod +x ./prestart.sh && ./prestart.sh


# Security settings
# OpenShift inserted users is in root group (gid=0)
RUN \
    adduser --quiet --shell /bin/false --gid 0 --system ops && \
    chown --recursive ops:root ${APP_HOME} && \
    # Give inserted user permissions
    chmod --recursive g=u ${APP_HOME}


USER ops
EXPOSE 8080
WORKDIR ${APP_HOME}/src/predictions


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
            "main:app" \
    ]

# Default port is 8080
CMD ["--bind=:8080"]
