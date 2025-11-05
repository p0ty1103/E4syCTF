FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat
WORKDIR /app
COPY . .
RUN chmod +x chall

CMD ["socat", "TCP-LISTEN:12345,fork", "EXEC:./chall"]