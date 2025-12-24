[app]
title = PDF Editor
package.name = pdfeditor
package.domain = org.mahesh
version = 1.0.0            # Required!

source.dir = .
source.include_exts = py,png,jpg,kv,pdf

requirements = python3,kivy,pymupdf

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# 🔴 CI/CD Android settings
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

[python]
# Python settings (optional)
# target_version = 3

[android]
# Optional Android-specific settings
# android.arch = armeabi-v7a

