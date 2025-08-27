# syntax=docker/dockerfile:1

FROM python:3.11

ENV PYTHONUNBUFFERED=1  

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3006

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--timeout", "600", "--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
