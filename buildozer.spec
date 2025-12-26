[app]
title = PDF Editor Pro
package.name = pdfeditorpro
package.domain = org.pdfeditor
source.dir = .
source.include_exts = py,png,jpg,kv
version = 1.0.0
requirements = python3,kivy,pillow,pypdf
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[android]
android.api = 33
android.minapi = 21

# 🔒 HARD PIN — DO NOT CHANGE
android.build_tools_version = 33.0.2
android.ndk = 25.1.8937393
android.arch = arm64-v8a

# 🔒 CI STABILITY
android.accept_sdk_license = true
android.skip_update = true
android.enable_androidx = true

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.allow_backup = true
