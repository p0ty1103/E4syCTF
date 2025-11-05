FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY server/ ./server/
WORKDIR /src/server

RUN dotnet restore
RUN dotnet publish -c Release -r linux-x64 --self-contained -p:PublishSingleFile=true -o /app/publish

FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    libicu70 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash e4syctf
WORKDIR /home/e4syctf

COPY --from=build /app/publish /home/e4syctf/app

COPY server/run.sh /home/e4syctf/run.sh

COPY flag.txt /home/e4syctf/flag.txt

RUN chown -R e4syctf:e4syctf /home/e4syctf && chmod +x /home/e4syctf/run.sh

USER e4syctf

EXPOSE 9999

CMD ["/home/e4syctf/run.sh"]