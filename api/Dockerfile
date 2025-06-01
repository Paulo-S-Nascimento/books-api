FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install prometheus_client

EXPOSE 8000
EXPOSE 8001

CMD ["python", "server.py"]