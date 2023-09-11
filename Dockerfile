FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

EXPOSE 8080

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080" ]