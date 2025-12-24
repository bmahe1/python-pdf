[app]

# App information
title = PDF Editor Pro
package.name = pdfeditorpro
package.domain = org.pdfeditor
version = 1.0.0

# Source files
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,otf,txt

# Requirements
requirements = python3,kivy,mupdf,pillow,openssl,urllib3,charset-normalizer,idna,pyopenssl

# Android specific
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_MEDIA_LOCATION
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.arch = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True

# Build settings
orientation = portrait
fullscreen = 0
log_level = 2
warn_on_root = 1
