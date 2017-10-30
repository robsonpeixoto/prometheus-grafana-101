FROM python:3.6-alpine

WORKDIR /code
ADD requirements.txt /code
RUN apk add --no-cache --virtual .build-dependencies gcc musl-dev && \
    pip install -r requirements.txt && \
    apk del .build-dependencies

ADD . /code
CMD ["python3", "hello.py"]
