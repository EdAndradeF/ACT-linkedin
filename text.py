from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.by import By
import dotenv
import os



env = dotenv.load_dotenv('.env')


class Chrome:


    def __init__(self, url):

        self.log = os.getenv('email')
        self.senha = os.getenv('senha')
        print('\n\nOIE!!\n Bora rodar..')
        self.ser = Service('chromedriver.exe')
        self.option = webdriver.ChromeOptions()
        # self.option.add_argument('--headless')
        self.driver = webdriver.Chrome(service=self.ser,
                                       options=self.option)
        self.driver.get(url)


    def login(self):
        self.driver.find_element(By.ID,
                                 'session_key').send_keys(self.log)
        self.driver.find_element(By.ID,
                                 'session_password').send_keys(self.senha)
        self.driver.find_element(By.XPATH,
                                 '//*[@id="main-content"]/section[1]/div/div/form/button').click()



    def conect(self, num):
        self.pg = 1+num
        inicio.driver.get(f'https://www.linkedin.com/search/results/people/?connectionOf=%5B%22ACoAACE0LVQBQqhtxtpGIVdhw-RFHGoCLQ6Z230%22%5D&network=%5B%22F%22%2C%22S%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&sid=Frz&page={self.pg}')
        sleep(1.5)
        self.pg_butao = self.driver.find_elements(By.TAG_NAME, "button")

        for conex in self.pg_butao:
            if conex.text == 'Conectar':
                conex.click()
                sleep(1)
                for x in self.driver.find_elements(By.TAG_NAME, 'button'):
                    if x.text == 'Enviar':
                        x.click()
                        sleep(1.5)
                        fim = [x for x in self.driver.find_elements(By.TAG_NAME, 'button') if x.text == 'Entendi']
                        if len(fim):
                            print('Limite aucancado')
                            return

        if self.pg < 100:
            self.conect(self.pg)


    def bye(self):
        self.driver.close()
        print('tchau, tchau')




if __name__ == '__main__':

    link = 'https://www.linkedin.com/'

    inicio = Chrome(link)
    inicio.login()

    inicio.conect(0)

    inicio.bye()



