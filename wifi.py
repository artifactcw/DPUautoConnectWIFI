import subprocess

import selenium.common.exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.edge.options import Options

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service


class Wifi:
    def __init__(self, ssid):
        # 使用示例
        target_ssid = "DPU_LianTong"  # 替换为你的目标 WiFi 名称
        current_ssid = self.get_current_wifi_ssid()

        if current_ssid:
            print("当前 SSID:", current_ssid)
        else:
            print("无 WiFi 连接.")

        if current_ssid != target_ssid:
            print("非目标WIFI连接. Connecting...")
            self.connect_to_wifi(target_ssid)
        else:
            print("已连接目标 WiFi"+ssid)

    def get_current_wifi_ssid(self):
        """ 获取当前连接的 WiFi 名称 """
        try:
            # 使用 netsh 命令获取无线网络接口信息
            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True,
                                    encoding='utf-8')

            if result.returncode != 0:
                print("WiFi信息获取错误:", result.stderr)
                return None

            # 解析输出内容，找出 SSID
            output = result.stdout
            ssid = None
            lines = output.split('\n')
            for line in lines:
                if "SSID" in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        ssid = parts[1].strip()
                        break
            return ssid
        except Exception as e:
            print("Error occurred:", e)
            return None

    def connect_to_wifi(self, ssid):
        """ 连接到指定的 WiFi 网络 """
        try:
            # 使用 netsh 命令连接到指定的 WiFi
            result = subprocess.run(['netsh', 'wlan', 'connect', 'name=' + ssid], capture_output=True, text=True,
                                    encoding='utf-8')
            if result.returncode != 0:
                print("Error connecting to WiFi:", result.stderr)
            else:
                print("Connected to WiFi:", ssid)
        except Exception as e:
            print("Error occurred:", e)


class AutoEgde:
    def __init__(self, url, username,pwd):
        self.edge_options = Options()
        self.edge_options.add_argument("--headless")
        self.edge_options.add_argument("--disable-gpu")
        self.edge_options.add_argument("--window-size=1920,1080")

        self.service = Service(executable_path="edgedriver_win64/msedgedriver.exe")
        self.driver = webdriver.Edge(service=self.service, options=self.edge_options)
        self.driver.get(url)
        print("成功打开网页")

        try:
            self.userNameInput(username)
            self.pwd_tipInput(pwd)
            self.loginClick()
            print("自动登录完成")
            self.driver.close()
        except selenium.common.exceptions.NoSuchElementException:
            print("ERRO 控件不存在")
        except Exception:
            print("ERRO 未知错误")

    def userNameInput(self,username):
        username_input = self.driver.find_element(By.ID, "username")
        print("已找到username输入控件")
        username_input.send_keys(username)
        print("成功输入username")

    def pwd_tipInput(self,pwd):
        pwd_tip = self.driver.find_element(By.ID, "pwd_tip")
        print("已找到pwd_tip控件")
        actions = ActionChains(self.driver)
        actions.click(pwd_tip).perform()
        actions.send_keys(pwd).perform()
        print("成功输入pwd控件")


    def loginClick(self):
        loginlink = self.driver.find_element(By.ID,"loginLink")
        loginlink.click()


def fileRead(file_name):
    with open(file_name,"r", encoding="utf-8") as f:
        number = f.readline().split()
        password = f.readline().split()
    return number, password


wifi = Wifi(ssid="DPU_LianTong")
try:
    number, password = fileRead("loginSet.txt")
except IndexError:
    print("未修改文件")
except Exception:
    print("未知错误")

print(number,password,type(number),type(password))

edge = AutoEgde("http://210.30.48.32/", number, password)

