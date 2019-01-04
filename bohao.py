import os,time

#TODO 进行拨号
def aa():
    os.system("pppoe-start")
    os.system("ifconfig")

#TODO 断开拨号
def dd():
    os.system("pppoe-stop")
    os.system("/bin/systemctl stop NetworkManager.service")

while True:
    dd()
    time.sleep(1)
    aa()
    time.sleep(120)
