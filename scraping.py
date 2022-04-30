from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.by import By
import dotenv
import os
import pandas as pd

from diver_config import ChromeDriver

env = dotenv.load_dotenv('.env')


class Bot:

    def __init__(self, window=True):
        self.site = 'https://www.linkedin.com/'
        self.driver = ChromeDriver(window=window).driver
        self.driver.get(self.site)
        self.login()
        self.data = {}

    def login(self):
        self.driver.find_element(By.ID,
                                 'session_key').send_keys(os.getenv('email'))
        self.driver.find_element(By.ID,
                                 'session_password').send_keys(os.getenv('senha'))
        self.driver.find_element(By.XPATH,
                                 '//*[@id="main-content"]/section[1]/div/div/form/button').click()

    def bye(self):
        self.driver.close()
        print('tchau, tchau')

    def conect(self, num=0):
        self.pg = 1+num
        self.driver.get(f'{self.site}search/results/people/?connectionOf=%5B%22ACoAACE0LVQBQqhtxtpGIVdhw-RFHGoCLQ6Z230%22%5D&network=%5B%22F%22%2C%22S%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&sid=Frz&page={self.pg}')
        sleep(1.5)
        self.pg_butao = self.driver.find_elements(By.TAG_NAME, "button")

        for conex in self.pg_butao:
            if conex.text == 'Conectar':
                conex.click()
                sleep(1)
                confirm = self.driver.find_elements(By.TAG_NAME, 'button')
                for x in confirm:
                    if x.text == 'Enviar':
                        x.click()
                        sleep(1.5)
                        break
                    if x.text == 'Entendi':
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
                # self.candidatura()
                self.vaga_descricao(id)
                if len(lista_ids) == 24:
                    break
        datad = pd.DataFrame(self.d)
        return

    def vaga_descricao(self, id, job_page=False):
        title = 'h2'
        if job_page:
            title = 'h1'
        sleep(2)
        self.data[id] = {}
        top = self.driver.find_element(By.CLASS_NAME, 'jobs-unified-top-card')
        article = self.driver.find_element(By.CLASS_NAME, 'jobs-description__content')

        local, *cands = top.find_elements(By.CLASS_NAME, 'jobs-unified-top-card__bullet')
        if cands:
            self.data[id]['candidatos'] = cands[0].text

        dia = top.find_elements(By.CLASS_NAME, 'jobs-unified-top-card__posted-date')
        if dia:
            self.data[id]['data_publicacao'] = dia[0].text

        butao_atividade = top.find_elements(By.CLASS_NAME, 'post-apply-timeline__button-container')
        if butao_atividade:
            butao_atividade[0].click()

        atividade = top.find_element(By.CLASS_NAME, 'post-apply-timeline').find_element(By.TAG_NAME, 'ul')
        atividade = atividade.text.split('\n')
        self.data[id]['atividade'] = [(atividade[ind], atividade[ind+1]) for ind in range(0, len(atividade), 2)]

        article.parent.find_element(By.CLASS_NAME, 'artdeco-card__actions').click()
        self.data[id] = {
            'titulo': top.find_element(By.TAG_NAME, title).text,
            'empresa': top.find_element(By.CLASS_NAME, 'jobs-unified-top-card__company-name').text,
            'local': local.text,
            'local_trabalho': top.find_element(By.CLASS_NAME, 'jobs-unified-top-card__workplace-type').text,
            'descricao': article.find_element(By.ID, 'job-details').text
                        }
        recrutador = article.find_elements(By.CLASS_NAME, 'jobs-poster__name')
        if len(recrutador):
            self.data[id]['recrutador'] = recrutador[0].text

        tags = top.find_elements(By.CLASS_NAME, 'jobs-unified-top-card__job-insight')
        detalhes = []
        for elem in tags:
            if not elem.get_attribute('class').endswith('highlight'):
                item = elem.text.split('·')
                detalhes.append(item[0])
                if len(item) > 1:
                    detalhes.append(item[1])
                else:
                    detalhes.append(None)
        self.data[id]['detalhes'] = detalhes

    def percode(self, id):
        vaga = f'{self.site}jobs/view/{id}/'
        self.driver.get(vaga)
        self.vaga_descricao(id, job_page=True)

    def minhasvagas(self, start=0):
        self.driver.get(f'{self.site}my-items/saved-jobs/?cardType=APPLIED&start={start}')
        lista_vagas = {self.driver.find_elements(By.CLASS_NAME, 'app-aware-link')}
        vagas_id = {link.get_attribute('href').split('/')[5] for link in lista_vagas}
        for id in vagas_id:
            self.percode(id)
        if not len(vagas_id) < 10:
            self.minhasvagas(start=start+10)



    def candidatura(self):
        self.driver.find_element(By.CLASS_NAME, 'jobs-apply-button--top-card').click()
        r = self.driver.find_element(By.TAG_NAME, 'footer').find_element(By.TAG_NAME, 'button').click()
        s =21



if __name__ == '__main__':
    inicio = Bot()
    # inicio.conect(7)
    # inicio.vagas('analista de dados')
    # inicio.minhasvagas()
    inicio.percode(3040865550)
    inicio.bye()








'7'