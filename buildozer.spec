[app]

title = Temettu
package. name = temettu
package. domain = org.temettu

source.dir = . 
source.include_exts = py,png,jpg,kv,atlas

version = 1.0. 0

requirements = python3,kivy,requests,pillow

orientation = portrait

fullscreen = 0

android. permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
