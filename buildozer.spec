[app]
title = PDF Editor Pro
package.name = pdfeditorpro
package.domain = org.pdfeditor
version = 1.0.0

source.dir = .
source.include_exts = py,png,jpg,kv,ttf,otf,txt

requirements = python3,kivy,pymupdf,pillow

orientation = portrait
fullscreen = 0
log_level = 2

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_MEDIA_LOCATION

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True

warn_on_root = 0
