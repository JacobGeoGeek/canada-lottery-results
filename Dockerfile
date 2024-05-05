FROM python:3.12-slim

WORKDIR /app

COPY __init__.py /app/__init__.py
COPY ./requirements.txt /app/requirements.txt
COPY alembic.ini /app/alembic.ini
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV ENVIRONMENT="DEV"
ENV ROOT_PATH=""
ENV PORT=8080
ENV HOST="0.0.0.0"
ENV RAPIDAPI_PROXY_SECRET=""
ENV DATABASE_CONNECTION_STRING=""
ENV SENDER_EMAIL=""
ENV SENDER_PASSWORD=""
ENV RECIPIENT_EMAIL=""
ENV SMTP_SERVER="smtp.gmail.com"
ENV SMTP_PORT=587

EXPOSE ${PORT}

ENTRYPOINT bash /app/entrypoint.sh