#!/bin/bash
set -e

echo "=== Starting APK build process ==="

# Check if required files exist
if [ ! -f "main.py" ]; then
    echo "ERROR: main.py not found!"
    echo "Creating a simple test app..."
    cat > main.py << 'EOF'
from kivy.app import App
from kivy.uix.label import Label

class PDFApp(App):
    def build(self):
        return Label(text='PDF Editor Pro\nBuilt with Docker', font_size=30)

if __name__ == '__main__':
    PDFApp().run()
EOF
fi

if [ ! -f "buildozer.spec" ]; then
    echo "ERROR: buildozer.spec not found!"
    echo "Creating buildozer.spec..."
    cat > buildozer.spec << 'EOF'
[app]
title = PDF Editor Pro
package.name = pdfeditorpro
package.domain = org.pdf
version = 1.0.0
source.dir = .
source.include_exts = py,png,jpg,kv,txt
requirements = python3,kivy==2.1.0
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 23b
orientation = portrait
fullscreen = 0
warn_on_root = 0
EOF
fi

echo "=== Initializing Buildozer ==="
buildozer init 2>&1 || true

echo "=== Cleaning previous builds ==="
buildozer android clean 2>&1 || true

echo "=== Building APK (this will take 20-30 minutes) ==="
# Build with timeout and verbose output
timeout 3600 buildozer -v android debug 2>&1 | tee build.log

echo "=== Checking build result ==="
if ls bin/*.apk 1> /dev/null 2>&1; then
    echo "✅ APK build successful!"
    APK_FILE=$(ls bin/*.apk | head -1)
    echo "APK: $APK_FILE"
    
    # Copy APK to output directory (mounted volume)
    mkdir -p /app/output
    cp "$APK_FILE" /app/output/
    echo "✅ APK copied to output directory"
else
    echo "❌ APK build failed!"
    echo "=== Build log errors ==="
    grep -i "error\|fail\|exception" build.log | head -20
    exit 1
fi
