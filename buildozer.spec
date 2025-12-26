[app]
title = PDF Editor Pro
package.name = pdfeditorpro
package.domain = org.pdfeditor
source.dir = .
source.include_exts = py,png,jpg,kv
version = 1.0.0

# Keep dependencies minimal and fast
requirements = python3,kivy,pillow,pypdf

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[android]
# SDK / API
android.api = 33
android.minapi = 21

# ✅ CRITICAL: pin build-tools to avoid 36.x license bug
android.build_tools_version = 33.0.2

# NDK
android.ndk = 25.1.8937393

# Architecture (fastest)
android.arch = arm64-v8a

# Stability / CI options
android.accept_sdk_license = true
android.skip_update = true
android.enable_androidx = true

# Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.allow_backup = true
