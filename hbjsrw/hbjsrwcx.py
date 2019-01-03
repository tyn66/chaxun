from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time,re,json
import sys,os
sys.path.append(os.getcwd())
from hbjsrw.utils import utils,yzm

def hbjsrw1(**kwargs):
    # driver = webdriver.PhantomJS()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver = webdriver.Chrome()
    driver.set_page_load_timeout(5)

    try:
        driver.get("http://dzjc.tsjsr.com/index-315-2.html")
        cph = kwargs["cph"]
        qlw = cph[1:2].upper()
        cph1 = cph[2:]
        #TODO 模拟点击车牌前两位

        driver.find_element_by_xpath(utils.dict1[qlw]).click()

        # TODO 模拟输入车牌后五位
        driver.find_element_by_id("carnum").send_keys(cph1)

        #TODO 模拟点击查询
        driver.find_element_by_id("button_submit").click()

        #TODO 拼接完整车牌号
        return jietu(driver,cph)
    except Exception as e:
        driver.quit()
        # L = ["服务器错误"]
        jsonL = {
            "code": 2,
            "msg": "服务器错误",
            "data": "",
        }
        with open("hbjsrw.txt", "a+") as f:
            f.write("河北驾驶人网爬虫错误1\n%s\n"%e)
        return json.dumps(jsonL, ensure_ascii=False)

def jietu(driver,cph):
    try:
        b = "%s.png"%(cph)
        time.sleep(1)
        handles = driver.window_handles
        driver.switch_to.window(driver.window_handles[len(handles)-1])
        driver.save_screenshot(b)
        imgelement = driver.find_element_by_xpath('//*[@id="piccode"]')  # 定位验证码
        location = imgelement.location  # 获取验证码x,y轴坐标
        size = imgelement.size  # 获取验证码的长宽
        rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                  int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
        i = Image.open(b)  # 打开截图
        frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
        frame4.save(b) # 保存我们接下来的验证码图片 进行打码
        return yzm1(driver,cph)
    except Exception as e:
        driver.quit()
        # L = ["服务器错误"]
        jsonL = {
            "code": 2,
            "msg": "服务器错误",
            "data": "",
        }
        with open("hbjsrw.txt", "a+") as f:
            f.write("河北驾驶人网爬虫错误2\n%s\n" % e)
        return json.dumps(jsonL, ensure_ascii=False)

def yzm1(driver,cph):
    try:
        b = "%s.png" % (cph)
        yzm2 = yzm.sbyzm(b)
        driver.find_element_by_id("code").send_keys(yzm2)
        driver.find_element_by_id("button_submit").click()
        try:
            time.sleep(0.5)
            print("重新截图")
            driver.find_element_by_xpath('//*[@id="state"]/input').click()
            return jietu(driver,cph)
        except :
            return cjh(driver,cph)
    except Exception as e:
        driver.quit()
        # L = ["服务器错误"]
        jsonL = {
            "code": 2,
            "msg": "服务器错误",
            "data": "",
        }
        with open("hbjsrw.txt", "a+") as f:
            f.write("河北驾驶人网爬虫错误3\n%s\n" % e)
        return json.dumps(jsonL, ensure_ascii=False)

def cjh(driver,cph):
    try:
        time.sleep(1)
        aa = driver.find_element_by_id('p02_01').text
        if aa == "请正确输入车架号后四位！":
            driver.quit()
            # L = ["车牌号输入有误"]
            jsonL = {
                "code": 0,
                "msg":"车牌号输入有误",
                "data": "",
            }
            return json.dumps(jsonL, ensure_ascii=False)
        else:
            time.sleep(1)
            aa = driver.find_element_by_id('p02_01').text
            if aa == "请正确输入车架号后四位！":
                driver.quit()
                # L = ["车牌号,车架号输入有误"]
                jsonL = {
                    "code": 0,
                    "msg":"车架号输入有误",
                    "data": "",
                }
                return json.dumps(jsonL, ensure_ascii=False)
            else:
                driver.quit()
                # L = ["服务器错误"]
                jsonL = {
                    "code": 2,
                    "msg": "服务器错误",
                    "data": "",
                }
                with open("hbjsrw.txt", "a+") as f:
                    f.write("河北驾驶人网爬虫错误4\n")
                return json.dumps(jsonL, ensure_ascii=False)
    except :
        try:
            return jieguo(driver,cph)
        except Exception as e:
            driver.quit()
            # L = ["服务器错误"]
            jsonL = {
                "code": 2,
                "msg": "服务器错误",
                "data": "",
            }
            with open("hbjsrw.txt", "a+") as f:
                f.write("河北驾驶人网爬虫错误5\n%s\n"%e)
            return json.dumps(jsonL, ensure_ascii=False)


def jieguo(driver,cph):
    try:
        time.sleep(0.5)
        aa = driver.page_source.replace('\n', '').replace('\r', '').replace('\t', '')
        bb = re.findall('累计违法： (.*?)条',aa)
        L = []
        if bb[0] == "0":
            driver.quit()
            dictd = {}
            dictd["cph"] = cph
            dictd["youwuwz"] = "暂无违章记录"
            L.append(dictd)
            jsonL = {
                "code": 1,
                "msg":"查询成功",
                "data": L,
            }
            return json.dumps(jsonL, ensure_ascii=False)
        else:
            cc = re.findall('class="con_box1".*?<p>(.*?)</p>.*?<h4>(.*?)</h4>.*?:(.*?)</p>.*?<p>罚款(.*?)元</p>.*?<p>扣(.*?)分</p> ',aa)
            for i in cc:
                dictd = {}
                dictd["cph"] = cph #车牌号
                dictd["youwuwz"] = "有违章记录"
                dictd["jffakuan"] = "罚款%s元扣%s分" %(i[3],i[4]) #扣几分罚多少钱
                dictd["time1"] = i[0] #违章时间
                dictd["site"] = i[1] #违章地址
                dictd["miaoshu"] = i[2] #违章描述
                L.append(dictd)
            driver.quit()
            jsonL = {
                "code": 1,
                "msg":"查询成功",
                "data": L,
            }
            with open("hbjsrw.txt", "a+") as f:
                f.write("\n河北驾驶人网爬虫成功")
            return json.dumps(jsonL, ensure_ascii=False)
    except Exception as e:
        driver.quit()
        # L = ["服务器错误"]
        jsonL = {
            "code": 2,
            "msg": "服务器错误",
            "data": "",
        }
        with open("hbjsrw.txt", "a+") as f:
            f.write("河北驾驶人网爬虫错误6\n%s\n")
        return json.dumps(jsonL, ensure_ascii=False)

if __name__ == '__main__':
    hbjsrw1()
    # while True:
    #     aa = hbjsrw(cph = "冀B6X9Y8" )
    #     print(aa)