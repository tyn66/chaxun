import datetime,socket,psutil,time,requests,json
def Heartbeat():
    """
    时间，ip地址，内存使用率，磁盘使用率
    :return:
    """
    #TODO ip地址
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    channel_ip = s.getsockname()[0] #ip地址
    s.close()

    #TODO 内存使用率
    memory = psutil.virtual_memory()
    channel_memery_total = round(memory.total / 1024 / 1024,2) #总内存
    channel_memery_used = round(memory.used / 1024 / 1024 ,2)#已用内存

    #TODO 磁盘使用率
    a = psutil.disk_usage('/')
    b = a.total / 1024 / 1024 / 1024 #磁盘总容量
    c = a.percent #磁盘使用率
    channel_disk_total = round(b,1)
    channel_disk_used = round(b*c,1)/100

    # TODO 监控服务器网卡使用率
    count = psutil.net_io_counters()
    time.sleep(1)
    count1 = psutil.net_io_counters()
    channel_bandwidth_total = 11111.11
    channel_bandwidth_used = ((count1.bytes_sent - count.bytes_sent) + (count1.bytes_recv  - count.bytes_recv))/1024*8

    channel_province = '冀'
    channel_id = 3
    channel_flag = 1
    # channel_type = 1 #1 为不要验证码
    need_vin = 4 #车架号 0 为不需要 4为后四位 6为后六位99为完整的
    need_engine_number = 0 #发动机号 0 为不需要 4为后四位 6为后六位99为完整的
    need_captcha = 0 #验证码 0 为不要验证码,1 为需要验证码
    need_car_type = 1
    a = {
        "channel_province": channel_province, #省份
        "channel_id": channel_id, # 通道ID
        "channel_ip": channel_ip, #服务器ip
        "channel_flag": channel_flag, #标识
        # "channel_type": channel_type,  # 通道类型
        "channel_memery_total": channel_memery_total, #总内存
        "channel_memery_used": channel_memery_used, #已用内存
        "channel_disk_total": channel_disk_total, #磁盘总量
        "channel_disk_used": channel_disk_used, #已用磁盘量
        "channel_bandwidth_total": channel_bandwidth_total, # 总带宽
        "channel_bandwidth_used": channel_bandwidth_used,#已用带宽
        "need_vin" : need_vin,#车架号 0 为不需要 4为后四位 6为后六位99为完整的
        "need_engine_number" : need_engine_number,#发动机号 0 为不需要 4为后四位 6为后六位99为完整的
        "need_captcha" : need_captcha,#验证码 0 为不要验证码,1 为需要验证码
        "need_car_type" : need_car_type,
    }
    return a

print(Heartbeat())


if __name__ == '__main__':
    try:
        while True:
            # url = "http://10.1.141.146:8080/0/"
            url = "http://ga.qibeiwang.com/danger/channel/index"
            data = Heartbeat()
            a = requests.post(url=url,data = data).content
            b = json.loads(a)
            print(b)
            time.sleep(60)
    except Exception as e:
        with open("heartbeat.txt","a+") as f:
            f.write("%s\n"%e)

