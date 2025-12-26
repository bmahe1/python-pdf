[app]
title = PDF Editor Pro
package.name = pdfeditorpro
package.domain = org.pdfeditor
source.dir = .
source.include_exts = py,png,jpg,kv
version = 1.0.0

# Keep deps minimal for speed
requirements = python3,kivy,pillow,pypdf

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[android]
# SDK / NDK
android.api = 33
android.minapi = 21
android.ndk = 25.1.8937393

# Build speed & stability
android.arch = arm64-v8a
android.skip_update = true
android.accept_sdk_license = true
android.enable_androidx = true

# Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.allow_backup = true
