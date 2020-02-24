FROM python:3.7

WORKDIR /app/

COPY requirements.txt /app/

COPY ml-model-dynamic-hosting/models/miniloandefault-rfc.joblib /app/models/
COPY ml-model-dynamic-hosting/models/miniloandefault-svc.joblib /app/models/
COPY ml-model-dynamic-hosting/models/miniloandefault-lr.joblib /app/models/

COPY ml-model-dynamic-hosting/models/miniloandefault-rfc.pkl /app/models/
COPY ml-model-dynamic-hosting/models/miniloandefault-svc.pkl /app/models/
COPY ml-model-dynamic-hosting/models/miniloandefault-lr.pkl /app/models/

COPY ml-model-dynamic-hosting/main.py ml-model-dynamic-hosting/__init__.py ml-model-dynamic-hosting/wsgi.py /app/


RUN pip install -r ./requirements.txt



ENV ENVIRONMENT local
USER nobody

EXPOSE 5000

# Default parameters:
#   Suppose user have at least 2 cores. The recommended number of worker is ((2 x $num_cores) + 1) = 5.
#   worker-class is not 'gthread'(Asyn) because ML is CPU bounded
#   Container schedulers typically expect logs to come out on stdout/stderr, thus gunicorn is configured to do so.
#   Gunicorn needs to store its temporary file in memory(/dev/shm)
CMD ["--workers=5", "--worker-class=sync", "--log-file=-", "--worker-tmp-dir", "/dev/shm"]

ENTRYPOINT ["gunicorn", "-b :5000", "wsgi:app"]