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
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tabela_almoco = soup.find('table', class_='refeicao almoco')
    tabela_jantar = soup.find('table', class_='refeicao jantar')
        
    driver.quit()
    return tabela_almoco, tabela_jantar
    
def para_json(tabela):
    data = {}  # Dicionário para armazenar os dados
    categoria_atual = None

    for linhas in tabela.find_all('tr'):
        celulas = linhas.find_all('td')
        if celulas and len(celulas) == 2:
            categoria = celulas[0].text.strip()
            item = celulas[1].text.strip()


            # Se a categoria mudou, criar uma nova lista
            if categoria != categoria_atual:
                data[categoria] = []

            data[categoria].append({
                "itens": item
            })

            categoria_atual = categoria
    
    return json.dumps(data, ensure_ascii=False, indent=4)
    
def criar_mensagem(almoco):
    if almoco == True:
        saudacao = 'Bom dia'
    else:
        saudacao = 'Boa tarde'
    pass

tabela_almoco, tabela_jantar = acesso_site()
json_almoco = para_json(tabela_almoco)
json_jantar = para_json(tabela_jantar)

print('---Almoço---')
with open('almoco.json', 'w', encoding='utf-8') as arquivo_almoco:
    arquivo_almoco.write(json_almoco)

print('---Jantar---')
with open('jantar.json', 'w', encoding='utf-8') as arquivo_jantar:
    arquivo_jantar.write(json_jantar)