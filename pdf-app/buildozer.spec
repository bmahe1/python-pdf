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

[buildozer]
log_level = 2
