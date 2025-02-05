FROM python:3.12-alpine as base
WORKDIR /app/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk add --update --virtual .build-deps \
    build-base \
    python3-dev \
    libpq \
    gcc \
    libffi-dev

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

FROM python:3.12-alpine
WORKDIR /app/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /app:$PYTHONPATH

RUN apk add --update --no-cache libpq gettext

COPY --from=base /usr/local/bin/ /usr/local/bin/
COPY --from=base /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/

COPY ./start.dev.sh .
COPY ./start.prod.sh .

RUN chmod +x ./start.dev.sh && dos2unix ./start.dev.sh
RUN chmod +x ./start.prod.sh && dos2unix ./start.prod.sh

COPY ./telegram_bot/ ./telegram_bot/
