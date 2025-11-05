FROM python:3.9-slim

RUN apt-get update && apt-get install -y socat

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --break-system-packages

CMD ["socat", "TCP-LISTEN:9900,fork", "EXEC:python3 chall.py"]