FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pycryptodome

WORKDIR /app

COPY main.py /app/main.py

RUN chmod +x /app/main.py

CMD socat TCP-LISTEN:7777,reuseaddr,fork EXEC:"python3 /app/main.py"