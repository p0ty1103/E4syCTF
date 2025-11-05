FROM ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y socat && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r e4syctf && useradd -r -g e4syctf e4syctf
WORKDIR /home/e4syctf

COPY item_shop .
COPY libc.so.6 ./libc.so.6
COPY ld-linux-x86-64.so.2 ./ld-linux-x86-64.so.2
COPY flag.txt .

RUN chown -R e4syctf:e4syctf /home/e4syctf && \
    chmod 755 /home/e4syctf/item_shop

USER e4syctf

EXPOSE 9001

CMD ["socat", "TCP-LISTEN:9001,reuseaddr,fork", "EXEC:/home/e4syctf/ld-linux-x86-64.so.2 --library-path /home/e4syctf/ /home/e4syctf/item_shop,stderr"]