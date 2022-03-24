from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.by import By
import dotenv
import os
import pandas as pd



env = dotenv.load_dotenv('.env')


class Chrome:

    def __init__(self):

        self.site = 'https://www.linkedin.com/'
        self.log = os.getenv('email')
        self.senha = os.getenv('senha')
        print('\n\nOIE!!\n Bora rodar..')
        self.ser = Service('chromedriver.exe')
        self.option = webdriver.ChromeOptions()
        # self.option.add_argument('--headless')
        self.driver = webdriver.Chrome(service=self.ser,
                                       options=self.option)
        self.driver.set_window_size(1200, 900)
        self.driver.get(self.site)
        self.login()
        self.d = []

    def login(self):
        self.driver.find_element(By.ID,
                                 'session_key').send_keys(self.log)
        self.driver.find_element(By.ID,
                                 'session_password').send_keys(self.senha)
        self.driver.find_element(By.XPATH,
                                 '//*[@id="main-content"]/section[1]/div/div/form/button').click()

    def bye(self):
        self.driver.close()
        print('tchau, tchau')

    def conect(self, num):
        self.pg = 1+num
        inicio.driver.get(f'{self.site}search/results/people/?connectionOf=%5B%22ACoAACE0LVQBQqhtxtpGIVdhw-RFHGoCLQ6Z230%22%5D&network=%5B%22F%22%2C%22S%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&sid=Frz&page={self.pg}')
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

    def vagas(self, busca, simples=True, r=2, inicio=0):

        simplificado = f'f_AL={simples}'
        local = f'f_WT={r}'
        palavras = f'keywords={busca.replace(" ", "%20")}'
        sort = f'sortBy=R'
        page = f'start={inicio}'
        self.pesquisa = f'{self.site}jobs/search/?{simplificado}&{local}&{palavras}&{sort}&{page}'
        self.driver.get(self.pesquisa)
        sleep(2)
        elementos = self.driver.find_elements(By.TAG_NAME, 'li')
        lista_ids = []
        for ele in elementos:
            if not ele.get_attribute('data-occludable-job-id'):
                elementos.remove(ele)
            else:
                id = ele.get_attribute('data-occludable-job-id')
                lista_ids.append(id)
                ele.click()
                self.candidatura()
                self.vaga_desc(id)
                if len(lista_ids) == 24:
                    break
        datad = pd.DataFrame(self.d)
        return


    def vaga_desc(self, id, job_page=False):
        title = 'h2'
        if job_page:
            title = 'h1'
        sleep(2)
        data = {}

        top = self.driver.find_element(By.CLASS_NAME, 'jobs-unified-top-card')
        article = self.driver.find_element(By.CLASS_NAME, 'jobs-description__content')

        local, cands, *x = top.find_elements(By.CLASS_NAME, 'jobs-unified-top-card__bullet')

        data[id] = {'titulo': top.find_element(By.TAG_NAME, title).text,
                    'empresa': top.find_element(By.CLASS_NAME, 'jobs-unified-top-card__company-name').text,
                    'local': local.text, 'candidatos': cands.text,
                    'local_trabalho': top.find_element(By.CLASS_NAME, 'jobs-unified-top-card__workplace-type').text,
                    'data_publicacao': top.find_element(By.CLASS_NAME, 'jobs-unified-top-card__posted-date').text,
                    'descricao': article.find_elements(By.TAG_NAME, 'span')[-1].text
                    }
        recrutador = article.find_elements(By.CLASS_NAME, 'jobs-poster__name')
        if len(recrutador):
            data[id]['recrutador'] = recrutador[0].text

        tags = top.find_elements(By.CLASS_NAME, 'jobs-unified-top-card__job-insight')
        for elem in tags:
            test = elem.text



        s = 67890


    def percode(self, id):
        vaga = f'{self.site}jobs/view/{id}/'
        self.driver.get(vaga)
        self.vaga_desc(id, job_page=True)

    def minhasvagas(self):
        self.driver.get(f'{self.site}my-items/saved-jobs/')
        lista_vagas = self.driver.find_element(By.CLASS_NAME, 'reusable-search__entity-result-list')
        vagas_id = [link.get_attribute('href').split('/')[5] for link in lista_vagas.find_elements(By.TAG_NAME, 'a')][::2]
        for id in vagas_id:
            self.percode(id)


        vaga=789



    def candidatura(self):
        self.driver.find_element(By.CLASS_NAME, 'jobs-apply-button--top-card').click()
        r = self.driver.find_element(By.TAG_NAME, 'footer').find_element(By.TAG_NAME, 'button').click()
        s =21




if __name__ == '__main__':

    link = 'https://www.linkedin.com/'

    inicio = Chrome()

    # inicio.conect(0)
    # inicio.vagas('analista de dados')
    inicio.minhasvagas()
    # inicio.percode(2961122950)
    inicio.bye()








'7'