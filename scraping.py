from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import json
import re

url = 'https://www.ufc.br/restaurante/cardapio/5-restaurante-universitario-de-quixada/'

def acesso_site():
    option = Options()
    option.add_argument('-headless') 
    driver = webdriver.Firefox() #Adicionar options depois
    driver.get(url+ '2023-08-28') #Data teste
    
    # Aguarde o carregamento dinâmico (ajuste o tempo conforme necessário)
    driver.implicitly_wait(10)  # Espera até 10 segundos
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tabela_almoco = soup.find('table', class_='refeicao almoco')
    tabela_jantar = soup.find('table', class_='refeicao jantar')
    
    driver.quit()
    return tabela_almoco, tabela_jantar
    
def para_json(tabela):
    rows = tabela.find_all('tr', class_='item')
     
    categorias = {
        'Principal': [],
        'Vegetariano': [],
        'Salada': [],
        'Guarnição': [],
        'Acompanhamento': [],
        'Suco': [],
        'Sobremesa': []
    }
    
    for linha in rows:
        cols = linha.find_all('td')
        if cols:
            categoria = cols[0].get_text(strip=True)
            itens = [desc.get_text(strip=True) for col in cols[1:] for desc in col.find_all('span', class_='desc')]
            categorias[categoria].extend(itens)
    
    return categorias

def montar_mensagem(almoco):
    if almoco == True:
        mensagem_cardapio = 'Bom dia, alunos'
    else:
        mensagem_cardapio = 'Boa tarde, alunos'
        
    return mensagem_cardapio

tabela_almoco, tabela_jantar = acesso_site()
almoco_json = para_json(tabela_almoco)
jantar_json = para_json(tabela_jantar)

with open('almoco.json', 'w', encoding='utf-8') as arquivo_almoco:
    json.dump(almoco_json, arquivo_almoco, indent=4, ensure_ascii=False)

with open('jantar.json', 'w', encoding='utf-8') as arquivo_jantar:
    json.dump(jantar_json, arquivo_jantar, indent=4, ensure_ascii=False)