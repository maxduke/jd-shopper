FROM alpine:latest
MAINTAINER MaxDuke <maxduke@gmail.com>

# Create app directory
WORKDIR /app

# Copy files
COPY . .

RUN set -ex \
    && apk update \
    && apk upgrade \
    && apk add --no-cache --update python3 \
    && ln -sf python3 /usr/bin/python \
    && python3 -m ensurepip \
    && pip3 install --no-cache --upgrade pip setuptools \
# Install app dependencies
    && apk add --no-cache --virtual .build-deps g++ libxml2-dev libxslt-dev python3-dev \
    && apk add --no-cache libxslt  \
    && pip3 install -r /app/requirements.txt \
    && apk del .build-deps

EXPOSE 12021

CMD [ "python3", "runserver.py" ]
