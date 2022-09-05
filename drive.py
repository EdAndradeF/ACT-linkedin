import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import platform


class Chrome:
    '''
        configura Webdriver.chrome e trata execões para de metodos de espera e procura
    '''
    def __init__(self, 
                window=True , 
                download='~/Downloads', 
                max_window=False,
                min_window=False,
                window_size=(950, 950)
            ) -> None:

        '''
            window  bool .> [default: True] se false desabilita a navegação por janela
            download str .> [default: pasta padrao linux] caminho para repositorio alternatino para download
         max_window bool .> [default: True] se True abre a janela do navegador maximizada
            |se max_window=False .v  
            min_window bool .> [default: True] se True abre a janela do navegador com o tamnho minimo
                | se min_window=False .v 
                window_size tuple[int] .> [default: (600, 600)] configura o tamanho da janela (largura,  altura)
        '''

        self.sistema = platform.system().lower()
        if self.sistema == 'windows':
            self.ser = Service('chromedriver.exe') # versao win
        else:
            self.ser = Service('extracao/chromedriver')     # versao linux
        
        self.option = webdriver.ChromeOptions()
        self.path_download = {
                "profile.default_content_settings.popups": 0,
                "download.default_directory": download,  # repositorio do download
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
            }     #parametros necessarios para efetuar downloads em repositorios especificos
                    
        self.option.add_experimental_option('prefs', self.path_download)
        if not window: # ativa e desativa abertura de janelas
            self.option.add_argument('--headless') # necessario para downloads pelo navegador
        
        
        self.driver = webdriver.Chrome(service=self.ser,
                                        options=self.option)
        if max_window:
            self.driver.maximize_window()
        elif min_window:
            self.driver.set_window_size(10, 10)
        else:
            self.driver.set_window_size(*window_size)

    def __repr__(self) -> str:
        site = self.current_url().split('.')[1]
        return f'<WebDriverChrome_{self.sistema}-{site}>'


    def current_url(self) -> str:
        '''returna o endereço do site atual'''
        return self.driver.current_url

    def bye(self) -> None:
        '''encerra webdriver'''
        print('MAL FEITO, FEITO')
        self.driver.close() 

    def get(self, url:str) -> None:  
        '''acessa ulr'''  
        self.driver.get(url)
    
    def page_source(self) -> str:
        '''return texto html da pagina'''
        return self.driver.page_source

    def find_elements(self, attr:By, vattr:str) -> list:
        '''
            trata excecao do metodo: find_elements
                        se nenhum elemento for encontrado
                        retornará uma lista vazia
                    
            attr str .> atributo do elemento html 
           vattr str .> valor do atribudo especificado
            return .> lista com elementos encontrados
                    ou .> uma lista vazia
        '''
        try:
            return self.driver.find_elements(attr, vattr)
        except NoSuchElementException as e:
            print('elemento nao encontrado -- tente outra coisa')
            return []

    def find_element(self, attr:By, vattr:str) -> WebElement:
        '''
            trata excecao do metodo:  find_element
                            se o elemento nao for encontrado
                            returnará None
            attr str .> atributo do elemento html 
           vattr str .> valor do atribudo especificado
              return .> WebDriverElement
                    ou .> None
        '''
        try:
            return self.driver.find_element(attr, vattr)
        except NoSuchElementException as e:
            print('elemento nao encontrado -- tente outra coisa')
            return None

    def waitFindElement(self, localizador:tuple[str], enquanto:str='elements', tempo=5) -> WebElement:
        '''
            trata TimeoutException de WebDriverWait que espera algo acontecer antes de prosseguir
            se o tempo for exedido exibe mensagem de erro e retorna None 
            
            se enquanto elements ou element .v
                | localizador tuple[str] .> tupla com atribudos para localização
            se enquanto url .v
                | localizador str .> url a ser verificada3
            
            tempo int .> tempo de espera antes de TimeoutException
            retorna .> WebElement 
            retorn .> (None, str)
        '''
        # attr, value = localizador
        espera = {
            'elements': EC.presence_of_all_elements_located,
            'element': EC.presence_of_element_located,
            'url': EC.url_changes
        }
        try:
            elemento = WebDriverWait(self.driver, 5).until(
                espera[enquanto](localizador)
            )
        except TimeoutException as e:
            # print(e)
            txt = f'"tentar novamente \n {self.current_url()}\
                \n TEMPO excedido, CONTEUDO NAO CARREGADO" \n '
            print(txt)
            return None, txt
        else:
            print(self.driver.current_url, '\n >>')
            return elemento

    def scroll_down(self, attr:tuple) -> None:
        '''
            encontra o ultimo elemento especificado da pagina e corre até ele

            attr tuple[str] .> tupla com atributo e valor do elemento a ser achado

        '''
        elemento = self.find_elements(*attr)[-1]
        ActionChains(self.driver).scroll_to_element(elemento).perform() 
                # scroler ate o elemento
        # sleep(1)
        self.driver.execute_script("window.scrollBy(0, 100);")
                # desce a pagina 100 pixels para simular interação humana
        sleep(1)





if __name__ =='__main__':
    presunto = Chrome(window=True)
    presunto.get('https://www.linkedin.com/')
    print()
    sleep(5)
    presunto.bye()