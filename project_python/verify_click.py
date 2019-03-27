from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains
import time
from io import BytesIO
from PIL import Image
from chaojiying import Chaojiying_Client


# 生成类
class VerificationClick(object):
    # 初始化
    def __init__(self, user, pw, soft_id):
        self.user = user
        self.pw = pw
        self.id = soft_id
        self.url = 'http://dun.163.com/trial/picture-click'
        chrome = self.webdrive_open()
        self.driver = webdriver.Chrome(chrome_options=chrome,
                                       executable_path='chromedriver.exe')
        self.wait = WebDriverWait(self.driver, 10)

    # 设置浏览器格式
    def webdrive_open(self):
        option = Options()
        option.add_argument('--window-size=1366,768')
        option.add_argument('--disable-infobars')
        return option

    # 访问url
    def log_in_url(self):
        self.driver.get(self.url)

    # 页面操作
    def get_action(self):
        self.log_in_url()
        button = self.wait.until(expected_conditions.presence_of_element_located((
            By.XPATH, '//*[@class="tcapt_item is-left"]//*[@class="yidun_tips"]'
        )))
        # print(button)
        actions = ActionChains(driver=self.driver)
        # 模拟页面翻页
        ActionChains(self.driver).move_to_element(button)
        # self.driver.excute_script("window.scrollTo(0, document.body.scrollHeight)")
        actions.click(button)
        actions.perform()

    # 获取图片
    def get_img(self):
        self.get_action()
        location = self.wait.until(expected_conditions.visibility_of_element_located((
            By.XPATH, '//*[@class="tcapt_item is-left"]//*[@class="yidun_bg-img"]'
        ))).location
        img = BytesIO(self.driver.get_screenshot_as_png())
        im = Image.open(img)
        print(location)

        old_img = im.crop((location['x'] + 126, location['y']-12, location['x'] + 500, location['y'] + 250))
        # old_img.show()
        new_img = old_img.resize((324, 260))
        # new_img.show()
        pic_save = BytesIO()
        new_img.save(pic_save, format('png'))
        img_post = pic_save.getvalue()
        return img_post

    # 连接超级鹰接口获取点击位置
    def pic_post(self, img_post):
        cjy = Chaojiying_Client(self.user, self.pw, self.id)
        x = cjy.PostPic(img_post, 9103).get('pic_str')
        print(x)
        position = [i.split(',') for i in (x.split('|'))]
        print(position)
        return position

    # 图片点击
    def click_pic(self, position):
        loc = self.wait.until(expected_conditions.visibility_of_element_located((
            By.XPATH, '//*[@class="tcapt_item is-left"]//*[@class="yidun_bg-img"]'
        )))
        new_position = []
        for x, y in position:
            pos = (int(x) + 2, int(y) - 25)
            new_position.append(pos)
        ActionChains(self.driver).move_to_element_with_offset(loc, new_position[0][0], new_position[0][1]).click().perform()
        time.sleep(1)
        first_position = new_position[0]
        for second_position in new_position[1:]:
            for x, y in self.trajectory(first_position, second_position):
                ActionChains(self.driver).move_to_element_with_offset(loc, x, y).perform()

            ActionChains(self.driver).click().perform()
            time.sleep(1)
            first_position = second_position

    # 点击轨迹
    def trajectory(self, first_position, second_position):
        position_list = []
        x = (int(second_position[0]) - int(first_position[0])) / 20
        y = (int(second_position[1]) - int(first_position[1])) / 20
        for i in range(20):
            position = (int(first_position[0] + round(x * i)), int(first_position[1] + round(y * i)))
            position_list.append(position)
        return position_list

    def run(self):
        self.click_pic(self.pic_post(self.get_img()))
        # self.get_img()
        time.sleep(10)
        # self.driver.quit()


if __name__ == '__main__':
    a = VerificationClick('m125705171', 'm1257051717', '898279')
    a.run()