# Use Ubuntu 20.04 as base
FROM ubuntu:20.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    python3.9-dev \
    git \
    wget \
    unzip \
    openjdk-11-jdk \
    build-essential \
    libssl-dev \
    libffi-dev \
    zlib1g-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libncurses5-dev \
    libreadline-dev \
    pkg-config \
    autoconf \
    automake \
    libtool \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.9 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Install Python packages
RUN python3 -m pip install --upgrade pip
RUN pip3 install buildozer cython virtualenv

# Create non-root user (buildozer doesn't like root)
RUN useradd -m -s /bin/bash builder
USER builder
WORKDIR /home/builder

# Set up Android SDK environment
ENV ANDROID_HOME=/home/builder/.buildozer/android/platform/android-sdk
ENV PATH="${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools:${PATH}"

# Create app directory
RUN mkdir -p /home/builder/app
WORKDIR /home/builder/app

# Copy build script
COPY --chown=builder:builder build-app.sh /home/builder/app/

# Copy application files
COPY --chown=builder:builder . /home/builder/app/

# Set execute permission
RUN chmod +x /home/builder/app/build-app.sh

# Set entrypoint
ENTRYPOINT ["/home/builder/app/build-app.sh"]
