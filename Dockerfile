FROM public.ecr.aws/amazonlinux/amazonlinux:2

# Install minimal dependencies
RUN yum update -y && \
    yum install -y \
    python3 \
    python3-pip \
    git \
    wget \
    unzip \
    zip \
    java-11-openjdk \
    which \
    && yum clean all

# Install buildozer
RUN pip3 install buildozer

WORKDIR /app

# Copy application
COPY . .

CMD ["/bin/bash"]
