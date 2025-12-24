FROM public.ecr.aws/amazonlinux/amazonlinux:2

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
    && yum clean all

# Install Buildozer and dependencies
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install buildozer cython==0.29.19 virtualenv

# Install Android SDK
RUN mkdir -p /opt/android-sdk
RUN cd /opt/android-sdk && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip && \
    unzip -q commandlinetools-linux-8512546_latest.zip && \
    rm commandlinetools-linux-8512546_latest.zip && \
    mkdir -p cmdline-tools && \
    mv tools cmdline-tools/latest

# Set environment variables
ENV ANDROID_HOME=/opt/android-sdk \
    PATH=$PATH:/opt/android-sdk/cmdline-tools/latest/bin:/opt/android-sdk/platform-tools

# Accept licenses (non-interactive)
RUN yes | /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager --licenses > /dev/null 2>&1 || true

WORKDIR /app

COPY . .

CMD ["/bin/bash"]
