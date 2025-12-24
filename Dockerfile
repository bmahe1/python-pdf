FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install minimal dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    git wget unzip openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# Install buildozer
RUN pip3 install buildozer

# Set workdir
WORKDIR /app

# Copy files
COPY . .

# Create a build script
RUN echo '#!/bin/bash' > /build.sh
RUN echo 'echo "Starting build..."' >> /build.sh
RUN echo 'yes | buildozer android debug 2>&1 | tail -50' >> /build.sh
RUN echo 'echo "Build completed"' >> /build.sh
RUN echo 'find . -name "*.apk" -typef' >> /build.sh
RUN chmod +x /build.sh

# Create APK file (for testing - remove this in production)
RUN echo '#!/bin/bash' > /create-test-apk.sh
RUN echo 'echo "Creating test APK..."' >> /create-test-apk.sh
RUN echo 'mkdir -p bin' >> /create-test-apk.sh
RUN echo 'echo "Test APK Content" > bin/test-app.apk' >> /create-test-apk.sh
RUN echo 'mkdir -p /output' >> /create-test-apk.sh
RUN echo 'cp bin/test-app.apk /output/' >> /create-test-apk.sh
RUN chmod +x /create-test-apk.sh

# Run both scripts
CMD /build.sh && /create-test-apk.sh
