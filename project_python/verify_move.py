from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains
import time
import re
from PIL import Image
from io import BytesIO
import requests


class MoveVerification(object):
    # 初始化
    def __init__(self):
        self.url = 'https://www.huxiu.com'
        browers = self.start_webdriver()
        self.driver = webdriver.Chrome(chrome_options=browers,
                                       executable_path='chromedriver.exe')
        self.wait = WebDriverWait(self.driver, 10)

    # 设置浏览器
    def start_webdriver(self):
        option = Options()
        option.add_argument('--window-size=1500,900')
        option.add_argument('--disable-infobars')
        # option.add_argument('--headless')
        # browser = webdriver.Chrome(chrome_options=option, executable_path='chromedriver.exe')
        # browser.get('http://www.baidu.com')
        return option

    # 访问url
    def driver_url(self):
        self.driver.get(self.url)
        login_button = self.driver.find_element_by_xpath('//a[@class="js-login"]')
        login_button.click()

    # 获取验证码图片（乱序）
    def get_img(self):
        less_img_list = self.wait.until(expected_conditions.presence_of_all_elements_located((
            By.XPATH, '//div[@class="user-login-box"]//div[@class="gt_cut_bg gt_show"]/div'
        )))
        all_img_list = self.wait.until(expected_conditions.presence_of_all_elements_located((
            By.XPATH, '//div[@class="user-login-box"]//div[@class="gt_cut_fullbg gt_show"]/div'
        )))
        # get_less_img = re.findall(r'url\("(.*?)"\);', less_img_list[0].get_attribute('style'))
        # get_all_img = re.findall(r'url\("(.*?)"\);', all_img_list[0].get_attribute('style'))
        # print(get_all_img[0])
        # print(get_less_img[0])
        less_img = self.get_full_img(less_img_list)
        full_img = self.get_full_img(all_img_list)
        distence = self.get_distance(less_img, full_img)
        self.mouse_move(distence)

    # 生成完整验证码图片
    def get_full_img(self, img_list):
        img_url = re.findall(r'url\("(.*?)"\);', img_list[0].get_attribute('style'))[0]
        style_list = [i.get_attribute('style') for i in img_list]
        position_list = [re.findall(r'position: -(.*?)px -?.*?px;', i)[0] for i in style_list]
        img_file = BytesIO(requests.get(img_url).content)
        old_image = Image.open(img_file)
        # old_image.show()

        new_image = Image.new('RGB', (260, 116))
        up_count = 0
        down_count = 0
        for i in position_list[:26]:
            crop_image = old_image.crop((int(i), 58, int(i)+10, 116))
            up_count += 10
            new_image.paste(crop_image, (up_count, 0))
        for j in position_list[26:]:
            crop_image = old_image.crop((int(j), 0, int(j)+10, 58))
            down_count += 10
            new_image.paste(crop_image, (down_count, 58))
        return new_image

    # 获取移动距离
    def get_distance(self, less, full):
        def diffierent(a, b):
            for i in range(3):
                if abs(a[i] - b[i]) > 50:
                    return False

        for i in range(260):
            for j in range(116):
                if diffierent(less.getpixel((i, j)), full.getpixel((i, j))) is False:
                    return i

    # 控制鼠标移动滑块
    def mouse_move(self, distence):
        print(distence)
        distence = distence - 20
        button = self.driver.find_element_by_xpath('//button[@class="js-btn-sms-login btn-login"]')
        block = self.driver.find_element_by_xpath('//div[@class="gt_slider_knob gt_show"]')
        actions = ActionChains(driver=self.driver)
        actions.click_and_hold(block)
        time.sleep(1)
        for i in self.move_by(distence):
            actions.move_by_offset(i, 0)
        time.sleep(1)
        actions.release()
        actions.perform()

    # 移动轨迹
    def move_by(self, distence):
        v = 0
        t = 0.1
        mid = distence * 3 / 5
        move_position_li = []
        move_position = 0
        while move_position < distence:
            if move_position < mid:
                a = 8
            else:
                a = -8
            move_po = v * t + 0.5 * a * t * t
            move_position_li.append(round(move_po))
            move_position += move_po
            v += t * a
        dis_ture = sum(move_position_li)

        if dis_ture > move_position:
            move_position_li.extend(int(dis_ture - move_position) * [-1])
        elif dis_ture < move_position:
            move_position_li.extend(int(move_position - dis_ture) * [1])

        move_position_li.extend(10 * [1, 0] + 10 * [0] + 10 * [-1, 0])

        print(move_position_li)
        return move_position_li

    # 运行程序
    def run(self):
        try:
            self.driver_url()
            self.get_img()
        finally:
            time.sleep(5)
            self.driver.quit()


if __name__ == '__main__':
    a = MoveVerification()
    a.run()
