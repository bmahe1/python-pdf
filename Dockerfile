FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    git wget curl unzip zip \
    openjdk-17-jdk \
    libssl-dev libffi-dev libsqlite3-dev \
    libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install buildozer cython kivy

WORKDIR /app

COPY . .

CMD ["buildozer", "android", "debug"]
