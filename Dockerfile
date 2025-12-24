FROM ubuntu:20.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install everything
RUN apt-get update && apt-get install -y \
    python3.9 python3-pip python3.9-dev \
    git wget unzip openjdk-11-jdk \
    build-essential libssl-dev libffi-dev \
    zlib1g-dev libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Install buildozer
RUN pip3 install buildozer cython

# Set up app directory
WORKDIR /app

# Copy app files
COPY . .

# Build command
CMD buildozer android debug && cp -r bin /app/output/ 2>/dev/null || echo "Build may have issues"
