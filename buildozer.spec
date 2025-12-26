[app]
title = PDF Editor Pro
package.name = pdfeditorpro
package.domain = org.pdfeditor
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,json,txt
version = 1.0.0
requirements = python3,kivy==2.1.0,pypdf2,reportlab,pillow
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25.1.8937393
android.arch = arm64-v8a
android.gradle_dependencies = com.itextpdf:itext7-core:7.2.5

[ios]

[buildozer]
log_level = 2
