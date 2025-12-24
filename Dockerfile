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
    gcc \
    gcc-c++ \
    make \
    patch \
    zlib-devel \
    openssl-devel \
    && yum clean all

# Install buildozer and PDF libraries
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install buildozer cython==0.29.19
    # Uncomment for real PDF support:
    # pip3 install PyPDF2 reportlab pdf2image pillow

# Install Android SDK
RUN mkdir -p /opt/android-sdk/cmdline-tools && \
    cd /opt/android-sdk && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-7583922_latest.zip && \
    unzip -q commandlinetools-linux-7583922_latest.zip && \
    mv cmdline-tools latest && \
    mv latest cmdline-tools/ && \
    rm commandlinetools-linux-7583922_latest.zip

ENV ANDROID_HOME=/opt/android-sdk \
    PATH=$PATH:/opt/android-sdk/cmdline-tools/latest/bin:/opt/android-sdk/platform-tools

WORKDIR /app

COPY . .

CMD ["/bin/bash"]
