from selenium import webdriver
from PIL import Image
from jgw.utils.utils import getNoHtml
from jgw.utils.jgw_utils import dictsfjc,dictszm,dictcllx
from jgw.utils.ipc import LL
import time,re,json,random

def pachong(**kwargs):
    # chromeOptions = webdriver.ChromeOptions()
    # a = random.randint(0,len(LL))
    # print(LL[a][0])
    # # 设置代理
    # chromeOptions.add_argument("--proxy-server=http://%s:%s"%(LL[a][0],LL[a][1]))
    # # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
    # driver = webdriver.Chrome(chrome_options = chromeOptions)
    driver = webdriver.Chrome()
    driver.maximize_window()
    url = "http://m.hbgajg.com/"
    driver.get(url)
    try:
        b = driver.find_element_by_id("reload-button").text
        print(b)
        if b == '运行 Windows 网络诊断':
            driver.quit()
            L = ["网络连接错误"]
            jsonL = {
                "code": 0,
                "data": L,
            }
            return json.dumps(jsonL, ensure_ascii=False)
    except Exception as e:
        print(e)
    #TODO 模拟点击省份简称
    time.sleep(0.5)
    sfjc = kwargs["sfjc"]
    # sfjc = "冀"
    driver.find_element_by_xpath(dictsfjc[sfjc]).click()
    # driver.find_element_by_xpath('//*[@id="carArea"]/option[3]').click()
    #TODO 模拟点击字母
    time.sleep(0.5)
    szm = kwargs["szm"]
    # szm = "B"
    driver.find_element_by_xpath(dictszm[str.upper(szm)]).click()
    #TODO 模拟输入车牌号
    time.sleep(0.5)
    cph = kwargs["cph"]
    # cph = "6X9Y8"
    driver.find_element_by_id("CC_JDCWZ_Two").send_keys(cph)
    #TODO 模拟点击车辆类型
    time.sleep(0.5)
    cllx = kwargs["cllx"]
    # cllx = "小型汽车"
    driver.find_element_by_xpath(dictcllx[cllx]).click()
    #TODO 模拟输入车辆识别号后四位
    time.sleep(0.5)
    sbm = kwargs["sbm"]
    # sbm = "7986"
    driver.find_element_by_id("CC_JDCWZ_Four").send_keys(sbm)
    driver.find_element_by_class_name("srhbtn").click()
    pachongjietu(driver)
    #跳转最新页面
def pachongjietu(driver):
    time.sleep(2)
    handles = driver.window_handles
    driver.switch_to.window(driver.window_handles[len(handles)-1])
    driver.save_screenshot("截图.jpg")
    imgelement = driver.find_element_by_xpath('//*[@id="checkcodeimg"]')  # 定位验证码
    location = imgelement.location  # 获取验证码x,y轴坐标
    size = imgelement.size  # 获取验证码的长宽
    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
              int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
    i = Image.open("截图.png")  # 打开截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4.save('验证码.png') # 保存我们接下来的验证码图片 进行打码
    pachongshuaxin(driver)
def pachongshuaxin(driver,**kwargs):
    # hyz = kwargs["hyz"]
    hyz = input("是否换一张")
    # hyz = kwargs["hyz"]
    if hyz == "是":
        driver.find_element_by_xpath('//*[@id="checkcodeform"]/div/div[1]/a').click()
        pachongjietu(driver)
    else:
        # yzm = kwargs["yzm"]
        yzm = input("请输入汉字或汉字拼音")
        # yzm = kwargs["yzm"]
        driver.find_element_by_id("inputcode").send_keys(yzm)
        driver.find_element_by_class_name("srhbtn").click()
        pachongjieguo(driver)
def pachongjieguo(driver):
    time.sleep(2)
    # 跳转最新页面
    handles = driver.window_handles
    driver.switch_to.window(driver.window_handles[len(handles)-1])
    a = driver.page_source.replace('\n', '').replace('\r', '').replace('\t', '')
    b = re.findall('<title>(.*?)</title>',a)
    if b[0] == "违法查询结果 - 河北公安交管手机网":
        time.sleep(5)
        a = driver.page_source.replace('\n', '').replace('\r', '').replace('\t', '')
        b = re.findall('车辆状态</td><td><p>(.*?)</p>.*?机动车违法信息.*?class="ph">(.*?)</p>',a)
        print(b[0][0])
        if b[0][0] == "违法未处理":
            c = re.findall('违章时间.*?<strong>(.*?)</strong>.*?违章处理.*?<p>(.*?)</p>.*?采集机关.*?<p>(.*?)</p>.*?违法地址.*?<p>(.*?)</p>.*?违法行为.*?:(.*?)</p>',a)
            driver.quit()
            L = []
            for i in c:
                dictd = {}
                dictd["time"] = getNoHtml(i[0])
                dictd["jffakuan"] = getNoHtml(i[1])
                dictd["chuli"] = b[0][0]
                dictd["cjjg"] = getNoHtml(i[2])
                dictd["site"] = getNoHtml(i[3])
                dictd["miaoshu"] = getNoHtml(i[4])
                L.append(dictd)
            # 关闭浏览器
            driver.quit()
            jsonL = {
                "code": 1,
                "data": L,
            }
            return json.dumps(jsonL, ensure_ascii=False)
    else:
        L = ["验证码输入错误"]
        jsonL = {
            "code": 2,
            "data": L,
        }
        return json.dumps(jsonL, ensure_ascii=False)
# pachong(
#     sfjc = input('输入省份简称'),szm = input("输入首字母"),cph = input('输入车牌号后五位'),
#     cllx = input('输入车辆类型'),sbm = input('输入车辆识别号四位')
# )
