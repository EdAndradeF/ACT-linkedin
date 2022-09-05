from curses import meta
from importlib.metadata import metadata
from time import sleep
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import dotenv
import os
import pandas as pd
import json
from drive import Chrome
from datetime import date
from selenium.common.exceptions import NoSuchElementException

env = dotenv.load_dotenv('.env')


def trat(func, args):
    try:
        r = func(*args)
        return r
    except:
        print('deu erro')
        class Caô:
            text = None
            def get_attribute(self, lorota):
                return None
        return Caô()

def is_in(elemento, item) -> list: #not in uso 
    '''reduce function
        compara o item com elemento para defenir se item esta em elemento
        caso se item nao fizer parte de elemteno, item se torna o elemento 
    '''
    if not isinstance(elemento, list):
        elemento = [elemento]
   
    if item in elemento[0]:
        elemento.append(item)
    else:
        elemento[0] = item                   
    return elemento

def linha0(tag:WebElement) -> dict:
    
    def getEle(tag:WebElement, colum_attr:dict):
        d = {}
        for key, vlr in colum_attr.items():
             d[key] = trat(tag.find_element, (By.CLASS_NAME, vlr)).text
        return d
        
    dic = {}
    tag1 = tag.find_element(By.CLASS_NAME, 'jobs-unified-top-card__subtitle-primary-grouping')    
    tag2 = tag.find_element(By.CLASS_NAME, 'jobs-unified-top-card__subtitle-secondary-grouping')

    if tag1.text:
        colum_attr1 = {
            'nome_empresa': 'jobs-unified-top-card__company-name',
            'localidade': 'jobs-unified-top-card__bullet',
            'local_trabalho': 'jobs-unified-top-card__workplace-type'
        }
        dic.update(getEle(tag1, colum_attr1))     
    
    if tag2.text:
        colum_attr2 = {
            'data_post': 'jobs-unified-top-card__posted-date',
            'quantidade_inscritos': 'jobs-unified-top-card__bullet'
        }
        dic.update(getEle(tag2, colum_attr2))
        
    dic['perfil_empresa'] = None
    if dic['nome_empresa']:
        dic['perfil_empresa'] = trat(
            tag1.find_element, (By.TAG_NAME, 'a')
            ).get_attribute('href')    
    return dic

def recruter(tag:WebElement):
    if not tag:
        return
    dic = {
        'nome_recrut': tag.find_element(By.TAG_NAME, 'strong').text, 
        'perfil_recrut': tag.find_element(By.TAG_NAME, 'a').get_attribute('href'),
        'titulos_recrut': tag.find_element('class name', 'hirer-card__hirer-job-title').text
    }
    em_comum = tag.text.split('\n')[-1]
    dic['qnt_conex_comum'] = int(em_comum.split()[0]) if 'em comum' in em_comum else None
    return dic



