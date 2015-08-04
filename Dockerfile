#
# Dockerfile for kugou
#

FROM alpine
MAINTAINER kev <noreply@datageek.info>

COPY . /code
WORKDIR /code

RUN apk add -U curl python3 \
    && curl -sSL https://bootstrap.pypa.io/get-pip.py | python3 \
    && pip install -r requirements.txt \
    && rm -rf /var/cache/apk/*

EXPOSE 80
CMD ["python3", "run.py"]
