import os
import random
import time
import base64
# import requests
import cv2
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import numpy as np
from PIL import Image as Im

os.chdir('.')
def pic_download(url,type):
    url = url
    root = "../img_db/"
    # path = root + str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))+'.png'
    path = root + type + '.png'
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if os.path.exists(path):
            os.remove(path)
        #如果图片是url的格式
        # r = requests.get(url)
        # r.raise_for_status()
        #如果图片是base64编码的
        data=url.split(',')[1]
        img=base64.b64decode(data)
        # 使用with语句可以不用自己手动关闭已经打开的文件流
        with open(path, "wb") as f:  # 开始写文件，wb代表写二进制文件
            f.write(img)
            print(f.name)
        print("下载完成")
        return f.name
    except Exception as e:
        print("获取失败!" + str(e))

def get_distance(small_url, big_url):
    # 引用上面的图片下载
    otemp = pic_download(small_url, 'small')

    time.sleep(2)

    # 引用上面的图片下载
    oblk = pic_download(big_url, 'big')

    # # 计算拼图还原距离
    target = cv2.imread(otemp, 0)
    template = cv2.imread(oblk, 0)
    w, h = target.shape[::-1]
    temp = 'temp.jpg'
    targ = 'targ.jpg'
    cv2.imwrite(temp, template)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    target = abs(255 - target)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    template = cv2.imread(temp)
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)
    # 缺口位置
    print((y, x, y + w, x + h))

    # 调用PIL Image 做测试
    image = Im.open(oblk)

    xy = (y + 20, x + 20, y + w - 20, x + h - 20)
    # 切割
    imagecrop = image.crop(xy)
    # 保存切割的缺口
    saveFileName = "../img_db/" + str(time.time()) + "_new_image.png"
    imagecrop.save(saveFileName)
    return y

def darbra_track(distance):

    print("Start cal track")
    moveTracks = []
    i = 0.0
    while (i <= distance+5):
        x = random.randint(5, 8)
        
        if random.randint(0, 1)==1:
            y = random.randint(0, 2)
        else:
            y = 0 - random.randint(0, 2)
       
        s = 0
        if(i/distance > 0.05):
            if(i/distance<0.85):
                s = random.randint(2, 5)
            else :
                s = random.randint(10, 15)
            
        else :
            s = random.randint(20, 30)
        
        moveTracks.append([x, y, s])
        i = i + x
    
    ## append last position
    cc = i > distance
    j = 0
    while(j < abs(distance-i)):
        x = random.randint(1, 3)
        s = random.randint(100, 200)
        if (cc) :
            moveTracks.append([-x, 0, s])
        else :
            moveTracks.append([x, 0, s])

        j = j+x

    return moveTracks
    
def move_mouse2(browser,element, tracks):
    # 按下鼠标左键
    ActionChains(browser).click_and_hold(element).perform()

    for track in tracks:
        print("move track - ", track)
        ActionChains(browser).move_by_offset(track[0], track[1]).perform()
        time.sleep(track[2]/1000.0)

    ActionChains(browser).release(on_element=element).perform()

def move_mouse(browser,distance,element):
    has_gone_dist=0
    remaining_dist = distance
    # distance += randint(-10, 10)
    # 按下鼠标左键
    ActionChains(browser).click_and_hold(element).perform()
    time.sleep(0.5)
    while remaining_dist > 0:
        ratio = remaining_dist / distance
        if ratio < 0.2:
            # 开始阶段移动较慢
            span = random.randint(4, 5)
        elif ratio < 0.4:
            # 结束阶段移动较慢
            span = random.randint(20, 30)
        elif ratio > 0.8:
            # 结束阶段移动较慢
            span = random.randint(8, 10)
        else:
            # 中间部分移动快
            span = random.randint(30, 40)
        ActionChains(browser).move_by_offset(span, random.randint(-5, 5)).perform()
        remaining_dist -= span
        has_gone_dist += span
        time.sleep(random.randint(5, 20) / 100)

    ActionChains(browser).move_by_offset(remaining_dist, random.randint(-5, 5)).perform()
    ActionChains(browser).release(on_element=element).perform()


if __name__=='__main__':
    #打开浏览器
    browser = webdriver.Chrome(executable_path='./drivers/chromedriver_mac')
    #网址
    url='http://jd.com'
    #打开京东网站
    browser.get(url)
    wait = WebDriverWait(browser,10)
    #步骤一点击登录
    button = wait.until((EC.presence_of_element_located((By.XPATH, '//*[@id="ttbar-login"]/A[1]'))))
    button.click()
    # #步骤二，点击输入账号登陆
    # button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/DIV[2]/DIV[1]/DIV/DIV[3]/A')))
    # button.click()
    # 步骤三，点击账户登录
    acount_bt = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/DIV[2]/DIV[1]/DIV/DIV[3]/A')))
    acount_bt.click()
    #步骤四
    input_username=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="loginname"]')))
    input_username.send_keys('username')
    time.sleep(2)
    input_password = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="nloginpwd"]')))
    input_password.send_keys('password')
    # 步骤4，点击登陆
    button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginsubmit"]')))
    button.click()
    #判断是否有滑动页面
    try:
        code=browser.find_element_by_xpath('//*[@id="JDJRV-wrap-loginsubmit"]/DIV/DIV/DIV/DIV[1]/DIV[2]/DIV[1]/IMG')        
        url1=browser.current_url
        while True:
            image1=wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="JDJRV-wrap-loginsubmit"]/DIV/DIV/DIV/DIV[1]/DIV[2]/DIV[1]/IMG')))
            image1url=image1.get_attribute('src')
            # //*[@id="JDJRV-wrap-loginsubmit"]/DIV/DIV/DIV/DIV[1]/DIV[2]/DIV[1]/IMG
            # print("slider-image-url:", image1url)
            image2=wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="JDJRV-wrap-loginsubmit"]/DIV/DIV/DIV/DIV[1]/DIV[2]/DIV[2]/IMG')))
            image2url=image2.get_attribute('src')
            # print("big-picture-url", image2url)
            distance =get_distance(image2url, image1url)
            print("distance:", distance)
            #网页上的尺寸差
            distance = distance * (279/ 360)
            print("revisedd distance:", distance)
            element=wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="JDJRV-wrap-loginsubmit"]/DIV/DIV/DIV/DIV[2]/DIV[3]')))
            move_mouse(browser,distance,element)
            # tracks = darbra_track(distance)
            #print("tracks:", tracks)
            # move_mouse2(browser, element, tracks)

            url2=browser.current_url
            if url2==url1:
                print('验证失败，将再次验证')
                time.sleep(1)
            else:
                break
    except Exception as e:
        print(e)



