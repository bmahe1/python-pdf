[app]

# App information
title = PDF Editor Pro
package.name = pdfeditorpro
package.domain = org.pdfeditor
version = 1.0.0

# Source files
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,txt,xml,json

# Requirements - CRITICAL for PDF functionality
requirements = python3,kivy==2.2.1,mupdf,pillow,openssl,urllib3,charset-normalizer,idna,pyopenssl,certifi,chardet

# Android specific
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_MEDIA_LOCATION,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_path = /root/.buildozer/android/platform/android-ndk-r25b
android.sdk_path = /root/.buildozer/android/platform/android-sdk
android.arch = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = True
android.install_location = auto

# Build settings
orientation = portrait
fullscreen = 0
log_level = 2
warn_on_root = 1

# Graphics (optional - for better performance)
#graphics = opengl

# Presplash screen (optional)
#presplash.filename = %(source.dir)s/assets/presplash.png
#presplash.color = #FFFFFF

# Icon (optional)
#icon.filename = %(source.dir)s/assets/icon.png

# Python-for-android settings
p4a.branch = develop
android.private_storage = True
android.enable_androidx = True

# Build optimization
android.num_cores = 4
android.build_tools_version = 33.0.0

# Signing (uncomment for release)
#android.release_artifact = .apk
#android.keystore = release.keystore
#android.keystore_passwd = 
#android.keyalias = 
#android.keyalias_passwd = 

# Logging
log_level = 2
log_level = 2
