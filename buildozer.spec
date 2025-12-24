[app]
title = PDF Editor Pro
package.name = pdfeditor
package.domain = org.pdfeditor
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf
version = 1.0.0
requirements = python3,kivy==2.1.0
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.sdk = 23
android.ndk = 23b
android.arch = arm64-v8a

# Increase heap size for better performance
android.heap_size = 512m

# Add these for PDF libraries (if using real PDF manipulation)
# android.gradle_dependencies = com.itextpdf:itext7-core:7.2.5
