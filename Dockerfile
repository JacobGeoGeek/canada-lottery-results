FROM python:3.12-slim

WORKDIR /app

COPY __init__.py /app/__init__.py
COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

ENV PYTHONPATH "${PYTHONPATH}:/app"

EXPOSE 8080

CMD [ "python", "src/main.py"]