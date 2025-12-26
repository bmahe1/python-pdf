FROM ubuntu:22.04

# Set non-interactive frontend for apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    wget \
    curl \
    unzip \
    zip \
    libssl-dev \
    libffi-dev \
    libsqlite3-dev \
    libjpeg-dev \
    zlib1g-dev \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# Install Android SDK
RUN mkdir -p /opt/android-sdk
RUN cd /opt/android-sdk && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip && \
    unzip -q commandlinetools-linux-9477386_latest.zip && \
    rm commandlinetools-linux-9477386_latest.zip && \
    mkdir -p cmdline-tools && \
    mv cmdline-tools/bin cmdline-tools/latest

# Set environment variables
ENV ANDROID_HOME=/opt/android-sdk \
    PATH=$PATH:/opt/android-sdk/cmdline-tools/latest

# Accept licenses
RUN yes | /opt/android-sdk/cmdline-tools/latest/sdkmanager --licenses > /dev/null 2>&1 || true

# Install build tools
RUN /opt/android-sdk/cmdline-tools/latest/sdkmanager \
    "platform-tools" \
    "platforms;android-33" \
    "build-tools;33.0.2"

# Install Python dependencies
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install buildozer cython

WORKDIR /app

COPY . .

# Build command
CMD ["buildozer", "android", "debug"]
