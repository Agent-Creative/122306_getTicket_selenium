#春运电脑抢票软件
#注：本程序可用于购买高铁二等座和硬卧，支持学生票，后续功能有待进一步开发
#注：已激活
import requests
import time
import datetime
import selenium
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

#读入车站信息
f=open("station_numl.csv","rb")
data=[]
for line in f:
    line=line.decode().replace("\n","")
    data.append(line.split(","))

def get_StationNum(str):
    for i in range(len(data)):
        if data[i][0]==str:
            return data[i][1]
        elif i==len(data)-1:
            print("请确认车站名称")

what_to_do="book"   #book or Enquire
where_to_start= "北京"#中文输入
where_to_go=    "南昌"
seatprefer='A'  #座位选择
start_num=get_StationNum(where_to_start)
go_num=get_StationNum(where_to_go)
isGtrain=1 #高铁为1，普通查询为0
if what_to_do=="Enquire":
    print("Processing,please wait")
else:   #购票  
    way_to_book=1 #时间查询为1，车次查询为0 
    train_no="Z304"
    time_to_go=10   #最早时间
    time_to_go_1=14 #最晚时间


month_current=datetime.datetime.now().month
op=1    #"希望扫码（稳定推荐）登陆还是密码登陆（不太稳）？扫码请按1，密码请按0"
if op==0:
    user="123456"     #需修改
    password="123456"   #需修改

#打开网页
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
#option.add_argument(r'--user--data--dir=C:\Users\nuoya\AppData\Local\Google\Chrome\User Data')#这一行可以关掉，但不建议
driver = webdriver.Chrome(options=option)
driver.get(r"https://www.12306.cn/index/index.html")
driver.maximize_window()

#查询票务信息
def ENQUIRE(cnt):
    driver.find_element_by_id("fromStationText").click()
    time.sleep(0.05)
    driver.find_element_by_id("fromStationText").send_keys(where_to_start)
    driver.find_element_by_xpath("//div[contains(@cturn,"+start_num+")]").click()
    driver.find_element_by_id("toStationText").click()
    time.sleep(0.05)
    driver.find_element_by_id("toStationText").send_keys(where_to_go)
    driver.find_element_by_xpath("//div[contains(@cturn,"+go_num+")]").click()
    js = "document.getElementById('train_date').removeAttribute('readonly')"#输入日期
    driver.execute_script(js)
    driver.find_element_by_id('train_date').clear()
    driver.find_element_by_id('train_date').send_keys("2020-12-20")#需修改
    driver.find_element_by_id('train_date').send_keys(Keys.ENTER)
    driver.find_element_by_id('train_date').click()
    ActionChains(driver).move_by_offset(210,470).click().perform()
    if cnt==1:
        driver.find_element_by_id('isHighDan').click()
    driver.find_element_by_id('search_one').click()#点击查询按钮

def get_by_trainNum():
    ENQUIRE(isGtrain)
    n = driver.window_handles  # 这个时候会生成一个新窗口或新标签页的句柄，代表这个窗口的模拟driver
    driver.switch_to_window(n[-1])  # driver切换至最新生产的页面
    time.sleep(0.1)
    list=['1','3','5','7','9','11','13','15','17','19','21','23','25','27','29','31','33','35','37','39','41','43','45','47','49','51','53','55','57','59','61','63','65','67','69','71','73','75','77','79','81','83','85','87','89','91','93','95','97','99','101','103','105','107','109','111','113','115','117','119','121','123','125','127','129','131','133','135','137','139','141','143','145','147','149','151','153','155','157','159','161','163','165','167','169','171','173','175','177','179','181','183','185','187','189','191','193','195','197','199','201','203','205','207','209','211','213','215','217','219','221','223','225','227','229','231','233','235','237','239','241','243','245','247','249','251','253','255','257','259','261','263','265','267','269','271','273','275','277','279','281','283','285','287','289','291','293','295','297','299','301','303','305','307','309','311','313','315','317','319','321','323','325','327','329','331','333','335','337','339','341','343','345','347','349','351','353','355','357','359','361','363','365','367','369','371','373','375','377','379','381','383','385','387','389','391','393','395','397','399']
    for i in range (200):
        str=driver.find_element_by_xpath("/html/body/div[8]/div[7]/table/tbody[1]/tr["+list[i]+"]/td[1]/div/div[1]/div/a").text
        if str==train_no:
            try:
                driver.find_element_by_xpath("/html/body/div[8]/div[7]/table/tbody[1]/tr["+list[i]+"]/td[13]/a").click()
                if op==0:
                    BOOKING_1()
                else:
                    BOOKING_2()
                    break
            except(NoSuchElementException):
                print("购票失败，本车次无座")

