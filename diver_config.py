from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class ChromeDriver:

    def __init__(self):

        print('\n\nOIE!!\n Bora rodar..')
        self.ser = Service('chromedriver.exe')
        self.option = webdriver.ChromeOptions()
        # self.option.add_argument('--headless')
        self.driver = webdriver.Chrome(service=self.ser,
                                       options=self.option)
        self.driver.set_window_size(1200, 900)