import pycom
import os


pycom.heartbeat(False)

print("booting")
if "next" in os.listdir() :
    print("Installing updates")
    if "old" in os.listdir() :
        for file_name in os.listdir("old") :
            os.remove("old/" + file_name)
        os.rmdir("old")
    os.rename("main", "old")
    os.rename("next/.version_on_reboot", "next/version.py")
    os.rename("next", "main")

print("launching")
print("cwd : ", os.getcwd())
print("listdir : ", os.listdir())
from main import main
print("bad")
