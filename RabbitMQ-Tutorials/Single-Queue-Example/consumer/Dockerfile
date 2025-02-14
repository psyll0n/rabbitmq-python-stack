FROM python:3.9

WORKDIR /app
COPY app.py .

RUN pip install pika

CMD ["python", "app.py"]