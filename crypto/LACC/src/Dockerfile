FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install numpy

WORKDIR /app

COPY chall.py /app/chall.py

RUN chmod +x /app/chall.py

CMD ["python3", "/app/chall.py"]
