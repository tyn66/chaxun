import os,time

def aa():
    os.system("ifconfig")
    os.system("pppoe-start")
def dd():
    os.system("pppoe-stop")
    os.system("/bin/systemctl stop NetworkManager.service")

while True:
    dd()
    time.sleep(1)
    aa()
    time.sleep(1)
