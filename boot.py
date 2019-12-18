import pycom
import os


pycom.heartbeat(False)

print("booting")
if "next" in os.listdir() :
    print("Installing updates")
    os.rename("main", "old2")
    os.rename("next", "main")

print("launching")
print("cwd : ", os.getcwd())
print("listdir : ", os.listdir())
from main import main
print("success")