def GOTO(kind_train):#最后界面,形参1表示高铁，支持选座
    n = driver.window_handles  # 这个时候会生成一个新窗口或新标签页的句柄，代表这个窗口的模拟driver
    driver.switch_to_window(n[-1])  # driver切换至最新生产的页面
    driver.find_element_by_xpath("/html/body/div[10]/div[3]/div[2]/div[1]/div[2]/ul/li/label").click()
    WebDriverWait(driver,10,0.2).until(expected_conditions.invisibility_of_element(driver.find_element_by_id("dialog_xsertcj_ok")),'失败')
    ele=driver.find_element_by_id("submitOrder_id")
    driver.execute_script('arguments[0].click()',ele)
    n = driver.window_handles 
    driver.switch_to_window(n[-1])  
    time.sleep(1)
    if kind_train==1:
        if   seatprefer=='A':
            driver.find_element_by_xpath("/html/body/div[24]/div/div[5]/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[2]/ul[1]/li[1]/a").click()
        elif seatprefer=='B':
            driver.find_element_by_xpath("/html/body/div[24]/div/div[5]/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[2]/ul[1]/li[2]/a").click()
        elif seatprefer=='C':
            driver.find_element_by_xpath("/html/body/div[24]/div/div[5]/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[2]/ul[1]/li[3]/a").click()
        elif seatprefer=='D':
            driver.find_element_by_xpath("/html/body/div[24]/div/div[5]/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[2]/ul[2]/li[1]/a").click()
        elif seatprefer=='E':
            driver.find_element_by_xpath("/html/body/div[24]/div/div[5]/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[2]/ul[2]/li[2]/a").click()
    time.sleep(10)
    #driver.find_element_by_id("qr_submit_id").click()
    print("Yes!")

def BOOKING_1():#账号登录，不稳定，不推荐
    driver.find_element_by_link_text("账号登录").click()
    time.sleep(0.1)
    driver.find_element_by_id("J-userName").send_keys(user)
    time.sleep(0.1)
    driver.find_element_by_id("J-password").send_keys(password)
    time.sleep(4)
    GOTO(isGtrain)#进入新页面之后
    

def BOOKING_2():#扫码登录，推荐
    #用户扫码
    WebDriverWait(driver,15,0.5).until(expected_conditions.url_to_be('https://kyfw.12306.cn/otn/confirmPassenger/initDc'),'失败')
    GOTO(isGtrain)

def get_by_trainTime():
    ENQUIRE(isGtrain)
    n = driver.window_handles  # 这个时候会生成一个新窗口或新标签页的句柄，代表这个窗口的模拟driver
    driver.switch_to_window(n[-1])  # driver切换至最新生产的页面
    time.sleep(0.5)
    list=['1','3','5','7','9','11','13','15','17','19','21','23','25','27','29','31','33','35','37','39','41','43','45','47','49','51','53','55','57','59','61','63','65','67','69','71','73','75','77','79','81','83','85','87','89','91','93','95','97','99','101','103','105','107','109','111','113','115','117','119','121','123','125','127','129','131','133','135','137','139','141','143','145','147','149','151','153','155','157','159','161','163','165','167','169','171','173','175','177','179','181','183','185','187','189','191','193','195','197','199','201','203','205','207','209','211','213','215','217','219','221','223','225','227','229','231','233','235','237','239','241','243','245','247','249','251','253','255','257','259','261','263','265','267','269','271','273','275','277','279','281','283','285','287','289','291','293','295','297','299','301','303','305','307','309','311','313','315','317','319','321','323','325','327','329','331','333','335','337','339','341','343','345','347','349','351','353','355','357','359','361','363','365','367','369','371','373','375','377','379','381','383','385','387','389','391','393','395','397','399']
    for i in range (200):
       str=driver.find_element_by_xpath("/html/body/div[8]/div[7]/table/tbody[1]/tr["+list[i]+"]/td[1]/div/div[3]/strong[1]").text
       time_1,time_2=map(int, str.split(":"))
       if time_1>=time_to_go and time_1<time_to_go_1:
            try:
                driver.find_element_by_xpath("/html/body/div[8]/div[7]/table/tbody[1]/tr["+list[i+7]+"]/td[13]").click()
                if op==0:
                    BOOKING_1()
                else:
                    BOOKING_2()
                    break
            except(NoSuchElementException):
                continue
       elif time_1>=time_to_go_1:
           print("购票失败，时间段为空")

if what_to_do=="Enquire":
    ENQUIRE(option_enquire)
    print("The work is done.Congratulations")
else:
    if way_to_book==1:
        get_by_trainTime()
    else:
        get_by_trainNum()






