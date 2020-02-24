FROM python:3.7


# Install dependencies and this project
WORKDIR /build/
COPY . /build/
RUN python3 -m pip install -r requirements.txt &&\
    python ./setup.py install


# prepare runtime environment
WORKDIR /app/
COPY ./runtime /app/runtime


ENV ENVIRONMENT local
USER nobody
EXPOSE 5000


# Default parameters:
#   Suppose user have at least 2 cores. The recommended number of worker is ((2 x $num_cores) + 1) = 5.
#   worker-class is not 'gthread'(Asyn) because ML is CPU bounded
#   Container schedulers typically expect logs to come out on stdout/stderr, thus gunicorn is configured to do so.
#   Gunicorn needs to store its temporary file in memory(/dev/shm)
CMD ["--workers=5", "--worker-class=sync", "--log-file=-", "--worker-tmp-dir", "/dev/shm"]

ENTRYPOINT ["gunicorn", "-b :5000", "--chdir", "/app/runtime", "wsgi:app"]