import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from datetime import datetime

url = 'https://www.ufc.br/restaurante/cardapio/5-restaurante-universitario-de-quixada/'
driver_path = '/caminho/para/geckodriver'

def acesso_site():
    data_temp = datetime.now()
    data_hoje = data_temp.strftime('%Y-%m-%d')
    option = Options()
    option.headless = True
    driver = webdriver.Firefox(executable_path="geckodriver")
    driver.get(url + data_hoje)
    
    #soup = BeautifulSoup(driver.page_source, 'html.parser')
        
    #driver.quit()

acesso_site()