class LinkedIn:

    def __init__(self, window=True):
        self.hoje = date.today().strftime("%d-%m-%y")
        self.site = 'https://www.linkedin.com/'
        self.driver = Chrome(window=window)
        self.driver.get(self.site)
        self.login()
        self.datavaga = {}
        self.lista_idVagas = set()
        self.qnt_vagas = 0

    def __repr__(self) -> str:
        return f'linkedin-dados'

    def login(self):
        '''

        '''
        self.driver.find_element(By.ID,
                                 'session_key').send_keys(os.getenv('email'))
        self.driver.find_element(By.ID,
                                 'session_password').send_keys(os.getenv('senha'))
        self.driver.find_element(By.XPATH,
                                 '//*[@id="main-content"]/section[1]/div/div/form/button').click()

    def vagas(self, busca, simples=True, r=2, inicio=0): 
        #todo refatorar!!!!!!#todo refatorar!!!!!!
        #todo refatorar!!!!!!#todo refatorar!!!!!!
        simplificado = f'f_AL={simples}'
        local = f'f_WT={r}'
        palavras = f'keywords={busca.replace(" ", "%20")}'
        sort = f'sortBy=R'
        page = f'start={inicio}'
        self.pesquisa = f'{self.site}jobs/search/?{simplificado}&{local}&{palavras}&{sort}&{page}'
        self.driver.get(self.pesquisa)
        # sleep(2)
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

    def vaga_descricao(self, id, job_page=True) -> dict:
        ''' 
            idealmente seria salvo o html da pagina para futuramente ser extraido os dados 
            (com BeautifullSoup) - porém o acesso ao site necessita de certa lentidão de navegação,
            então preferi - como uma forme de espera fazer o script olhar "manualmente" e coletar os dados 
            durante o scraper 

            vai estrair e separar os dados em um dicionario
            
            id .> id da vaga (serve como caminho add ao final de  https://www.linkedin.com/jobs/view/{id})
            
            job_page .> especifica se esta na pagina do vaga ou em uma pagina de busca
            
            return .> um dicionario com os dados da pagina

        '''
        title = 'h1' if job_page else 'h2'
        
        # sleep(3)
        self.data = {id: {}}
            # conteiner de detalhes sobre a empresa
        top = self.driver.waitFindElement((By.CLASS_NAME, 'jobs-unified-top-card'), 'element')

        self.data[id]['nome_vaga'] = top.find_element(By.TAG_NAME, title).text
        print(self.data[id]['nome_vaga'])
        emp_loc_dat = top.find_element(By.CLASS_NAME, 'jobs-unified-top-card__primary-description')
        self.data[id].update(linha0(emp_loc_dat))

        sleep(1)
        # detalhes da empresa (tabela)
        listas = top.find_elements(By.TAG_NAME, 'ul')
        lis = []        
        for tags in listas:
            uls = [x.text for x in tags.find_elements(By.TAG_NAME, 'li')]
            lis.append(uls) 
        detalhes, *atividade = lis
        self.data[id]['detalhes'] = detalhes
        if atividade:
            self.data[id]['estagio'] = atividade[0]

        # VAGA FECHADA
        fechada = self.driver.find_element('class name', 'artdeco-inline-feedback__message')
        self.data[id]['vaga_fechada'] = fechada.text if fechada else None


        #recrutador
        recrutador_full = self.driver.waitFindElement((By.CLASS_NAME, 'hirer-card__hirer-information'), 'element')
        self.data[id]['recrutador'] = None
        if isinstance(recrutador_full, WebElement):
            print('tem recrutador')
            self.data[id]['recrutador'] = recruter(recrutador_full)

        # descricao
        article = self.driver.find_element(By.TAG_NAME, 'article')
        article.parent.find_element(By.CLASS_NAME, 'artdeco-card__actions').click()
        self.data[id]['descricao'] = article.text
        self.datavaga.update(self.data)

        '''
                            daqui pra baixo decrepitado 
        

        article = self.driver.find_element(By.CLASS_NAME, 'jobs-description__content')

        local, *cands = top.find_elements(By.CLASS_NAME, 'jobs-unified-top-card__bullet')
        if cands:
            data['candidatos'] = cands[0].text
        elif top.find_elements(By.CLASS_NAME, 'jobs-unified-top-card__applicant-count'):
            data['candidatos'] = top.find_elements(By.CLASS_NAME, 'jobs-unified-top-card__applicant-count')[0].text

        dia = top.find_elements(By.CLASS_NAME, 'jobs-unified-top-card__posted-date')
        if dia:
            data['data_publicacao'] = dia[0].text

        butao_atividade = top.find_elements(By.CLASS_NAME, 'post-apply-timeline__button-container')
        if butao_atividade:
            butao_atividade[0].click()

        atividade = top.find_element(By.CLASS_NAME, 'post-apply-timeline').find_element(By.TAG_NAME, 'ul')
        atividade = atividade.text.split('\n')
        data['atividade'] = [(atividade[ind], atividade[ind+1]) for ind in range(0, len(atividade), 2)]

        article.parent.find_element(By.CLASS_NAME, 'artdeco-card__actions').click()
        data['titulo'] = top.find_element(By.TAG_NAME, title).text
        data['empresa'] = top.find_element(By.CLASS_NAME, 'jobs-unified-top-card__company-name').text
        data['local'] = local.text
        
            
        local_trabalho = top.find_elements(By.CLASS_NAME, 'jobs-unified-top-card__workplace-type')
        if local_trabalho:
            data['local_trabalho'] = local_trabalho[0].text
        recrutador = article.find_elements(By.CLASS_NAME, 'jobs-poster__name')
        if len(recrutador):
            data['recrutador'] = recrutador[0].text

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
        data['detalhes'] = detalhes

        vaga_fechada = top.find_elements(By.CLASS_NAME ,'artdeco-inline-feedback__message')
        if vaga_fechada:
            data['aceita_inscricao'] =  vaga_fechada[0].text

        data['descricao'] = article.find_element(By.ID, 'job-details').text
        self.datavaga.append(data)
'''

    def setQnt(self, qnt:WebElement, text:str) -> None:
        '''
        remove texto especificado e devolve inteiro
        caso o atributo qnt_vagas for 0
            qnt WebElement .> elemento com texto e numero
                  text str .> texto a ser retirado com o metodo .strip()
        '''
        if not self.qnt_vagas:
            self.qnt_vagas = int(qnt.text.strip(text))

    def minhasvagas(self, start:int=0) -> None:
        '''
            lista todas as ids das vagas salvas como canditaturas realizadas

            start int .> pagina numero da pagina inicial de vagas candidatadas 
                        |.> de 10 em 10 

            test bool .>  caso True pega apenas os links da primeira pagina
        '''

        self.driver.get(f'{self.site}my-items/saved-jobs/?cardType=APPLIED&start={start}')
        sleep(2)

        #quantidade de
        qnt = self.driver.find_element(By.CLASS_NAME, 'workflow-navigation__item')
        self.setQnt(qnt,'Minhas vagas\n')

        # conteiner com lista de vagas
        vagas = self.driver.find_element(By.CLASS_NAME, 'workflow-results-container')

        # endereco das vagas
        lista_vagas = vagas.find_elements(By.TAG_NAME, 'a')
                # id_vagas usa set para eliminar as duplicadas  
        id_vagas = {a.get_attribute('href')
                        for a in lista_vagas 
                        if '/jobs/view/' in a.get_attribute('href')}
        self.lista_idVagas.update(id_vagas)

        if start < self.qnt_vagas:
            self.minhasvagas(start=start+10)
            
    def getFullVagas(self, start:int=0):
        ''' 
            lista todas as vagas registradas e itera para acessar 1 a 1 
                chamando o metodo percode
            start int .> pagina numero da pagina inicial de vagas candidatadas 
                        |.> de 10 em 10 
        '''
        self.minhasvagas(start)
        conto = 0 # < len(self.lista_idVagas)
        for url in self.lista_idVagas:
            print(conto, "/", len(self.lista_idVagas))
            conto += 1
            self.percode(url)     

    def percode(self, Vg):
        self.driver.get(Vg)
        idVaga = Vg.split('/')[5] 
        self.vaga_descricao(idVaga, job_page=True)
        self.save_html(
            self.data,
            idVaga,
            self.data[idVaga]['nome_vaga']
        )   
        
    def save_json(self, path:str='data/lake/bronze/json'):
        arq = Path(path) / f'{self.hoje}_linkedin_vagas.json'
        with open(arq, 'w') as j:        
            json.dump(j, self.datavaga)
    
    def save_html(self, id, nome, path:str='data/lake/bronze/html'):
        arq = Path(path) / f"{self.hoje}_{nome} _{id}.html"
        with open(arq, 'w') as html:
            html.write(self.driver.page_source)


    def candidatura(self):
        self.driver.find_element(By.CLASS_NAME, 'jobs-apply-button--top-card').click()
        r = self.driver.find_element(By.TAG_NAME, 'footer').find_element(By.TAG_NAME, 'button').click()
        s = 21

    def conect(self, num=0):
        self.pg = 1+num
        self.driver.get(f'{self.site}search/results/people/?connectionOf=%5B%22ACoAACE0LVQBQqhtxtpGIVdhw-RFHGoCLQ6Z230%22%5D&network=%5B%22F%22%2C%22S%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&sid=Frz&page={self.pg}')
        # sleep(1.5)
        self.pg_butao = self.driver.find_elements(By.TAG_NAME, "button")

        for conex in self.pg_butao:
            if conex.text == 'Conectar':
                conex.click()
                # sleep(1)
                confirm = self.driver.find_elements(By.TAG_NAME, 'button')
                for x in confirm:
                    if x.text == 'Enviar':
                        x.click()
                        # sleep(1.5)
                        break
                    if x.text == 'Entendi':
                        print('Limite aucancado')
                        return

        if self.pg < 100:
            self.conect(self.pg)


if __name__ == '__main__':
    inicio = LinkedIn(window=False)
    # inicio.conect(7)
    # inicio.vagas('analista de dados')
    # inicio.percode('3212451203')
    
    inicio.getFullVagas()
    inicio.save_json()
    inicio.driver.bye()








'7'