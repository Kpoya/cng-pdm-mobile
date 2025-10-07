[app]
title = CNG PdM App
package.name = cngpdm
package.domain = org.example

source.dir = .
source.include_exts = py,pkl,txt

version = 0.1
requirements = python3,kivy,pandas,scikit-learn==1.6.1,numpy

[buildozer]
log_level = 2

[app]
android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
