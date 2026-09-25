FROM python:3.12-slim

WORKDIR /app

COPY calculator.py .

CMD ["python", "calculator.py"]
