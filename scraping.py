from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from datetime import datetime

url = 'https://www.ufc.br/restaurante/cardapio/5-restaurante-universitario-de-quixada/'

def acesso_site():
    option = Options()
    option.add_argument('-headless') 
    driver = webdriver.Firefox() #Adicionar options depois
    driver.get(url+ '2023-08-28') #Data teste
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tabela_almoco = soup.find('table', class_='refeicao almoco')
    tabela_jantar = soup.find('table', class_='refeicao jantar')
    print('---Almoço---')
    for linhas in tabela_almoco.find_all('tr'):
        celulas= linhas.find_all('td')
        if celulas:
            for celula in celulas:
                print(celula.text)
                
    print('---Jantar---')
    for linhas in tabela_jantar.find_all('tr'):
        celulas= linhas.find_all('td')
        if celulas:
            for celula in celulas:
                print(celula.text)
        
    driver.quit()
    
def criar_mensagem(almoco, jantar):
    pass

acesso_site()
