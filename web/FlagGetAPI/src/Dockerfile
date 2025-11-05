FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --break-system-packages

CMD ["python3", "server.py"]