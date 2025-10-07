[app]
title = CNG PdM App
package.name = cngpdm
package.domain = org.example

source.dir = .
source.include_exts = py,pkl,txt

version = 0.1
requirements = python3,kivy,pandas,scikit-learn,numpy  # Removed ==1.6.1 to avoid p4a conflict

[buildozer]
log_level = 2

[app]
android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
p4a.branch = master  # Latest p4a for toolchain fixes
p4a.bootstrap = sdl2  # Explicit bootstrap for Kivy
