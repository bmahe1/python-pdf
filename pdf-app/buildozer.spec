[app]
title = PDF Editor
package.name = pdfeditor
package.domain = org.mahesh

source.dir = .
source.include_exts = py,png,jpg,kv,pdf

requirements = python3,kivy,pymupdf

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# 🔴 REQUIRED FOR CI
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
