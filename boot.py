import pycom
import os


pycom.heartbeat(False)

print("booting")
if "next" in os.listdir() :
    print("Installing updates")
    os.rename("main", "old")
    os.rename("next/.version_on_reboot", "next/version.py")
    os.rename("next", "main")

print("launching")
print("cwd : ", os.getcwd())
print("listdir : ", os.listdir())
from main import main
print("success")
