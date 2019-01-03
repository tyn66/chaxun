from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time,re,json
import os
import sys
sys.path.append(os.getcwd())
from cxy.utils import utils
def cxy(**kwargs):
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    driver = webdriver.Chrome()

    # driver = webdriver.PhantomJS()
    driver.set_page_load_timeout(5)

    try:
        cph = kwargs["cph"]
        cjh = kwargs["sbm"]
        cityname = cph[1]
        cph1 = cph[2:]
        driver.get("http://www.cx580.cn/query.php")
        #TODO 将不可见元素变为可见元素
        js = "document.getElementById('Province').style.display='block'"  # 编写JS语句
        driver.execute_script(js)  # 执行JS

        js = "document.getElementById('City').style.display='block'"  # 编写JS语句
        driver.execute_script(js)  # 执行JS

        #TODO 模拟点击省份
        driver.find_element_by_xpath('//*[@id="Province"]/option[9]').click()
        driver.find_element_by_xpath(utils.dictcphszm[cityname]).click()

        # TODO 模拟输入车牌后五位
        driver.find_element_by_id("txtCarNumber").send_keys(cph1)

        # TODO 模拟输入车架号
        driver.find_element_by_id("txtCarCode").send_keys(cjh)

        #TODO 模拟点击智能验证
        driver.find_element_by_id("rectMask").click()
        time.sleep(2.5)

        #TODO 模拟点击开始查询
        driver.find_element_by_id("BtnSubmit").click()
        handles = driver.window_handles
        driver.switch_to.window(driver.window_handles[len(handles) - 1])
        a = driver.page_source.replace('\n', '').replace('\r', '').replace('\t', '')
        b = re.findall('class="noresult">(.*?)</div>',a)
        if len(b)>0:
            L = []
            if b[0] == "输入车牌号有误":
                driver.quit()
                # dictd = {}
                # dictd["cph"] = cph
                # dictd["youwuwz"] = "输入车牌号有误"
                # L.append(dictd)
                jsonL = {
                    "code": 0,
                    "msg" :"输入车牌号有误",
                    "data": "",
                }
                return json.dumps(jsonL, ensure_ascii=False)
            elif b[0] == "错误：车架号错误":
                driver.quit()
                # dictd = {}
                # dictd["cph"] = cph
                # dictd["youwuwz"] = "车架号错误"
                # L.append(dictd)
                jsonL = {
                    "code": 0,
                    "msg":"车架号错误",
                    "data": "",
                }
                return json.dumps(jsonL, ensure_ascii=False)
            elif b[0] == "错误：错误=&gt;车辆信息错误":
                driver.quit()
                # dictd = {}
                # dictd["cph"] = cph
                # dictd["youwuwz"] = "车辆信息错误"
                # L.append(dictd)
                jsonL = {
                    "code": 0,
                    "msg":"车辆信息错误",
                    "data": "",
                }
                return json.dumps(jsonL, ensure_ascii=False)
            elif b[0] == "暂无违章记录！":
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
        c = re.findall('违章时间：(.*?)</span>.*?违章地点：(.*?)</span>.*?违章原因：(.*?)</span>.*?class="row_gs">.*?</p><p>(.*?)</p><p>(.*?)</p>',a)
        if len(c) == 0 :
            # driver.quit()
            # L = ["服务器错误"]
            jsonL = {
                "code": 2,
                "msg": "服务器错误",
                "data": "",
            }
            with open("cxy.txt", "a+") as f:
                f.write("车行易模拟点击验证时间太短\n")
            return json.dumps(jsonL, ensure_ascii=False)
        L = []
        for i in c:
            dictd = {}
            dictd["cph"] = cph
            dictd["youwuwz"] = "有违章记录"
            dictd["jffakuan"] = "罚款%s元扣%s分" %(i[3],i[4])
            dictd["time1"] = i[0]
            dictd["site"] = i[1]
            dictd["miaoshu"] = i[2]
            L.append(dictd)
        driver.quit()
        jsonL = {
            "code": 1,
            "msg": "查询成功",
            "data": L,
        }
        return json.dumps(jsonL, ensure_ascii=False)

    except Exception as e:
        driver.quit()
        # L = ["服务器错误"]
        jsonL = {
            "code": 2,
            "msg": "服务器错误",
            "data": "",
        }
        # utils.logger.warning("车行易爬虫错误")
        with open("cxy.txt", "a+") as f:
            f.write("车行易爬虫错误\n")
        return json.dumps(jsonL, ensure_ascii=False)

if __name__ == '__main__':
    # cxy()
    print(cxy(cph="冀E742Y6",sbm="3985"))