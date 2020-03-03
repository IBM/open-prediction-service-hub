FROM python:3.7

ENV ENVIRONMENT "local"
ENV BUILD_DIR="/app/build"
ENV RUNTIME_DIR="/app/runtime"


# Install dependencies and this project
WORKDIR ${BUILD_DIR}
COPY . ${BUILD_DIR}
RUN python3 -m pip install -r requirements.txt && python ${BUILD_DIR}/setup.py install


# Prepare runtime environment
WORKDIR ${RUNTIME_DIR}
COPY ./runtime ${RUNTIME_DIR}


# Prepare example ml model
RUN bash ${BUILD_DIR}/src/dynamic_hosting/example_model_training/train.sh &&\
    mkdir -p ${RUNTIME_DIR}/example_models/ &&\
    cp -r ${BUILD_DIR}/example_models/* ${RUNTIME_DIR}/example_models


USER nobody
EXPOSE 5000


# Default parameters:
#   Suppose user have at least 2 cores. The recommended number of worker is ((2 x $num_cores) + 1) = 5.
#   worker-class is not 'gthread'(Asyn) because ML is CPU bounded
#   Container schedulers typically expect logs to come out on stdout/stderr, thus gunicorn is configured to do so.
#   Gunicorn needs to store its temporary file in memory(/dev/shm)
CMD ["--workers=5", "--worker-class=sync", "--log-file=-", "--worker-tmp-dir", "/dev/shm"]

ENTRYPOINT ["gunicorn", "-b :5000", "--chdir", "/app/runtime", "wsgi:app"]