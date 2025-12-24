FROM public.ecr.aws/amazonlinux/amazonlinux:2

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    ANDROID_HOME=/opt/android-sdk \
    PATH=$PATH:/opt/android-sdk/tools/bin:/opt/android-sdk/platform-tools

# Install system dependencies
RUN yum update -y && \
    yum install -y \
    python3 \
    python3-pip \
    python3-devel \
    git \
    wget \
    curl \
    unzip \
    zip \
    tar \
    which \
    java-11-openjdk-devel \
    gcc \
    gcc-c++ \
    make \
    patch \
    zlib-devel \
    openssl-devel \
    sqlite-devel \
    ncurses-devel \
    bzip2-devel \
    readline-devel \
    tk-devel \
    gdbm-devel \
    xz-devel \
    libffi-devel \
    mesa-libGL-devel \
    mesa-libGLU-devel \
    libXext \
    libXrender \
    libSM \
    libICE \
    libXt \
    libX11 \
    libXau \
    libxcb \
    && yum clean all

# Install Buildozer dependencies
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install buildozer cython==0.29.19

# Install Android SDK (minimal)
RUN mkdir -p /opt/android-sdk && \
    cd /opt/android-sdk && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-7583922_latest.zip && \
    unzip -q commandlinetools-linux-7583922_latest.zip && \
    rm commandlinetools-linux-7583922_latest.zip && \
    mkdir -p cmdline-tools && \
    mv tools cmdline-tools/latest

# Accept Android SDK licenses
RUN yes | /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager --licenses > /dev/null 2>&1 || true

# Create working directory
WORKDIR /app

# Copy application files
COPY . .

# Default command - will be overridden by docker run
CMD ["/bin/bash"]
